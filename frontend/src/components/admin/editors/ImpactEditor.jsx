import { useState } from 'react'
import { api } from '../../../api/client'
import Modal, { FormField, Toast } from '../Modal'
import { useListEditor } from './useListEditor'

function ImpactForm({ initial, onSave, saving, onClose }) {
  const [form, setForm] = useState({ metric: '', label: '', description: '', order: 0, ...initial })
  const s = (key) => (e) => setForm(f => ({ ...f, [key]: e.target.value }))

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSave(form) }} className="space-y-0">
      <div className="grid grid-cols-3 gap-3">
        <FormField label="Metric (e.g. 30+)"><input className="admin-input" required value={form.metric} onChange={s('metric')} placeholder="30+" /></FormField>
        <FormField label="Label"><input className="admin-input" required value={form.label} onChange={s('label')} placeholder="Enterprise AI Solutions" /></FormField>
        <FormField label="Order"><input className="admin-input" type="number" value={form.order} onChange={e => setForm(f => ({ ...f, order: parseInt(e.target.value) || 0 }))} /></FormField>
      </div>
      <FormField label="Description (shown on hover)"><input className="admin-input" value={form.description} onChange={s('description')} /></FormField>
      <div className="flex gap-3 pt-3 border-t border-cloud">
        <button type="submit" disabled={saving} className="btn-primary text-xs">{saving ? 'Saving…' : 'Save'}</button>
        <button type="button" onClick={onClose} className="btn-ghost text-xs">Cancel</button>
      </div>
    </form>
  )
}

export default function ImpactEditor() {
  const { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete } =
    useListEditor(api.getImpact, api.createImpact, api.updateImpact, api.deleteImpact)

  if (loading) return <div className="text-sm text-silver">Loading…</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-xs text-silver font-mono">{items.length} metrics</p>
        <button onClick={() => openNew()} className="btn-primary text-xs">+ Add</button>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {items.map(item => (
          <div key={item.id} className="bg-white border border-cloud px-5 py-4 flex items-start justify-between gap-4">
            <div>
              <p className="text-2xl font-black text-ink">{item.metric}</p>
              <p className="text-sm font-semibold text-graphite">{item.label}</p>
              <p className="text-xs text-silver mt-0.5">{item.description}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => openEdit(item)} className="btn-ghost text-xs">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        ))}
      </div>
      {editing !== null && (
        <Modal title={editing.id ? 'Edit Metric' : 'Add Metric'} onClose={closeModal}>
          <ImpactForm initial={editing} onSave={handleSave} saving={saving} onClose={closeModal} />
        </Modal>
      )}
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
