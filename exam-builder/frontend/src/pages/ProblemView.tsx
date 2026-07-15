import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import type { Problem, ContentBlock } from '../ln/problem/l0/types'
import { ProblemRenderer } from '../components/problem'
import './ProblemView.css'

export default function ProblemView() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [raw, setRaw] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/problems/${id}`)
      .then(r => r.json())
      .then(data => { setRaw(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [id])

  if (loading) {
    return <div className="a4-viewer"><p className="a4-message">Loading...</p></div>
  }
  if (!raw) {
    return <div className="a4-viewer"><p className="a4-message">Problem not found</p></div>
  }

  const problem: Problem = raw.content && Array.isArray(raw.content)
    ? raw as Problem
    : fromLegacy(raw)

  const title = raw.title ?? `Problem ${id}`

  return (
    <div className="a4-viewer">
      <div className="a4-toolbar">
        <button onClick={() => navigate('/problems')}>Back</button>
        <span className="a4-toolbar-title">{title}</span>
        <button onClick={() => window.print()}>Print</button>
      </div>
      <div className="a4-paper">
        <ProblemRenderer problem={problem} problemNumber={1} />
      </div>
    </div>
  )
}

function fromLegacy(p: any): Problem {
  const blocks: ContentBlock[] = []
  if (p.description) blocks.push({ type: 'text', content: p.description })
  if (p.code) blocks.push({ type: 'code', content: p.code, language: 'python' })
  if (p.input && p.output) {
    blocks.push({ type: 'io-sample', input: p.input, output: p.output })
  } else {
    if (p.input) blocks.push({ type: 'input-sample', content: p.input })
    if (p.output) blocks.push({ type: 'output-sample', content: p.output })
  }
  if (blocks.length === 0) {
    blocks.push({ type: 'text', content: '(No content)' })
  }
  return { type: 'short', content: blocks }
}
