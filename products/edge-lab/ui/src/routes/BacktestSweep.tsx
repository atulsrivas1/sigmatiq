import { useState } from 'react'
import { api } from '../api/client'

export default function BacktestSweep(){
  const [modelId, setModelId] = useState('spy_opt_0dte_hourly')
  const [packId, setPackId] = useState('zeroedge')
  const [start, setStart] = useState('2024-06-01')
  const [end, setEnd] = useState('2024-06-30')
  const [thresholds, setThresholds] = useState('0.50,0.52,0.54;0.55,0.60,0.65')
  const [hours, setHours] = useState('13,14,15;13,14')
  const [topPcts, setTopPcts] = useState('0.10;0.15')
  const [splits, setSplits] = useState(5)
  const [embargo, setEmbargo] = useState(0)
  const [tag, setTag] = useState('sweep')
  const [busy, setBusy] = useState(false)
  const [res, setRes] = useState<any>(null)

  const runSweep = async (preset?: boolean) => {
    setBusy(true); setRes(null)
    try {
      const payload = {
        model_id: modelId,
        pack_id: packId,
        start, end,
        thresholds_variants: (preset? ['0.50,0.52,0.54','0.55,0.60,0.65'] : thresholds.split(';').filter(Boolean)),
        allowed_hours_variants: (preset? ['13,14,15','13,14'] : hours.split(';').filter(Boolean)),
        top_pct_variants: (preset? [0.10, 0.15] : topPcts.split(';').map(s=>parseFloat(s)).filter(v=>!isNaN(v))),
        splits, embargo, tag,
      }
      const r = await api.post('/backtest_sweep', payload)
      setRes(r)
    } catch (e:any) {
      setRes({ ok:false, error: String(e) })
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-3">Backtest Sweep</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <label className="block">Model ID
          <input className="input w-full" value={modelId} onChange={e=>setModelId(e.target.value)} />
        </label>
        <label className="block">Pack ID
          <input className="input w-full" value={packId} onChange={e=>setPackId(e.target.value)} />
        </label>
        <label className="block">Start
          <input className="input w-full" value={start} onChange={e=>setStart(e.target.value)} />
        </label>
        <label className="block">End
          <input className="input w-full" value={end} onChange={e=>setEnd(e.target.value)} />
        </label>
        <label className="block">Thresholds variants (semicolon-separated)
          <input className="input w-full" value={thresholds} onChange={e=>setThresholds(e.target.value)} />
        </label>
        <label className="block">Allowed hours variants (semicolon-separated)
          <input className="input w-full" value={hours} onChange={e=>setHours(e.target.value)} />
        </label>
        <label className="block">Top-% variants (semicolon-separated)
          <input className="input w-full" value={topPcts} onChange={e=>setTopPcts(e.target.value)} />
        </label>
        <label className="block">Splits
          <input className="input w-full" type="number" value={splits} onChange={e=>setSplits(parseInt(e.target.value||'5'))} />
        </label>
        <label className="block">Embargo
          <input className="input w-full" type="number" value={embargo} onChange={e=>setEmbargo(parseFloat(e.target.value||'0'))} />
        </label>
        <label className="block">Tag
          <input className="input w-full" value={tag} onChange={e=>setTag(e.target.value)} />
        </label>
      </div>
      <div className="mt-4 flex gap-2">
        <button className="btn btn-primary" onClick={()=>runSweep(false)} disabled={busy}>Run Sweep</button>
        <button className="btn btn-outline" onClick={()=>runSweep(true)} disabled={busy}>Run Preset</button>
      </div>
      {busy && <div className="mt-3">Running…</div>}
      {res && (
        <div className="mt-4">
          {res.error && <div className="text-red-500">{res.error}</div>}
          {res.ok && (
            <div>
              <div className="small">Top Results</div>
              <table className="w-full text-sm border border-border rounded mt-2">
                <thead className="bg-surface2">
                  <tr>
                    <th className="text-left p-2">Kind</th>
                    <th className="text-left p-2">Thresholds</th>
                    <th className="text-left p-2">Top-%</th>
                    <th className="text-left p-2">Hours</th>
                    <th className="text-left p-2">Best Sharpe</th>
                    <th className="text-left p-2">Best Cum</th>
                  </tr>
                </thead>
                <tbody>
                {(res.runs||[]).map((row:any, i:number)=> (
                  <tr key={i} className="border-t border-border">
                    <td className="p-2">{row.kind}</td>
                    <td className="p-2">{row.thresholds||'-'}</td>
                    <td className="p-2">{row.top_pct??'-'}</td>
                    <td className="p-2">{row.allowed_hours||'-'}</td>
                    <td className="p-2">{row.result?.best_sharpe_hourly??'-'}</td>
                    <td className="p-2">{row.result?.best_cum_ret??'-'}</td>
                  </tr>
                ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

