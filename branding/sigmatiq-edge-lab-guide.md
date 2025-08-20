# SIGMATIQ Sigma Lab - Complete Implementation Guide

## Important: Critical Fixes Applied
This guide has been updated with the following critical fixes:

### ✅ Must-Fix Issues (Resolved)
- **API Client**: Fixed query string encoding, uses `import.meta.env.VITE_*` for Vite, proper `APIError` class defined
- **Environment**: Consistent relative `/api` URLs with Nginx proxy to avoid CORS issues  
- **React Router**: All `navigate()` calls now properly import `useNavigate` hook
- **React Query v5**: Updated to use `gcTime` instead of `cacheTime`, `placeholderData: keepPreviousData`
- **TypeScript**: Fixed typo `getParityStatus` (was `getPariryStatus`), added missing `refetch` destructuring
- **SVG Text**: Uses inline `style` prop instead of unreliable SVG attributes, added `role="img"` and `aria-label`
- **Dependencies**: Added all missing packages (@tanstack/react-virtual, testing libraries, Playwright)
- **State Management**: Unified to single Zustand store with convenience hooks
- **CI/CD**: Docker image uses namespaced repo `${{ secrets.DOCKER_USERNAME }}/sigmatiq-sigma-lab`
- **Security**: Added CSP, HSTS, X-Frame-Options headers to Nginx config
- **Accessibility**: Documented WCAG AA contrast ratios and borderline cases

### 📦 Chart Library Strategy
Choose **Recharts only** for v1 to minimize bundle size, or lazy-load D3 for advanced visualizations.

---

