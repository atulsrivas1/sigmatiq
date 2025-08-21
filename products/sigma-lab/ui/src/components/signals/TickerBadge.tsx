import React from 'react'

export const TickerBadge: React.FC<{ ticker: string }>= ({ ticker }) => {
  return <span className="badge badge-neutral" style={{ fontFamily: 'Monaco, monospace' }}>{ticker}</span>
}

