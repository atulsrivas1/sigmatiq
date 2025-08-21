import React from 'react'

export const Sparkline: React.FC<{ points?: string; stroke?: string; fill?: string; height?: number }>= ({
  points = '0,20 20,10 40,16 60,12 80,9 100,7 120,11',
  stroke = 'var(--sigmatiq-bright-teal)',
  fill = 'none',
  height = 28,
}) => {
  return (
    <svg width="100%" height={height} viewBox="0 0 120 28">
      <polyline points={points} fill={fill} stroke={stroke} strokeWidth="2"/>
    </svg>
  )
}

