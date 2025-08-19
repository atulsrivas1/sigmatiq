import { useEffect, useState } from 'react'
import SignalCard from '../components/SignalCard'
import { api } from '../api/client'

type SignalRow = {
  date?: string
  model_id?: string
  ticker?: string
  side?: string
  entry_mode?: string
  entry_ref_px?: number
  stop_px?: number
  target_px?: number
  rank?: number
}

export default function Signals(){
  const [rows, setRows] = useState<SignalRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    let alive = true
    setLoading(true); setError(null)
    api.get<{ rows: SignalRow[] }>(`/signals?limit=50&offset=0`)
      .then(d => { if (!alive) return; setRows(d.rows || []); setLoading(false) })
      .catch(e => { if (!alive) return; setError(String(e)); setLoading(false) })
    return () => { alive = false }
  }, [])
  return (
    <div>
      <h2 className="text-xl font-bold mb-3">Signals</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {rows.map((r, i) => (
            <SignalCard key={i}
              ticker={r.ticker || '-'}
              modelId={r.model_id}
              date={r.date}
              side={r.side}
              rank={r.rank}
              entry={r.entry_ref_px}
              stop={r.stop_px}
              target={r.target_px}
            />
          ))}
        </div>
      )}
    </div>
  )
}

