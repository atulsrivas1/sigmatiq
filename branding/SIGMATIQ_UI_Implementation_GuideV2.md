# SIGMATIQ Edge Lab - Complete Implementation Guide

## Table of Contents
1. [Overview](#overview)
2. [Design System](#design-system)
3. [Component Architecture](#component-architecture)
4. [Page Implementations](#page-implementations)
5. [Pipeline Workflow](#pipeline-workflow)
6. [API Integration](#api-integration)
7. [State Management](#state-management)
8. [Deployment Guide](#deployment-guide)

---

## Overview

SIGMATIQ Edge Lab is a sophisticated trading platform UI that combines financial data visualization with machine learning model management. The platform follows a dark-themed aesthetic with teal and golden accents, optimized for trading operations and model evaluation workflows.

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
      <svg width={showText ? dim.logo * 4 : dim.logo} height={dim.logo} viewBox={`0 0 ${showText ? 220 : 60} 60`}>
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
            fontFamily="var(--font-sans)" 
            fontSize={dim.text} 
            fontWeight="300" 
            fill="var(--color-text-1)"
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
      <svg width={showText ? dim.logo * 4 : dim.logo} height={dim.logo} viewBox={`0 0 ${showText ? 220 : 60} 60`}>
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
              fontFamily="var(--font-sans)" 
              fontSize={dim.text} 
              fontWeight="300" 
              fill="var(--color-text-1)"
            >
              SIGMA
            </text>
            <text 
              x="75" 
              y="45" 
              fontFamily="var(--font-sans)" 
              fontSize={dim.text * 0.8} 
              fontWeight="500" 
              fill={colors.secondary}
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

## Component Architecture

### Application Shell

```tsx
interface AppShellProps {
  children: React.ReactNode;
  theme?: 'dark' | 'light' | 'slate' | 'paper';
  density?: 'compact' | 'cozy' | 'comfortable';
}

const AppShell: React.FC<AppShellProps> = ({ children, theme = 'dark', density = 'cozy' }) => {
  return (
    <div className="app-shell" data-theme={theme} data-density={density}>
      <TopBar />
      <div className="main-layout">
        <Sidebar />
        <main className="content-area">
          {children}
        </main>
      </div>
      <CommandPalette />
      <AssistantPanel />
    </div>
  );
};
```

### Top Bar Component

```tsx
const TopBar: React.FC = () => {
  const { theme, setTheme, density, setDensity } = useAppSettings();
  
  return (
    <header className="top-bar">
      <div className="top-bar-left">
        <button className="menu-toggle" aria-label="Toggle menu">
          <MenuIcon />
        </button>
        <SigmatiqLogo size="small" variant="primary" />
        <SearchTrigger />
      </div>
      
      <div className="top-bar-right">
        <ThemeToggle value={theme} onChange={setTheme} />
        <DensitySelector value={density} onChange={setDensity} />
        <RiskProfileSelector />
        <NotificationBell />
        <UserMenu />
      </div>
    </header>
  );
};
```

### Sidebar Navigation with Product Logos

```tsx
const Sidebar: React.FC = () => {
  const location = useLocation();
  
  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <SigmaSuiteLogo product="lab" size="small" showText={false} />
        <span className="product-name">Edge Lab</span>
      </div>
      
      <div className="nav-section">
        <NavLink to="/dashboard" className="nav-item">
          <DashboardIcon />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/models" className="nav-item">
          <ModelsIcon />
          <span>Models</span>
        </NavLink>
        <NavLink to="/sweeps" className="nav-item">
          <SweepsIcon />
          <span>Sweeps</span>
        </NavLink>
        <NavLink to="/leaderboard" className="nav-item">
          <LeaderboardIcon />
          <span>Leaderboard</span>
        </NavLink>
      </div>
      
      <div className="nav-section nav-products">
        <div className="section-title">Products</div>
        <button className="product-switcher">
          <SigmaSuiteLogo product="sim" size="small" showText={false} />
          <span>SigmaSim</span>
        </button>
        <button className="product-switcher">
          <SigmaSuiteLogo product="pilot" size="small" showText={false} />
          <span>SigmaPilot</span>
        </button>
        <button className="product-switcher">
          <SigmaSuiteLogo product="market" size="small" showText={false} />
          <span>SigmaMarket</span>
        </button>
      </div>
    </nav>
  );
};
```

### Model Card Component

```tsx
interface ModelCardProps {
  model: Model;
  view: 'card' | 'row';
  onAction: (action: string, model: Model) => void;
}

const ModelCard: React.FC<ModelCardProps> = ({ model, view, onAction }) => {
  if (view === 'row') {
    return <ModelRow model={model} onAction={onAction} />;
  }
  
  return (
    <div className="card model-card">
      <div className="card-header">
        <div className="card-header-info">
          <div className="card-title">{model.id}</div>
          <div className="card-subtitle">
            {model.pack} • {model.horizon}
          </div>
        </div>
        <StatusBadge status={model.status} />
      </div>
      
      <TrustHUD 
        integrity={model.integrity}
        parity={model.parity}
        capacity={model.capacity}
      />
      
      <MetricsGrid metrics={model.metrics} />
      
      <MiniChart data={model.performance} />
      
      <LineageChips lineage={model.lineage} />
      
      <div className="card-actions">
        <Button variant="primary" onClick={() => onAction('open', model)}>
          Open
        </Button>
        <Button onClick={() => onAction('sweeps', model)}>
          Sweeps
        </Button>
        <Button onClick={() => onAction('train', model)}>
          Train
        </Button>
      </div>
    </div>
  );
};
```

### Trust HUD Component

```tsx
interface TrustHUDProps {
  integrity?: 'ok' | 'warn' | 'error';
  parity?: number;
  capacity?: 'low' | 'medium' | 'high';
}

const TrustHUD: React.FC<TrustHUDProps> = ({ integrity, parity, capacity }) => {
  return (
    <div className="trust-hud">
      <TrustBadge
        type="integrity"
        status={integrity}
        tooltip="Data Integrity: Checks for NaN, missing values"
      />
      <TrustBadge
        type="parity"
        status={getPariryStatus(parity)}
        value={parity}
        tooltip={`Model Parity: ${parity}%`}
      />
      <TrustBadge
        type="capacity"
        status={capacity}
        tooltip={`Capacity: ${capacity}`}
      />
    </div>
  );
};
```

### Gate Badge Component

```tsx
interface GateBadgeProps {
  passed: boolean;
  reasons?: string[];
  riskProfile: 'conservative' | 'balanced' | 'aggressive';
}

const GateBadge: React.FC<GateBadgeProps> = ({ passed, reasons, riskProfile }) => {
  return (
    <Tooltip
      content={
        <div className="gate-tooltip">
          <div className="gate-status">{passed ? 'Passed' : 'Failed'}</div>
          {reasons && (
            <ul className="gate-reasons">
              {reasons.map(reason => (
                <li key={reason}>{humanizeReason(reason)}</li>
              ))}
            </ul>
          )}
        </div>
      }
    >
      <div className={`gate-badge ${passed ? 'pass' : 'fail'}`}>
        {passed ? <CheckIcon /> : <XIcon />}
        <span>Gate</span>
      </div>
    </Tooltip>
  );
};
```

---

## Page Implementations

### Dashboard Page

```tsx
const Dashboard: React.FC = () => {
  const { data: recentModels } = useQuery(['models', 'recent']);
  const { data: lastRuns } = useQuery(['runs', 'recent']);
  const { data: health } = useQuery(['health']);
  
  return (
    <div className="dashboard-grid">
      <DashboardCard title="Recent Models">
        <RecentModelsList models={recentModels} />
      </DashboardCard>
      
      <DashboardCard title="Last Runs">
        <RunsList runs={lastRuns} />
      </DashboardCard>
      
      <DashboardCard title="Quick Actions">
        <QuickActions />
      </DashboardCard>
      
      <DashboardCard title="System Health">
        <HealthStatus status={health} />
      </DashboardCard>
    </div>
  );
};
```

### Models List Page

```tsx
const ModelsList: React.FC = () => {
  const [view, setView] = useState<'card' | 'row'>('card');
  const [filters, setFilters] = useState<ModelFilters>({});
  
  const { data, isLoading, error } = useQuery(
    ['models', filters],
    () => fetchModels(filters)
  );
  
  return (
    <div className="models-page">
      <ControlsBar>
        <SearchBox 
          placeholder="Search models..."
          onSearch={(query) => setFilters({ ...filters, search: query })}
        />
        <FilterGroup>
          <Select 
            label="Pack"
            options={PACK_OPTIONS}
            onChange={(pack) => setFilters({ ...filters, pack })}
          />
        </FilterGroup>
        <ViewToggle value={view} onChange={setView} />
        <Button variant="primary" onClick={() => navigate('/models/new')}>
          Create Model
        </Button>
      </ControlsBar>
      
      <div className={`cards-container ${view}-view`}>
        {isLoading && <LoadingSkeleton count={6} />}
        {error && <ErrorState error={error} onRetry={refetch} />}
        {data?.models.map(model => (
          <ModelCard 
            key={model.id}
            model={model}
            view={view}
            onAction={handleModelAction}
          />
        ))}
        {data?.models.length === 0 && (
          <EmptyState
            title="No models found"
            description="Create your first model to get started"
            action={
              <Button onClick={() => navigate('/models/new')}>
                Create Model
              </Button>
            }
          />
        )}
      </div>
    </div>
  );
};
```

### Create Model Wizard

```tsx
const CreateModelWizard: React.FC = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<CreateModelData>({});
  
  const steps = [
    { title: 'Choose Template', component: TemplateSelector },
    { title: 'Configure', component: ModelConfiguration },
    { title: 'Review', component: ReviewAndCreate }
  ];
  
  return (
    <div className="wizard-container">
      <WizardProgress steps={steps} currentStep={step} />
      
      <div className="wizard-content">
        {step === 1 && (
          <TemplateSelector
            onSelect={(template) => {
              setFormData({ ...formData, template });
              setStep(2);
            }}
          />
        )}
        
        {step === 2 && (
          <ModelConfiguration
            template={formData.template}
            onConfigure={(config) => {
              setFormData({ ...formData, ...config });
              setStep(3);
            }}
            onBack={() => setStep(1)}
          />
        )}
        
        {step === 3 && (
          <ReviewAndCreate
            data={formData}
            onConfirm={handleCreate}
            onBack={() => setStep(2)}
          />
        )}
      </div>
    </div>
  );
};
```

### Sweeps Configuration Page

```tsx
const SweepsPage: React.FC = () => {
  const [riskProfile, setRiskProfile] = useState<RiskProfile>('balanced');
  const [sweepConfig, setSweepConfig] = useState<SweepConfig>(DEFAULT_SWEEP_CONFIG);
  const [results, setResults] = useState<SweepResults | null>(null);
  
  const { mutate: runSweep, isLoading } = useMutation(
    (config: SweepConfig) => api.runSweep(config),
    {
      onSuccess: (data) => setResults(data)
    }
  );
  
  return (
    <div className="sweeps-container">
      <div className="sweeps-header">
        <h1>Sweeps Configuration</h1>
        <RiskProfileSelector value={riskProfile} onChange={setRiskProfile} />
      </div>
      
      <div className="sweeps-config">
        <ConfigurationPanel
          config={sweepConfig}
          onChange={setSweepConfig}
          riskProfile={riskProfile}
        />
        
        <WhatIfPanel
          config={sweepConfig}
          onChange={setSweepConfig}
          showDeltas
        />
        
        <Button 
          variant="primary" 
          onClick={() => runSweep(sweepConfig)}
          loading={isLoading}
        >
          Run Sweep
        </Button>
      </div>
      
      {results && (
        <SweepsResults
          results={results}
          onSelect={handleSelection}
          onCompare={handleCompare}
        />
      )}
    </div>
  );
};
```

### Leaderboard Page

```tsx
const LeaderboardPage: React.FC = () => {
  const [filters, setFilters] = useState<LeaderboardFilters>({
    passGateOnly: true,
    riskProfile: 'balanced'
  });
  
  const { data, isLoading } = useQuery(
    ['leaderboard', filters],
    () => api.getLeaderboard(filters)
  );
  
  return (
    <div className="leaderboard-container">
      <LeaderboardFilters
        filters={filters}
        onChange={setFilters}
      />
      
      <DataTable
        columns={LEADERBOARD_COLUMNS}
        data={data?.entries || []}
        loading={isLoading}
        renderRow={(entry) => (
          <LeaderboardRow
            entry={entry}
            onAction={handleAction}
            showGateBadge
          />
        )}
      />
      
      <SelectionCart />
    </div>
  );
};
```

---

## Pipeline Workflow

### Build → Sweeps → Leaderboard → Train Flow

```tsx
// Pipeline context to maintain state across workflow
const PipelineProvider: React.FC = ({ children }) => {
  const [pipeline, setPipeline] = useState<PipelineState>({
    currentStep: 'build',
    matrixSha: null,
    sweepResults: [],
    selections: []
  });
  
  return (
    <PipelineContext.Provider value={{ pipeline, setPipeline }}>
      {children}
    </PipelineContext.Provider>
  );
};

// Step components use shared context
const BuildStep: React.FC = () => {
  const { pipeline, setPipeline } = usePipeline();
  
  const handleBuildComplete = (result: BuildResult) => {
    setPipeline({
      ...pipeline,
      matrixSha: result.matrixSha,
      currentStep: 'sweeps'
    });
    
    toast.success('Matrix built successfully');
    navigate('/sweeps');
  };
  
  return (
    <BuildForm onComplete={handleBuildComplete} />
  );
};
```

---

## API Integration

### API Client Setup

```typescript
class APIClient {
  private baseURL: string;
  private headers: HeadersInit;
  
  constructor(config: APIConfig) {
    this.baseURL = config.baseURL || process.env.REACT_APP_API_URL;
    this.headers = {
      'Content-Type': 'application/json',
      ...config.headers
    };
  }
  
  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...this.headers,
          ...options?.headers
        }
      });
      
      if (!response.ok) {
        throw new APIError(response.status, await response.text());
      }
      
      return await response.json();
    } catch (error) {
      // Handle network errors, retry logic
      throw error;
    }
  }
  
  // Model endpoints
  models = {
    list: (filters?: ModelFilters) => 
      this.request<ModelList>('/models', { params: filters }),
    
    create: (data: CreateModelData) =>
      this.request<Model>('/models', { 
        method: 'POST', 
        body: JSON.stringify(data) 
      }),
    
    get: (id: string) =>
      this.request<Model>(`/models/${id}`),
    
    update: (id: string, data: Partial<Model>) =>
      this.request<Model>(`/models/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
      })
  };
  
  // Pipeline endpoints
  pipeline = {
    build: (config: BuildConfig) =>
      this.request<BuildResult>('/build_matrix', {
        method: 'POST',
        body: JSON.stringify(config)
      }),
    
    sweep: (config: SweepConfig) =>
      this.request<SweepResults>('/backtest_sweep', {
        method: 'POST',
        body: JSON.stringify(config)
      }),
    
    train: (selections: TrainSelection[]) =>
      this.request<TrainResult>('/train', {
        method: 'POST',
        body: JSON.stringify({ selections })
      })
  };
}

export const api = new APIClient({
  baseURL: process.env.REACT_APP_API_URL
});
```

### React Query Setup

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false
    },
    mutations: {
      onError: (error) => {
        toast.error(getErrorMessage(error));
      }
    }
  }
});

// Custom hooks for data fetching
export const useModels = (filters?: ModelFilters) => {
  return useQuery(
    ['models', filters],
    () => api.models.list(filters),
    {
      keepPreviousData: true
    }
  );
};

export const useCreateModel = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    (data: CreateModelData) => api.models.create(data),
    {
      onSuccess: (newModel) => {
        queryClient.invalidateQueries(['models']);
        toast.success(`Model ${newModel.id} created successfully`);
      }
    }
  );
};
```

---

## State Management

### Global State with Zustand

```typescript
interface AppState {
  // Theme & UI
  theme: Theme;
  density: Density;
  sidebarCollapsed: boolean;
  
  // User preferences
  riskProfile: RiskProfile;
  
  // Selection cart
  selections: Selection[];
  
  // Actions
  setTheme: (theme: Theme) => void;
  setDensity: (density: Density) => void;
  toggleSidebar: () => void;
  setRiskProfile: (profile: RiskProfile) => void;
  addSelection: (selection: Selection) => void;
  removeSelection: (id: string) => void;
  clearSelections: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // Initial state
      theme: 'dark',
      density: 'cozy',
      sidebarCollapsed: false,
      riskProfile: 'balanced',
      selections: [],
      
      // Actions
      setTheme: (theme) => set({ theme }),
      setDensity: (density) => set({ density }),
      toggleSidebar: () => set((state) => ({ 
        sidebarCollapsed: !state.sidebarCollapsed 
      })),
      setRiskProfile: (riskProfile) => set({ riskProfile }),
      addSelection: (selection) => set((state) => ({
        selections: [...state.selections, selection]
      })),
      removeSelection: (id) => set((state) => ({
        selections: state.selections.filter(s => s.id !== id)
      })),
      clearSelections: () => set({ selections: [] })
    }),
    {
      name: 'sigmatiq-app-state',
      partialize: (state) => ({
        theme: state.theme,
        density: state.density,
        riskProfile: state.riskProfile
      })
    }
  )
);
```

### Form State Management

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema validation
const createModelSchema = z.object({
  name: z.string().min(3).max(50),
  templateId: z.string(),
  riskProfile: z.enum(['conservative', 'balanced', 'aggressive']),
  pack: z.string(),
  config: z.object({
    startDate: z.string(),
    endDate: z.string(),
    thresholds: z.array(z.number()),
    allowedHours: z.array(z.number().min(0).max(23))
  })
});

type CreateModelForm = z.infer<typeof createModelSchema>;

// Form component
const CreateModelForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting }
  } = useForm<CreateModelForm>({
    resolver: zodResolver(createModelSchema),
    defaultValues: {
      riskProfile: 'balanced'
    }
  });
  
  const onSubmit = async (data: CreateModelForm) => {
    try {
      await api.models.create(data);
      toast.success('Model created successfully');
      navigate('/models');
    } catch (error) {
      toast.error('Failed to create model');
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
};
```

---

## Deployment Guide

### Build Configuration

```json
// package.json
{
  "name": "sigmatiq-edge-lab",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.0.0",
    "@tanstack/react-table": "^8.10.0",
    "zustand": "^4.4.0",
    "react-hook-form": "^7.47.0",
    "zod": "^3.22.0",
    "d3": "^7.8.0",
    "recharts": "^2.9.0",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@vitejs/plugin-react": "^4.1.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "vitest": "^0.34.0",
    "eslint": "^8.50.0",
    "prettier": "^3.0.0"
  }
}
```

### Environment Configuration

```bash
# .env.development
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_MOCK=true

# .env.production
VITE_API_URL=https://api.sigmatiq.com
VITE_WS_URL=wss://api.sigmatiq.com/ws
VITE_ENABLE_MOCK=false
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name _;
    
    root /usr/share/nginx/html;
    index index.html;
    
    # Enable gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Cache static assets
    location /assets {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API proxy
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # WebSocket proxy
    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - run: npm ci
      - run: npm run type-check
      - run: npm run lint
      - run: npm test
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t sigmatiq-edge-lab:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push sigmatiq-edge-lab:${{ github.sha }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/edge-lab edge-lab=sigmatiq-edge-lab:${{ github.sha }}
          kubectl rollout status deployment/edge-lab
```

---

## Performance Optimization

### Code Splitting

```typescript
// Lazy load heavy components
const ChartsModule = lazy(() => import('./modules/Charts'));
const AdminModule = lazy(() => import('./modules/Admin'));

// Route-based splitting
const routes = [
  {
    path: '/charts',
    element: (
      <Suspense fallback={<LoadingSpinner />}>
        <ChartsModule />
      </Suspense>
    )
  }
];
```

### Virtual Scrolling

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

const VirtualTable: React.FC<{ data: any[] }> = ({ data }) => {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 40, // row height
    overscan: 5
  });
  
  return (
    <div ref={parentRef} className="virtual-scroll-container">
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`
            }}
          >
            <TableRow data={data[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
};
```

### Memoization

```typescript
// Memoize expensive computations
const ExpensiveChart = memo(({ data }: { data: ChartData[] }) => {
  const processedData = useMemo(() => 
    processChartData(data), 
    [data]
  );
  
  return <Chart data={processedData} />;
});

// Memoize callbacks
const handleAction = useCallback((action: string, model: Model) => {
  switch(action) {
    case 'open':
      navigate(`/models/${model.id}`);
      break;
    case 'train':
      startTraining(model);
      break;
  }
}, [navigate, startTraining]);
```

---

## Accessibility Checklist

- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible (`:focus-visible`)
- [ ] ARIA labels on icon buttons
- [ ] Form validation messages announced to screen readers
- [ ] Color contrast meets WCAG AA standards (4.5:1)
- [ ] Skip navigation links provided
- [ ] Semantic HTML structure
- [ ] Loading states announced
- [ ] Error messages associated with form fields
- [ ] Tooltips accessible via keyboard
- [ ] Modal focus trapped
- [ ] Tables have proper headers and scope

---

## Testing Strategy

### Unit Tests

```typescript
// Component testing with React Testing Library
describe('ModelCard', () => {
  it('renders model information correctly', () => {
    const model = mockModel();
    render(<ModelCard model={model} view="card" />);
    
    expect(screen.getByText(model.id)).toBeInTheDocument();
    expect(screen.getByText(model.pack)).toBeInTheDocument();
  });
  
  it('handles action clicks', () => {
    const onAction = vi.fn();
    render(<ModelCard model={mockModel()} onAction={onAction} />);
    
    fireEvent.click(screen.getByText('Open'));
    expect(onAction).toHaveBeenCalledWith('open', expect.any(Object));
  });
});
```

### Integration Tests

```typescript
// API integration testing
describe('Models API', () => {
  it('fetches models with filters', async () => {
    const { result } = renderHook(() => 
      useModels({ pack: 'zerosigma' })
    );
    
    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });
    
    expect(result.current.data.models).toHaveLength(5);
    expect(result.current.data.models[0].pack).toBe('zerosigma');
  });
});
```

### E2E Tests

```typescript
// Playwright E2E tests
test('complete model creation flow', async ({ page }) => {
  await page.goto('/models/new');
  
  // Select template
  await page.click('[data-template="zerosigma-starter"]');
  await page.click('button:has-text("Next")');
  
  // Configure model
  await page.fill('[name="name"]', 'Test Model');
  await page.click('[data-risk="balanced"]');
  await page.click('button:has-text("Next")');
  
  // Review and create
  await page.click('button:has-text("Create Model")');
  
  // Verify redirect to models list
  await expect(page).toHaveURL('/models');
  await expect(page.locator('text=Test Model')).toBeVisible();
});
```

---

## Monitoring & Analytics

### Error Tracking

```typescript
// Sentry integration
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: process.env.VITE_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay()
  ]
});

