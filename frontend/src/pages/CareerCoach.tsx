import { useEffect, useState } from 'react'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Select from '../components/ui/Select'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { useRoles } from '../hooks/useRoles'

interface Roadmap {
  id: number
  target_role: string
  required_skills: string[]
  learning_roadmap: { phase: string; duration: string; topics: string[] }[]
  recommended_courses: { name: string; platform: string; url: string }[]
  recommended_projects: { title: string; description: string }[]
  estimated_timeline: string
}

export default function CareerCoach() {
  const roles = useRoles()
  const [role, setRole] = useState(roles[0])
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.get('/career/roadmaps').then((r) => {
      if (r.data.length) setRoadmap(r.data[0])
    })
  }, [])

  const generate = async () => {
    setLoading(true)
    try {
      const { data } = await api.post('/career/roadmap', { target_role: role })
      setRoadmap(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="animate-fade-in space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Career Coach</h1>
        <p className="text-gray-500">Get a personalized learning roadmap for your target role</p>
      </div>

      <Card>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <Select
              label="Target Role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              options={roles.map((r) => ({ value: r, label: r }))}
            />
          </div>
          <Button onClick={generate} loading={loading}>
            Generate Roadmap
          </Button>
        </div>
      </Card>

      {loading && <LoadingSpinner message="Generating your career roadmap..." />}

      {roadmap && !loading && (
        <div className="space-y-6">
          <div className="rounded-xl bg-gradient-to-r from-primary-500 to-purple-600 p-6 text-white">
            <h2 className="text-xl font-bold">{roadmap.target_role} Roadmap</h2>
            <p className="mt-1 opacity-90">Estimated timeline: {roadmap.estimated_timeline}</p>
          </div>

          <Card title="Required Skills">
            <div className="flex flex-wrap gap-2">
              {roadmap.required_skills?.map((s) => (
                <span key={s} className="rounded-full bg-primary-100 px-3 py-1 text-sm text-primary-700 dark:bg-primary-900/30 dark:text-primary-300">{s}</span>
              ))}
            </div>
          </Card>

          <Card title="Learning Roadmap">
            <div className="space-y-4">
              {roadmap.learning_roadmap?.map((phase, i) => (
                <div key={i} className="border-l-4 border-primary-500 pl-4">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{phase.phase}</h4>
                  <p className="text-sm text-gray-500">{phase.duration}</p>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {phase.topics?.map((t) => (
                      <span key={t} className="rounded bg-gray-100 px-2 py-0.5 text-xs dark:bg-gray-800">{t}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <div className="grid gap-6 md:grid-cols-2">
            <Card title="Recommended Courses">
              <ul className="space-y-3">
                {roadmap.recommended_courses?.map((c, i) => (
                  <li key={i} className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800">
                    <p className="font-medium text-gray-900 dark:text-white">{c.name}</p>
                    <p className="text-xs text-gray-500">{c.platform}</p>
                  </li>
                ))}
              </ul>
            </Card>
            <Card title="Recommended Projects">
              <ul className="space-y-3">
                {roadmap.recommended_projects?.map((p, i) => (
                  <li key={i} className="rounded-lg bg-gray-50 p-3 dark:bg-gray-800">
                    <p className="font-medium text-gray-900 dark:text-white">{p.title}</p>
                    <p className="text-sm text-gray-500">{p.description}</p>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
