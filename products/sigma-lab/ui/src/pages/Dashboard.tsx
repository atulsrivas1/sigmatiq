import React, { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { Card, CardActions, CardBadge, CardChart, CardContent, CardHeader, CardHeaderInfo, CardIcon, CardMeta, CardStats, StatItem } from '../components/ui/Card'
import { Icon } from '../components/Icon'
import './Dashboard.css'

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
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [models, setModels] = useState<ModelItem[]>([])
  const [runs, setRuns] = useState<LeaderboardRow[]>([])
  const [health, setHealth] = useState<HealthResp | null>(null)

  // Filters for the models area
  const [view, setView] = useState<ViewMode>('card')
  const [search, setSearch] = useState('')
  const [packFilter, setPackFilter] = useState('')
  const [sortBy, setSortBy] = useState<'updated' | 'sharpe' | 'ret' | 'trades'>('updated')

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        setLoading(true)
        setError(null)
        const [mRes, lbRes, hRes] = await Promise.all([
          apiService.getModels(),
          apiService.getLeaderboard({ limit: 10 }),
          apiService.getHealth(),
        ])
        if (!mounted) return
        setModels((mRes.data.models || []).map((m: any) => ({
          id: m.id || m.config?.model_id,
          model_id: m.config?.model_id || m.id,
          pack_id: m.config?.pack,
          updated_at: m.updated_at,
        })))
        setRuns(lbRes.data.rows || [])
        setHealth(hRes.data)
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
        {/* Top Grid: Recent Models, Last Runs, Quick Actions, Health */}
        <div className="dashboard-grid">
          {/* Recent Models */}
          <div className="dashboard-card">
            <div className="dashboard-card-title">Recent Models</div>
            <div className="recent-models-list">
              {loading && <div className="text-muted">Loading…</div>}
              {!loading && models.slice(0,5).map((m) => (
                <div className="recent-model-item" key={m.model_id}>
                  <div className="recent-model-info">
                    <div className="recent-model-id">{m.model_id}</div>
                    <div className="recent-model-meta">{m.pack_id || '—'} • {m.updated_at || 'recently'}</div>
                  </div>
                  <Link to={`/models/${m.model_id}/designer`} className="btn btn-secondary btn-sm">Open</Link>
                </div>
              ))}
              {!loading && models.length === 0 && (
                <div className="text-muted">No recent models.</div>
              )}
            </div>
          </div>

          {/* Last Runs */}
          <div className="dashboard-card">
            <div className="dashboard-card-title">Last Runs</div>
            <div className="recent-models-list">
              {loading && <div className="text-muted">Loading…</div>}
              {!loading && runs.slice(0,5).map((r, idx) => (
                <div className="recent-model-item" key={`${r.model_id}-${idx}`}>
                  <div className="recent-model-info">
                    <div className="recent-model-id">{r.model_id}</div>
                    <div className="recent-model-meta">{r.started_at || '—'} • Sharpe {r.sharpe?.toFixed(2) ?? '—'} • Trades {r.trades ?? '—'}</div>
                  </div>
                  <Link to={`/leaderboard`} className="btn btn-secondary btn-sm">View</Link>
                </div>
              ))}
              {!loading && runs.length === 0 && (
                <div className="text-muted">No runs yet.</div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="dashboard-card">
            <div className="dashboard-card-title">Quick Actions</div>
            <div className="quick-actions">
              <Link to="/models/new" className="quick-action-btn primary">
                <Icon name="plus" size={16} />
                <span>Create Model</span>
              </Link>
              <Link to="/composer/backtest" className="quick-action-btn">
                <Icon name="backtest" size={16} />
                <span>Run Backtest</span>
              </Link>
              <Link to="/sweeps" className="quick-action-btn">
                <Icon name="sweeps" size={16} />
                <span>Open Sweeps</span>
              </Link>
              <Link to="/leaderboard" className="quick-action-btn">
                <Icon name="leaderboard" size={16} />
                <span>Open Leaderboard</span>
              </Link>
            </div>
          </div>

          {/* Health */}
          <div className="dashboard-card">
            <div className="dashboard-card-title">Health</div>
            <div className="health-status">
              <div className="health-item">
                <div className="health-label">API</div>
                <div className={`health-value ${health?.ok ? 'ok' : 'error'}`}>{health?.ok ? 'ok' : 'error'}</div>
              </div>
              <div className="health-item">
                <div className="health-label">DB</div>
                <div className={`health-value ${(health?.deps?.db === 'mock' || health?.deps?.db === 'ok') ? 'ok' : 'warn'}`}>{health?.deps?.db || 'n/a'}</div>
              </div>
              <div className="health-item">
                <div className="health-label">Service</div>
                <div className={`health-value ok`}>{health?.service || '—'}</div>
              </div>
            </div>
            <div style={{ marginTop: 12 }}>
              <Link to="/health" className="btn btn-secondary btn-sm">View details</Link>
            </div>
          </div>
        </div>

        {/* Controls bar */}
        <div className="controls-bar">
          <div className="search-box">
            <input className="search-input" placeholder="Search model_id…" value={search} onChange={e => setSearch(e.target.value)} />
            <span className="search-icon">🔎</span>
          </div>
          <div className="filter-group">
            <select className="filter-select" value={packFilter} onChange={e => setPackFilter(e.target.value)}>
              <option value="">All Packs</option>
              {packs.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
            <select className="filter-select" value={sortBy} onChange={e => setSortBy(e.target.value as any)}>
              <option value="updated">Sort: Updated</option>
              <option value="sharpe">Sort: Sharpe</option>
              <option value="ret">Sort: Return</option>
              <option value="trades">Sort: Trades</option>
            </select>
          </div>
          <div className="view-toggle">
            <button className={`view-option ${view === 'card' ? 'active' : ''}`} onClick={() => setView('card')}>▦ Cards</button>
            <button className={`view-option ${view === 'row' ? 'active' : ''}`} onClick={() => setView('row')}>☰ Rows</button>
          </div>
        </div>

        {/* Models cards/rows */}
        <div className={`cards-container ${view === 'card' ? 'card-view' : 'row-view'}`}>
          {error && <div className="text-error" role="alert">{error}</div>}
          {loading && <div className="text-muted">Loading models…</div>}
          {!loading && sorted.length === 0 && <div className="text-muted">No models match your filters.</div>}
          {!loading && sorted.map((r, idx) => (
            <Card key={`${r.model_id}-${r.pack_id}`} className="model-card">
              <CardHeader>
                <CardIcon color={r.pack_id === 'swingsigma' ? 'var(--sigmatiq-golden)' : 'var(--sigmatiq-bright-teal)'}>
                  {r.pack_id === 'swingsigma' ? (
                    <Icon name="checkPath" size={16} color="var(--color-bg)" />
                  ) : (
                    <Icon name="trendUp" size={16} color="var(--color-bg)" />
                  )}
                </CardIcon>
                <CardHeaderInfo title={r.model_id} subtitle={`${r.pack_id} • ${r.updated_at || 'recently'}`} />
                <CardBadge variant={r.pack_id === 'swingsigma' ? 'warning' : (r.sharpe || 0) > 1 ? 'success' : 'warning'}>
                  {r.pack_id === 'swingsigma' ? 'TRAINING' : (r.sharpe || 0) > 1 ? 'ACTIVE' : 'WATCH'}
                </CardBadge>
              </CardHeader>
              <CardContent>
                <CardStats columns={2}>
                  <StatItem label="Sharpe" value={typeof r.sharpe === 'number' ? r.sharpe.toFixed(2) : '—'} />
                  <StatItem label="Return" value={typeof r.cum_ret === 'number' ? `${(r.cum_ret * 100).toFixed(1)}%` : '—'} variant={(r.cum_ret || 0) > 0 ? 'positive' : (r.cum_ret || 0) < 0 ? 'negative' : 'default'} />
                  <StatItem label="Win Rate" value={`${Math.round((r.win_rate || 0) * 100)}%`} />
                  <StatItem label="Trades" value={r.trades ?? '—'} />
                </CardStats>
                <CardChart>
                  <svg className="mini-chart" viewBox="0 0 200 40">
                    <path d="M 0 30 Q 40 25 80 20 T 160 10 L 200 8" stroke="var(--sigmatiq-bright-teal)" strokeWidth="1.5" fill="none"/>
                  </svg>
                </CardChart>
                <CardMeta>
                  <span>Updated {r.updated_at ? '' : 'recently'}</span>
                  <span>Risk: Balanced</span>
                </CardMeta>
              </CardContent>
              <CardActions>
                <Link to={`/models/${r.model_id}/designer`} className="card-btn primary">Open</Link>
                <Link to={`/sweeps?model=${r.model_id}`} className="card-btn">Sweeps</Link>
                <Link to={`/composer/train?model=${r.model_id}`} className="card-btn">Train</Link>
              </CardActions>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