## Table of Contents
1. [Overview](#overview)
2. [Design System](#design-system)
3. [Logo System](#logo-system)
4. [Icon System](#icon-system)
5. [Component Architecture](#component-architecture)
6. [Page Implementations](#page-implementations)
7. [Pipeline Workflow](#pipeline-workflow)
8. [API Integration](#api-integration)
9. [State Management](#state-management)
10. [Deployment Guide](#deployment-guide)

---

## Overview

SIGMATIQ Sigma Lab is a sophisticated trading platform UI that combines financial data visualization with machine learning model management. The platform follows a dark-themed aesthetic with teal and golden accents, optimized for trading operations and model evaluation workflows.

### Core Workflow
```mermaid
Build → Sweeps → Leaderboard → Selection → Train → Deploy
```

### Tech Stack
- **Frontend**: React 18+ with TypeScript
- **Styling**: CSS Variables + Tailwind utilities
- **State**: Zustand/Redux Toolkit
- **Data Fetching**: TanStack Query
- **Charts**: D3.js + Recharts
- **Tables**: TanStack Table (virtualized)
- **Forms**: React Hook Form + Zod

---

## Design System

### Color Palette

```css
:root {
  /* Primary Brand Colors */
  --sigmatiq-teal-primary: #1ABC9C;
  --sigmatiq-teal-light: #48C9B0;
  --sigmatiq-teal-dark: #16A085;
  --sigmatiq-golden: #F59E0B;
  --sigmatiq-cream: #E8E3D9;
  --sigmatiq-slate: #334155;
  
  /* Dark Theme (Default) */
  --color-bg: #0A1414;
  --color-surface-1: #0F1A1A;
  --color-surface-2: #111827;
  --color-surface-3: #1A2F2F;
  --color-border: #2A3F3F;
  --color-text-1: #F5F5F7;
  --color-text-2: #8FA5A5;
  --color-text-3: #6A8080;
  
  /* Status Colors */
  --status-success: #00C4A7;
  --status-warning: #FFB800;
  --status-error: #FF5757;
  --status-info: #3B82F6;
  
  /* Semantic Tokens */
  --color-positive: #10B981;
  --color-negative: #EF4444;
  --color-neutral: #6B7280;
}

/* Light Theme Override */
[data-theme="light"] {
  --color-bg: #FFFFFF;
  --color-surface-1: #F9FAFB;
  --color-surface-2: #F3F4F6;
  --color-surface-3: #E5E7EB;
  --color-text-1: #111827;
  --color-text-2: #6B7280;
  --color-text-3: #9CA3AF;
}
```

### Typography

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
  --font-mono: 'Monaco', 'Menlo', 'Courier New', monospace;
  
  /* Type Scale */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
}
```

### Spacing System

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

### Density Modes

```css
/* Density tokens affect spacing and sizing */
[data-density="compact"] {
  --row-height: 32px;
  --card-padding: var(--space-3);
  --input-height: 32px;
}

[data-density="cozy"] {
  --row-height: 40px;
  --card-padding: var(--space-4);
  --input-height: 36px;
}

[data-density="comfortable"] {
  --row-height: 48px;
  --card-padding: var(--space-5);
  --input-height: 40px;
}
```

---

## Logo System

### Brand Architecture
SIGMATIQ uses a dual-logo system to differentiate corporate identity from product platforms:
- **Square Grid** (SIGMATIQ Corporate): Represents stability, structure, and reliability
- **Diamond Grid** (Sigma Suite Products): Suggests movement, innovation, and premium positioning

### Logo Components

#### SIGMATIQ Corporate Logo (Square Grid)
```tsx
interface SigmatiqLogoProps {
  size?: 'small' | 'medium' | 'large';
  variant?: 'primary' | 'monochrome' | 'outline';
  showText?: boolean;
}

export const SigmatiqLogo: React.FC<SigmatiqLogoProps> = ({ 
  size = 'medium', 
  variant = 'primary',
  showText = true 
}) => {
  const dimensions = {
    small: { logo: 24, text: 14 },
    medium: { logo: 40, text: 18 },
    large: { logo: 54, text: 24 }
  };
  
  const dim = dimensions[size];
  
  return (
    <div className="logo-sigmatiq">
      <svg 
        width={showText ? dim.logo * 4 : dim.logo} 
        height={dim.logo} 
        viewBox={`0 0 ${showText ? 220 : 60} 60`}
        role="img"
        aria-label="SIGMATIQ Logo"
      >
        <g transform="translate(5, 5)">
          {variant === 'primary' && (
            <>
              <rect x="0" y="0" width="23" height="23" fill="#1ABC9C" rx="3"/>
              <rect x="27" y="0" width="23" height="23" fill="#48C9B0" rx="3"/>
              <rect x="0" y="27" width="23" height="23" fill="#F59E0B" rx="3"/>
              <rect x="27" y="27" width="23" height="23" fill="#16A085" rx="3"/>
            </>
          )}
          {variant === 'monochrome' && (
            <>
              <rect x="0" y="0" width="23" height="23" fill="#1ABC9C" rx="3"/>
              <rect x="27" y="0" width="23" height="23" fill="#1ABC9C" rx="3" opacity="0.7"/>
              <rect x="0" y="27" width="23" height="23" fill="#1ABC9C" rx="3" opacity="0.5"/>
              <rect x="27" y="27" width="23" height="23" fill="#1ABC9C" rx="3" opacity="0.3"/>
            </>
          )}
          {variant === 'outline' && (
            <>
              <rect x="0" y="0" width="54" height="54" fill="none" stroke="#1ABC9C" strokeWidth="2" rx="3"/>
              <line x1="27" y1="0" x2="27" y2="54" stroke="#1ABC9C" strokeWidth="2"/>
              <line x1="0" y1="27" x2="54" y2="27" stroke="#1ABC9C" strokeWidth="2"/>
            </>
          )}
        </g>
        {showText && (
          <text 
            x="75" 
            y="35" 
            className="logo-text"
            style={{ fontFamily: 'var(--font-sans)', fontSize: dim.text, fontWeight: 300, fill: 'var(--color-text-1)' }}
          >
            SIGMATIQ
          </text>
        )}
      </svg>
    </div>
  );
};
```

#### Sigma Suite Logo (Diamond Grid)
```tsx
interface SigmaSuiteLogoProps {
  size?: 'small' | 'medium' | 'large';
  animated?: boolean;
  showText?: boolean;
  product?: 'suite' | 'lab' | 'pilot' | 'sim' | 'market';
}

export const SigmaSuiteLogo: React.FC<SigmaSuiteLogoProps> = ({ 
  size = 'medium',
  animated = false,
  showText = true,
  product = 'suite'
}) => {
  const dimensions = {
    small: { logo: 24, text: 14 },
    medium: { logo: 40, text: 18 },
    large: { logo: 54, text: 24 }
  };
  
  const dim = dimensions[size];
  
  const productColors = {
    suite: { primary: '#1ABC9C', secondary: '#F59E0B' },
    lab: { primary: '#1ABC9C', secondary: '#1ABC9C' },
    pilot: { primary: '#334155', secondary: '#E8E3D9' },
    sim: { primary: '#16A085', secondary: '#48C9B0' },
    market: { primary: '#F59E0B', secondary: '#1ABC9C' }
  };
  
  const colors = productColors[product];
  
  return (
    <div className="logo-sigma-suite">
      <svg 
        width={showText ? dim.logo * 4 : dim.logo} 
        height={dim.logo} 
        viewBox={`0 0 ${showText ? 220 : 60} 60`}
        role="img"
        aria-label={`Sigma ${product.charAt(0).toUpperCase() + product.slice(1)} Logo`}
      >
        <g transform={`translate(${dim.logo / 2}, ${dim.logo / 2})`}>
          <g 
            transform="rotate(45)" 
            className={animated ? 'rotate-slow' : ''}
          >
            {product === 'suite' ? (
              <>
                <rect x="-11" y="-11" width="22" height="22" fill="#1ABC9C" rx="3"/>
                <rect x="11" y="-11" width="22" height="22" fill="#48C9B0" rx="3"/>
                <rect x="-11" y="11" width="22" height="22" fill="#F59E0B" rx="3"/>
                <rect x="11" y="11" width="22" height="22" fill="#16A085" rx="3"/>
              </>
            ) : (
              <>
                <rect x="-11" y="-11" width="22" height="22" fill={colors.primary} rx="3"/>
                <rect x="11" y="-11" width="22" height="22" fill={colors.secondary} rx="3"/>
                <rect x="-11" y="11" width="22" height="22" fill={colors.secondary} rx="3"/>
                <rect x="11" y="11" width="22" height="22" fill={colors.primary} rx="3"/>
              </>
            )}
          </g>
        </g>
        {showText && (
          <>
            <text 
              x="75" 
              y="25" 
              className="logo-text"
              style={{ fontFamily: 'var(--font-sans)', fontSize: dim.text, fontWeight: 300, fill: 'var(--color-text-1)' }}
            >
              SIGMA
            </text>
            <text 
              x="75" 
              y="45" 
              className="logo-text-sub"
              style={{ fontFamily: 'var(--font-sans)', fontSize: dim.text * 0.8, fontWeight: 500, fill: colors.secondary }}
            >
              {product.toUpperCase()}
            </text>
          </>
        )}
      </svg>
    </div>
  );
};
```

#### Favicon Component
```tsx
export const Favicon: React.FC<{ size?: number }> = ({ size = 32 }) => (
  <svg width={size} height={size} viewBox="0 0 32 32">
    <rect x="2" y="2" width="12" height="12" fill="#1ABC9C" rx="1"/>
    <rect x="16" y="2" width="12" height="12" fill="#48C9B0" rx="1"/>
    <rect x="2" y="16" width="12" height="12" fill="#F59E0B" rx="1"/>
    <rect x="16" y="16" width="12" height="12" fill="#16A085" rx="1"/>
  </svg>
);
```

### Logo CSS Animations
```css
/* Rotation animations for dynamic logos */
@keyframes rotate-slow {
  from { transform: rotate(45deg); }
  to { transform: rotate(405deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.rotate-slow {
  animation: rotate-slow 30s linear infinite;
}

.pulse-effect {
  animation: pulse 3s ease-in-out infinite;
}

/* Logo hover effects */
.logo-sigmatiq:hover rect,
.logo-sigma-suite:hover rect {
  transition: all 0.3s ease;
  filter: brightness(1.1);
}
```

### Usage Guidelines

#### When to Use Each Logo
```tsx
// Corporate contexts - use Square Grid
<SigmatiqLogo variant="primary" size="large" />

// Product interfaces - use Diamond Grid
<SigmaSuiteLogo product="lab" size="medium" animated />

// Navigation bar - compact version
<SigmatiqLogo size="small" showText={false} />

// Loading states - animated diamond
<SigmaSuiteLogo animated showText={false} />
```

---

## Icon System

### Icon Component Library

```tsx
// Base Icon Component
interface IconProps {
  size?: 'small' | 'medium' | 'large';
  color?: string;
  className?: string;
}

const iconSizes = {
  small: 16,
  medium: 20,
  large: 24
};

// Navigation Icons
export const DashboardIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="3" y="3" width="7" height="7" stroke={color} strokeWidth="2" rx="1"/>
    <rect x="14" y="3" width="7" height="7" stroke={color} strokeWidth="2" rx="1"/>
    <rect x="3" y="14" width="7" height="7" stroke={color} strokeWidth="2" rx="1"/>
    <rect x="14" y="14" width="7" height="7" stroke={color} strokeWidth="2" rx="1"/>
  </svg>
);

export const ModelsIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke={color} strokeWidth="2" strokeLinejoin="round"/>
    <path d="M12 22V12" stroke={color} strokeWidth="2"/>
    <path d="M12 12L2 7" stroke={color} strokeWidth="2"/>
    <path d="M12 12L22 7" stroke={color} strokeWidth="2"/>
  </svg>
);

export const SweepsIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M3 12H7" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M10 12H14" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M17 12H21" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <circle cx="5" cy="12" r="2" fill={color}/>
    <circle cx="12" cy="12" r="2" fill={color}/>
    <circle cx="19" cy="12" r="2" fill={color}/>
    <path d="M5 12V6" stroke={color} strokeWidth="1" strokeLinecap="round"/>
    <path d="M12 12V18" stroke={color} strokeWidth="1" strokeLinecap="round"/>
    <path d="M19 12V8" stroke={color} strokeWidth="1" strokeLinecap="round"/>
  </svg>
);

export const LeaderboardIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="7" y="10" width="4" height="10" stroke={color} strokeWidth="2" rx="1"/>
    <rect x="13" y="4" width="4" height="16" stroke={color} strokeWidth="2" rx="1"/>
    <rect x="3" y="14" width="4" height="6" stroke={color} strokeWidth="2" rx="1"/>
  </svg>
);

// Action Icons
export const PlayIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M5 3L19 12L5 21V3Z" fill={color}/>
  </svg>
);

export const PauseIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="6" y="4" width="4" height="16" fill={color} rx="1"/>
    <rect x="14" y="4" width="4" height="16" fill={color} rx="1"/>
  </svg>
);

export const DownloadIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M21 15V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V15" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M7 10L12 15L17 10" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 15V3" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const FilterIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M22 3H2L10 12.46V19L14 21V12.46L22 3Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const SearchIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <circle cx="11" cy="11" r="8" stroke={color} strokeWidth="2"/>
    <path d="M21 21L16.65 16.65" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const CompareIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M18 20V10" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M18 10L15 13" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M21 13L18 10" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M6 4V14" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M6 14L3 11" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M9 11L6 14" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const CartIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <circle cx="9" cy="21" r="1" fill={color}/>
    <circle cx="20" cy="21" r="1" fill={color}/>
    <path d="M1 1H5L7.68 14.39C7.77 14.85 8.21 15.16 8.68 15.18H19.4C19.85 15.16 20.23 14.85 20.32 14.39L23 6H6" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Status Icons
export const CheckIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M20 6L9 17L4 12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const XIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M18 6L6 18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M6 6L18 18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const AlertIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M10.29 3.86L1.82 18C1.64 18.33 1.64 18.74 1.82 19.08C2 19.41 2.35 19.62 2.72 19.62H21.28C21.65 19.62 22 19.41 22.18 19.08C22.36 18.74 22.36 18.33 22.18 18L13.71 3.86C13.53 3.53 13.18 3.31 12.81 3.31C12.44 3.31 12.09 3.53 11.91 3.86H10.29Z" stroke={color} strokeWidth="2" strokeLinejoin="round"/>
    <path d="M12 9V13" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <circle cx="12" cy="17" r="0.5" fill={color}/>
  </svg>
);

export const InfoIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2"/>
    <path d="M12 16V12" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <circle cx="12" cy="8" r="0.5" fill={color}/>
  </svg>
);

export const SpinnerIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={`animate-spin ${className}`}>
    <path d="M12 2V6" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
    <path d="M12 18V22" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
    <path d="M4.93 4.93L7.76 7.76" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
    <path d="M16.24 16.24L19.07 19.07" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
    <path d="M2 12H6" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
    <path d="M18 12H22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M4.93 19.07L7.76 16.24" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
    <path d="M16.24 7.76L19.07 4.93" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.25"/>
  </svg>
);

// Trust HUD Icons
export const ShieldIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M12 2L4 7V11C4 16.5 7.5 21.26 12 22C16.5 21.26 20 16.5 20 11V7L12 2Z" stroke={color} strokeWidth="2" strokeLinejoin="round"/>
    <path d="M12 8V12" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 16H12.01" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const CapacityIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="3" y="8" width="18" height="10" stroke={color} strokeWidth="2" rx="2"/>
    <rect x="7" y="12" width="10" height="2" fill={color}/>
    <path d="M21 11V15" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const ParityIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M12 2V22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M5 9L12 2L19 9" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M5 15L12 22L19 15" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Chart Icons
export const LineChartIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M3 12L9 6L13 10L21 2" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M21 2V8H15" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const BarChartIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="3" y="12" width="4" height="9" fill={color}/>
    <rect x="10" y="5" width="4" height="16" fill={color}/>
    <rect x="17" y="8" width="4" height="13" fill={color}/>
  </svg>
);

export const HeatmapIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="3" y="3" width="6" height="6" fill={color} opacity="0.3"/>
    <rect x="9" y="3" width="6" height="6" fill={color} opacity="0.5"/>
    <rect x="15" y="3" width="6" height="6" fill={color} opacity="0.7"/>
    <rect x="3" y="9" width="6" height="6" fill={color} opacity="0.5"/>
    <rect x="9" y="9" width="6" height="6" fill={color} opacity="0.9"/>
    <rect x="15" y="9" width="6" height="6" fill={color} opacity="0.4"/>
    <rect x="3" y="15" width="6" height="6" fill={color} opacity="0.7"/>
    <rect x="9" y="15" width="6" height="6" fill={color} opacity="0.4"/>
    <rect x="15" y="15" width="6" height="6" fill={color} opacity="0.6"/>
  </svg>
);

// View Toggle Icons
export const GridViewIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="3" y="3" width="7" height="7" stroke={color} strokeWidth="2"/>
    <rect x="14" y="3" width="7" height="7" stroke={color} strokeWidth="2"/>
    <rect x="3" y="14" width="7" height="7" stroke={color} strokeWidth="2"/>
    <rect x="14" y="14" width="7" height="7" stroke={color} strokeWidth="2"/>
  </svg>
);