// Error boundary
export const ErrorBoundary = Sentry.withErrorBoundary(App, {
  fallback: ({ error, resetError }) => (
    <ErrorFallback error={error} onReset={resetError} />
  ),
  showDialog: true
});
```

### Performance Monitoring

```typescript
// Web Vitals tracking
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

const sendToAnalytics = ({ name, delta, id }) => {
  // Send to analytics endpoint
  fetch('/api/analytics/vitals', {
    method: 'POST',
    body: JSON.stringify({ name, value: delta, id })
  });
};

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

---

## Troubleshooting Guide

### Common Issues

1. **WebSocket Connection Failed**
   - Check CORS configuration
   - Verify WSS certificate in production
   - Check firewall rules

2. **Theme Not Persisting**
   - Clear localStorage
   - Check browser storage quota
   - Verify zustand persist configuration

3. **Charts Not Rendering**
   - Check D3/Recharts versions
   - Verify data format matches schema
   - Check for NaN/Infinity values

4. **API Rate Limiting**
   - Implement request debouncing
   - Use React Query cache effectively
   - Add retry with exponential backoff

5. **Memory Leaks**
   - Clean up event listeners
   - Cancel pending requests on unmount
   - Dispose of chart instances

---

## Future Enhancements

### Phase 2 Features
- [ ] Real-time collaboration
- [ ] Advanced charting with TradingView
- [ ] ML model versioning UI
- [ ] A/B testing framework
- [ ] Multi-tenancy support

### Phase 3 Features
- [ ] Mobile native app
- [ ] Offline mode with sync
- [ ] Voice commands
- [ ] AR/VR trading interface
- [ ] Blockchain integration

---

## Support & Documentation

- **Documentation**: https://docs.sigmatiq.com
- **API Reference**: https://api.sigmatiq.com/docs
- **Support**: support@sigmatiq.com
- **Community**: https://discord.gg/sigmatiq

## License

Copyright © 2025 SIGMATIQ. All rights reserved.