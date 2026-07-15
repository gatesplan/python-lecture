import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { renderExam } from '../api'
import './ExamPrint.css'

export default function ExamPrint() {
  const { id } = useParams()
  const [exam, setExam] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    renderExam(id)
      .then(setExam)
      .catch(err => setError(err.message))
  }, [id])

  if (error) return <div style={{ padding: 40, color: 'red' }}>Error: {error}</div>
  if (!exam) return <div style={{ padding: 40 }}>Loading...</div>

  let num = 1

  return (
    <div className="print-page">
      <div className="print-actions">
        <button onClick={() => window.print()}>Print (Ctrl+P)</button>
        <button onClick={() => window.close()} style={{ marginLeft: 8 }}>Close</button>
      </div>

      <h1>{exam.title}</h1>

      {exam.sections.map((section, sIdx) => (
        <div key={sIdx}>
          <h2>{section.title}</h2>
          {section.problems.map((p) => {
            const n = num++
            return (
              <div key={p.id} className="problem">
                <div className="problem-header">
                  <span className="problem-number">{n}. </span>
                  {p.description}
                </div>
                {p.code && <div className="code-block">{p.code}</div>}
                {p.input && <div className="input-example">{p.input}</div>}
                {p.output && <div className="output-example">{p.output}</div>}
                {p.hint && <div className="hint">{p.hint}</div>}
                {exam.show_solutions && p.solution && (
                  <div className="solution">{p.solution}</div>
                )}
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}
