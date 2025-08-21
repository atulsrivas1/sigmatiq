import React, { useEffect, useMemo, useState } from 'react'
import './Dashboard.css'
import { RecentModels } from '../components/dashboard/RecentModels'
import { LastRuns } from '../components/dashboard/LastRuns'
import { QuickActions } from '../components/dashboard/QuickActions'
import { SystemHealth } from '../components/dashboard/SystemHealth'
import { ControlsBar } from '../components/models/ControlsBar'
import { ModelsContainer } from '../components/models/ModelsContainer'
import { Pagination } from '../components/models/Pagination'
import { apiService } from '../services/api'
import type { ModelCardModel } from '../components/models/ModelCard'

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
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // API-backed state
  const [recentItems, setRecentItems] = useState<{ id: string; pack: string; color: string; updatedAt: string }[]>([])
  const [lastRuns, setLastRuns] = useState<{ name: string; sub: string; type: 'success'|'running'|'failed' }[]>([])
  const [healthItems, setHealthItems] = useState<{ label: string; value: string; className: 'ok'|'warn'|'error'; color: string; icon: 'shield'|'rows'|'globe' }[]>([])
  const [modelsData, setModelsData] = useState<ModelCardModel[]>([])

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        setLoading(true)
        setError(null)
        const [modelsRes, lbRes, healthRes] = await Promise.all([
          apiService.getModels(),
          apiService.getLeaderboard({ limit: 10 }),
          apiService.getHealth(),
        ])
        if (!mounted) return

        const models = (modelsRes.data.models || []).map((m: any) => ({
          id: m.id || m.config?.model_id,
          pack: m.config?.pack || m.pack || 'zerosigma',
        }))

        // Recent models list (take first 3)
        const packColors: Record<string, string> = {
          zerosigma: 'var(--sigmatiq-bright-teal)',
          swingsigma: 'var(--sigmatiq-golden)',
          weeklysigma: 'var(--sigmatiq-teal-dark)',
        }
        const recent = models.slice(0, 3).map((m: any) => ({
          id: m.id,
          pack: m.pack,
          color: packColors[(m.pack || '').toLowerCase()] || 'var(--sigmatiq-bright-teal)',
          updatedAt: 'recently',
        }))
        setRecentItems(recent)

        // Last runs from leaderboard
        const rows = lbRes.data.rows || []
        const runsMapped = rows.slice(0, 5).map((r: any) => ({
          name: r.model_id,
          sub: `${r.model_id} • ${r.started_at || ''}`,
          type: r.gate?.pass ? 'success' : 'failed',
        }))
        setLastRuns(runsMapped)

        // Health
        const h = healthRes.data || {}
        const healthList = [
          { label: 'API', value: h.ok ? 'OPERATIONAL' : 'ERROR', className: (h.ok ? 'ok' : 'error') as any, color: 'var(--status-success)', icon: 'shield' as const },
          { label: 'Database', value: (h.deps?.db || 'UNKNOWN').toString().toUpperCase(), className: (h.deps?.db === 'ok' || h.deps?.db === 'mock') ? 'ok' : 'warn', color: 'var(--status-warning)', icon: 'rows' as const },
          { label: 'Service', value: (h.service || 'UNKNOWN').toString().toUpperCase(), className: 'ok' as const, color: 'var(--status-success)', icon: 'globe' as const },
        ]
        setHealthItems(healthList)

        // Model cards from leaderboard (fallback to models when needed)
        const cards: ModelCardModel[] = rows.slice(0, 6).map((r: any, i: number) => ({
          id: r.model_id,
          title: r.model_id,
          subtitle: `${r.pack_id || 'pack'} • ${r.started_at || ''}`,
          iconName: 'barChart',
          iconBg: (r.pack_id === 'swingsigma') ? 'var(--sigmatiq-golden)' : 'var(--sigmatiq-bright-teal)',
          badge: r.gate?.pass ? 'Active' : 'Watch',
          badgeClass: r.gate?.pass ? 'success' : 'warning',
          stats: [
            { label: 'Sharpe', value: (typeof r.sharpe === 'number' ? r.sharpe.toFixed(2) : '—'), trend: (r.sharpe || 0) > 1 ? 'positive' : undefined },
            { label: 'Win Rate', value: (typeof r.win_rate === 'number' ? Math.round(r.win_rate * 100) + '%' : '—') },
            { label: 'Trades', value: (r.trades ?? '—').toString() },
            { label: 'Return', value: (typeof r.cum_ret === 'number' ? (r.cum_ret * 100).toFixed(1) + '%' : '—'), trend: (r.cum_ret || 0) > 0 ? 'positive' : (r.cum_ret || 0) < 0 ? 'negative' : undefined },
          ],
          chart: i % 2 === 0 ? 'g1' : 'g2',
          updated: r.started_at ? 'recently' : '—',
          risk: 'Balanced',
          actions: ['Open', 'Backtest'],
        }))
        // Fallback if leaderboard empty: show basic cards from models
        const fallback = models.slice(0, 3).map((m: any) => ({
          id: m.id,
          title: m.id,
          subtitle: `${m.pack} • recently`,
          iconName: 'barChart' as const,
          iconBg: 'var(--sigmatiq-bright-teal)',
          badge: 'Watch',
          badgeClass: 'warning' as const,
          stats: [
            { label: 'Sharpe', value: '—' },
            { label: 'Win Rate', value: '—' },
            { label: 'Trades', value: '—' },
            { label: 'Return', value: '—' },
          ],
          chart: 'line-teal' as const,
          updated: 'recently',
          risk: 'Balanced',
          actions: ['Open', 'Backtest'],
        }))
        setModelsData(cards.length ? cards : fallback)
      } catch (e: any) {
        if (!mounted) return
        setError(e?.message || 'Failed to load dashboard data')
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => { mounted = false }
  }, [])

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
            <RecentModels items={recentItems} />
            <LastRuns runs={lastRuns} />
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
