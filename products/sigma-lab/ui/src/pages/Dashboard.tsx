import React, { useEffect, useMemo, useState } from 'react'
import './Dashboard.css'
import { RecentModels } from '../components/dashboard/RecentModels'
import { LastRuns } from '../components/dashboard/LastRuns'
import { QuickActions } from '../components/dashboard/QuickActions'
import { SystemHealth } from '../components/dashboard/SystemHealth'
import { ControlsBar } from '../components/models/ControlsBar'
import { ModelsContainer } from '../components/models/ModelsContainer'
import { Pagination } from '../components/models/Pagination'
import { recentModels, runs, healthItems } from '../data/dashboard'
import { modelsData } from '../data/models'

interface ModelItem {
  id?: string
  model_id: string
  pack_id?: string
  updated_at?: string
}

interface LeaderboardRow {
  started_at?: string
  model_id: string
  pack_id: string
  sharpe?: number
  trades?: number
  win_rate?: number
  max_drawdown?: number
  cum_ret?: number
  gate?: { pass: boolean; reasons?: string[] }
  tag?: string
}

interface HealthResp {
  ok: boolean
  service: string
  version: string
  now: string
  deps?: Record<string, string>
}

type ViewMode = 'card' | 'row'

export const Dashboard: React.FC = () => {
  const [view, setView] = useState<ViewMode>('card')

  const packs = useMemo(() => Array.from(new Set(models.map(m => m.pack_id).filter(Boolean))) as string[], [models])

  // Synthesize a "models to display" list using leaderboard rows for metrics
  const modelRows = useMemo(() => {
    const list = runs.map(r => ({
      model_id: r.model_id,
      pack_id: r.pack_id,
      sharpe: r.sharpe ?? 0,
      win_rate: r.win_rate ?? 0,
      trades: r.trades ?? 0,
      cum_ret: r.cum_ret ?? 0,
      updated_at: r.started_at,
    }))
    return list
  }, [runs])

  const filtered = useMemo(() => {
    return modelRows.filter(r =>
      (!search || r.model_id.toLowerCase().includes(search.toLowerCase())) &&
      (!packFilter || r.pack_id === packFilter)
    )
  }, [modelRows, search, packFilter])

  const sorted = useMemo(() => {
    const arr = [...filtered]
    switch (sortBy) {
      case 'sharpe':
        arr.sort((a, b) => (b.sharpe || 0) - (a.sharpe || 0)); break
      case 'ret':
        arr.sort((a, b) => (b.cum_ret || 0) - (a.cum_ret || 0)); break
      case 'trades':
        arr.sort((a, b) => (b.trades || 0) - (a.trades || 0)); break
      default:
        arr.sort((a, b) => (b.updated_at || '').localeCompare(a.updated_at || ''))
    }
    return arr
  }, [filtered, sortBy])

  return (
    <div className="dashboard-page">
      <div className="container">
        {/* Dashboard Section */}
        <section className="section">
          <div className="section-header">
            <h2 className="section-title">Dashboard</h2>
          </div>
          
          <div className="dashboard-grid">
            <RecentModels items={recentModels} />
            <LastRuns runs={runs} />
            <QuickActions />
            <SystemHealth items={healthItems as any} />
          </div>
        </section>

        {/* Models Section */}
        <section className="section">
          <div className="section-header">
            <h2 className="section-title">Models</h2>
          </div>

          <ControlsBar view={view} setView={setView} />
          <ModelsContainer view={view} models={modelsData} />
          <Pagination total={modelsData.length} />
        </section>
      </div>
    </div>
  )
}
