import { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import Select from '../components/ui/Select'
import { useRoles } from '../hooks/useRoles'

export default function Settings() {
  const { user, refreshUser, isDemo } = useAuth()
  const roles = useRoles()
  const [displayName, setDisplayName] = useState(user?.display_name || '')
  const [targetRole, setTargetRole] = useState(user?.target_role || roles[0])
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  const save = async () => {
    setSaving(true)
    setMessage('')
    try {
      await api.put('/auth/me', { display_name: displayName, target_role: targetRole })
      await refreshUser()
      setMessage('Profile updated successfully')
    } catch {
      setMessage('Failed to update profile')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="animate-fade-in mx-auto max-w-lg space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="text-gray-500">Manage your profile and career preferences</p>
      </div>

      {isDemo && (
        <div className="rounded-lg bg-amber-50 p-4 text-sm text-amber-800 dark:bg-amber-900/20 dark:text-amber-300">
          You are using demo mode. Configure Firebase for real authentication.
        </div>
      )}

      <Card>
        <div className="space-y-4">
          <Input label="Email" value={user?.email || ''} disabled />
          <Input label="Display Name" value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
          <Select
            label="Target Role"
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            options={roles.map((r) => ({ value: r, label: r }))}
          />
          {message && (
            <p className={`text-sm ${message.includes('success') ? 'text-emerald-600' : 'text-red-500'}`}>
              {message}
            </p>
          )}
          <Button onClick={save} loading={saving}>Save Changes</Button>
        </div>
      </Card>
    </div>
  )
}
