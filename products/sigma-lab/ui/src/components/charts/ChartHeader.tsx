import React from 'react'

export const ChartHeader: React.FC<{ title: string; right?: React.ReactNode }>= ({ title, right }) => (
  <div className="chart-header">
    <div className="chart-title">{title}</div>
    <div className="chart-controls">{right}</div>
  </div>
)