export const ListViewIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <rect x="3" y="4" width="18" height="4" stroke={color} strokeWidth="2"/>
    <rect x="3" y="10" width="18" height="4" stroke={color} strokeWidth="2"/>
    <rect x="3" y="16" width="18" height="4" stroke={color} strokeWidth="2"/>
  </svg>
);

// Menu Icons
export const MenuIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <path d="M3 12H21" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M3 6H21" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M3 18H21" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const SettingsIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => (
  <svg width={iconSizes[size]} height={iconSizes[size]} viewBox="0 0 24 24" fill="none" className={className}>
    <circle cx="12" cy="12" r="3" stroke={color} strokeWidth="2"/>
    <path d="M12 1V5" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 19V23" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M4.22 4.22L6.34 6.34" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M17.66 17.66L19.78 19.78" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M1 12H5" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M19 12H23" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M4.22 19.78L6.34 17.66" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M17.66 6.34L19.78 4.22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Icon Usage Helper
export const Icon: React.FC<{ name: string } & IconProps> = ({ name, ...props }) => {
  const icons: Record<string, React.FC<IconProps>> = {
    dashboard: DashboardIcon,
    models: ModelsIcon,
    sweeps: SweepsIcon,
    leaderboard: LeaderboardIcon,
    play: PlayIcon,
    pause: PauseIcon,
    download: DownloadIcon,
    filter: FilterIcon,
    search: SearchIcon,
    compare: CompareIcon,
    cart: CartIcon,
    check: CheckIcon,
    x: XIcon,
    alert: AlertIcon,
    info: InfoIcon,
    spinner: SpinnerIcon,
    shield: ShieldIcon,
    capacity: CapacityIcon,
    parity: ParityIcon,
    lineChart: LineChartIcon,
    barChart: BarChartIcon,
    heatmap: HeatmapIcon,
    gridView: GridViewIcon,
    listView: ListViewIcon,
    menu: MenuIcon,
    settings: SettingsIcon
  };
  
  const IconComponent = icons[name];
  return IconComponent ? <IconComponent {...props} /> : null;
};
```

### Icon CSS

```css
/* Icon animations */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Icon hover effects */
.nav-item svg,
.btn svg {
  transition: all 0.2s ease;
}

.nav-item:hover svg {
  transform: translateX(2px);
}

.btn:hover svg {
  transform: scale(1.1);
}

/* Icon color states */
.icon-success { color: var(--status-success); }
.icon-warning { color: var(--status-warning); }
.icon-error { color: var(--status-error); }
.icon-info { color: var(--status-info); }
```

---

## Component Architecture

[Rest of the document continues with Component Architecture section...]