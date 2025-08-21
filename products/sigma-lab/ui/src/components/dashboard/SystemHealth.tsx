import React from 'react'
import { DashboardCard } from './DashboardCard'
import { Link } from 'react-router-dom'

type Item = { label: string; value: string; className: 'ok' | 'warn' | 'error'; color: string; icon: 'shield' | 'rows' | 'globe' }

export const SystemHealth: React.FC<{ items: Item[] }>= ({ items }) => {
  return (
    <DashboardCard title="System Health">
      <div className="health-status">
        {items.map((it, idx) => (
          <div className="health-item" key={idx}>
            {it.icon === 'shield' && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={it.color} strokeWidth="2">
                <path d="M12 2L4 7v5c0 5.5 3.5 10.26 8 11 4.5-.74 8-5.5 8-11V7l-8-5z"/>
              </svg>
            )}
            {it.icon === 'rows' && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={it.color} strokeWidth="2">
                <path d="M3 12h18M3 6h18M3 18h18"/>
              </svg>
            )}
            {it.icon === 'globe' && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={it.color} strokeWidth="2">
                <path d="M12 2v20M2 12h20"/>
                <circle cx="12" cy="12" r="9"/>
              </svg>
            )}
            <span className="health-label">{it.label}</span>
            <span className={`health-value ${it.className}`}>{it.value}</span>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 12 }}>
        <Link to="/health" className="btn btn-small" style={{ width: '100%' }}>View Details →</Link>
      </div>
    </DashboardCard>
  )
}

