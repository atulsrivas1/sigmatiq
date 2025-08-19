import { useEffect, useState } from 'react'
import { api } from '../api/client'

type ModelRow = { id: string, config?: any }

export default function Models(){
  const [rows, setRows] = useState<ModelRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    let alive = true
    setLoading(true); setError(null)
    api.get<{ models: ModelRow[] }>(`/models`)
      .then(d => { if (!alive) return; setRows(d.models || []); setLoading(false) })
      .catch(e => { if (!alive) return; setError(String(e)); setLoading(false) })
    return () => { alive = false }
  }, [])
  return (
    <div>
      <h2 className="text-xl font-bold mb-3">Models</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      {!loading && !error && (
        <table className="w-full text-sm border border-border rounded">
          <thead className="bg-surface2">
            <tr>
              <th className="text-left p-2">ID</th>
              <th className="text-left p-2">Ticker</th>
              <th className="text-left p-2">Model</th>
            </tr>
          </thead>
          <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="border-t border-border">
              <td className="p-2">{r.id}</td>
              <td className="p-2">{r.config?.ticker || '-'}</td>
              <td className="p-2">{r.config?.model || '-'}</td>
            </tr>
          ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

