import React from 'react'
import { DashboardCard } from './DashboardCard'

export const RecentModels: React.FC<{ items: { id: string; pack: string; color: string; updatedAt: string }[] }>= ({ items }) => {
  return (
    <DashboardCard title="Recent Models">
      <div className="recent-models-list">
        {items.map(m => (
          <div className="recent-model-item" key={m.id}>
            <div className="recent-model-info">
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ width: 4, height: 4, background: m.color, borderRadius: '50%' }} />
                <span className="recent-model-id">{m.id}</span>
              </div>
              <span className="recent-model-meta">{m.pack} • Updated {m.updatedAt}</span>
            </div>
            <button className="btn btn-small">Open</button>
          </div>
        ))}
      </div>
    </DashboardCard>
  )
}

