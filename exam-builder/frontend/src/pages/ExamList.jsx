import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getExams, deleteExam } from '../api'

export default function ExamList() {
  const [exams, setExams] = useState([])
  const navigate = useNavigate()

  const load = () => getExams().then(setExams)
  useEffect(() => { load() }, [])

  const handleDelete = async (id) => {
    if (!confirm('Delete?')) return
    await deleteExam(id)
    load()
  }

  return (
    <>
      <div className="page-header">
        <h1>Exams</h1>
        <button className="primary" onClick={() => navigate('/exams/new')}>+ New</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Sections</th>
            <th style={{ width: 220 }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {exams.map(e => (
            <tr key={e.id}>
              <td><Link to={`/exams/${e.id}/edit`}>{e.title || '(no title)'}</Link></td>
              <td>{e.sections.length}</td>
              <td className="actions">
                <button onClick={() => navigate(`/exams/${e.id}/edit`)}>Edit</button>
                <button onClick={() => window.open(`/exams/${e.id}/print`, '_blank')}>Print</button>
                <button className="danger" onClick={() => handleDelete(e.id)}>Del</button>
              </td>
            </tr>
          ))}
          {exams.length === 0 && (
            <tr><td colSpan={3} style={{ textAlign: 'center', color: '#999' }}>No exams yet</td></tr>
          )}
        </tbody>
      </table>
    </>
  )
}
