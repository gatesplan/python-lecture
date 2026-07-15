import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getExam, createExam, updateExam, getProblems, getTags } from '../api'

const EMPTY_SECTION = { title: '', source_type: 'random', problem_ids: [], tags: [], count: 3 }

export default function ExamEdit() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isNew = !id

  const [title, setTitle] = useState('')
  const [showSolutions, setShowSolutions] = useState(false)
  const [sections, setSections] = useState([])
  const [allTags, setAllTags] = useState([])
  const [allProblems, setAllProblems] = useState([])

  useEffect(() => {
    getTags().then(setAllTags)
    getProblems().then(setAllProblems)
    if (id) {
      getExam(id).then(e => {
        setTitle(e.title)
        setShowSolutions(e.show_solutions)
        setSections(e.sections)
      })
    }
  }, [id])

  const updateSection = (idx, patch) => {
    setSections(prev => prev.map((s, i) => i === idx ? { ...s, ...patch } : s))
  }

  const removeSection = (idx) => {
    setSections(prev => prev.filter((_, i) => i !== idx))
  }

  const addSection = () => {
    setSections(prev => [...prev, { ...EMPTY_SECTION }])
  }

  const toggleProblem = (sIdx, pid) => {
    setSections(prev => prev.map((s, i) => {
      if (i !== sIdx) return s
      const ids = s.problem_ids.includes(pid)
        ? s.problem_ids.filter(x => x !== pid)
        : [...s.problem_ids, pid]
      return { ...s, problem_ids: ids }
    }))
  }

  const toggleTag = (sIdx, tag) => {
    setSections(prev => prev.map((s, i) => {
      if (i !== sIdx) return s
      const tags = s.tags.includes(tag)
        ? s.tags.filter(x => x !== tag)
        : [...s.tags, tag]
      return { ...s, tags }
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const data = { title, show_solutions: showSolutions, sections }
    if (isNew) {
      await createExam(data)
    } else {
      await updateExam(id, data)
    }
    navigate('/exams')
  }

  return (
    <>
      <div className="page-header">
        <h1>{isNew ? 'New Exam' : 'Edit Exam'}</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title</label>
          <input value={title} onChange={e => setTitle(e.target.value)} required />
        </div>

        <div className="form-group">
          <label>
            <input type="checkbox" checked={showSolutions} onChange={e => setShowSolutions(e.target.checked)} />
            {' '}Show solutions
          </label>
        </div>

        <h2>Sections</h2>

        {sections.map((section, sIdx) => (
          <div key={sIdx} className="card">
            <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
              <input
                placeholder="Section title"
                value={section.title}
                onChange={e => updateSection(sIdx, { title: e.target.value })}
                style={{ flex: 1 }}
              />
              <select
                value={section.source_type}
                onChange={e => updateSection(sIdx, { source_type: e.target.value })}
                style={{ width: 120 }}
              >
                <option value="random">Random</option>
                <option value="manual">Manual</option>
              </select>
              <button type="button" className="danger" onClick={() => removeSection(sIdx)}>Remove</button>
            </div>

            {section.source_type === 'random' && (
              <div>
                <div className="form-group">
                  <label>Tags (click to toggle)</label>
                  <div>
                    {allTags.map(tag => (
                      <span
                        key={tag}
                        className="tag"
                        style={{
                          cursor: 'pointer',
                          background: section.tags.includes(tag) ? '#2563eb' : '#e5e7eb',
                          color: section.tags.includes(tag) ? '#fff' : '#374151',
                        }}
                        onClick={() => toggleTag(sIdx, tag)}
                      >
                        {tag}
                      </span>
                    ))}
                    {allTags.length === 0 && <span style={{ color: '#999' }}>No tags</span>}
                  </div>
                </div>
                <div className="form-group">
                  <label>Count</label>
                  <input
                    type="number" min={1} value={section.count}
                    onChange={e => updateSection(sIdx, { count: parseInt(e.target.value) || 1 })}
                    style={{ width: 80 }}
                  />
                </div>
              </div>
            )}

            {section.source_type === 'manual' && (
              <div className="form-group">
                <label>Select problems</label>
                <div style={{ maxHeight: 200, overflow: 'auto', border: '1px solid #e5e5e5', borderRadius: 4, padding: 8 }}>
                  {allProblems.map(p => (
                    <label key={p.id} style={{ display: 'block', marginBottom: 4, cursor: 'pointer' }}>
                      <input
                        type="checkbox"
                        checked={section.problem_ids.includes(p.id)}
                        onChange={() => toggleProblem(sIdx, p.id)}
                      />
                      {' '}{p.title || '(no title)'}
                      {p.tags.map(t => <span key={t} className="tag" style={{ marginLeft: 4 }}>{t}</span>)}
                    </label>
                  ))}
                  {allProblems.length === 0 && <span style={{ color: '#999' }}>No problems</span>}
                </div>
              </div>
            )}
          </div>
        ))}

        <button type="button" onClick={addSection} className="mb-16">+ Add Section</button>

        <div className="actions mt-16">
          <button type="submit" className="primary">Save</button>
          <button type="button" onClick={() => navigate('/exams')}>Cancel</button>
        </div>
      </form>
    </>
  )
}
