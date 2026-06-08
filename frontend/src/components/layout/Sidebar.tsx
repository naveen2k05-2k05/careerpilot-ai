import { NavLink } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { useTheme } from '../../contexts/ThemeContext'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/resume', label: 'Resume Analyzer', icon: '📄' },
  { to: '/career-coach', label: 'Career Coach', icon: '🎯' },
  { to: '/job-match', label: 'Job Match', icon: '🔍' },
  { to: '/interview-coach', label: 'Interview Coach', icon: '💬' },
  { to: '/mock-interview', label: 'Mock Interview', icon: '🎤' },
  { to: '/projects', label: 'Projects', icon: '🚀' },
  { to: '/learning', label: 'Learning Tracker', icon: '📚' },
  { to: '/applications', label: 'Applications', icon: '💼' },
  { to: '/analytics', label: 'Analytics', icon: '📈' },
  { to: '/settings', label: 'Settings', icon: '⚙️' },
]

export default function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  const { logout, user } = useAuth()
  const { theme, toggleTheme } = useTheme()

  return (
    <aside className="flex h-full w-64 flex-col border-r border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-900">
      <div className="border-b border-gray-200 p-6 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 text-white font-bold">
            CP
          </div>
          <div>
            <h1 className="font-bold text-gray-900 dark:text-white">CareerPilot</h1>
            <p className="text-xs text-gray-500">AI Career Coach</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-4">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800'
              }`
            }
          >
            <span>{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-gray-200 p-4 dark:border-gray-700">
        <div className="mb-3 flex items-center gap-3 rounded-lg bg-gray-50 p-3 dark:bg-gray-800">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-700 dark:bg-primary-900 dark:text-primary-300">
            {user?.display_name?.[0] || user?.email?.[0]?.toUpperCase() || 'U'}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-gray-900 dark:text-white">
              {user?.display_name || 'User'}
            </p>
            <p className="truncate text-xs text-gray-500">{user?.email}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={toggleTheme}
            className="flex-1 rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-600 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
          >
            {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
          </button>
          <button
            onClick={logout}
            className="flex-1 rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-red-600 hover:bg-red-50 dark:border-gray-600 dark:hover:bg-red-900/20"
          >
            Logout
          </button>
        </div>
      </div>
    </aside>
  )
}
