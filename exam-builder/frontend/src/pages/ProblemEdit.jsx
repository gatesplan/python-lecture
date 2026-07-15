import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getProblem, createProblem, updateProblem } from '../api'
import TagInput from '../components/TagInput'

const EMPTY = {
  title: '',
  description: '',
  code: '',
  input: '',
  output: '',
  hint: '',
  solution: '',
  tags: [],
}

export default function ProblemEdit() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isNew = !id
  const [form, setForm] = useState({ ...EMPTY })

  useEffect(() => {
    if (id) {
      getProblem(id).then(p => setForm({
        title: p.title || '',
        description: p.description || '',
        code: p.code || '',
        input: p.input || '',
        output: p.output || '',
        hint: p.hint || '',
        solution: p.solution || '',
        tags: p.tags || [],
      }))
    }
  }, [id])

  const set = (key, val) => setForm(prev => ({ ...prev, [key]: val }))

  const handleTab = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault()
      const ta = e.target
      const start = ta.selectionStart
      const end = ta.selectionEnd
      ta.value = ta.value.substring(0, start) + '    ' + ta.value.substring(end)
      ta.selectionStart = ta.selectionEnd = start + 4
      set(e.target.name, ta.value)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const data = {
      ...form,
      code: form.code || null,
      input: form.input || null,
      output: form.output || null,
      hint: form.hint || null,
      solution: form.solution || null,
    }
    if (isNew) {
      await createProblem(data)
    } else {
      await updateProblem(id, data)
    }
    navigate('/problems')
  }

  return (
    <>
      <div className="page-header">
        <h1>{isNew ? 'New Problem' : 'Edit Problem'}</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title</label>
          <input value={form.title} onChange={e => set('title', e.target.value)} required />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea rows={3} value={form.description} onChange={e => set('description', e.target.value)} required />
        </div>

        <div className="form-group">
          <label>Code</label>
          <textarea className="code" rows={8} name="code" value={form.code}
            onChange={e => set('code', e.target.value)} onKeyDown={handleTab} />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div className="form-group">
            <label>Input</label>
            <textarea className="code" rows={4} name="input" value={form.input}
              onChange={e => set('input', e.target.value)} onKeyDown={handleTab} />
          </div>
          <div className="form-group">
            <label>Output</label>
            <textarea className="code" rows={4} name="output" value={form.output}
              onChange={e => set('output', e.target.value)} onKeyDown={handleTab} />
          </div>
        </div>

        <div className="form-group">
          <label>Hint</label>
          <textarea rows={2} value={form.hint} onChange={e => set('hint', e.target.value)} />
        </div>

        <div className="form-group">
          <label>Solution</label>
          <textarea className="code" rows={6} name="solution" value={form.solution}
            onChange={e => set('solution', e.target.value)} onKeyDown={handleTab} />
        </div>

        <div className="form-group">
          <label>Tags</label>
          <TagInput tags={form.tags} onChange={tags => set('tags', tags)} />
        </div>

        <div className="actions mt-16">
          <button type="submit" className="primary">Save</button>
          <button type="button" onClick={() => navigate('/problems')}>Cancel</button>
        </div>
      </form>
    </>
  )
}
