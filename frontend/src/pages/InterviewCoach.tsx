import { useState } from 'react'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Select from '../components/ui/Select'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { useRoles } from '../hooks/useRoles'
const DIFFICULTIES = ['beginner', 'intermediate', 'advanced']
const TYPES = ['hr', 'technical', 'project', 'scenario']

export default function InterviewCoach() {
  const roles = useRoles()
  const [role, setRole] = useState(roles[0])
  const [difficulty, setDifficulty] = useState('intermediate')
  const [questions, setQuestions] = useState<Record<string, string[]> | null>(null)
  const [loading, setLoading] = useState(false)

  const generate = async () => {
    setLoading(true)
    try {
      const { data } = await api.post('/interviews/questions', {
        target_role: role,
        difficulty,
        question_types: TYPES,
      })
      setQuestions(data.questions)
    } finally {
      setLoading(false)
    }
  }

  const typeLabels: Record<string, string> = {
    hr: 'HR Questions',
    technical: 'Technical Questions',
    project: 'Project-Based Questions',
    scenario: 'Scenario-Based Questions',
  }

  return (
    <div className="animate-fade-in space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">AI Interview Coach</h1>
        <p className="text-gray-500">Generate tailored interview questions by role and difficulty</p>
      </div>

      <Card>
        <div className="grid gap-4 sm:grid-cols-3">
          <Select label="Target Role" value={role} onChange={(e) => setRole(e.target.value)} options={roles.map((r) => ({ value: r, label: r }))} />
          <Select label="Difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} options={DIFFICULTIES.map((d) => ({ value: d, label: d.charAt(0).toUpperCase() + d.slice(1) }))} />
          <div className="flex items-end">
            <Button onClick={generate} loading={loading} className="w-full">Generate Questions</Button>
          </div>
        </div>
      </Card>

      {loading && <LoadingSpinner message="Generating interview questions..." />}

      {questions && !loading && (
        <div className="grid gap-6 md:grid-cols-2">
          {TYPES.map((type) => (
            <Card key={type} title={typeLabels[type]}>
              <ol className="list-decimal space-y-2 pl-5">
                {questions[type]?.map((q, i) => (
                  <li key={i} className="text-sm text-gray-600 dark:text-gray-300">{q}</li>
                ))}
              </ol>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
