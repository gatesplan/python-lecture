import { useNavigate, useParams } from 'react-router-dom'
import type { Problem } from '../ln/problem/l0/types'
import { ProblemRenderer } from '../components/problem'
import './ProblemView.css'
import { allProblems } from '../data/allProblems'

const problems = allProblems as Problem[]

export default function ProblemDraftView() {
  const { idx } = useParams()
  const navigate = useNavigate()
  const i = Number(idx)
  const problem = problems[i]

  if (!problem) {
    return <div className="a4-viewer"><p>Problem not found</p></div>
  }

  return (
    <div className="a4-viewer">
      <div className="a4-toolbar">
        <button onClick={() => navigate('/')}>Back</button>
        <span className="a4-toolbar-title">Problem {i + 1} / {problems.length}</span>
        <div style={{ display: 'flex', gap: 8 }}>
          {i > 0 && <button onClick={() => navigate(`/problems/draft/${i - 1}`)}>Prev</button>}
          {i < problems.length - 1 && <button onClick={() => navigate(`/problems/draft/${i + 1}`)}>Next</button>}
        </div>
      </div>
      <div className="a4-paper">
        <ProblemRenderer problem={problem} problemNumber={i + 1} />
      </div>
    </div>
  )
}
