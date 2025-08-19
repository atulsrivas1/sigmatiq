export default function SignalCard({ ticker, modelId, date, side, rank, entry, stop, target, confidence }: any){
  const cls = side === 'buy' ? 'positive' : side === 'sell' ? 'negative' : ''
  const confPct = typeof confidence === 'number' ? Math.round(confidence * 100) : undefined
  return (
    <article className={`signal-card ${cls}`}>
      <div>
        <div className="header">
          <div className="ticker">{ticker}</div>
          <div className="model">{modelId}</div>
          <div className="time">{date}</div>
        </div>
        <div className="body">
          <div>
            <div className="tags">
              {typeof rank==='number' && <span className="tag">Rank #{rank}</span>}
              {side && <span className="tag">{side.toUpperCase()}</span>}
              {entry && <span className="tag">Entry {fmt(entry)}</span>}
              {stop && <span className="tag">Stop {fmt(stop)}</span>}
              {target && <span className="tag">Target {fmt(target)}</span>}
            </div>
          </div>
          <div>
            <div className="confidence" aria-valuenow={confPct} aria-valuemin={0} aria-valuemax={100}>
              <span style={{ width: `${confPct ?? 0}%` }} />
            </div>
          </div>
        </div>
      </div>
      <div className="actions">
        <button className="btn btn-outline">Details</button>
        <button className="btn btn-primary">Simulate</button>
      </div>
    </article>
  )
}

function fmt(x?: number){ return typeof x==='number' ? x.toFixed(2) : '-' }

