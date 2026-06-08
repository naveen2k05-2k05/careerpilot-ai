import { useEffect, useState } from 'react'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Select from '../components/ui/Select'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { useRoles } from '../hooks/useRoles'

interface Project {
  title: string
  description: string
  technologies: string[]
  difficulty: string
  resume_impact: string
}

interface ProjectData {
  beginner: Project[]
  intermediate: Project[]
  advanced: Project[]
}

interface UserProject {
  id: number
  title: string
  status: string
}

export default function Projects() {
  const roles = useRoles()
  const [role, setRole] = useState(roles[0])
  const [projects, setProjects] = useState<ProjectData | null>(null)
  const [myProjects, setMyProjects] = useState<UserProject[]>([])
  const [loading, setLoading] = useState(false)

  const fetchMyProjects = () => {
    api.get('/projects/my').then((r) => setMyProjects(r.data)).catch(() => {})
  }

  useEffect(() => { fetchMyProjects() }, [])

  const fetchProjects = async () => {
    setLoading(true)
    try {
      const { data } = await api.get(`/projects/recommendations?target_role=${encodeURIComponent(role)}`)
      setProjects(data)
    } finally {
      setLoading(false)
    }
  }

  const saveProject = async (title: string) => {
    await api.post('/projects/my', { title, status: 'recommended' })
    fetchMyProjects()
  }

  const updateStatus = async (id: number, status: string) => {
    await api.put(`/projects/my/${id}`, { status })
    fetchMyProjects()
  }

  const levels = ['beginner', 'intermediate', 'advanced'] as const
  const levelColors: Record<string, string> = {
    beginner: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300',
    intermediate: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
    advanced: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
  }

  return (
    <div className="animate-fade-in space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Project Recommendations</h1>
        <p className="text-gray-500">Build portfolio projects that boost your resume</p>
      </div>

      {myProjects.length > 0 && (
        <Card title="My Portfolio Projects">
          <div className="space-y-2">
            {myProjects.map((p) => (
              <div key={p.id} className="flex items-center justify-between rounded-lg bg-gray-50 p-3 dark:bg-gray-800">
                <span className="font-medium text-gray-900 dark:text-white">{p.title}</span>
                <select
                  value={p.status}
                  onChange={(e) => updateStatus(p.id, e.target.value)}
                  className="rounded border border-gray-300 bg-white px-2 py-1 text-xs dark:border-gray-600 dark:bg-gray-900"
                >
                  <option value="recommended">Recommended</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
            ))}
          </div>
        </Card>
      )}

      <Card>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
          <div className="flex-1">
            <Select label="Target Role" value={role} onChange={(e) => setRole(e.target.value)} options={roles.map((r) => ({ value: r, label: r }))} />
          </div>
          <Button onClick={fetchProjects} loading={loading}>Get Recommendations</Button>
        </div>
      </Card>

      {loading && <LoadingSpinner />}

      {projects && !loading && (
        <div className="space-y-8">
          {levels.map((level) => (
            <div key={level}>
              <h2 className="mb-4 text-lg font-semibold capitalize text-gray-900 dark:text-white">{level} Projects</h2>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {projects[level]?.map((p, i) => (
                  <Card key={i}>
                    <div className="mb-2 flex items-center justify-between">
                      <h3 className="font-semibold text-gray-900 dark:text-white">{p.title}</h3>
                      <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${levelColors[p.difficulty] || levelColors[level]}`}>
                        {p.difficulty}
                      </span>
                    </div>
                    <p className="mb-3 text-sm text-gray-500">{p.description}</p>
                    <div className="mb-3 flex flex-wrap gap-1">
                      {p.technologies?.map((t) => (
                        <span key={t} className="rounded bg-gray-100 px-2 py-0.5 text-xs dark:bg-gray-800">{t}</span>
                      ))}
                    </div>
                    <p className="mb-3 text-xs text-primary-600 dark:text-primary-400">
                      Resume Impact: {p.resume_impact}
                    </p>
                    <Button size="sm" variant="secondary" onClick={() => saveProject(p.title)}>
                      Add to Portfolio
                    </Button>
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
