import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Select from '../components/ui/Select'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { useRoles } from '../hooks/useRoles'

interface Message {
  id?: number
  role: string
  content: string
  evaluation?: {
    score?: number
    feedback: string
    needs_clarification?: boolean
    clarification_prompt?: string
    strengths?: string[]
    areas_to_improve?: string[]
  }
}

export default function MockInterview() {
  const roles = useRoles()
  const [interviewId, setInterviewId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [answer, setAnswer] = useState('')
  const [role, setRole] = useState(roles[0])
  const [difficulty, setDifficulty] = useState('intermediate')
  const [loading, setLoading] = useState(false)
  const [sending, setSending] = useState(false)
  const [complete, setComplete] = useState(false)
  const [showExitConfirm, setShowExitConfirm] = useState(false)
  const [needsClarification, setNeedsClarification] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()

  const questionCount = messages.filter((m) => m.role === 'interviewer').length
  const answeredCount = messages.filter((m) => m.role === 'candidate' && m.evaluation?.score !== undefined).length

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const startInterview = async () => {
    setLoading(true)
    try {
      const { data } = await api.post('/interviews', {
        title: `${role} Mock Interview`,
        difficulty,
        target_role: role,
      })
      setInterviewId(data.id)
      setMessages(data.messages || [])
      setComplete(false)
    } finally {
      setLoading(false)
    }
  }

  const sendAnswer = async () => {
    if (!answer.trim() || !interviewId) return
    setSending(true)
    const userMsg: Message = { role: 'candidate', content: answer }
    setMessages((prev) => [...prev, userMsg])
    setAnswer('')
    try {
      const { data } = await api.post(`/interviews/${interviewId}/message`, { content: answer })
      if (data.evaluation) {
        setMessages((prev) => {
          const updated = [...prev]
          const lastIdx = updated.length - 1
          if (lastIdx >= 0) updated[lastIdx] = { ...updated[lastIdx], evaluation: data.evaluation }
          return updated
        })
        // If clarification needed, show prompt instead of next question
        if (data.evaluation.needs_clarification) {
          setNeedsClarification(true)
          if (data.evaluation.clarification_prompt) {
            setMessages((prev) => [...prev, { role: 'interviewer', content: data.evaluation.clarification_prompt }])
          }
        } else {
          setNeedsClarification(false)
          // Stop after 10 questions instead of 5
          if (questionCount >= 10) {
            setComplete(true)
          } else if (data.next_question) {
            setMessages((prev) => [...prev, { role: 'interviewer', content: data.next_question }])
          }
        }
      }
    } finally {
      setSending(false)
    }
  }

  const finishAndGetFeedback = async () => {
    if (!interviewId) return
    setLoading(true)
    try {
      await api.post(`/interviews/${interviewId}/complete`)
      navigate(`/interview-feedback/${interviewId}`)
    } finally {
      setLoading(false)
    }
  }

  if (!interviewId) {
    return (
      <div className="animate-fade-in mx-auto max-w-lg space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Mock Interview</h1>
          <p className="text-gray-500">AI-powered interview simulation</p>
        </div>
        <Card>
          <div className="space-y-4">
            <Select label="Target Role" value={role} onChange={(e) => setRole(e.target.value)} options={roles.map((r) => ({ value: r, label: r }))} />
            <Select label="Difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} options={['beginner', 'intermediate', 'advanced'].map((d) => ({ value: d, label: d.charAt(0).toUpperCase() + d.slice(1) }))} />
            <Button onClick={startInterview} loading={loading} className="w-full">Start Interview</Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="animate-fade-in flex h-[calc(100vh-8rem)] flex-col">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">Mock Interview — {role}</h1>
          <p className="mt-1 text-sm text-gray-500">Question {questionCount} of 10 • {answeredCount} answered</p>
          <div className="mt-2 h-2 w-48 rounded-full bg-gray-200 dark:bg-gray-700">
            <div
              className="h-full rounded-full bg-primary-600 transition-all"
              style={{ width: `${(questionCount / 10) * 100}%` }}
            />
          </div>
        </div>
        <div className="flex gap-2">
          {complete ? (
            <Button onClick={finishAndGetFeedback} loading={loading}>Get Feedback & Score</Button>
          ) : (
            <Button onClick={() => setShowExitConfirm(true)} variant="secondary">Exit Interview</Button>
          )}
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto rounded-xl border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'candidate' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl px-4 py-3 ${
              msg.role === 'candidate'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-white'
            }`}>
              <p className="text-xs font-medium opacity-70 mb-1">
                {msg.role === 'candidate' ? 'You' : 'Interviewer'}
              </p>
              <p className="text-sm">{msg.content}</p>
              {msg.evaluation && (
                <div className="mt-3 space-y-2 rounded-lg bg-white/20 p-3 text-xs">
                  {msg.evaluation.needs_clarification ? (
                    <div className="text-yellow-100">
                      ⚠️ {msg.evaluation.feedback}
                    </div>
                  ) : (
                    <>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">Score: {msg.evaluation.score}/10</span>
                        <div className="h-2 flex-1 rounded-full bg-white/30">
                          <div
                            className="h-full rounded-full bg-white transition-all"
                            style={{ width: `${(msg.evaluation.score! / 10) * 100}%` }}
                          />
                        </div>
                      </div>
                      <p>{msg.evaluation.feedback}</p>
                      {msg.evaluation.strengths && msg.evaluation.strengths.length > 0 && (
                        <div>
                          <p className="font-semibold">✅ Strengths:</p>
                          <ul className="list-inside list-disc">
                            {msg.evaluation.strengths.map((s, idx) => <li key={idx}>{s}</li>)}
                          </ul>
                        </div>
                      )}
                      {msg.evaluation.areas_to_improve && msg.evaluation.areas_to_improve.length > 0 && (
                        <div>
                          <p className="font-semibold">📈 Areas to Improve:</p>
                          <ul className="list-inside list-disc">
                            {msg.evaluation.areas_to_improve.map((a, idx) => <li key={idx}>{a}</li>)}
                          </ul>
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        {sending && <LoadingSpinner message="Evaluating your answer..." />}
        <div ref={bottomRef} />
      </div>

      {!complete && (
        <div className="mt-4 space-y-3">
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendAnswer())}
            placeholder={needsClarification ? "Please provide a more detailed answer..." : "Type your answer..."}
            rows={2}
            className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm focus:border-primary-500 focus:outline-none dark:border-gray-600 dark:bg-gray-800 dark:text-white"
          />
          <Button onClick={sendAnswer} loading={sending} disabled={!answer.trim()} className="w-full">
            {needsClarification ? 'Try Again' : 'Submit Answer'}
          </Button>
        </div>
      )}

      {showExitConfirm && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50">
          <div className="rounded-xl bg-white p-6 dark:bg-gray-900">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white">Exit Interview?</h2>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
              You've completed {questionCount}/10 questions. You can still view your feedback and score.
            </p>
            <div className="mt-6 flex gap-3">
              <Button onClick={() => setShowExitConfirm(false)} variant="secondary" className="flex-1">
                Keep Going
              </Button>
              <Button
                onClick={() => {
                  setShowExitConfirm(false)
                  setComplete(true)
                }}
                className="flex-1"
              >
                Exit & Get Score
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
