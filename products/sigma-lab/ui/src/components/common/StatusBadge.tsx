import React from 'react'

type Variant = 'success' | 'warning' | 'error' | 'info' | 'neutral'

export const StatusBadge: React.FC<{ variant?: Variant; children: React.ReactNode }>= ({ variant='neutral', children }) => {
  const className =
    variant === 'success' ? 'badge badge-success' :
    variant === 'warning' ? 'badge badge-warning' :
    variant === 'error' ? 'badge badge-error' :
    variant === 'info' ? 'badge badge-info' : 'badge badge-neutral'
  return <span className={className}>{children}</span>
}

