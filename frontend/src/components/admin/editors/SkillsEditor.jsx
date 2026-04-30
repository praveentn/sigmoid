import { useState } from 'react'
import { api } from '../../../api/client'
import Modal, { FormField, Toast } from '../Modal'
import { useListEditor } from './useListEditor'

function SkillForm({ initial, onSave, saving, onClose }) {
  const [form, setForm] = useState({ category: '', items: [], order: 0, ...initial })
  const [itemsText, setItemsText] = useState(form.items?.join(', ') || '')

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSave({ ...form, items: itemsText.split(',').map(s => s.trim()).filter(Boolean) }) }} className="space-y-0">
      <div className="grid grid-cols-2 gap-3">
        <FormField label="Category"><input className="admin-input" required value={form.category} onChange={e => setForm(f => ({ ...f, category: e.target.value }))} /></FormField>
        <FormField label="Order"><input className="admin-input" type="number" value={form.order} onChange={e => setForm(f => ({ ...f, order: parseInt(e.target.value) || 0 }))} /></FormField>
      </div>
      <FormField label="Items (comma separated)">
        <textarea className="admin-input h-24 resize-none" value={itemsText} onChange={e => setItemsText(e.target.value)} placeholder="Python, FastAPI, React, ..." />
      </FormField>
      <div className="flex gap-3 pt-3 border-t border-cloud">
        <button type="submit" disabled={saving} className="btn-primary text-xs">{saving ? 'Saving…' : 'Save'}</button>
        <button type="button" onClick={onClose} className="btn-ghost text-xs">Cancel</button>
      </div>
    </form>
  )
}

export default function SkillsEditor() {
  const { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete } =
    useListEditor(api.getSkills, api.createSkill, api.updateSkill, api.deleteSkill)

  if (loading) return <div className="text-sm text-silver">Loading…</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-xs text-silver font-mono">{items.length} categories</p>
        <button onClick={() => openNew()} className="btn-primary text-xs">+ Add</button>
      </div>
      <div className="space-y-2">
        {items.map(item => (
          <div key={item.id} className="bg-white border border-cloud px-5 py-4 flex items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-ink">{item.category}</p>
              <p className="text-xs text-silver">{item.items?.join(', ')}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => openEdit(item)} className="btn-ghost text-xs">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        ))}
      </div>
      {editing !== null && (
        <Modal title={editing.id ? 'Edit Skill Category' : 'Add Skill Category'} onClose={closeModal}>
          <SkillForm initial={editing} onSave={handleSave} saving={saving} onClose={closeModal} />
        </Modal>
      )}
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
