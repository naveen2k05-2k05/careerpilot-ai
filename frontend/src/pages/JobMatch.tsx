import { useState } from 'react'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Textarea from '../components/ui/Textarea'
import Input from '../components/ui/Input'
import LoadingSpinner from '../components/ui/LoadingSpinner'

interface SkillGap {
  skill: string
  importance: string
  current_level: string
  learning_path?: string
  estimated_weeks?: number
}

interface MatchResult {
  match_percentage: number
  match_breakdown?: { technical_skills: number; soft_skills: number; experience_level: number }
  missing_skills: string[]
  skill_gap_analysis: SkillGap[]
  action_plan: string[]
  recommendation?: string
}

export default function JobMatch() {
  const [jobDescription, setJobDescription] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [role, setRole] = useState('')
  const [saveApplication, setSaveApplication] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<MatchResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyze = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description')
      return
    }
    setLoading(true)
    setError('')
    try {
      let data
      if (file) {
        const form = new FormData()
        form.append('file', file)
        form.append('job_description', jobDescription)
        const res = await api.post('/job-match/analyze-upload', form, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        data = res.data
      } else {
        const res = await api.post('/job-match/analyze', {
          job_description: jobDescription,
          company_name: companyName || undefined,
          role: role || undefined,
          save_application: saveApplication && !!companyName && !!role,
        })
        data = res.data
      }
      setResult(data)
    } catch {
      setError('Analysis failed. Upload a resume or analyze an existing one first.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="animate-fade-in space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Job Match Analyzer</h1>
        <p className="text-gray-500">Compare your resume against a job description</p>
      </div>

      <Card>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Resume (optional upload)</label>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:rounded-lg file:border-0 file:bg-primary-50 file:px-4 file:py-2 file:text-sm file:font-medium file:text-primary-700"
            />
            <p className="mt-1 text-xs text-gray-400">Leave empty to use your latest uploaded resume</p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input label="Company (optional)" value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="Acme Corp" />
            <Input label="Role (optional)" value={role} onChange={(e) => setRole(e.target.value)} placeholder="Software Engineer" />
          </div>
          <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
            <input type="checkbox" checked={saveApplication} onChange={(e) => setSaveApplication(e.target.checked)} />
            Save as job application after analysis
          </label>
          <Textarea
            label="Job Description"
            rows={8}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the full job description here..."
          />
          {error && <p className="text-sm text-red-500">{error}</p>}
          <Button onClick={analyze} loading={loading}>Analyze Match</Button>
        </div>
      </Card>

      {loading && <LoadingSpinner message="Analyzing job match..." />}

      {result && !loading && (
        <div className="space-y-6">
          <Card className="bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-800/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Overall Match Score</p>
                <p className="mt-1 text-4xl font-bold text-primary-600 dark:text-primary-400">{Math.round(result.match_percentage)}%</p>
              </div>
              <div className="text-right">
                <div className="inline-flex h-20 w-20 items-center justify-center rounded-full bg-white dark:bg-gray-800">
                  <span className="text-2xl font-bold text-primary-600">{Math.round(result.match_percentage)}%</span>
                </div>
              </div>
            </div>
            {result.recommendation && <p className="mt-4 text-sm text-gray-700 dark:text-gray-300">✨ {result.recommendation}</p>}
          </Card>

          {result.match_breakdown && (
            <Card title="Match Breakdown">
              <div className="grid gap-4 sm:grid-cols-3">
                {[
                  { label: 'Technical Skills', value: result.match_breakdown.technical_skills },
                  { label: 'Soft Skills', value: result.match_breakdown.soft_skills },
                  { label: 'Experience Level', value: result.match_breakdown.experience_level },
                ].map((item) => (
                  <div key={item.label} className="rounded-lg bg-gray-50 p-4 dark:bg-gray-800">
                    <p className="text-xs font-medium text-gray-600 dark:text-gray-400">{item.label}</p>
                    <div className="mt-2 flex items-end gap-2">
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">{item.value}%</p>
                    </div>
                    <div className="mt-2 h-2 w-full rounded-full bg-gray-200 dark:bg-gray-700">
                      <div 
                        className={`h-full rounded-full transition-all ${
                          item.value >= 70 ? 'bg-green-500' : item.value >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${item.value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          <Card title="🎯 Skill Gap Analysis & Learning Path">
            <div className="space-y-3">
              {result.skill_gap_analysis && result.skill_gap_analysis.length > 0 ? (
                result.skill_gap_analysis.map((gap, i) => (
                  <div key={i} className="rounded-lg border border-gray-200 p-4 dark:border-gray-700">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h4 className="font-semibold text-gray-900 dark:text-white">{gap.skill}</h4>
                          <span className={`rounded-full px-2 py-1 text-xs font-medium ${
                            gap.importance === 'high'
                              ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                              : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
                          }`}>
                            {gap.importance} priority
                          </span>
                        </div>
                        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">Current Level: {gap.current_level}</p>
                        {gap.learning_path && (
                          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">📚 {gap.learning_path}</p>
                        )}
                        {gap.estimated_weeks && (
                          <p className="mt-1 text-xs text-gray-500">⏱️ Estimated learning time: {gap.estimated_weeks} weeks</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-600 dark:text-gray-400">✅ No major skill gaps detected - you're well-positioned!</p>
              )}
            </div>
          </Card>

          <Card title="📋 Your Personalized Action Plan">
            <div className="space-y-3">
              {result.action_plan?.map((step, i) => (
                <div key={i} className="flex gap-3 rounded-lg bg-gray-50 p-3 dark:bg-gray-800">
                  <div className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 text-xs font-bold text-primary-700 dark:bg-primary-900/30 dark:text-primary-400">
                    {i + 1}
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{step}</p>
                </div>
              ))}
            </div>
          </Card>

          {result.missing_skills && result.missing_skills.length > 0 && (
            <Card title="⚠️ Skills to Develop">
              <div className="flex flex-wrap gap-2">
                {result.missing_skills.map((skill) => (
                  <span key={skill} className="inline-flex items-center gap-1 rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-700 dark:bg-red-900/20 dark:text-red-400">
                    {skill}
                  </span>
                ))}
              </div>
              <p className="mt-4 text-xs text-gray-500 dark:text-gray-400">
                Focus on the high-priority skills listed above to maximize your chances of getting this role.
              </p>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
