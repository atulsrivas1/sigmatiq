import React from 'react'

export const KPIStat: React.FC<{ label: string; value: React.ReactNode; trend?: 'positive'|'negative' }>= ({ label, value, trend }) => {
  const valueClass = trend === 'positive' ? 'stat-value positive' : trend === 'negative' ? 'stat-value negative' : 'stat-value'
  return (
    <div className="stat-item">
      <span className="stat-label">{label}</span>
      <span className={valueClass}>{value}</span>
    </div>
  )
}

