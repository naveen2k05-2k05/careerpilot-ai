import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'
import { Radar } from 'react-chartjs-2'
import api from '../services/api'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

interface Feedback {
  technical_score: number
  communication_score: number
  confidence_score: number
  overall_rating: number
  improvement_suggestions: string[]
  detailed_feedback: string
}

export default function InterviewFeedback() {
  const { id } = useParams()
  const [feedback, setFeedback] = useState<Feedback | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      api.get(`/interviews/${id}/feedback`)
        .then((r) => setFeedback(r.data))
        .catch(() => api.post(`/interviews/${id}/complete`).then((r) => setFeedback(r.data)))
        .finally(() => setLoading(false))
    }
  }, [id])

  if (loading) return <LoadingSpinner />
  if (!feedback) return <div className="text-red-500">Feedback not found</div>

  const chartData = {
    labels: ['Technical', 'Communication', 'Confidence', 'Overall'],
    datasets: [{
      label: 'Scores',
      data: [
        feedback.technical_score,
        feedback.communication_score,
        feedback.confidence_score,
        feedback.overall_rating,
      ],
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      borderColor: 'rgb(59, 130, 246)',
      pointBackgroundColor: 'rgb(59, 130, 246)',
    }],
  }

  return (
    <div className="animate-fade-in mx-auto max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Interview Feedback</h1>
        <p className="text-gray-500">Your performance analysis</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Overall Rating" className="text-center">
          <p className="text-5xl font-bold text-primary-600">{Math.round(feedback.overall_rating)}%</p>
        </Card>
        <Card title="Score Breakdown">
          <div className="h-64">
            <Radar data={chartData} options={{ scales: { r: { min: 0, max: 100 } }, maintainAspectRatio: false }} />
          </div>
        </Card>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        {[
          { label: 'Technical', score: feedback.technical_score },
          { label: 'Communication', score: feedback.communication_score },
          { label: 'Confidence', score: feedback.confidence_score },
        ].map((s) => (
          <Card key={s.label} className="text-center">
            <p className="text-sm text-gray-500">{s.label}</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{Math.round(s.score)}%</p>
          </Card>
        ))}
      </div>

      <Card title="Detailed Feedback">
        <p className="text-sm text-gray-600 dark:text-gray-300">{feedback.detailed_feedback}</p>
      </Card>

      <Card title="Improvement Suggestions">
        <ul className="space-y-2">
          {feedback.improvement_suggestions?.map((s, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-300">
              <span className="text-primary-500">→</span> {s}
            </li>
          ))}
        </ul>
      </Card>
    </div>
  )
}
