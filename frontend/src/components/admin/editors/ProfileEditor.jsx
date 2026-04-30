import { useEffect, useState } from 'react'
import { api } from '../../../api/client'
import { FormField } from '../Modal'
import { Toast } from '../Modal'

export default function ProfileEditor() {
  const [form, setForm] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    api.getProfile().then(r => { setForm(r.data); setLoading(false) })
  }, [])

  const handleChange = (key, value) => setForm(f => ({ ...f, [key]: value }))

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const res = await api.updateProfile(form)
      setForm(res.data)
      setToast({ message: 'Profile updated', type: 'success' })
    } catch {
      setToast({ message: 'Failed to save', type: 'error' })
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="text-sm text-silver">Loading...</div>

  return (
    <div className="max-w-2xl">
      <form onSubmit={handleSave} className="space-y-0">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <FormField label="Full Name">
            <input className="admin-input" value={form.name || ''} onChange={e => handleChange('name', e.target.value)} />
          </FormField>
          <FormField label="Company">
            <input className="admin-input" value={form.company || ''} onChange={e => handleChange('company', e.target.value)} />
          </FormField>
        </div>

        <FormField label="Title">
          <input className="admin-input" value={form.title || ''} onChange={e => handleChange('title', e.target.value)} />
        </FormField>

        <FormField label="Tagline">
          <textarea className="admin-input h-20 resize-none" value={form.tagline || ''} onChange={e => handleChange('tagline', e.target.value)} />
        </FormField>

        <FormField label="Bio">
          <textarea className="admin-input h-40 resize-y" value={form.bio || ''} onChange={e => handleChange('bio', e.target.value)} />
        </FormField>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormField label="Email">
            <input className="admin-input" type="email" value={form.email || ''} onChange={e => handleChange('email', e.target.value)} />
          </FormField>
          <FormField label="Phone">
            <input className="admin-input" value={form.phone || ''} onChange={e => handleChange('phone', e.target.value)} />
          </FormField>
          <FormField label="Location">
            <input className="admin-input" value={form.location || ''} onChange={e => handleChange('location', e.target.value)} />
          </FormField>
          <FormField label="Visa Info">
            <input className="admin-input" value={form.visa_info || ''} onChange={e => handleChange('visa_info', e.target.value)} />
          </FormField>
          <FormField label="LinkedIn URL">
            <input className="admin-input" value={form.linkedin_url || ''} onChange={e => handleChange('linkedin_url', e.target.value)} />
          </FormField>
          <FormField label="Credly URL">
            <input className="admin-input" value={form.credly_url || ''} onChange={e => handleChange('credly_url', e.target.value)} />
          </FormField>
          <FormField label="Years Experience">
            <input className="admin-input" type="number" value={form.years_experience || ''} onChange={e => handleChange('years_experience', parseInt(e.target.value))} />
          </FormField>
          <FormField label="Solutions Delivered">
            <input className="admin-input" type="number" value={form.solutions_delivered || ''} onChange={e => handleChange('solutions_delivered', parseInt(e.target.value))} />
          </FormField>
        </div>

        <div className="pt-4 border-t border-cloud mt-6">
          <button
            type="submit"
            disabled={saving}
            className="btn-primary text-sm disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
