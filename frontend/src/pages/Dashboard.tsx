import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import StatCard from '../components/ui/StatCard'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { useAuth } from '../contexts/AuthContext'

interface DashboardData {
  resume_score: number
  interview_readiness: number
  skills_progress: number
  applications_count: number
  upcoming_interviews: { id: number; title: string; scheduled_at: string; target_role: string }[]
  recommendations: string[]
}

export default function Dashboard() {
  const { user } = useAuth()
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/dashboard').then((r) => setData(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />
  if (!data) return <div className="text-red-500">Failed to load dashboard</div>

  return (
    <div className="animate-fade-in space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Welcome back, {user?.display_name || 'there'} 👋
        </h1>
        <p className="mt-1 text-gray-500">Your career command center</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Resume Score" value={`${Math.round(data.resume_score)}%`} icon={<span>📄</span>} color="primary" />
        <StatCard title="Interview Readiness" value={`${Math.round(data.interview_readiness)}%`} icon={<span>🎤</span>} color="purple" />
        <StatCard title="Skills Progress" value={`${Math.round(data.skills_progress)}%`} icon={<span>📚</span>} color="green" />
        <StatCard title="Applications" value={data.applications_count} icon={<span>💼</span>} color="orange" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Upcoming Interviews" subtitle="Your scheduled sessions">
          {data.upcoming_interviews.length === 0 ? (
            <p className="text-sm text-gray-500">No upcoming interviews. <Link to="/mock-interview" className="text-primary-600 hover:underline">Start a mock interview</Link></p>
          ) : (
            <ul className="space-y-3">
              {data.upcoming_interviews.map((i) => (
                <li key={i.id} className="flex items-center justify-between rounded-lg bg-gray-50 p-3 dark:bg-gray-800">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{i.title}</p>
                    <p className="text-xs text-gray-500">{i.target_role}</p>
                  </div>
                  <span className="text-xs text-gray-400">{i.scheduled_at ? new Date(i.scheduled_at).toLocaleDateString() : 'TBD'}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card title="Recommendations" subtitle="Personalized for you">
          <ul className="space-y-2">
            {data.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-300">
                <span className="text-primary-500">→</span>
                {rec}
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { to: '/resume', label: 'Analyze Resume', icon: '📄' },
          { to: '/mock-interview', label: 'Mock Interview', icon: '🎤' },
          { to: '/career-coach', label: 'Career Roadmap', icon: '🎯' },
          { to: '/applications', label: 'Track Applications', icon: '💼' },
        ].map((action) => (
          <Link
            key={action.to}
            to={action.to}
            className="flex items-center gap-3 rounded-xl border border-gray-200 bg-white p-4 transition-all hover:border-primary-300 hover:shadow-md dark:border-gray-700 dark:bg-gray-900 dark:hover:border-primary-600"
          >
            <span className="text-2xl">{action.icon}</span>
            <span className="font-medium text-gray-900 dark:text-white">{action.label}</span>
          </Link>
        ))}
      </div>
    </div>
  )
}
