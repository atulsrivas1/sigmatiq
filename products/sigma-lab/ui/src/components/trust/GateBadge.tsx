import React from 'react'

export const GateBadge: React.FC<{ pass: boolean; reasons?: string[] }>= ({ pass, reasons = [] }) => {
  const cls = pass ? 'gate-badge pass' : 'gate-badge fail'
  const title = pass ? 'All Gates Passed' : 'Gate Failed'
  return (
    <span className={cls} tabIndex={0} aria-haspopup="true">
      {pass ? 'PASS' : 'FAIL'}
      <div className="gate-tooltip" role="tooltip">
        <div className="gate-tooltip-title">{title}</div>
        {reasons.length > 0 && (
          <ul className="gate-reasons">
            {reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        )}
      </div>
    </span>
  )
}

