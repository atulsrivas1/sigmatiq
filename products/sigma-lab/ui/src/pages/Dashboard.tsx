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
  // Dev-only mock overlay toggles for aligning with design mocks
  const [overlayRecent, setOverlayRecent] = useState(false)
  const [overlayRuns, setOverlayRuns] = useState(false)
  const enableOverlay = (import.meta as any)?.env?.VITE_DEBUG_OVERLAY === '1'
  const mockUrl = (import.meta as any)?.env?.VITE_DEBUG_CARD_MOCK_URL || '/debug/dashboard_cards.png'

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
        {/* Dashboard Section */}
        <section className="section">
          <div className="section-header">
            <h2 className="section-title">Dashboard</h2>
          </div>
          
          <div className="dashboard-grid">
          {/* Recent Models */}
          <div className="dashboard-card dashboard-card--recent">
            <div className="dashboard-card-header">
              <h3 className="dashboard-card-title">Recent Models</h3>
              {enableOverlay && (
                <button className="dev-overlay-toggle" onClick={() => setOverlayRecent(v => !v)} aria-pressed={overlayRecent}>
                  {overlayRecent ? 'Hide Mock' : 'Show Mock'}
                </button>
              )}
            </div>
            {enableOverlay && overlayRecent && (
              <div className="dev-mock-overlay" aria-hidden style={{ backgroundImage: `url(${mockUrl})` }} />
            )}
            <div className="recent-models-list">
              {loading && <div className="text-muted">Loading…</div>}
              {!loading && models.slice(0,3).map((m) => {
                const packColors: Record<string, string> = {
                  'zerosigma': 'var(--sigmatiq-bright-teal)',
                  'swingsigma': 'var(--sigmatiq-golden)',
                  'weeklysigma': 'var(--sigmatiq-teal-dark)',
                };
                const dotColor = packColors[m.pack_id?.toLowerCase() || ''] || 'var(--sigmatiq-bright-teal)';
                return (
                  <div className="recent-model-item" key={m.model_id}>
                    <div className="recent-model-info">
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div style={{ width: 4, height: 4, background: dotColor, borderRadius: '50%' }} />
                        <span className="recent-model-id">{m.model_id}</span>
                      </div>
                      <span className="recent-model-meta">{m.pack_id || '—'} • Updated {m.updated_at ? '2h ago' : 'recently'}</span>
                    </div>
                    <button className="btn btn-small">Open</button>
                  </div>
                );
              })}
              {!loading && models.length === 0 && (
                <div className="text-muted">No recent models.</div>
              )}
            </div>
          </div>

          {/* Last Runs */}
          <div className="dashboard-card dashboard-card--runs">
            <div className="dashboard-card-header">
              <div className="dashboard-card-title">Last Runs</div>
              {enableOverlay && (
                <button className="dev-overlay-toggle" onClick={() => setOverlayRuns(v => !v)} aria-pressed={overlayRuns}>
                  {overlayRuns ? 'Hide Mock' : 'Show Mock'}
                </button>
              )}
            </div>
            {enableOverlay && overlayRuns && (
              <div className="dev-mock-overlay" aria-hidden style={{ backgroundImage: `url(${mockUrl})` }} />
            )}
            <div className="recent-models-list">
              {loading && <div className="text-muted">Loading…</div>}
              {!loading && runs.slice(0,5).map((r, idx) => (
                <div className="recent-model-item" key={`${r.model_id}-${idx}`}>
                  <div className="recent-model-info">
                    <div className="recent-model-id">{r.model_id}</div>
                    <div className="recent-model-meta">{(r.started_at || '—').slice(0, 16)} • Sharpe {r.sharpe?.toFixed(2) ?? '—'} • Trades {r.trades ?? '—'}</div>
                  </div>
                  <Link to={`/leaderboard`} className="btn btn-ghost btn-sm">View</Link>
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
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                Create Model
              </Link>
              <Link to="/composer/backtest" className="quick-action-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 3l14 9-14 9V3z"/>
                </svg>
                Run Backtest
              </Link>
              <Link to="/sweeps" className="quick-action-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 12H7M10 12H14M17 12H21"/>
                  <circle cx="5" cy="12" r="2"/>
                  <circle cx="12" cy="12" r="2"/>
                  <circle cx="19" cy="12" r="2"/>
                </svg>
                Open Sweeps
              </Link>
              <Link to="/showcase" className="quick-action-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
                View Docs
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
              <Link to="/health" className="btn btn-small" style={{ width: '100%' }}>View Details →</Link>
            </div>
          </div>
        </div>
        </section>

        {/* Models Section */}
        <section className="section">
          <div className="section-header">
            <h2 className="section-title">Models</h2>
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
                    <defs>
                      <linearGradient id={`gradient-${idx}`} x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style={{stopColor: r.pack_id === 'swingsigma' ? 'var(--sigmatiq-golden)' : 'var(--sigmatiq-bright-teal)', stopOpacity: 0.3}} />
                        <stop offset="100%" style={{stopColor: r.pack_id === 'swingsigma' ? 'var(--sigmatiq-golden)' : 'var(--sigmatiq-bright-teal)', stopOpacity: 0}} />
                      </linearGradient>
                    </defs>
                    <path d="M 0 30 Q 40 25 80 20 T 160 10 L 200 8" stroke={r.pack_id === 'swingsigma' ? 'var(--sigmatiq-golden)' : 'var(--sigmatiq-bright-teal)'} strokeWidth="1.5" fill="none"/>
                    <path d="M 0 30 Q 40 25 80 20 T 160 10 L 200 8 L 200 40 L 0 40 Z" fill={`url(#gradient-${idx})`}/>
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
        </section>
      </div>
    </div>
  )
}
