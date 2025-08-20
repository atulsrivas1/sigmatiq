import React from 'react'
import './Badge.css'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'success' | 'warning' | 'error' | 'info' | 'default' | 'neutral'
  size?: 'sm' | 'md' | 'lg'
  dot?: boolean
  className?: string
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  size = 'md',
  dot = false,
  className = ''
}) => {
  const classes = [
    'badge',
    `badge-${variant}`,
    `badge-${size}`,
    dot && 'badge-dot',
    className
  ].filter(Boolean).join(' ')

  return (
    <span className={classes}>
      {dot && <span className="badge-dot-indicator" />}
      {children}
    </span>
  )
}

// Status Badge - specific for status indicators
interface StatusBadgeProps {
  status: 'active' | 'inactive' | 'training' | 'paused' | 'error' | 'success' | 'pending'
  className?: string
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  className = ''
}) => {
  const statusConfig = {
    active: { variant: 'success' as const, label: 'ACTIVE' },
    inactive: { variant: 'neutral' as const, label: 'INACTIVE' },
    training: { variant: 'warning' as const, label: 'TRAINING' },
    paused: { variant: 'error' as const, label: 'PAUSED' },
    error: { variant: 'error' as const, label: 'ERROR' },
    success: { variant: 'success' as const, label: 'SUCCESS' },
    pending: { variant: 'info' as const, label: 'PENDING' }
  }

  const config = statusConfig[status]

  return (
    <Badge variant={config.variant} size="sm" className={className}>
      {config.label}
    </Badge>
  )
}

// Risk Profile Badge - specific for risk levels
interface RiskBadgeProps {
  risk: 'conservative' | 'balanced' | 'aggressive'
  className?: string
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({
  risk,
  className = ''
}) => {
  const riskConfig = {
    conservative: { variant: 'success' as const, label: 'Conservative' },
    balanced: { variant: 'info' as const, label: 'Balanced' },
    aggressive: { variant: 'warning' as const, label: 'Aggressive' }
  }

  const config = riskConfig[risk]

  return (
    <Badge variant={config.variant} size="sm" className={className}>
      {config.label}
    </Badge>
  )
}

// Pack Badge - specific for pack identification
interface PackBadgeProps {
  pack: string
  className?: string
}

export const PackBadge: React.FC<PackBadgeProps> = ({
  pack,
  className = ''
}) => {
  return (
    <Badge variant="neutral" size="sm" className={`pack-badge ${className}`}>
      {pack}
    </Badge>
  )
}