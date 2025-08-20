import React from 'react'
import './Card.css'

interface CardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  onClick,
  hoverable = true
}) => {
  const classes = [
    'card',
    hoverable && 'card-hoverable',
    onClick && 'card-clickable',
    className
  ].filter(Boolean).join(' ')

  return (
    <div className={classes} onClick={onClick}>
      {children}
    </div>
  )
}

interface CardHeaderProps {
  children: React.ReactNode
  className?: string
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  className = ''
}) => {
  return (
    <div className={`card-header ${className}`}>
      {children}
    </div>
  )
}

interface CardIconProps {
  children: React.ReactNode
  color?: string
  className?: string
}

export const CardIcon: React.FC<CardIconProps> = ({
  children,
  color = 'var(--sigmatiq-bright-teal)',
  className = ''
}) => {
  return (
    <div className={`card-icon ${className}`} style={{ background: color }}>
      {children}
    </div>
  )
}

interface CardHeaderInfoProps {
  title?: string
  subtitle?: string
  className?: string
  children?: React.ReactNode
}

export const CardHeaderInfo: React.FC<CardHeaderInfoProps> = ({
  title,
  subtitle,
  className = '',
  children
}) => {
  return (
    <div className={`card-header-info ${className}`}>
      {title && <div className="card-title">{title}</div>}
      {subtitle && <div className="card-subtitle">{subtitle}</div>}
      {children}
    </div>
  )
}

interface CardBadgeProps {
  children: React.ReactNode
  variant?: 'success' | 'warning' | 'error' | 'info' | 'default'
  className?: string
}

export const CardBadge: React.FC<CardBadgeProps> = ({
  children,
  variant = 'default',
  className = ''
}) => {
  return (
    <span className={`card-badge ${variant} ${className}`}>
      {children}
    </span>
  )
}

interface CardContentProps {
  children: React.ReactNode
  className?: string
}

export const CardContent: React.FC<CardContentProps> = ({
  children,
  className = ''
}) => {
  return <div className={`card-content ${className}`}>{children}</div>
}

interface CardStatsProps {
  children: React.ReactNode
  columns?: 1 | 2 | 3 | 4
  className?: string
}

export const CardStats: React.FC<CardStatsProps> = ({
  children,
  columns = 2,
  className = ''
}) => {
  return (
    <div className={`card-stats card-stats-${columns} ${className}`}>
      {children}
    </div>
  )
}

interface StatItemProps {
  label: string
  value: string | number
  variant?: 'default' | 'positive' | 'negative'
  className?: string
}

export const StatItem: React.FC<StatItemProps> = ({
  label,
  value,
  variant = 'default',
  className = ''
}) => {
  return (
    <div className={`stat-item ${className}`}>
      <span className="stat-label">{label}</span>
      <span className={`stat-value ${variant}`}>{value}</span>
    </div>
  )
}

interface CardChartProps {
  children: React.ReactNode
  className?: string
}

export const CardChart: React.FC<CardChartProps> = ({
  children,
  className = ''
}) => {
  return (
    <div className={`card-chart ${className}`}>
      {children}
    </div>
  )
}

interface CardMetaProps {
  children: React.ReactNode
  className?: string
}

export const CardMeta: React.FC<CardMetaProps> = ({
  children,
  className = ''
}) => {
  return (
    <div className={`card-meta ${className}`}>
      {children}
    </div>
  )
}

interface CardActionsProps {
  children: React.ReactNode
  className?: string
}

export const CardActions: React.FC<CardActionsProps> = ({
  children,
  className = ''
}) => {
  return (
    <div className={`card-actions ${className}`}>
      {children}
    </div>
  )
}

interface CardButtonProps {
  children: React.ReactNode
  primary?: boolean
  onClick?: (e: React.MouseEvent) => void
  className?: string
}

export const CardButton: React.FC<CardButtonProps> = ({
  children,
  primary = false,
  onClick,
  className = ''
}) => {
  return (
    <button
      className={`card-btn ${primary ? 'primary' : ''} ${className}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}