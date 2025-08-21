import React from 'react'

export const SidePill: React.FC<{ side?: 'Long'|'Short'|string }>= ({ side }) => {
  const s = (side || '').toLowerCase()
  const cls = 'pill ' + (s === 'long' ? 'pill-success' : s === 'short' ? 'pill-error' : 'pill-info')
  const label = side || '—'
  return <span className={cls}>{label}</span>
}

