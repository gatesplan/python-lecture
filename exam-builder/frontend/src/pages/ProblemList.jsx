import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { allProblems as draftProblems } from '../data/allProblems'

function normalizeIdToken(token) {
  const t = token.trim()
  if (!t) return null
  // 명시적 ID(g1-001, fb-01 등)는 그대로 매칭
  if (/^[a-z][a-z0-9]*-\d+$/i.test(t)) return t
  // 순수 숫자는 화면 목록의 위치(#)로 해석
  if (/^\d+$/.test(t)) {
    const pos = Number(t)
    if (pos >= 1 && pos <= draftProblems.length) return draftProblems[pos - 1].id
  }
  return null
}

function parseIdInput(raw) {
  const out = []
  for (const chunk of raw.split(',')) {
    const c = chunk.trim()
    if (!c) continue
    const range = c.match(/^(\d+)\s*-\s*(\d+)$/)
    if (range) {
      const [, aStr, bStr] = range
      let a = Number(aStr), b = Number(bStr)
      if (a > b) [a, b] = [b, a]
      for (let n = a; n <= b; n++) {
        const id = normalizeIdToken(String(n))
        if (id) out.push(id)
      }
      continue
    }
    const id = normalizeIdToken(c)
    if (id) out.push(id)
  }
  return out
}

function mulberry32(seed) {
  return function () {
    seed |= 0
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function seededShuffle(arr, seed) {
  const rng = mulberry32(seed)
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export default function ProblemList() {
  const navigate = useNavigate()
  const [count, setCount] = useState(5)
  const [useSeed, setUseSeed] = useState(false)
  const [seed, setSeed] = useState(() => Math.floor(Math.random() * 9000) + 1000)
  const [idInput, setIdInput] = useState('')

  const handleRandom = () => {
    const indices = Array.from({ length: draftProblems.length }, (_, i) => i)
    const n = Math.min(count, draftProblems.length)
    const actualSeed = useSeed ? seed : Math.floor(Math.random() * 9000) + 1000
    const shuffled = seededShuffle(indices, actualSeed)
    const picked = shuffled.slice(0, n).sort((a, b) => a - b)
    navigate(`/preview?pick=${picked.join(',')}&seed=${actualSeed}`)
  }

  const handleShowByIds = () => {
    const ids = parseIdInput(idInput)
    if (ids.length === 0) return
    navigate(`/preview?ids=${ids.join(',')}`)
  }

  return (
    <>
      <div className="page-header">
        <h1>Problems ({draftProblems.length})</h1>
      </div>

      <div style={{ marginBottom: 16, display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>Random</label>
        <input
          type="number" min={1} max={draftProblems.length}
          value={count} onChange={e => setCount(Number(e.target.value))}
          style={{ width: 60 }}
        />
        <label style={{ marginLeft: 8, display: 'flex', alignItems: 'center', gap: 4 }}>
          <input
            type="checkbox"
            checked={useSeed}
            onChange={e => setUseSeed(e.target.checked)}
          />
          Seed
        </label>
        {useSeed && (
          <input
            type="number"
            value={seed}
            onChange={e => setSeed(Number(e.target.value))}
            style={{ width: 80 }}
          />
        )}
        <button onClick={handleRandom}>Generate</button>
        <button onClick={() => navigate('/preview')}>Preview All</button>
      </div>

      <div style={{ marginBottom: 16, display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>By ID</label>
        <input
          type="text"
          placeholder="예: 1, 3, 5 또는 1-10 (목록 # 번호), 또는 g1-001"
          value={idInput}
          onChange={e => setIdInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') handleShowByIds() }}
          style={{ width: 260 }}
        />
        <button onClick={handleShowByIds}>Show</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>ID</th>
            <th>Type</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {draftProblems.map((p, i) => (
            <tr key={p.id || i}>
              <td>{i + 1}</td>
              <td>{p.id || '-'}</td>
              <td>{p.type}</td>
              <td>
                <span
                  style={{ cursor: 'pointer', color: '#0066cc', textDecoration: 'underline' }}
                  onClick={() => navigate(`/problems/draft/${i}`)}
                >
                  view
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
