import { useState } from 'react'
import { api } from '../../../api/client'
import Modal, { FormField, Toast } from '../Modal'
import { useListEditor } from './useListEditor'

function ResearchForm({ initial, onSave, saving, onClose }) {
  const [form, setForm] = useState({ title: '', description: '', type: 'publication', focus_area: '', order: 0, ...initial })
  const s = (key) => (e) => setForm(f => ({ ...f, [key]: e.target.value }))

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSave(form) }} className="space-y-0">
      <FormField label="Title"><input className="admin-input" required value={form.title} onChange={s('title')} /></FormField>
      <div className="grid grid-cols-3 gap-3">
        <FormField label="Type">
          <select className="admin-input" value={form.type} onChange={s('type')}>
            <option value="publication">Publication</option>
            <option value="thesis">Thesis</option>
            <option value="article">Article</option>
          </select>
        </FormField>
        <FormField label="Focus Area"><input className="admin-input" value={form.focus_area} onChange={s('focus_area')} /></FormField>
        <FormField label="Order"><input className="admin-input" type="number" value={form.order} onChange={e => setForm(f => ({ ...f, order: parseInt(e.target.value) || 0 }))} /></FormField>
      </div>
      <FormField label="Description"><textarea className="admin-input h-24 resize-none" value={form.description} onChange={s('description')} /></FormField>
      <div className="flex gap-3 pt-3 border-t border-cloud">
        <button type="submit" disabled={saving} className="btn-primary text-xs">{saving ? 'Saving…' : 'Save'}</button>
        <button type="button" onClick={onClose} className="btn-ghost text-xs">Cancel</button>
      </div>
    </form>
  )
}

export default function ResearchEditor() {
  const { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete } =
    useListEditor(api.getResearch, api.createResearch, api.updateResearch, api.deleteResearch)

  if (loading) return <div className="text-sm text-silver">Loading…</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-xs text-silver font-mono">{items.length} items</p>
        <button onClick={() => openNew()} className="btn-primary text-xs">+ Add</button>
      </div>
      <div className="space-y-2">
        {items.map(item => (
          <div key={item.id} className="bg-white border border-cloud px-5 py-4 flex items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-ink">{item.title}</p>
              <p className="text-xs text-silver capitalize">{item.type} · {item.focus_area}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => openEdit(item)} className="btn-ghost text-xs">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        ))}
      </div>
      {editing !== null && (
        <Modal title={editing.id ? 'Edit Research' : 'Add Research'} onClose={closeModal}>
          <ResearchForm initial={editing} onSave={handleSave} saving={saving} onClose={closeModal} />
        </Modal>
      )}
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
