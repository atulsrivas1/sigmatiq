import React from 'react'
import { FreshIcon } from '../common/FreshIcon'

export type JobStatus = 'running' | 'completed' | 'failed' | 'queued'

export const JobStatusPill: React.FC<{ status: JobStatus }>= ({ status }) => {
  const cls =
    status === 'running' ? 'pill pill-info' :
    status === 'completed' ? 'pill pill-success' :
    status === 'failed' ? 'pill pill-error' : 'pill pill-warning'
  const icon =
    status === 'running' ? <FreshIcon name="spinner" size={14} /> :
    status === 'completed' ? <FreshIcon name="trendCheck" size={14} /> :
    status === 'failed' ? <FreshIcon name="alertCircle" size={14} /> : <FreshIcon name="clock" size={14} />
  const label = status.charAt(0).toUpperCase() + status.slice(1)
  return (
    <span className={cls}>
      {icon}
      {label}
    </span>
  )
}

