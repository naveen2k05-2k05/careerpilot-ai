import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { isDevMode } from '../../lib/auth'
import api from '../../services/api'
import { isFirebaseConfigured } from '../../config/firebase'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login, googleLogin, demoLogin } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!email || !password) {
      setError('Please fill in all fields')
      return
    }
    setLoading(true)
    try {
      await login(email, password)
      // if user has no resumes yet, take them to resume analyzer to upload
      const { data } = await api.get('/resumes')
      if (!data || data.length === 0) navigate('/resume?first=1')
      else navigate('/dashboard')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogle = async () => {
    setLoading(true)
    try {
      if (!isFirebaseConfigured()) {
        throw new Error('Firebase is not configured. Set VITE_FIREBASE_API_KEY in frontend/.env')
      }
      await googleLogin()
      const { data } = await api.get('/resumes')
      if (!data || data.length === 0) navigate('/resume?first=1')
      else navigate('/dashboard')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Google login failed')
    } finally {
      setLoading(false)
    }
  }

  const firebaseConfigured = isFirebaseConfigured()

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-primary-50 via-white to-purple-50 p-4 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950">
      <div className="w-full max-w-md animate-fade-in">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 text-2xl font-bold text-white shadow-lg">
            CP
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Welcome back</h1>
          <p className="mt-2 text-gray-500">Sign in to CareerPilot AI</p>
        </div>

        <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl dark:border-gray-700 dark:bg-gray-900">
          {error && (
            <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600 dark:bg-red-900/20 dark:text-red-400">
              {error}
            </div>
          )}
          {!firebaseConfigured && (
            <div className="mb-4 rounded-lg bg-yellow-50 p-3 text-sm text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-300">
              Firebase is not configured correctly. To use Google sign-in, update <code>frontend/.env</code> with your Firebase web config and restart the dev server.
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
            <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
            <div className="text-right">
              <Link to="/forgot-password" className="text-sm text-primary-600 hover:underline">
                Forgot password?
              </Link>
            </div>
            <Button type="submit" loading={loading} className="w-full">
              Sign In
            </Button>
          </form>

          <div className="my-6 flex items-center gap-4">
            <div className="h-px flex-1 bg-gray-200 dark:bg-gray-700" />
            <span className="text-xs text-gray-400">OR</span>
            <div className="h-px flex-1 bg-gray-200 dark:bg-gray-700" />
          </div>

          <Button variant="secondary" onClick={handleGoogle} loading={loading} className="w-full" disabled={!firebaseConfigured}>
            Continue with Google
          </Button>

          {isDevMode() && (
            <>
              <div className="my-6 flex items-center gap-4">
                <div className="h-px flex-1 bg-gray-200 dark:bg-gray-700" />
                <span className="text-xs text-gray-400">DEV</span>
                <div className="h-px flex-1 bg-gray-200 dark:bg-gray-700" />
              </div>
              <Button
                variant="ghost"
                loading={loading}
                className="w-full border border-dashed border-primary-300 text-primary-600"
                  onClick={async () => {
                  setLoading(true)
                  setError('')
                  try {
                    await demoLogin()
                    try {
                      const { data } = await api.get('/resumes')
                      if (!data || data.length === 0) navigate('/resume?first=1')
                      else navigate('/dashboard')
                    } catch {
                      navigate('/dashboard')
                    }
                  } catch (err: unknown) {
                    setError(err instanceof Error ? err.message : 'Demo login failed')
                  } finally {
                    setLoading(false)
                  }
                }}
              >
                Continue as Demo User
              </Button>
            </>
          )}

          <p className="mt-6 text-center text-sm text-gray-500">
            Don't have an account?{' '}
            <Link to="/signup" className="font-medium text-primary-600 hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
