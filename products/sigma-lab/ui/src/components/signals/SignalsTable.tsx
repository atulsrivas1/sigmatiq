import React from 'react'

export type SignalsRow = {
  ts: string
  model: string
  ticker: string
  side?: string
  conf?: number
  pack?: string
}

export const SignalsTable: React.FC<{ rows: SignalsRow[] }>= ({ rows }) => {
  return (
    <table className="table signals-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Model</th>
          <th>Ticker</th>
          <th>Side</th>
          <th>Confidence</th>
          <th>Pack</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r, i) => (
          <tr key={i}>
            <td>{r.ts}</td>
            <td>{r.model}</td>
            <td>{r.ticker}</td>
            <td>{r.side || '—'}</td>
            <td>{typeof r.conf === 'number' ? r.conf.toFixed(2) : '—'}</td>
            <td>{r.pack || '—'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

