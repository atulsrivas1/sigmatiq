import { useEffect, useState } from 'react'
import SignalCard from '../components/SignalCard'
import { api } from '../api/client'

type SignalRow = {
  date?: string; model_id?: string; ticker?: string; side?: string;
  entry_ref_px?: number; stop_px?: number; target_px?: number; rank?: number;
  score_total?: number;
}

export default function Dashboard(){
  const [rows, setRows] = useState<SignalRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    let alive = true
    setLoading(true); setError(null)
    api.get<{ rows: SignalRow[] }>(`/signals?limit=8&offset=0`)
      .then(d => { if (!alive) return; setRows(d.rows || []); setLoading(false) })
      .catch(e => { if (!alive) return; setError(String(e)); setLoading(false) })
    return () => { alive = false }
  }, [])

  return (
    <>
      <header className="hero">
        <div className="inner">
          <div>
            <div className="small">Sigmatiq Edge — Dashboard</div>
            <h1 className="font-display m-0">Alerts & Signal Cards</h1>
          </div>
        </div>
      </header>

      <main className="container mt-4">
        <section className="grid">
          <div className="col-8">
            <div className="panel">
              <div className="row" style={{ justifyContent:'space-between' }}>
                <div className="small">Live Signal Feed</div>
              </div>
              <div className="feed" aria-live="polite" aria-relevant="additions">
                {loading && <div>Loading...</div>}
                {error && <div className="text-red-500">{error}</div>}
                {!loading && !error && rows.map((r,i) => (
                  <SignalCard key={i}
                    ticker={r.ticker || '-'}
                    modelId={r.model_id}
                    date={r.date}
                    side={r.side}
                    rank={r.rank}
                    entry={r.entry_ref_px}
                    stop={r.stop_px}
                    target={r.target_px}
                    confidence={typeof r.score_total==='number'? Math.max(0, Math.min(1, r.score_total)): undefined}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="col-4">
            <div className="panel">
              <div className="small">System Alerts</div>
              <div className="alert signal" role="status" style={{ marginTop: '8px' }}>
                <div className="icon">&#9889;</div>
                <div>
                  <div className="title">New signals available</div>
                  <div className="meta">Latest feed updated</div>
                </div>
                <div className="actions">
                  <button className="btn btn-outline" onClick={()=>window.location.reload()}>Refresh</button>
                </div>
              </div>
            </div>

            <div className="panel" style={{ marginTop: '16px' }}>
              <div className="small">KPIs</div>
              <div className="kpi" style={{ marginTop: '10px' }}>
                <div className="label">Signals (page)</div>
                <div className="value">{rows.length}</div>
              </div>
              <div className="kpi">
                <div className="label">Theme</div>
                <div className="value">{document.documentElement.getAttribute('data-theme')}</div>
              </div>
              <div className="kpi">
                <div className="label">Pack</div>
                <div className="value">{document.documentElement.getAttribute('data-edge')}</div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}

