import { Routes, Route, Navigate } from 'react-router-dom'
import { AppShell } from './layouts/AppShell'
import { DashboardFresh as Dashboard } from './pages/DashboardFresh'
import { Models } from './pages/Models'
import { ModelCreate } from './pages/ModelCreate'
import { ModelDesigner } from './pages/ModelDesigner'
import { Composer } from './pages/Composer'
import { Sweeps } from './pages/Sweeps'
import { Leaderboard } from './pages/Leaderboard'
import { Signals } from './pages/Signals'
import { Health } from './pages/Health'
import { Overlay } from './pages/Overlay'
import { ComponentShowcase } from './pages/ComponentShowcase'

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppShell />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="models">
          <Route index element={<Models />} />
          <Route path="new" element={<ModelCreate />} />
          <Route path=":id/designer" element={<ModelDesigner />} />
        </Route>
        <Route path="composer/*" element={<Composer />} />
        <Route path="sweeps" element={<Sweeps />} />
        <Route path="leaderboard" element={<Leaderboard />} />
        <Route path="signals/*" element={<Signals />} />
        <Route path="overlay" element={<Overlay />} />
        <Route path="health" element={<Health />} />
        <Route path="showcase" element={<ComponentShowcase />} />
      </Route>
    </Routes>
  )
}

export default App
