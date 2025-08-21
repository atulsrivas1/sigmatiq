import React from 'react'

export const DashboardCard: React.FC<{ title: string; children: React.ReactNode; }>= ({ title, children }) => {
  return (
    <div className="dashboard-card">
      <h3 className="dashboard-card-title">{title}</h3>
      {children}
    </div>
  )
}

