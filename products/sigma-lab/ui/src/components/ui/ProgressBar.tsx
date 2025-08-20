import React from 'react'
import './ProgressBar.css'

export interface ProgressBarProps {
  value: number
  max?: number
  label?: string
  showValue?: boolean
  variant?: 'default' | 'success' | 'warning' | 'error' | 'gradient'
  size?: 'sm' | 'md' | 'lg'
  animated?: boolean
  className?: string
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  label,
  showValue = false,
  variant = 'default',
  size = 'md',
  animated = false,
  className = ''
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  
  const getVariantClass = () => {
    if (variant !== 'default') return variant
    if (percentage >= 90) return 'error'
    if (percentage >= 70) return 'warning'
    return 'success'
  }

  return (
    <div className={`progress-container ${className}`}>
      {label && (
        <div className="progress-label">
          <span>{label}</span>
          {showValue && <span className="progress-value">{value}/{max}</span>}
        </div>
      )}
      <div className={`progress-bar progress-bar-${size}`}>
        <div 
          className={`progress-fill progress-fill-${getVariantClass()} ${animated ? 'progress-animated' : ''}`}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
    </div>
  )
}

// Capacity Bar Component (specialized progress bar)
export interface CapacityBarProps {
  used: number
  total: number
  label?: string
  thresholdWarning?: number
  thresholdError?: number
  showPercentage?: boolean
  className?: string
}

export const CapacityBar: React.FC<CapacityBarProps> = ({
  used,
  total,
  label,
  thresholdWarning = 70,
  thresholdError = 90,
  showPercentage = true,
  className = ''
}) => {
  const percentage = Math.min(Math.max((used / total) * 100, 0), 100)
  
  const getStatus = () => {
    if (percentage >= thresholdError) return 'error'
    if (percentage >= thresholdWarning) return 'warning'
    return 'success'
  }

  return (
    <div className={`capacity-container ${className}`}>
      <div className="capacity-bar">
        <div 
          className={`capacity-fill capacity-fill-${getStatus()}`}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={used}
          aria-valuemin={0}
          aria-valuemax={total}
          aria-label={label || 'Capacity'}
        />
      </div>
      <div className="capacity-label">
        {label && <span className="capacity-text">{label}</span>}
        <span className="capacity-values">
          {used.toLocaleString()}/{total.toLocaleString()}
          {showPercentage && (
            <span className={`capacity-percentage capacity-percentage-${getStatus()}`}>
              ({percentage.toFixed(1)}%)
            </span>
          )}
        </span>
      </div>
    </div>
  )
}