import React from 'react'

interface LogoProps {
  size?: number
  showText?: boolean
  className?: string
}

export const Logo: React.FC<LogoProps> = ({ size = 36, showText = true, className = '' }) => {
  return (
    <div className={`logo ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
      <svg width={size} height={size} viewBox="0 0 40 40" style={{ flexShrink: 0 }}>
        <g transform="translate(20, 20) rotate(45)">
          <rect x="-9" y="-9" width="8" height="8" fill="#6AAFA7" rx="1"/>
          <rect x="1" y="-9" width="8" height="8" fill="#C4975C" rx="1"/>
          <rect x="-9" y="1" width="8" height="8" fill="#4A8B83" rx="1"/>
          <rect x="1" y="1" width="8" height="8" fill="#6AAFA7" rx="1"/>
        </g>
      </svg>
      {showText && (
        <div style={{ display: 'flex', gap: '4px', alignItems: 'baseline' }}>
          <span style={{ color: 'var(--color-text-1)', fontSize: 18, fontWeight: 300 }}>SIGMA</span>
          <span style={{ color: 'var(--sigmatiq-bright-teal)', fontSize: 18, fontWeight: 600 }}>LAB</span>
        </div>
      )}
    </div>
  )
}
