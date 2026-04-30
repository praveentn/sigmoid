import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function AdminLogin() {
  const { login, user, loading } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (!loading && user) navigate('/admin/dashboard')
  }, [user, loading, navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login(form.username, form.password)
      navigate('/admin/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid credentials')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-ink flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        {/* Header */}
        <div className="mb-10">
          <p className="text-xs font-mono tracking-[0.3em] text-snow/30 uppercase mb-4">Admin Access</p>
          <h1 className="text-3xl font-black text-snow tracking-tight">Sign In</h1>
          <p className="text-sm text-snow/40 mt-2">Praveen T N — Portfolio CMS</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-mono text-snow/40 uppercase tracking-wide mb-1.5">
              Username
            </label>
            <input
              type="text"
              value={form.username}
              onChange={e => setForm({ ...form, username: e.target.value })}
              className="w-full bg-ink-soft border border-ink-muted text-snow px-4 py-3 text-sm focus:outline-none focus:border-snow/50 transition-colors"
              placeholder="admin"
              required
              autoFocus
            />
          </div>

          <div>
            <label className="block text-xs font-mono text-snow/40 uppercase tracking-wide mb-1.5">
              Password
            </label>
            <input
              type="password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
              className="w-full bg-ink-soft border border-ink-muted text-snow px-4 py-3 text-sm focus:outline-none focus:border-snow/50 transition-colors"
              placeholder="••••••••"
              required
            />
          </div>

          {error && (
            <p className="text-xs text-red-400 font-mono">{error}</p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-snow text-ink py-3 text-sm font-semibold tracking-wide hover:bg-cloud transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-2"
          >
            {submitting ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-8 text-center">
          <a href="/" className="text-xs font-mono text-snow/20 hover:text-snow/40 transition-colors">
            ← Back to portfolio
          </a>
        </div>
      </div>
    </div>
  )
}
