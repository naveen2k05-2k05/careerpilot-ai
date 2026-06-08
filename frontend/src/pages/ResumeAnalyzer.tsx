import { useEffect, useState, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import api from '../services/api'
import Card from '../components/ui/Card'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import EmptyState from '../components/ui/EmptyState'

interface Resume {
  id: number
  filename: string
  ats_score: number
  strengths: string[]
  weaknesses: string[]
  improvements: string[]
  extracted_skills: string[]
  missing_skills: string[]
  created_at: string
}

export default function ResumeAnalyzer() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [result, setResult] = useState<Resume | null>(null)
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [error, setError] = useState('')
  const [searchParams] = useSearchParams()
  const fileInputRef = useRef<HTMLInputElement | null>(null)

  useEffect(() => {
    api.get('/resumes').then((r) => setResumes(r.data)).finally(() => setFetching(false))
  }, [])

  useEffect(() => {
    // If redirected after first login, auto-open the file picker
    if (searchParams.get('first') === '1') {
      setTimeout(() => fileInputRef.current?.click(), 250)
    }
  }, [searchParams])

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setLoading(true)
    setError('')
    const form = new FormData()
    form.append('file', file)
    try {
      const { data } = await api.post('/resumes/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(data.resume)
      setResumes((prev) => [data.resume, ...prev])
    } catch {
      setError('Failed to analyze resume. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const display = result || resumes[0]

  if (fetching) return <LoadingSpinner />

  return (
    <div className="animate-fade-in space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Resume Analyzer</h1>
          <p className="text-gray-500">Upload PDF or DOCX for ATS analysis</p>
        </div>
        <label className="inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700">
          <input ref={fileInputRef} type="file" accept=".pdf,.docx" onChange={handleUpload} className="hidden" disabled={loading} />
          {loading ? 'Analyzing...' : 'Upload Resume'}
        </label>
      </div>

      {error && <div className="rounded-lg bg-red-50 p-4 text-red-600">{error}</div>}

      {!display ? (
        <EmptyState
          icon="📄"
          title="No resume analyzed yet"
          description="Upload your resume to get ATS score, skill extraction, and improvement suggestions."
          action={
            <label>
              <input type="file" accept=".pdf,.docx" onChange={handleUpload} className="hidden" />
              <span className="cursor-pointer rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700">
                Upload Resume
              </span>
            </label>
          }
        />
      ) : (
        <>
          <div className="grid gap-6 lg:grid-cols-3">
            <Card className="text-center lg:col-span-1">
              <p className="text-sm text-gray-500">ATS Score</p>
              <div className="relative mx-auto my-4 h-32 w-32">
                <svg className="h-full w-full -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="8" className="text-gray-200 dark:text-gray-700" />
                  <circle
                    cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="8"
                    strokeDasharray={`${(display.ats_score / 100) * 283} 283`}
                    className="text-primary-500"
                  />
                </svg>
                <span className="absolute inset-0 flex items-center justify-center text-3xl font-bold text-gray-900 dark:text-white">
                  {Math.round(display.ats_score)}%
                </span>
              </div>
              <p className="text-sm text-gray-500">{display.filename}</p>
            </Card>

            <div className="space-y-4 lg:col-span-2">
              <Card title="Strengths">
                <ul className="space-y-1">
                  {display.strengths?.map((s, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-emerald-700 dark:text-emerald-400">
                      <span>✓</span> {s}
                    </li>
                  ))}
                </ul>
              </Card>
              <Card title="Weaknesses">
                <ul className="space-y-1">
                  {display.weaknesses?.map((w, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-amber-700 dark:text-amber-400">
                      <span>!</span> {w}
                    </li>
                  ))}
                </ul>
              </Card>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <Card title="Extracted Skills">
              <div className="flex flex-wrap gap-2">
                {display.extracted_skills?.map((s) => (
                  <span key={s} className="rounded-full bg-primary-100 px-3 py-1 text-sm text-primary-700 dark:bg-primary-900/30 dark:text-primary-300">{s}</span>
                ))}
              </div>
            </Card>
            <Card title="Missing Skills">
              <div className="flex flex-wrap gap-2">
                {display.missing_skills?.map((s) => (
                  <span key={s} className="rounded-full bg-red-100 px-3 py-1 text-sm text-red-700 dark:bg-red-900/30 dark:text-red-300">{s}</span>
                ))}
              </div>
            </Card>
          </div>

          <Card title="Recommended Improvements">
            <ol className="list-decimal space-y-2 pl-5">
              {display.improvements?.map((imp, i) => (
                <li key={i} className="text-sm text-gray-600 dark:text-gray-300">{imp}</li>
              ))}
            </ol>
          </Card>
        </>
      )}
    </div>
  )
}
