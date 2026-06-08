import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import ProtectedRoute from './components/ProtectedRoute'
import DashboardLayout from './components/layout/DashboardLayout'
import Login from './pages/auth/Login'
import Signup from './pages/auth/Signup'
import ForgotPassword from './pages/auth/ForgotPassword'
import Dashboard from './pages/Dashboard'
import ResumeAnalyzer from './pages/ResumeAnalyzer'
import CareerCoach from './pages/CareerCoach'
import JobMatch from './pages/JobMatch'
import InterviewCoach from './pages/InterviewCoach'
import MockInterview from './pages/MockInterview'
import InterviewFeedback from './pages/InterviewFeedback'
import Projects from './pages/Projects'
import LearningTracker from './pages/LearningTracker'
import Applications from './pages/Applications'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/resume" element={<ResumeAnalyzer />} />
              <Route path="/career-coach" element={<CareerCoach />} />
              <Route path="/job-match" element={<JobMatch />} />
              <Route path="/interview-coach" element={<InterviewCoach />} />
              <Route path="/mock-interview" element={<MockInterview />} />
              <Route path="/interview-feedback/:id" element={<InterviewFeedback />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/learning" element={<LearningTracker />} />
              <Route path="/applications" element={<Applications />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
            </Route>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  )
}
