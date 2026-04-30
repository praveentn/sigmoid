import { useState } from 'react'
import { api } from '../../../api/client'
import Modal, { FormField, Toast } from '../Modal'
import { useListEditor } from './useListEditor'

function CertForm({ initial, onSave, saving, onClose }) {
  const [form, setForm] = useState({ name: '', issuer: '', year: '', is_featured: false, order: 0, ...initial })
  const s = (key) => (e) => setForm(f => ({ ...f, [key]: e.target.value }))

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSave(form) }} className="space-y-0">
      <FormField label="Certification Name"><input className="admin-input" required value={form.name} onChange={s('name')} /></FormField>
      <div className="grid grid-cols-3 gap-3">
        <FormField label="Issuer"><input className="admin-input" value={form.issuer} onChange={s('issuer')} /></FormField>
        <FormField label="Year"><input className="admin-input" value={form.year} onChange={s('year')} /></FormField>
        <FormField label="Order"><input className="admin-input" type="number" value={form.order} onChange={e => setForm(f => ({ ...f, order: parseInt(e.target.value) || 0 }))} /></FormField>
      </div>
      <div className="flex items-center gap-2 mb-4">
        <input type="checkbox" id="featured" checked={form.is_featured} onChange={e => setForm(f => ({ ...f, is_featured: e.target.checked }))} />
        <label htmlFor="featured" className="text-xs text-graphite">Featured (shown prominently)</label>
      </div>
      <div className="flex gap-3 pt-3 border-t border-cloud">
        <button type="submit" disabled={saving} className="btn-primary text-xs">{saving ? 'Saving…' : 'Save'}</button>
        <button type="button" onClick={onClose} className="btn-ghost text-xs">Cancel</button>
      </div>
    </form>
  )
}

export default function CertificationsEditor() {
  const { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete } =
    useListEditor(api.getCertifications, api.createCertification, api.updateCertification, api.deleteCertification)

  if (loading) return <div className="text-sm text-silver">Loading…</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-xs text-silver font-mono">{items.length} certifications</p>
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
              <p className="text-xs text-silver">{item.issuer} · {item.year}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => openEdit(item)} className="btn-ghost text-xs">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        ))}
      </div>
      {editing !== null && (
        <Modal title={editing.id ? 'Edit Certification' : 'Add Certification'} onClose={closeModal}>
          <CertForm initial={editing} onSave={handleSave} saving={saving} onClose={closeModal} />
        </Modal>
      )}
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
