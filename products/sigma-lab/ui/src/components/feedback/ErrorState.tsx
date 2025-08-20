import React from 'react'
import './ErrorState.css'

export interface ErrorStateProps {
  variant?: 'connection' | 'validation' | 'server' | 'custom'
  title: string
  message?: string
  details?: string | string[]
  actions?: React.ReactNode
  className?: string
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  variant = 'server',
  title,
  message,
  details,
  actions,
  className = ''
}) => {
  const renderDetails = () => {
    if (!details) return null
    
    if (Array.isArray(details)) {
      return (
        <ul className="error-state-details-list">
          {details.map((detail, index) => (
            <li key={index}>{detail}</li>
          ))}
        </ul>
      )
    }
    
    return <div className="error-state-details-text">{details}</div>
  }

  return (
    <div className={`error-state error-state-${variant} ${className}`} role="alert">
      <div className="error-state-title">{title}</div>
      {message && <div className="error-state-message">{message}</div>}
      {details && (
        <div className="error-state-details">
          {renderDetails()}
        </div>
      )}
      {actions && <div className="error-state-actions">{actions}</div>}
    </div>
  )
}

// Error Banner Component
export interface ErrorBannerProps {
  variant?: 'critical' | 'warning' | 'info'
  message: string
  dismissible?: boolean
  onDismiss?: () => void
  className?: string
}

export const ErrorBanner: React.FC<ErrorBannerProps> = ({
  variant = 'critical',
  message,
  dismissible = true,
  onDismiss,
  className = ''
}) => {
  const icons = {
    critical: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
    ),
    warning: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
      </svg>
    ),
    info: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="16" x2="12" y2="12"/>
        <line x1="12" y1="8" x2="12.01" y2="8"/>
      </svg>
    )
  }

  return (
    <div 
      className={`error-banner error-banner-${variant} ${className}`}
      role={variant === 'critical' ? 'alert' : 'status'}
      aria-live={variant === 'warning' ? 'polite' : undefined}
    >
      <div className="error-banner-content">
        <span className="error-banner-icon" aria-hidden="true">
          {icons[variant]}
        </span>
        <span className="error-banner-message">{message}</span>
      </div>
      {dismissible && (
        <button 
          className="error-banner-close"
          onClick={onDismiss}
          aria-label="Dismiss"
        >
          ×
        </button>
      )}
    </div>
  )
}