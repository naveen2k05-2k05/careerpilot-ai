import { useEffect, useState } from 'react'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import Select from '../components/ui/Select'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import EmptyState from '../components/ui/EmptyState'

interface Application {
  id: number
  company_name: string
  role: string
  status: string
  application_date: string
  notes: string | null
}

const STATUSES = [
  { value: 'applied', label: 'Applied' },
  { value: 'under_review', label: 'Under Review' },
  { value: 'interview_scheduled', label: 'Interview Scheduled' },
  { value: 'rejected', label: 'Rejected' },
  { value: 'offer_received', label: 'Offer Received' },
]

const statusColors: Record<string, string> = {
  applied: 'bg-blue-100 text-blue-700',
  under_review: 'bg-amber-100 text-amber-700',
  interview_scheduled: 'bg-purple-100 text-purple-700',
  rejected: 'bg-red-100 text-red-700',
  offer_received: 'bg-emerald-100 text-emerald-700',
}

export default function Applications() {
  const [apps, setApps] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ company_name: '', role: '', status: 'applied', notes: '' })

  const fetchApps = () => {
    api.get('/applications').then((r) => setApps(r.data)).finally(() => setLoading(false))
  }

  useEffect(() => { fetchApps() }, [])

  const addApp = async () => {
    if (!form.company_name || !form.role) return
    await api.post('/applications', form)
    setForm({ company_name: '', role: '', status: 'applied', notes: '' })
    setShowForm(false)
    fetchApps()
  }

  const updateStatus = async (id: number, status: string) => {
    await api.put(`/applications/${id}`, { status })
    fetchApps()
  }

  const deleteApp = async (id: number) => {
    await api.delete(`/applications/${id}`)
    fetchApps()
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="animate-fade-in space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Job Applications</h1>
          <p className="text-gray-500">Track your job search pipeline</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>Add Application</Button>
      </div>

      {showForm && (
        <Card>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input label="Company" value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} />
            <Input label="Role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} />
            <Select label="Status" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })} options={STATUSES} />
            <Input label="Notes" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
          </div>
          <div className="mt-4 flex gap-2">
            <Button onClick={addApp}>Save</Button>
            <Button variant="secondary" onClick={() => setShowForm(false)}>Cancel</Button>
          </div>
        </Card>
      )}

      {apps.length === 0 ? (
        <EmptyState icon="💼" title="No applications yet" description="Start tracking your job applications." action={<Button onClick={() => setShowForm(true)}>Add Application</Button>} />
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Company</th>
                <th className="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Role</th>
                <th className="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Status</th>
                <th className="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Date</th>
                <th className="px-4 py-3 font-medium text-gray-600 dark:text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {apps.map((app) => (
                <tr key={app.id} className="bg-white dark:bg-gray-900">
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{app.company_name}</td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{app.role}</td>
                  <td className="px-4 py-3">
                    <select
                      value={app.status}
                      onChange={(e) => updateStatus(app.id, e.target.value)}
                      className={`rounded-full border-0 px-2 py-1 text-xs font-medium ${statusColors[app.status]}`}
                    >
                      {STATUSES.map((s) => (
                        <option key={s.value} value={s.value}>{s.label}</option>
                      ))}
                    </select>
                  </td>
                  <td className="px-4 py-3 text-gray-500">{new Date(app.application_date).toLocaleDateString()}</td>
                  <td className="px-4 py-3">
                    <button onClick={() => deleteApp(app.id)} className="text-xs text-red-500 hover:underline">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
