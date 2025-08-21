import React from 'react'

export const ConfidenceBadge: React.FC<{ value?: number }>= ({ value }) => {
  let cls = 'badge'
  if (typeof value === 'number') {
    if (value >= 0.7) cls += ' badge-success'
    else if (value >= 0.5) cls += ' badge-warning'
    else cls += ' badge-neutral'
  } else {
    cls += ' badge-neutral'
  }
  return <span className={cls}>{typeof value === 'number' ? value.toFixed(2) : '—'}</span>
}

