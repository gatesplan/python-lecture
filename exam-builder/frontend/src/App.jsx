import { Routes, Route, NavLink, Outlet } from 'react-router-dom'
import ProblemList from './pages/ProblemList'
import ProblemView from './pages/ProblemView'
import ProblemDraftView from './pages/ProblemDraftView'
import Preview from './pages/Preview'

function Layout() {
  return (
    <>
      <nav>
        <span className="brand">Exam Builder</span>
        <NavLink to="/problems">Problems</NavLink>
      </nav>
      <div className="container">
        <Outlet />
      </div>
    </>
  )
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<ProblemList />} />
        <Route path="problems" element={<ProblemList />} />
      </Route>
      <Route path="problems/:id" element={<ProblemView />} />
      <Route path="problems/draft/:idx" element={<ProblemDraftView />} />
      <Route path="preview" element={<Preview />} />
    </Routes>
  )
}
