import React from 'react'

type Status = 'ok' | 'warn' | 'error'

export const HealthTile: React.FC<{ icon?: React.ReactNode; label: string; value: string; status?: Status }>= ({ icon, label, value, status='ok' }) => {
  return (
    <div className="health-tile">
      {icon}
      <span className="tile-label">{label}</span>
      <span className={`tile-value ${status}`}>{value}</span>
    </div>
  )
}

export const HealthTiles: React.FC<{ children: React.ReactNode }>= ({ children }) => (
  <div className="health-tiles">{children}</div>
)

