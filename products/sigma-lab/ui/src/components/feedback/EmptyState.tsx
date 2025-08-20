import React from 'react'
import './EmptyState.css'

export interface EmptyStateProps {
  variant?: 'no-data' | 'no-results' | 'first-time' | 'error' | 'custom'
  icon?: React.ReactNode
  title: string
  message?: string
  action?: React.ReactNode
  className?: string
}

const defaultIcons = {
  'no-data': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <line x1="9" y1="9" x2="15" y2="9" />
      <line x1="9" y1="15" x2="15" y2="15" />
    </svg>
  ),
  'no-results': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="11" cy="11" r="8" />
      <path d="M21 21l-4.35-4.35" />
    </svg>
  ),
  'first-time': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
    </svg>
  ),
  'error': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  )
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  variant = 'no-data',
  icon,
  title,
  message,
  action,
  className = ''
}) => {
  const displayIcon = icon || (variant !== 'custom' ? defaultIcons[variant] : null)

  return (
    <div className={`empty-state empty-state-${variant} ${className}`}>
      {displayIcon && (
        <div className="empty-state-icon" aria-hidden="true">
          {displayIcon}
        </div>
      )}
      <div className="empty-state-title">{title}</div>
      {message && <div className="empty-state-message">{message}</div>}
      {action && <div className="empty-state-action">{action}</div>}
    </div>
  )
}