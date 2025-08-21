import React from 'react'
import { FreshDashboardCard } from './DashboardCard'

type Run = { name: string; sub: string; type: 'success' | 'running' | 'failed' }

export const FreshLastRuns: React.FC<{ runs: Run[] }>= ({ runs }) => {
  return (
    <FreshDashboardCard title="Last Runs">
      <div className="recent-models-list">
        {runs.map((r, idx) => (
          <div className="recent-model-item" key={idx}>
            <div className="recent-model-info">
              <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                {r.type==='success' && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--status-success)" strokeWidth="2">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                )}
                {r.type==='running' && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--status-warning)" strokeWidth="2" className="animate-spin">
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                  </svg>
                )}
                {r.type==='failed' && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--status-error)" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                )}
                <span className="recent-model-id">{r.name}</span>
              </div>
              <span className="recent-model-meta">{r.sub}</span>
            </div>
            {r.type==='success' && <span className="badge badge-teal">Success</span>}
            {r.type==='running' && <span className="badge badge-golden">Running</span>}
            {r.type==='failed' && <span className="badge" style={{background:'rgba(255,87,87,0.2)', color:'var(--status-error)'}}>Failed</span>}
          </div>
        ))}
      </div>
    </FreshDashboardCard>
  )
}

