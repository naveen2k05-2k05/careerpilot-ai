import { useEffect, useState } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'
import api from '../services/api'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import StatCard from '../components/ui/StatCard'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

interface AnalyticsData {
  skill_progress: { skill: string; proficiency: number; target: number }[]
  ats_improvement: { date: string; score: number }[]
  interview_scores: { date: string; technical: number; communication: number; confidence: number; overall: number }[]
  application_success_rate: {
    total: number
    offers: number
    interviews: number
    rejected: number
    success_rate: number
    interview_rate: number
  }
}

export default function Analytics() {
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/analytics').then((r) => setData(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />
  if (!data) return <div className="text-red-500">Failed to load analytics</div>

  const atsChart = {
    labels: data.ats_improvement.map((d) => d.date),
    datasets: [{
      label: 'ATS Score',
      data: data.ats_improvement.map((d) => d.score),
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: true,
      tension: 0.3,
    }],
  }

  const interviewChart = {
    labels: data.interview_scores.map((d) => d.date),
    datasets: [
      { label: 'Technical', data: data.interview_scores.map((d) => d.technical), borderColor: '#3b82f6' },
      { label: 'Communication', data: data.interview_scores.map((d) => d.communication), borderColor: '#10b981' },
      { label: 'Confidence', data: data.interview_scores.map((d) => d.confidence), borderColor: '#f59e0b' },
      { label: 'Overall', data: data.interview_scores.map((d) => d.overall), borderColor: '#8b5cf6' },
    ],
  }

  const skillChart = {
    labels: data.skill_progress.map((s) => s.skill),
    datasets: [
      { label: 'Proficiency', data: data.skill_progress.map((s) => s.proficiency), backgroundColor: '#3b82f6' },
      { label: 'Target', data: data.skill_progress.map((s) => s.target), backgroundColor: '#e5e7eb' },
    ],
  }

  return (
    <div className="animate-fade-in space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Analytics Dashboard</h1>
        <p className="text-gray-500">Track your career progress over time</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Applications" value={data.application_success_rate.total} color="primary" />
        <StatCard title="Success Rate" value={`${data.application_success_rate.success_rate}%`} color="green" />
        <StatCard title="Interview Rate" value={`${data.application_success_rate.interview_rate}%`} color="purple" />
        <StatCard title="Offers" value={data.application_success_rate.offers} color="orange" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="ATS Score Improvement">
          {data.ats_improvement.length > 0 ? (
            <Line data={atsChart} options={{ responsive: true, scales: { y: { min: 0, max: 100 } } }} />
          ) : (
            <p className="py-8 text-center text-sm text-gray-500">Upload resumes to track ATS improvement</p>
          )}
        </Card>

        <Card title="Interview Scores">
          {data.interview_scores.length > 0 ? (
            <Line data={interviewChart} options={{ responsive: true, scales: { y: { min: 0, max: 100 } } }} />
          ) : (
            <p className="py-8 text-center text-sm text-gray-500">Complete mock interviews to see scores</p>
          )}
        </Card>
      </div>

      <Card title="Skill Progress">
        {data.skill_progress.length > 0 ? (
          <Bar data={skillChart} options={{ responsive: true, scales: { y: { min: 0, max: 100 } } }} />
        ) : (
          <p className="py-8 text-center text-sm text-gray-500">Add skills to your learning tracker</p>
        )}
      </Card>
    </div>
  )
}
