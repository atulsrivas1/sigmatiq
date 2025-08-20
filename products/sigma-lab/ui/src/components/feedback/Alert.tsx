import React from 'react'
import { Icon } from '../Icon'
import './Alert.css'

interface AlertProps {
  children: React.ReactNode
  variant?: 'success' | 'warning' | 'error' | 'info'
  title?: string
  dismissible?: boolean
  onDismiss?: () => void
  icon?: boolean
  className?: string
}

export const Alert: React.FC<AlertProps> = ({
  children,
  variant = 'info',
  title,
  dismissible = false,
  onDismiss,
  icon = true,
  className = ''
}) => {
  const iconMap = {
    success: 'check',
    warning: 'warning',
    error: 'close',
    info: 'info'
  }

  const classes = [
    'alert',
    `alert-${variant}`,
    className
  ].filter(Boolean).join(' ')

  return (
    <div className={classes} role="alert">
      {icon && (
        <div className="alert-icon">
          <Icon name={iconMap[variant]} size={18} />
        </div>
      )}
      
      <div className="alert-content">
        {title && <div className="alert-title">{title}</div>}
        <div className="alert-message">{children}</div>
      </div>
      
      {dismissible && (
        <button className="alert-dismiss" onClick={onDismiss} aria-label="Dismiss">
          <Icon name="close" size={16} />
        </button>
      )}
    </div>
  )
}

// Toast component for temporary notifications
interface ToastProps {
  children: React.ReactNode
  variant?: 'success' | 'warning' | 'error' | 'info'
  title?: string
  duration?: number
  onDismiss?: () => void
  className?: string
}

export const Toast: React.FC<ToastProps> = ({
  children,
  variant = 'info',
  title,
  duration = 5000,
  onDismiss,
  className = ''
}) => {
  React.useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onDismiss?.()
      }, duration)
      
      return () => clearTimeout(timer)
    }
  }, [duration, onDismiss])

  const classes = [
    'toast',
    `toast-${variant}`,
    className
  ].filter(Boolean).join(' ')

  return (
    <div className={classes}>
      <Alert
        variant={variant}
        title={title}
        dismissible
        onDismiss={onDismiss}
        className="toast-alert"
      >
        {children}
      </Alert>
    </div>
  )
}