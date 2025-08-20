import React from 'react'
import { Icon } from '../Icon'
import './Button.css'

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'success'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  icon?: string
  iconPosition?: 'left' | 'right'
  fullWidth?: boolean
  className?: string
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void
  type?: 'button' | 'submit' | 'reset'
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  className = '',
  onClick,
  type = 'button'
}) => {
  const classes = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    fullWidth && 'btn-full-width',
    loading && 'btn-loading',
    className
  ].filter(Boolean).join(' ')

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? (
        <>
          <div className="btn-spinner" />
          <span>{children}</span>
        </>
      ) : (
        <>
          {icon && iconPosition === 'left' && (
            <Icon name={icon} size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16} />
          )}
          <span>{children}</span>
          {icon && iconPosition === 'right' && (
            <Icon name={icon} size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16} />
          )}
        </>
      )}
    </button>
  )
}

// Icon-only button variant
interface IconButtonProps {
  icon: string
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'success'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  className?: string
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void
  'aria-label': string
}

export const IconButton: React.FC<IconButtonProps> = ({
  icon,
  variant = 'secondary',
  size = 'md',
  disabled = false,
  loading = false,
  className = '',
  onClick,
  'aria-label': ariaLabel
}) => {
  const classes = [
    'btn-icon',
    `btn-icon-${variant}`,
    `btn-icon-${size}`,
    loading && 'btn-loading',
    className
  ].filter(Boolean).join(' ')

  const iconSize = size === 'sm' ? 14 : size === 'lg' ? 20 : 16

  return (
    <button
      type="button"
      className={classes}
      disabled={disabled || loading}
      onClick={onClick}
      aria-label={ariaLabel}
    >
      {loading ? (
        <div className="btn-spinner" />
      ) : (
        <Icon name={icon} size={iconSize} />
      )}
    </button>
  )
}