import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'
import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  type User,
} from 'firebase/auth'
import { auth, googleProvider } from '../config/firebase'
import {
  clearDevToken,
  getDevToken,
  isDevMode,
  setDevToken,
  DEV_AUTH_TOKEN,
} from '../lib/auth'
import api from '../services/api'

interface AuthUser {
  id: number
  email: string
  display_name: string | null
  photo_url: string | null
  target_role: string | null
}

interface AuthContextType {
  firebaseUser: User | null
  user: AuthUser | null
  loading: boolean
  isDemo: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string) => Promise<void>
  googleLogin: () => Promise<void>
  demoLogin: () => Promise<void>
  logout: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [firebaseUser, setFirebaseUser] = useState<User | null>(null)
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [isDemo, setIsDemo] = useState(!!getDevToken())

  const fetchProfile = async () => {
    try {
      const { data } = await api.get('/auth/me')
      setUser(data)
      return true
    } catch {
      setUser(null)
      return false
    }
  }

  useEffect(() => {
    const init = async () => {
      const devToken = getDevToken()
      if (devToken) {
        setIsDemo(true)
        await fetchProfile()
        setLoading(false)
        return
      }

      const unsub = onAuthStateChanged(auth, async (fbUser) => {
        setFirebaseUser(fbUser)
        setIsDemo(false)
        if (fbUser) {
          await fetchProfile()
        } else {
          setUser(null)
        }
        setLoading(false)
      })
      return unsub
    }

    let unsub: (() => void) | undefined
    init().then((fn) => {
      unsub = fn
    })
    return () => unsub?.()
  }, [])

  const login = async (email: string, password: string) => {
    clearDevToken()
    setIsDemo(false)
    await signInWithEmailAndPassword(auth, email, password)
  }

  const signup = async (email: string, password: string) => {
    clearDevToken()
    setIsDemo(false)
    await createUserWithEmailAndPassword(auth, email, password)
  }

  const googleLogin = async () => {
    clearDevToken()
    setIsDemo(false)
    await signInWithPopup(auth, googleProvider)
  }

  const demoLogin = async () => {
    if (!isDevMode()) throw new Error('Demo mode is disabled')
    clearDevToken()
    await signOut(auth).catch(() => {})
    const { data } = await api.post('/auth/dev-login')
    const token = data.token || DEV_AUTH_TOKEN
    setDevToken(token)
    setIsDemo(true)
    setFirebaseUser(null)
    const profileLoaded = await fetchProfile()
    if (!profileLoaded) {
      clearDevToken()
      setIsDemo(false)
      throw new Error('Demo login failed to load profile')
    }
  }

  const logout = async () => {
    clearDevToken()
    setIsDemo(false)
    await signOut(auth).catch(() => {})
    setUser(null)
    setFirebaseUser(null)
  }

  const resetPassword = async (email: string) => {
    await sendPasswordResetEmail(auth, email)
  }

  const refreshUser = async () => {
    await fetchProfile()
  }

  return (
    <AuthContext.Provider
      value={{
        firebaseUser,
        user,
        loading,
        isDemo,
        login,
        signup,
        googleLogin,
        demoLogin,
        logout,
        resetPassword,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
