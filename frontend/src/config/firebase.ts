import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'

console.log("API KEY:", import.meta.env.VITE_FIREBASE_API_KEY)
console.log("AUTH DOMAIN:", import.meta.env.VITE_FIREBASE_AUTH_DOMAIN)
console.log("PROJECT ID:", import.meta.env.VITE_FIREBASE_PROJECT_ID)

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
}

console.log("Firebase Config:", firebaseConfig)
console.log(import.meta.env)

const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)
export const googleProvider = new GoogleAuthProvider()

const invalidFirebaseValue = (value: string | undefined) => {
  if (!value) return true
  const normalized = value.toLowerCase().trim()
  return normalized.startsWith('your-') || normalized.includes('placeholder') || normalized.includes('dev-project')
}

export function isFirebaseConfigured() {
  return (
    !invalidFirebaseValue(import.meta.env.VITE_FIREBASE_API_KEY) &&
    !invalidFirebaseValue(import.meta.env.VITE_FIREBASE_AUTH_DOMAIN) &&
    !invalidFirebaseValue(import.meta.env.VITE_FIREBASE_PROJECT_ID)
  )
}
