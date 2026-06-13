import { useNavigate, useSearchParams } from 'react-router-dom'
import type { Problem } from '../ln/problem/l0/types'
import { ProblemRenderer } from '../components/problem'
import { A4AutoLayout } from '../components/A4AutoLayout'
import './ProblemView.css'
import { allProblems as allProblemsRaw } from '../data/allProblems'

const allProblems = allProblemsRaw as Problem[]

export default function Preview() {
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const pick = params.get('pick')
  const idsParam = params.get('ids')

  const seed = params.get('seed')

  let problems: Problem[]
  if (idsParam) {
    const wanted = idsParam.split(',').map(s => s.trim()).filter(Boolean)
    const byId = new Map(allProblems.map(p => [p.id, p]))
    problems = wanted
      .map(id => byId.get(id))
      .filter((p): p is Problem => p !== undefined)
  } else if (pick) {
    const indices = pick.split(',').map(Number).filter(i => i >= 0 && i < allProblems.length)
    problems = indices.map(i => allProblems[i])
  } else {
    problems = allProblems
  }

  const buildHeader = seed ? (
    <div style={{ textAlign: 'center', fontSize: '11pt', fontWeight: 600, paddingBottom: '2mm' }}>
      V1 TestBuild {seed}
    </div>
  ) : null

  const items = problems.map((p, i) => (
    <ProblemRenderer key={i} problem={p} problemNumber={i + 1} />
  ))

  const explainItems = problems.map((p, i) => (
    <ProblemRenderer key={`ex-${i}`} problem={p} problemNumber={i + 1} showExplain />
  ))

  return (
    <div className="a4-viewer">
      <div className="a4-toolbar">
        <button onClick={() => navigate('/')}>Back</button>
        <span className="a4-toolbar-title">Preview ({problems.length})</span>
        <button onClick={() => window.print()}>Print</button>
      </div>
      <A4AutoLayout items={items} header={buildHeader} gapMm={40} maxPerColumn={2} />
      <A4AutoLayout items={explainItems} gapMm={40} maxPerColumn={2} />
    </div>
  )
}
