import React from 'react'

interface IconProps {
  name: string
  size?: number
  color?: string
  className?: string
}

const icons: Record<string, React.ReactElement> = {
  // Navigation Icons
  dashboard: (
    <>
      <rect x="3" y="3" width="7" height="7" rx="1"/>
      <rect x="14" y="3" width="7" height="7" rx="1"/>
      <rect x="3" y="14" width="7" height="7" rx="1"/>
      <rect x="14" y="14" width="7" height="7" rx="1"/>
    </>
  ),
  models: (
    <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" strokeLinejoin="round"/>
  ),
  build: (
    <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>
  ),
  train: (
    <>
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 6v6l4 2"/>
    </>
  ),
  backtest: (
    <>
      <path d="M3 3v18h18"/>
      <path d="M7 10l4 4 8-8"/>
    </>
  ),
  sweeps: (
    <>
      <line x1="3" y1="12" x2="7" y2="12"/>
      <line x1="10" y1="12" x2="14" y2="12"/>
      <line x1="17" y1="12" x2="21" y2="12"/>
      <line x1="5" y1="7" x2="9" y2="7"/>
      <line x1="15" y1="7" x2="19" y2="7"/>
      <line x1="5" y1="17" x2="9" y2="17"/>
      <line x1="15" y1="17" x2="19" y2="17"/>
    </>
  ),
  leaderboard: (
    <>
      <rect x="8" y="8" width="8" height="13" rx="1"/>
      <rect x="3" y="11" width="5" height="10" rx="1"/>
      <rect x="16" y="13" width="5" height="8" rx="1"/>
    </>
  ),
  signals: (
    <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
  ),
  overlay: (
    <>
      <rect x="3" y="3" width="18" height="18" rx="2"/>
      <rect x="7" y="7" width="10" height="10" rx="1" fill="currentColor" opacity="0.3"/>
    </>
  ),
  health: (
    <>
      <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
      <circle cx="12" cy="12" r="2" fill="currentColor"/>
    </>
  ),
  docs: (
    <>
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
    </>
  ),
  admin: (
    <>
      <circle cx="12" cy="12" r="3"/>
      <path d="M12 1v6m0 6v6m4.22-5.46l4.24-4.24M1.54 12.7l4.24 4.24m12.68 0l-4.24 4.24M6.34 7.76L2.1 3.52"/>
    </>
  ),
  
  // Action Icons
  plus: <path d="M12 5v14M5 12h14"/>,
  edit: (
    <>
      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
    </>
  ),
  delete: (
    <>
      <polyline points="3 6 5 6 21 6"/>
      <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
    </>
  ),
  refresh: (
    <>
      <polyline points="23 4 23 10 17 10"/>
      <polyline points="1 20 1 14 7 14"/>
      <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
    </>
  ),
  export: (
    <>
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
      <polyline points="7 10 12 15 17 10"/>
      <line x1="12" y1="15" x2="12" y2="3"/>
    </>
  ),
  search: (
    <><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></>
  ),
  filter: (
    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
  ),
  
  // UI Icons
  menu: <path d="M3 12h18M3 6h18M3 18h18"/>,
  close: <path d="M18 6L6 18M6 6l12 12"/>,
  chevronDown: <polyline points="6 9 12 15 18 9"/>,
  chevronRight: <polyline points="9 18 15 12 9 6"/>,
  chevronLeft: <polyline points="15 18 9 12 15 6"/>,
  check: <polyline points="20 6 9 17 4 12"/>,
  warning: (
    <>
      <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/>
      <line x1="12" y1="17" x2="12.01" y2="17"/>
    </>
  ),
  info: (
    <>
      <circle cx="12" cy="12" r="10"/>
      <line x1="12" y1="16" x2="12" y2="12"/>
      <line x1="12" y1="8" x2="12.01" y2="8"/>
    </>
  ),
  
  // Dashboard Icons
  grid: (
    <>
      <rect x="3" y="3" width="7" height="7" rx="1"/>
      <rect x="14" y="3" width="7" height="7" rx="1"/>
      <rect x="3" y="14" width="7" height="7" rx="1"/>
      <rect x="14" y="14" width="7" height="7" rx="1"/>
    </>
  ),
  cube: <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>,
  packsLayered: (
    <>
      <path d="M3 14h18v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5z"/>
      <path d="M5 9h14v5H5z"/>
      <path d="M7 4h10v5H7z"/>
    </>
  ),
  chart: (
    <>
      <path d="M3 3v18h18"/>
      <path d="M7 16l4-4 4 4 6-6"/>
    </>
  ),
  settings: (
    <>
      <circle cx="12" cy="12" r="3"/>
      <path d="M12 1v6m0 6v6m4.22-5.46l4.24-4.24M1.54 12.7l4.24 4.24m12.68 0l-4.24 4.24M6.34 7.76L2.1 3.52"/>
    </>
  ),
  
  // Status Icons
  success: (
    <>
      <circle cx="12" cy="12" r="10" fill="var(--status-success)" opacity="0.2"/>
      <polyline points="16 8 10 14 7 11" stroke="var(--status-success)" fill="none"/>
    </>
  ),
  error: (
    <>
      <circle cx="12" cy="12" r="10" fill="var(--status-error)" opacity="0.2"/>
      <line x1="15" y1="9" x2="9" y2="15" stroke="var(--status-error)"/>
      <line x1="9" y1="9" x2="15" y2="15" stroke="var(--status-error)"/>
    </>
  ),
  
  // Theme Icons
  theme: (
    <>
      <circle cx="12" cy="12" r="5"/>
      <path d="M12 1v6m0 6v6m4.22-5.46l4.24-4.24M1.54 12.7l4.24 4.24m12.68 0l-4.24 4.24M6.34 7.76L2.1 3.52"/>
    </>
  ),
  sun: (
    <>
      <circle cx="12" cy="12" r="5"/>
      <line x1="12" y1="1" x2="12" y2="3"/>
      <line x1="12" y1="21" x2="12" y2="23"/>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
      <line x1="1" y1="12" x2="3" y2="12"/>
      <line x1="21" y1="12" x2="23" y2="12"/>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </>
  ),
  moon: <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>,
  
  // Other Icons
  user: (
    <>
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
      <circle cx="12" cy="7" r="4"/>
    </>
  ),
  bell: (
    <>
      <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/>
      <path d="M13.73 21a2 2 0 01-3.46 0"/>
    </>
  ),
  command: (
    <>
      <path d="M18 3a3 3 0 00-3 3v12a3 3 0 003 3 3 3 0 003-3 3 3 0 00-3-3H6a3 3 0 00-3 3 3 3 0 003 3 3 3 0 003-3V6a3 3 0 00-3-3 3 3 0 00-3 3 3 3 0 003 3h12a3 3 0 003-3 3 3 0 00-3-3z"/>
    </>
  ),
  density: (
    <>
      <line x1="3" y1="6" x2="21" y2="6"/>
      <line x1="3" y1="12" x2="21" y2="12"/>
      <line x1="3" y1="18" x2="21" y2="18"/>
    </>
  )
}

export const Icon: React.FC<IconProps> = ({ 
  name, 
  size = 20, 
  color = 'currentColor',
  className = ''
}) => {
  const icon = icons[name]
  
  if (!icon) {
    console.warn(`Icon "${name}" not found`)
    return null
  }

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      {icon}
    </svg>
  )
}
