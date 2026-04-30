import { useState } from 'react'
import { api } from '../../../api/client'
import Modal, { FormField, Toast } from '../Modal'
import { useListEditor } from './useListEditor'

function ExperienceForm({ initial, onSave, saving, onClose }) {
  const [form, setForm] = useState({
    company: '', role: '', period_start: '', period_end: '', location: '',
    tagline: '', highlights: [], is_current: false, order: 0,
    ...initial,
  })
  const [highlightInput, setHighlightInput] = useState(form.highlights?.join('\n') || '')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave({ ...form, highlights: highlightInput.split('\n').map(s => s.trim()).filter(Boolean) })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-0">
      <div className="grid grid-cols-2 gap-3">
        <FormField label="Company">
          <input className="admin-input" required value={form.company} onChange={e => setForm(f => ({ ...f, company: e.target.value }))} />
        </FormField>
        <FormField label="Role">
          <input className="admin-input" required value={form.role} onChange={e => setForm(f => ({ ...f, role: e.target.value }))} />
        </FormField>
        <FormField label="Period Start">
          <input className="admin-input" placeholder="Oct 2021" value={form.period_start} onChange={e => setForm(f => ({ ...f, period_start: e.target.value }))} />
        </FormField>
        <FormField label="Period End">
          <input className="admin-input" placeholder="Present" value={form.period_end} onChange={e => setForm(f => ({ ...f, period_end: e.target.value }))} />
        </FormField>
      </div>
      <FormField label="Location">
        <input className="admin-input" value={form.location} onChange={e => setForm(f => ({ ...f, location: e.target.value }))} />
      </FormField>
      <FormField label="Tagline">
        <textarea className="admin-input h-16 resize-none" value={form.tagline} onChange={e => setForm(f => ({ ...f, tagline: e.target.value }))} />
      </FormField>
      <FormField label="Highlights (one per line)">
        <textarea className="admin-input h-36 resize-y font-mono text-xs" value={highlightInput} onChange={e => setHighlightInput(e.target.value)} />
      </FormField>
      <div className="flex items-center gap-3 mb-4">
        <input type="checkbox" id="is_current" checked={form.is_current} onChange={e => setForm(f => ({ ...f, is_current: e.target.checked }))} />
        <label htmlFor="is_current" className="text-xs text-graphite">Current role</label>
        <input className="admin-input w-20 ml-4" type="number" placeholder="Order" value={form.order} onChange={e => setForm(f => ({ ...f, order: parseInt(e.target.value) || 0 }))} />
        <span className="text-xs text-silver">Order</span>
      </div>
      <div className="flex gap-3 pt-3 border-t border-cloud">
        <button type="submit" disabled={saving} className="btn-primary text-xs">{saving ? 'Saving…' : 'Save'}</button>
        <button type="button" onClick={onClose} className="btn-ghost text-xs">Cancel</button>
      </div>
    </form>
  )
}

export default function ExperienceEditor() {
  const { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete } =
    useListEditor(api.getExperience, api.createExperience, api.updateExperience, api.deleteExperience)

  if (loading) return <div className="text-sm text-silver">Loading…</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-xs text-silver font-mono">{items.length} entries</p>
        <button onClick={() => openNew({ order: items.length + 1 })} className="btn-primary text-xs">+ Add</button>
      </div>

      <div className="space-y-2">
        {items.map(item => (
          <div key={item.id} className="bg-white border border-cloud px-5 py-4 flex items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-ink">{item.role}</p>
              <p className="text-xs text-silver">{item.company} · {item.period_start} — {item.period_end}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => openEdit(item)} className="btn-ghost text-xs">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        ))}
      </div>

      {editing !== null && (
        <Modal title={editing.id ? 'Edit Experience' : 'Add Experience'} onClose={closeModal} wide>
          <ExperienceForm initial={editing} onSave={handleSave} saving={saving} onClose={closeModal} />
        </Modal>
      )}
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
