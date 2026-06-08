import { useEffect, useState } from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'react-chartjs-2'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import Select from '../components/ui/Select'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import EmptyState from '../components/ui/EmptyState'

ChartJS.register(ArcElement, Tooltip, Legend)

interface LearningItem {
  id: number
  item_type: string
  title: string
  description: string | null
  status: string
  completed_at: string | null
}

export default function LearningTracker() {
  const [items, setItems] = useState<LearningItem[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ item_type: 'skill', title: '', description: '' })

  const fetchItems = () => {
    api.get('/learning').then((r) => setItems(r.data)).finally(() => setLoading(false))
  }

  useEffect(() => { fetchItems() }, [])

  const addItem = async () => {
    if (!form.title.trim()) return
    await api.post('/learning', form)
    setForm({ item_type: 'skill', title: '', description: '' })
    setShowForm(false)
    fetchItems()
  }

  const toggleComplete = async (item: LearningItem) => {
    await api.put(`/learning/${item.id}`, {
      status: item.status === 'completed' ? 'in_progress' : 'completed',
    })
    fetchItems()
  }

  const completed = items.filter((i) => i.status === 'completed').length
  const chartData = {
    labels: ['Completed', 'In Progress'],
    datasets: [{
      data: [completed, items.length - completed],
      backgroundColor: ['#10b981', '#e5e7eb'],
    }],
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="animate-fade-in space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Learning Tracker</h1>
          <p className="text-gray-500">Track skills, courses, and projects</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>Add Item</Button>
      </div>

      {showForm && (
        <Card>
          <div className="grid gap-4 sm:grid-cols-2">
            <Select
              label="Type"
              value={form.item_type}
              onChange={(e) => setForm({ ...form, item_type: e.target.value })}
              options={[
                { value: 'skill', label: 'Skill' },
                { value: 'course', label: 'Course' },
                { value: 'project', label: 'Project' },
                { value: 'interview', label: 'Interview Practice' },
              ]}
            />
            <Input label="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          </div>
          <div className="mt-4 flex gap-2">
            <Button onClick={addItem}>Save</Button>
            <Button variant="secondary" onClick={() => setShowForm(false)}>Cancel</Button>
          </div>
        </Card>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <Card title="Progress Overview" className="lg:col-span-1">
          <div className="h-48">
            <Doughnut data={chartData} options={{ maintainAspectRatio: false }} />
          </div>
          <p className="mt-2 text-center text-sm text-gray-500">
            {completed} of {items.length} completed
          </p>
        </Card>

        <div className="lg:col-span-2">
          {items.length === 0 ? (
            <EmptyState icon="📚" title="No learning items yet" description="Start tracking your skills and courses." />
          ) : (
            <div className="space-y-2">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900"
                >
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => toggleComplete(item)}
                      className={`flex h-6 w-6 items-center justify-center rounded-full border-2 ${
                        item.status === 'completed'
                          ? 'border-emerald-500 bg-emerald-500 text-white'
                          : 'border-gray-300 dark:border-gray-600'
                      }`}
                    >
                      {item.status === 'completed' && '✓'}
                    </button>
                    <div>
                      <p className={`font-medium ${item.status === 'completed' ? 'line-through text-gray-400' : 'text-gray-900 dark:text-white'}`}>
                        {item.title}
                      </p>
                      <p className="text-xs text-gray-500 capitalize">{item.item_type}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                      item.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {item.status.replace('_', ' ')}
                    </span>
                    <button
                      onClick={async () => { await api.delete(`/learning/${item.id}`); fetchItems() }}
                      className="text-xs text-red-500 hover:underline"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
