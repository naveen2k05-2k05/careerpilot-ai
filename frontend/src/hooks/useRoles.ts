import { useEffect, useState } from 'react'
import api from '../services/api'

const FALLBACK_ROLES = [
  'Software Engineer',
  'Data Analyst',
  'AI Engineer',
  'Data Scientist',
  'Full Stack Developer',
]

export function useRoles() {
  const [roles, setRoles] = useState<string[]>(FALLBACK_ROLES)

  useEffect(() => {
    api.get('/career/roles').then((r) => {
      if (r.data?.roles?.length) setRoles(r.data.roles)
    }).catch(() => {})
  }, [])

  return roles
}
