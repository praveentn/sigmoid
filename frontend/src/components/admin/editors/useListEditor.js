import { useEffect, useState } from 'react'

export function useListEditor(fetchFn, createFn, updateFn, deleteFn) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null) // null=closed, {} = new, item = existing
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  const load = async () => {
    const res = await fetchFn()
    setItems(res.data)
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  const openNew = (defaults = {}) => setEditing(defaults)
  const openEdit = (item) => setEditing({ ...item })
  const closeModal = () => setEditing(null)

  const handleSave = async (formData) => {
    setSaving(true)
    try {
      if (formData.id) {
        const res = await updateFn(formData.id, formData)
        setItems(items => items.map(i => i.id === formData.id ? res.data : i))
      } else {
        const res = await createFn(formData)
        setItems(items => [...items, res.data])
      }
      setEditing(null)
      setToast({ message: 'Saved successfully', type: 'success' })
    } catch (err) {
      setToast({ message: err.response?.data?.detail || 'Save failed', type: 'error' })
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this item?')) return
    try {
      await deleteFn(id)
      setItems(items => items.filter(i => i.id !== id))
      setToast({ message: 'Deleted', type: 'success' })
    } catch {
      setToast({ message: 'Delete failed', type: 'error' })
    }
  }

  return { items, loading, editing, saving, toast, setToast, openNew, openEdit, closeModal, handleSave, handleDelete }
}
