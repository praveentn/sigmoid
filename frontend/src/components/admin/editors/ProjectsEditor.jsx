import { useState } from 'react'
import { api } from '../../../api/client'
import Modal, { FormField, Toast } from '../Modal'
import { useListEditor } from './useListEditor'

function ProjectForm({ initial, onSave, saving, onClose }) {
  const [form, setForm] = useState({
    name: '', description: '', tech_stack: [], period: '', category: '',
    company: '', role: '', highlights: [], is_featured: false, order: 0,
    ...initial,
  })
  const [techText, setTechText] = useState(form.tech_stack?.join(', ') || '')
  const [highlightsText, setHighlightsText] = useState(form.highlights?.join('\n') || '')
  const s = (key) => (e) => setForm(f => ({ ...f, [key]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave({
      ...form,
      tech_stack: techText.split(',').map(s => s.trim()).filter(Boolean),
      highlights: highlightsText.split('\n').map(s => s.trim()).filter(Boolean),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-0">
      <div className="grid grid-cols-2 gap-3">
        <FormField label="Project Name"><input className="admin-input" required value={form.name} onChange={s('name')} /></FormField>
        <FormField label="Category"><input className="admin-input" value={form.category} onChange={s('category')} placeholder="Agentic AI, RAG, ML…" /></FormField>
        <FormField label="Company"><input className="admin-input" value={form.company} onChange={s('company')} /></FormField>
        <FormField label="Role"><input className="admin-input" value={form.role} onChange={s('role')} /></FormField>
        <FormField label="Period"><input className="admin-input" value={form.period} onChange={s('period')} placeholder="2023-2024" /></FormField>
        <FormField label="Order"><input className="admin-input" type="number" value={form.order} onChange={e => setForm(f => ({ ...f, order: parseInt(e.target.value) || 0 }))} /></FormField>
      </div>
      <FormField label="Description"><textarea className="admin-input h-20 resize-none" value={form.description} onChange={s('description')} /></FormField>
      <FormField label="Tech Stack (comma separated)"><input className="admin-input" value={techText} onChange={e => setTechText(e.target.value)} /></FormField>
      <FormField label="Highlights (one per line)">
        <textarea className="admin-input h-28 resize-y font-mono text-xs" value={highlightsText} onChange={e => setHighlightsText(e.target.value)} />
      </FormField>
      <div className="flex items-center gap-2 mb-4">
        <input type="checkbox" id="featured_proj" checked={form.is_featured} onChange={e => setForm(f => ({ ...f, is_featured: e.target.checked }))} />
        <label htmlFor="featured_proj" className="text-xs text-graphite">Featured project</label>
      </div>
      <div className="flex gap-3 pt-3 border-t border-cloud">
        <button type="submit" disabled={saving} className="btn-primary text-xs">{saving ? 'Saving…' : 'Save'}</button>
        <button type="button" onClick={onClose} className="btn-ghost text-xs">Cancel</button>
      </div>
    </form>
  )
}

export default function ProjectsEditor() {
  const { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete } =
    useListEditor(api.getProjects, api.createProject, api.updateProject, api.deleteProject)

  if (loading) return <div className="text-sm text-silver">Loading…</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-xs text-silver font-mono">{items.length} projects</p>
        <button onClick={() => openNew()} className="btn-primary text-xs">+ Add</button>
      </div>
      <div className="space-y-2">
        {items.map(item => (
          <div key={item.id} className="bg-white border border-cloud px-5 py-4 flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <p className="text-sm font-semibold text-ink">{item.name}</p>
                {item.is_featured && <span className="text-xs bg-ink text-snow px-1.5 py-0.5 font-mono">FEATURED</span>}
              </div>
              <p className="text-xs text-silver">{item.company} · {item.category} · {item.period}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => openEdit(item)} className="btn-ghost text-xs">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        ))}
      </div>
      {editing !== null && (
        <Modal title={editing.id ? 'Edit Project' : 'Add Project'} onClose={closeModal} wide>
          <ProjectForm initial={editing} onSave={handleSave} saving={saving} onClose={closeModal} />
        </Modal>
      )}
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
