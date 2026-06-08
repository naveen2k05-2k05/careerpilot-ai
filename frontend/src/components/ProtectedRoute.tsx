import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { getDevToken } from '../lib/auth'
import LoadingSpinner from './ui/LoadingSpinner'

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { firebaseUser, user, loading } = useAuth()

  if (loading) return <LoadingSpinner message="Checking authentication..." />
  if (!firebaseUser && !getDevToken()) return <Navigate to="/login" replace />
  if (!user) return <LoadingSpinner message="Loading profile..." />
  return <>{children}</>
}
