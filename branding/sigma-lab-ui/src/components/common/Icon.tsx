import React from 'react';

interface IconProps {
  name: string;
  size?: number;
  color?: string;
  className?: string;
}

const Fallback: React.FC<{label:string,size:number,color:string,className?:string}> = ({label,size,color,className}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
    <circle cx="12" cy="12" r="10" stroke={color} fill="none" strokeWidth="2" />
    <text x="12" y="16" fontSize="8" textAnchor="middle" fill={color}>{label.slice(0,2)}</text>
  </svg>
);

export const Icon: React.FC<IconProps> = ({ name, size = 18, color = 'currentColor', className }) => {
  const stroke = color;
  const icons: Record<string, JSX.Element> = {
    grid: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <rect x="3" y="3" width="7" height="7"/>
        <rect x="14" y="3" width="7" height="7"/>
        <rect x="3" y="14" width="7" height="7"/>
        <rect x="14" y="14" width="7" height="7"/>
      </svg>
    ),
    cube: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>
        <path d="M12 22V12"/>
        <path d="M12 12L2 7"/>
        <path d="M12 12L22 7"/>
      </svg>
    ),
    nodes: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <path d="M3 12H7M10 12H14M17 12H21"/>
        <circle cx="5" cy="12" r="2"/>
        <circle cx="12" cy="12" r="2"/>
        <circle cx="19" cy="12" r="2"/>
      </svg>
    ),
    check: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <polyline points="20 6 9 17 4 12"/>
      </svg>
    ),
    spinner: (
      <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
        <circle cx="12" cy="12" r="10" stroke={stroke} fill="none" strokeWidth="2" opacity="0.25"/>
        <path d="M22 12a10 10 0 0 0-10-10" stroke={stroke} strokeWidth="2"/>
      </svg>
    ),
    alert: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
        <line x1="12" y1="9" x2="12" y2="13"/>
        <line x1="12" y1="17" x2="12.01" y2="17"/>
      </svg>
    ),
    plus: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <line x1="12" y1="5" x2="12" y2="19"/>
        <line x1="5" y1="12" x2="19" y2="12"/>
      </svg>
    ),
    play: (
      <svg width={size} height={size} viewBox="0 0 24 24" className={className}>
        <path d="M5 3L19 12L5 21V3Z" fill={stroke}/>
      </svg>
    ),
    file: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
      </svg>
    ),
    barChart: (
      <svg width={size} height={size} viewBox="0 0 24 24" className={className} fill="none" stroke={stroke} strokeWidth="2">
        <rect x="3" y="12" width="4" height="9"/>
        <rect x="10" y="5" width="4" height="16"/>
        <rect x="17" y="8" width="4" height="13"/>
      </svg>
    ),
    dollarSign: (
      <svg width={size} height={size} viewBox="0 0 24 24" className={className} fill="none" stroke={stroke} strokeWidth="2">
        <line x1="12" y1="1" x2="12" y2="23"/>
        <path d="M17 5H9.5a3.5 3.5 0 000 7H14a3.5 3.5 0 010 7H6"/>
      </svg>
    ),
    fileText: (
      <svg width={size} height={size} viewBox="0 0 24 24" className={className} fill="none" stroke={stroke} strokeWidth="2">
        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
      </svg>
    ),
    shield: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <path d="M12 2L4 7V11C4 16.5 7.5 21.26 12 22C16.5 21.26 20 16.5 20 11V7L12 2Z"/>
        <path d="M12 8V12"/>
        <path d="M12 16H12.01"/>
      </svg>
    ),
    database: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <ellipse cx="12" cy="5" rx="9" ry="3"/>
        <path d="M3 5v6c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/>
        <path d="M3 11v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6"/>
      </svg>
    ),
    globe: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <circle cx="12" cy="12" r="10"/>
        <path d="M2 12h20M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20"/>
      </svg>
    ),
    trendUp: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <path d="M3 17l6-6 4 4 8-8"/>
      </svg>
    ),
    chart: (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth="2" className={className}>
        <rect x="3" y="10" width="4" height="11"/>
        <rect x="10" y="3" width="4" height="18"/>
        <rect x="17" y="7" width="4" height="14"/>
      </svg>
    ),
  };

  return icons[name] || <Fallback label={name} size={size} color={color} className={className}/>;
};
