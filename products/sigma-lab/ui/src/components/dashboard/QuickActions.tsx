import React from 'react'
import { Link } from 'react-router-dom'
import { DashboardCard } from './DashboardCard'

export const QuickActions: React.FC = () => {
  const actions = [
    { label: 'Create Model', primary: true, icon: 'plus', to: '/models/new' },
    { label: 'Run Backtest', primary: false, icon: 'play', to: '/composer/backtest' },
    { label: 'Open Sweeps', primary: false, icon: 'nodes', to: '/sweeps' },
    { label: 'View Docs', primary: false, icon: 'file', to: '/showcase' },
  ] as const

  return (
    <DashboardCard title="Quick Actions">
      <div className="quick-actions">
        {actions.map((a, i) => (
          <Link className={`quick-action-btn ${a.primary ? 'primary' : ''}`} key={i} to={a.to}>
            {a.icon === 'plus' && (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            )}
            {a.icon === 'play' && (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 3l14 9-14 9V3z"/>
              </svg>
            )}
            {a.icon === 'nodes' && (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 12H7M10 12H14M17 12H21"/>
                <circle cx="5" cy="12" r="2"/>
                <circle cx="12" cy="12" r="2"/>
                <circle cx="19" cy="12" r="2"/>
              </svg>
            )}
            {a.icon === 'file' && (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
            )}
            {a.label}
          </Link>
        ))}
      </div>
    </DashboardCard>
  )
}

