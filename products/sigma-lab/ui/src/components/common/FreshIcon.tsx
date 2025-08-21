import React from 'react'

export type IconName =
  | 'grid' | 'cube' | 'nodes' | 'barChart' | 'dollarSign' | 'fileText'
  | 'trendUp' | 'trendCheck' | 'clock' | 'spinner' | 'alertCircle'
  | 'chevronLeft' | 'chevronRight' | 'rows' | 'globe' | 'database' | 'shield'
  | 'play' | 'search'

export const FreshIcon: React.FC<{ name: IconName; size?: number; className?: string; stroke?: string; fill?: string; }> = ({
  name, size = 18, className, stroke = 'currentColor', fill = 'none'
}) => {
  const common = { width: size, height: size, viewBox: '0 0 24 24', fill, stroke, strokeWidth: 2 } as any
  switch (name) {
    case 'grid':
      return (<svg {...common} className={className}><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>)
    case 'cube':
      return (<svg {...common} className={className}><path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/><path d="M12 22V12"/><path d="M12 12L2 7"/><path d="M12 12L22 7"/></svg>)
    case 'nodes':
      return (<svg {...common} className={className}><path d="M3 12H7M10 12H14M17 12H21"/><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>)
    case 'barChart':
      return (<svg {...common} className={className}><rect x="7" y="10" width="4" height="10"/><rect x="13" y="4" width="4" height="16"/><rect x="3" y="14" width="4" height="6"/></svg>)
    case 'dollarSign':
      return (<svg {...common} className={className}><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7H14a3.5 3.5 0 010 7H6"/></svg>)
    case 'fileText':
      return (<svg {...common} className={className}><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>)
    case 'trendUp':
      return (<svg {...common} className={className}><path d="M7 17l5-5 5 5"/><path d="M12 12V3"/></svg>)
    case 'trendCheck':
      return (<svg {...common} className={className}><path d="M3 17l6-6 4 4 8-8"/></svg>)
    case 'clock':
      return (<svg {...common} className={className}><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>)
    case 'spinner':
      return (<svg {...common} className={className}><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>)
    case 'alertCircle':
      return (<svg {...common} className={className}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>)
    case 'chevronLeft':
      return (<svg {...common} className={className}><polyline points="15 18 9 12 15 6"/></svg>)
    case 'chevronRight':
      return (<svg {...common} className={className}><polyline points="9 18 15 12 9 6"/></svg>)
    case 'rows':
      return (<svg {...common} className={className}><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>)
    case 'globe':
      return (<svg {...common} className={className}><path d="M12 2v20M2 12h20"/><circle cx="12" cy="12" r="9"/></svg>)
    case 'database':
      return (<svg {...common} className={className}><path d="M3 12h18M3 6h18M3 18h18"/></svg>)
    case 'shield':
      return (<svg {...common} className={className}><path d="M12 2L4 7v5c0 5.5 3.5 10.26 8 11 4.5-.74 8-5.5 8-11V7l-8-5z"/></svg>)
    case 'play':
      return (<svg {...common} className={className}><path d="M5 3l14 9-14 9V3z"/></svg>)
    case 'search':
      return (<svg {...common} className={className}><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>)
    default:
      return null
  }
}
