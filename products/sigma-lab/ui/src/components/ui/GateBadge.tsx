import React, { useState } from 'react'
import './GateBadge.css'

interface GateViolation {
  rule: string
  passed: boolean
  actual?: string | number
  expected?: string | number
  message: string
}

interface GateBadgeProps {
  status: 'pass' | 'fail'
  violations?: number
  title?: string
  items?: GateViolation[]
  className?: string
}

export const GateBadge: React.FC<GateBadgeProps> = ({
  status,
  violations = 0,
  title,
  items = [],
  className = ''
}) => {
  const [showTooltip, setShowTooltip] = useState(false)
  
  const badgeText = status === 'pass' ? 'PASS' : 'FAIL'
  const defaultTitle = status === 'pass' 
    ? 'All Gates Passed' 
    : `Gate Failed (${violations} violation${violations !== 1 ? 's' : ''})`
  
  return (
    <div className="gate-badge-container">
      <button
        className={`gate-badge gate-badge-${status} ${className}`}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onFocus={() => setShowTooltip(true)}
        onBlur={() => setShowTooltip(false)}
        aria-label={title || defaultTitle}
      >
        {badgeText}
      </button>
      
      {showTooltip && items.length > 0 && (
        <div className={`gate-tooltip gate-tooltip-${status}`}>
          <div className="gate-tooltip-title">{title || defaultTitle}</div>
          <ul className="gate-tooltip-list">
            {items.map((item, index) => (
              <li key={index} className="gate-tooltip-item">
                <span className={`gate-icon ${item.passed ? 'gate-icon-pass' : 'gate-icon-fail'}`}>
                  {item.passed ? '✓' : '✗'}
                </span>
                <span className="gate-tooltip-text">{item.message}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

// Trust Badge component (for integrity, parity, capacity warnings)
interface TrustBadgeProps {
  type: 'integrity' | 'parity' | 'capacity'
  status: 'success' | 'warning' | 'error'
  label: string
  title?: string
  description?: string
  className?: string
}

export const TrustBadge: React.FC<TrustBadgeProps> = ({
  type,
  status,
  label,
  title,
  description,
  className = ''
}) => {
  const [showTooltip, setShowTooltip] = useState(false)
  
  const iconMap = {
    integrity: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
      </svg>
    ),
    parity: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="15" y1="9" x2="9" y2="15"/>
        <line x1="9" y1="9" x2="15" y2="15"/>
      </svg>
    ),
    capacity: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <line x1="12" y1="8" x2="12" y2="16"/>
      </svg>
    )
  }
  
  return (
    <div className="trust-badge-container">
      <button
        className={`trust-badge trust-badge-${status} ${className}`}
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onFocus={() => setShowTooltip(true)}
        onBlur={() => setShowTooltip(false)}
        aria-label={title || label}
      >
        {iconMap[type]}
        <span>{label}</span>
      </button>
      
      {showTooltip && (title || description) && (
        <div className={`trust-tooltip trust-tooltip-${status}`}>
          {title && <div className="trust-tooltip-title">{title}</div>}
          {description && <div className="trust-tooltip-description">{description}</div>}
        </div>
      )}
    </div>
  )
}