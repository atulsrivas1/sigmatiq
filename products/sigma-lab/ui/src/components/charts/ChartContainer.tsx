import React from 'react'

export const ChartContainer: React.FC<{ fullWidth?: boolean; children: React.ReactNode }>= ({ fullWidth, children }) => (
  <div className={`chart-container${fullWidth ? ' full-width' : ''}`}>{children}</div>
)

