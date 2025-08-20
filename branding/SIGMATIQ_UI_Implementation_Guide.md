# SIGMATIQ UI Implementation Guide for Claude Code

## Project Overview
SIGMATIQ Sigma Lab is a comprehensive trading platform with a flat, minimalist design system focused on accessibility, performance, and user experience. This guide reflects the final production-ready implementation with all refinements.

## 📁 Project Structure

```
sigmatiq/
├── src/
│   ├── components/
│   │   ├── core/           # P0 Priority Components
│   │   ├── analytics/      # P1 Priority Components
│   │   ├── admin/          # P2 Admin Components
│   │   └── shared/         # Shared UI elements
│   ├── styles/
│   │   ├── theme.css       # Design tokens & variables
│   │   ├── components.css  # Component styles
│   │   └── utilities.css   # Utility classes
│   ├── assets/
│   │   ├── logo/           # SIGMA LAB logo variants
│   │   └── icons/          # Icon library
│   ├── layouts/
│   │   ├── AppShell.jsx    # Main navigation shell
│   │   └── AdminLayout.jsx # Admin section layout
│   ├── contexts/
│   │   └── AppContext.jsx  # Global state management
│   ├── services/
│   │   ├── api.js          # API integration
│   │   └── websocket.js    # WebSocket service
│   └── data/
│       └── menu.json       # Navigation structure
```

## 🎨 Design System Setup

### 1. CSS Variables (Theme Tokens)
Updated flat design system with uniform backgrounds:

```css
/* styles/theme.css */
:root {
  /* Brand Colors - Updated */
  --sigmatiq-teal-primary: #1ABC9C;
  --sigmatiq-teal-light: #48C9B0;
  --sigmatiq-teal-dark: #16A085;
  --sigmatiq-bright-teal: #00C4A7;
  --sigmatiq-golden: #F59E0B;
  --sigmatiq-cream: #E8E3D9;
  
  /* Logo Colors */
  --logo-teal-1: #6AAFA7;
  --logo-teal-2: #4A8B83;
  --logo-golden: #C4975C;
  
  /* Flat Surface Colors - No elevation */
  --color-bg: #0A1414;
  --color-surface-1: #0F1A1A;      /* Uniform background */
  --color-surface-2: #111827;      /* Cards/components */
  --color-surface-3: #1A2F2F;      /* Hover states */
  --color-border: #2A3F3F;         /* Minimal borders only */
  
  /* Text Colors */
  --color-text-1: #F5F5F7;
  --color-text-2: #8FA5A5;
  --color-text-3: #6A8080;
  
  /* Status Colors */
  --status-success: #00C4A7;
  --status-warning: #FFB800;
  --status-error: #FF5757;
  --status-info: #3B82F6;
  
  /* Layout - Single Header */
  --header-height: 56px;
  --sidebar-width: 240px;
  --sidebar-collapsed: 60px;
  --mobile-tab-height: 56px;
}
```

## 🏗️ Component Implementation

### Logo Component - Diamond Formation
Updated 4-square diamond logo for SIGMA LAB:

```jsx
// components/shared/Logo.jsx
const Logo = ({ size = 40, showText = true }) => (
  <div className="logo">
    <svg width={size} height={size} viewBox="0 0 40 40">
      <g transform="translate(20, 20) rotate(45)">
        <rect x="-9" y="-9" width="8" height="8" fill="#6AAFA7" rx="1"/>
        <rect x="1" y="-9" width="8" height="8" fill="#C4975C" rx="1"/>
        <rect x="-9" y="1" width="8" height="8" fill="#4A8B83" rx="1"/>
        <rect x="1" y="1" width="8" height="8" fill="#6AAFA7" rx="1"/>
      </g>
    </svg>
    {showText && (
      <div className="logo-text">
        <span className="sigma">SIGMA</span>
        <span className="lab">LAB</span>
      </div>
    )}
  </div>
);
```

### Icon System
Create an icon component that can render all the icons used throughout the app:

```jsx
// components/shared/Icon.jsx
const icons = {
  dashboard: <rect x="3" y="3" width="7" height="7"/>,
  models: <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>,
  build: <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77..."/>,
  sweeps: <path d="M3 12H7M10 12H14M17 12H21"/>,
  leaderboard: <><rect x="8" y="8" width="8" height="13"/><rect x="3" y="11" width="5" height="10"/></>,
  signals: <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>,
  packs: <path d="M3 3h18v18H3zM9 9h6v6H9z"/>,
  health: <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>,
  docs: <><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></>,
  settings: <circle cx="12" cy="12" r="3"/>,
  theme: <circle cx="12" cy="12" r="5"/>,
  export: <><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></>,
  refresh: <><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></>,
  lightning: <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>,
  edit: <><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></>,
  plus: <path d="M12 5v14M5 12h14"/>,
  grid: <><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></>,
  cube: <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z"/>,
  chart: <><path d="M3 3v18h18"/><path d="M7 10l4 4 8-8"/></>,
  menu: <path d="M3 12h18M3 6h18M3 18h18"/>
};

const Icon = ({ name, size = 20, color = "currentColor" }) => (
  <svg 
    width={size} 
    height={size} 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke={color} 
    strokeWidth="2"
    aria-hidden="true"
  >
    {icons[name]}
  </svg>
);
```

## 🔧 Component Integration Guide

### Single Flat Header Component
Unified header with all controls:

```jsx
// components/core/Header.jsx
const Header = () => {
  const [currentDashboard, setCurrentDashboard] = useState(0);
  const dashboards = [
    { id: 'overview', icon: 'grid', name: 'Overview Dashboard' },
    { id: 'models', icon: 'cube', name: 'Models Dashboard' },
    { id: 'analytics', icon: 'chart', name: 'Analytics Dashboard' },
    { id: 'custom', icon: 'settings', name: 'Custom Dashboard' }
  ];

  const cycleDashboard = () => {
    setCurrentDashboard((prev) => (prev + 1) % 4);
  };

  return (
    <header className="main-header" role="banner">
      <div className="header-left">
        <Logo size={36} showText={true} />
      </div>
      
      <div className="header-controls">
        <button 
          className="icon-btn" 
          onClick={cycleDashboard}
          aria-label={`${dashboards[currentDashboard].name} - ${currentDashboard + 1} of 4`}
        >
          <Icon name={dashboards[currentDashboard].icon} />
          <Tooltip text={`${dashboards[currentDashboard].name} (${currentDashboard + 1}/4)`} />
        </button>
        
        <button className="icon-btn" aria-label="Toggle Theme">
          <Icon name="theme" />
          <Tooltip text="Toggle Theme" />
        </button>
        
        <button className="icon-btn" aria-label="Command Palette">
          <span className="cmd-k">⌘K</span>
          <Tooltip text="Command Palette (⌘K)" />
        </button>
      </div>
    </header>
  );
};
```

### P0 Components (Must Have - Implement First)

#### 1. Navigation Shell with Auto-Collapse
```jsx
// layouts/AppShell.jsx
import { Header, Sidebar, CommandPalette, QuickAccessDrawer } from '../components/core';

const AppShell = ({ children }) => (
  <div className="app-shell">
    <Header />
    <div className="main-layout">
      <Sidebar />
      <main className="content-area" id="main-content">
        {children}
      </main>
    </div>
    <CommandPalette />
    <QuickAccessDrawer />
  </div>
);
```

#### 2. Dashboard
```jsx
// pages/Dashboard.jsx
import { RecentModels, LastRuns, QuickActions, HealthStatus } from '../components/core/dashboard';

const Dashboard = () => (
  <div className="dashboard-grid">
    <DashboardCard title="System Overview">
      <HealthStatus />
    </DashboardCard>
    <DashboardCard title="Recent Activity">
      <RecentModels />
    </DashboardCard>
    <DashboardCard title="Performance Summary">
      <PerformanceMetrics />
    </DashboardCard>
  </div>
);
```

#### 3. Models List with Toggle View
```jsx
// components/core/ModelsList.jsx
const ModelsList = () => {
  const [viewType, setViewType] = useState('card');
  
  return (
    <>
      <ControlsBar onViewChange={setViewType} />
      {viewType === 'row' && <TableHeader />}
      <div className={`cards-container ${viewType}-view`}>
        {models.map(model => (
          viewType === 'card' 
            ? <ModelCard key={model.id} {...model} />
            : <ModelRow key={model.id} {...model} />
        ))}
      </div>
      <Pagination />
    </>
  );
};
```

#### 4. Create Model Wizard (3-Step)
```jsx
// components/core/CreateModelWizard.jsx
const CreateModelWizard = () => {
  const [step, setStep] = useState(1);
  
  return (
    <div className="wizard">
      <WizardSteps current={step} />
      {step === 1 && <TemplateSelector onSelect={handleTemplate} />}
      {step === 2 && <ConfigureModel template={selectedTemplate} />}
      {step === 3 && <ReviewAndCreate onConfirm={handleCreate} />}
    </div>
  );
};
```

#### 5. Build/Train/Backtest Tabs
```jsx
// components/core/BTBTabs.jsx
const BTBTabs = () => {
  const [activeTab, setActiveTab] = useState('build');
  
  return (
    <div className="btb-container">
      <TabNav tabs={['build', 'train', 'backtest']} onChange={setActiveTab} />
      {activeTab === 'build' && <BuildForm />}
      {activeTab === 'train' && <TrainForm />}
      {activeTab === 'backtest' && <BacktestForm />}
    </div>
  );
};
```

### P1 Components (Implement Second)

#### 6. Signals with Tabs
```jsx
// pages/Signals.jsx
const Signals = () => {
  const [activeTab, setActiveTab] = useState('leaderboard');
  
  return (
    <div className="signals-container">
      <TabNav tabs={['leaderboard', 'log', 'analytics']} onChange={setActiveTab} />
      {activeTab === 'leaderboard' && <SignalsLeaderboard />}
      {activeTab === 'log' && <SignalsLog />}
      {activeTab === 'analytics' && <SignalsAnalytics />}
    </div>
  );
};
```

#### 7. Options Overlay
```jsx
// components/analytics/OptionsOverlay.jsx
const OptionsOverlay = () => (
  <div className="options-overlay-container">
    <StrategySelector />
    <OptionsParameters />
    <ParitySummary />
    <OptionsChainPreview />
    <ActionButtons />
  </div>
);
```

### P2 Admin Components (Implement Last)

#### 8. Admin Layout
```jsx
// layouts/AdminLayout.jsx
const AdminLayout = ({ children }) => (
  <div className="admin-container">
    <AdminNotice />
    <AdminNav />
    {children}
  </div>
);
```

## 📱 Responsive Implementation

### Mobile Breakpoints
```css
/* Mobile First Approach */
@media (min-width: 768px) {
  .cards-container.card-view {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
  .sidebar { 
    position: relative;
    transform: translateX(0);
  }
}

@media (max-width: 767px) {
  .sidebar { 
    position: fixed;
    transform: translateX(-100%);
    top: var(--header-height);
  }
  .sidebar.active {
    transform: translateX(0);
  }
  .mobile-tab-bar { 
    display: flex;
  }
}
```

### Touch Optimization
```css
.btn, .card, .nav-item, .icon-btn {
  min-height: 44px; /* iOS touch target */
  -webkit-tap-highlight-color: transparent;
}

.card {
  touch-action: pan-y;
  user-select: none;
}
```

## 🎯 Implementation Priority Order

### Phase 1: Core Structure (Week 1)
- [x] Set up project structure and routing
- [x] Implement theme/design tokens
- [x] Create Logo and Icon components
- [x] Build AppShell with Single Header
- [x] Implement Auto-Collapse Sidebar
- [x] Add Quick Access Drawer (icon-only)
- [x] Add Command Palette (⌘K)

### Phase 2: P0 Components (Week 2-3)
- [ ] Dashboard with all cards
- [ ] Models List with card/row toggle
- [ ] Create Model Wizard (3-step)
- [ ] Build/Train/Backtest forms
- [ ] Sweeps with What-If controls
- [ ] Leaderboard with Gate badges
- [ ] Selection Cart
- [ ] AI Assistant panel
- [ ] WebSocket alerts
- [ ] Loading/Empty/Error states

### Phase 3: P1 Components (Week 4)
- [ ] Signals (Leaderboard, Log, Analytics)
- [ ] Options Overlay
- [ ] Health/Status page
- [ ] Performance Tab with charts
- [ ] Templates Gallery

### Phase 4: P2 Admin (Week 5)
- [ ] Admin Jobs management
- [ ] Quotas & Limits
- [ ] Risk Profiles management
- [ ] Packs Manager
- [ ] Templates Manager
- [ ] Feature Flags
- [ ] Data Health
- [ ] Audit & Logs
- [ ] Users & Roles

## 🔌 API Integration Points

### Data Fetching Pattern
```javascript
// services/api.js
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8080';

export const api = {
  models: {
    list: (params) => fetch(`${API_BASE}/models?${new URLSearchParams(params)}`),
    create: (data) => fetch(`${API_BASE}/models`, { 
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data) 
    }),
    get: (id) => fetch(`${API_BASE}/models/${id}`),
    update: (id, data) => fetch(`${API_BASE}/models/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }),
  },
  sweeps: {
    run: (data) => fetch(`${API_BASE}/backtest_sweep`, { 
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data) 
    }),
  },
  leaderboard: {
    get: (params) => fetch(`${API_BASE}/leaderboard?${new URLSearchParams(params)}`),
  },
  build: {
    matrix: (data) => fetch(`${API_BASE}/build_matrix`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }),
  },
  train: {
    start: (data) => fetch(`${API_BASE}/train`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }),
    batch: (selections) => fetch(`${API_BASE}/train/batch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(selections)
    }),
  },
  signals: {
    leaderboard: (params) => fetch(`${API_BASE}/signals/leaderboard?${new URLSearchParams(params)}`),
    log: (params) => fetch(`${API_BASE}/signals?${new URLSearchParams(params)}`),
    summary: (params) => fetch(`${API_BASE}/signals/summary?${new URLSearchParams(params)}`),
  },
  health: {
    check: () => fetch(`${API_BASE}/healthz`),
  }
};
```

### WebSocket Connection
```javascript
// services/websocket.js
class WebSocketService {
  constructor() {
    this.ws = null;
    this.subscribers = new Set();
  }

  connect() {
    this.ws = new WebSocket(process.env.REACT_APP_WS_URL || 'ws://localhost:8080/ws');
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.notify(data);
    };
    
    this.ws.onclose = () => {
      // Reconnect after 3 seconds
      setTimeout(() => this.connect(), 3000);
    };
  }

  subscribe(callback) {
    this.subscribers.add(callback);
    return () => this.subscribers.delete(callback);
  }

  notify(data) {
    this.subscribers.forEach(callback => callback(data));
  }
}

export const wsService = new WebSocketService();
```

## 🚀 State Management

### Context for Global State
```jsx
// contexts/AppContext.jsx
const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState('dark');
  const [riskProfile, setRiskProfile] = useState('balanced');
  const [selectionCart, setSelectionCart] = useState([]);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [currentDashboard, setCurrentDashboard] = useState(0);
  
  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
      if (e.key === 'Escape') {
        setCommandPaletteOpen(false);
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
  
  return (
    <AppContext.Provider value={{
      theme, setTheme,
      riskProfile, setRiskProfile,
      selectionCart, setSelectionCart,
      commandPaletteOpen, setCommandPaletteOpen,
      currentDashboard, setCurrentDashboard,
    }}>
      {children}
    </AppContext.Provider>
  );
};
```

## ⚡ Performance Optimizations

### Code Splitting
```javascript
// Lazy load heavy components
import { lazy, Suspense } from 'react';

const SignalsAnalytics = lazy(() => import('./components/analytics/SignalsAnalytics'));
const AdminDashboard = lazy(() => import('./pages/admin/Dashboard'));
const PerformanceTab = lazy(() => import('./components/analytics/PerformanceTab'));

// Usage with loading fallback
<Suspense fallback={<LoadingSpinner />}>
  <SignalsAnalytics />
</Suspense>
```

### Virtualization for Large Lists
```jsx
// For tables with 1000+ rows
import { FixedSizeList } from 'react-window';

const VirtualizedTable = ({ data }) => (
  <FixedSizeList
    height={600}
    itemCount={data.length}
    itemSize={48}
    width="100%"
  >
    {({ index, style }) => (
      <div style={style}>
        <ModelRow {...data[index]} />
      </div>
    )}
  </FixedSizeList>
);
```

### Debounced Search
```javascript
// hooks/useDebounce.js
const useDebounce = (value, delay = 300) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return debouncedValue;
};
```

## 🧪 Testing Strategy

### Component Testing
```javascript
// __tests__/ModelCard.test.js
import { render, screen } from '@testing-library/react';
import ModelCard from '../components/core/ModelCard';

test('ModelCard displays correct metrics', () => {
  const mockModel = {
    id: 'spy_opt_0dte_hourly',
    sharpe: 2.41,
    totalReturn: 24.5,
    winRate: 58,
    trades: 142
  };
  
  render(<ModelCard {...mockModel} />);
  
  expect(screen.getByText('2.41')).toBeInTheDocument(); // Sharpe
  expect(screen.getByText('+24.5%')).toBeInTheDocument(); // Return
  expect(screen.getByText('58%')).toBeInTheDocument(); // Win Rate
  expect(screen.getByText('142')).toBeInTheDocument(); // Trades
});
```

### Integration Testing
```javascript
// __tests__/Dashboard.integration.test.js
test('Dashboard loads and displays all sections', async () => {
  render(<Dashboard />);
  
  expect(await screen.findByText('System Overview')).toBeInTheDocument();
  expect(await screen.findByText('Recent Activity')).toBeInTheDocument();
  expect(await screen.findByText('Performance Summary')).toBeInTheDocument();
});
```

### Accessibility Testing
```javascript
// __tests__/accessibility.test.js
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('Header should be accessible', async () => {
  const { container } = render(<Header />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## 📋 Deployment Checklist

### Pre-Deployment
- [x] All design tokens imported correctly
- [x] Logo renders at all sizes (36-40px)
- [x] Icons display properly
- [x] Responsive breakpoints working
- [x] Mobile navigation functional
- [x] Command Palette (Cmd+K) working
- [x] Dashboard cycling (1→4→1) operational
- [x] Auto-collapse sidebar working
- [ ] Theme switching operational
- [ ] WebSocket connections established
- [ ] API endpoints connected
- [ ] Error states handled
- [ ] Loading states implemented
- [ ] Empty states designed

### Accessibility
- [x] WCAG AA compliance tested
- [x] Keyboard navigation working (Enter/Space)
- [x] Screen reader compatible
- [x] ARIA labels on all interactive elements
- [x] Focus states visible
- [x] Color contrast verified
- [x] Touch targets ≥ 44px
- [x] Skip links implemented

### Performance
- [x] No 3D transforms or heavy shadows
- [x] Flat hover states only
- [ ] Lighthouse score > 90
- [ ] Bundle size optimized
- [ ] Images optimized
- [ ] Code splitting implemented
- [ ] Lazy loading configured

## 📚 Component Usage Examples

### Using Trust HUD Badges
```jsx
import { TrustHUD } from './components/core/TrustHUD';

<TrustHUD 
  integrity="ok"
  parity={-2.1}
  capacity="high"
  onTooltip={(type) => console.log(`Tooltip shown for ${type}`)}
/>
```

### Using Gate Badges with Tooltips
```jsx
import { GateBadge } from './components/core/GateBadge';

<GateBadge 
  status="fail"
  reasons={[
    { code: 'min_trades_not_met', message: 'Min trades: 3 < 5' },
    { code: 'spread_above_limit', message: 'Spread: 12% > 10%' }
  ]}
/>
```

### Using Risk Profile Selector
```jsx
import { RiskProfileSelector } from './components/core/RiskProfileSelector';

<RiskProfileSelector 
  value={riskProfile}
  onChange={(profile) => {
    setRiskProfile(profile);
    updateRiskBudgets(profile);
  }}
  showDetails={true}
/>
```

### Using Selection Cart
```jsx
import { SelectionCart } from './components/core/SelectionCart';

<SelectionCart 
  items={selectedModels}
  onRemove={(id) => removeFromCart(id)}
  onTrain={() => trainSelected()}
  isOpen={cartOpen}
  onClose={() => setCartOpen(false)}
/>
```

### Using What-If Sliders
```jsx
import { WhatIfPanel } from './components/core/WhatIfPanel';

<WhatIfPanel 
  threshold={0.50}
  topN={20}
  onThresholdChange={(val) => updateThreshold(val)}
  onTopNChange={(val) => updateTopN(val)}
  showDeltas={true}
/>
```

### Using Quick Access Drawer (Icon-Only)
```jsx
import { QuickAccessDrawer } from './components/core/QuickAccessDrawer';

<QuickAccessDrawer 
  buttons={[
    { icon: 'dashboard', label: 'Dashboard', onClick: () => navigate('/') },
    { icon: 'models', label: 'Models', onClick: () => navigate('/models') },
    { icon: 'signals', label: 'Signals', onClick: () => navigate('/signals') },
    { icon: 'export', label: 'Export', onClick: () => exportData() },
    { icon: 'refresh', label: 'Refresh', onClick: () => refreshData() },
    { icon: 'lightning', label: 'Run Backtest', onClick: () => runBacktest() },
    { icon: 'settings', label: 'Settings', onClick: () => openSettings() },
  ]}
  editMode={false}
  onEditToggle={() => setEditMode(!editMode)}
/>
```

## 🔗 Component Dependencies Map

```mermaid
graph TD
    AppShell --> Header[Single Flat Header]
    AppShell --> Sidebar[Auto-Collapse Sidebar]
    AppShell --> CommandPalette
    AppShell --> QuickAccessDrawer[Icon-Only Quick Access]
    
    Header --> Logo[SIGMA LAB Logo]
    Header --> DashboardCycle[Dashboard Cycle 1-4]
    Header --> ThemeToggle
    Header --> CommandK[⌘K Button]
    
    Dashboard --> SystemOverview
    Dashboard --> RecentActivity
    Dashboard --> PerformanceSummary
    
    ModelsList --> ControlsBar
    ModelsList --> ModelCard
    ModelsList --> ModelRow
    ModelsList --> Pagination
    
    CreateWizard --> TemplateSelector
    CreateWizard --> ConfigureModel
    CreateWizard --> ReviewAndCreate
    
    Signals --> SignalsLeaderboard
    Signals --> SignalsLog
    Signals --> SignalsAnalytics
    
    Admin --> Jobs
    Admin --> Quotas
    Admin --> RiskProfiles
    Admin --> PacksManager
    Admin --> TemplatesManager
    Admin --> FeatureFlags
    Admin --> DataHealth
    Admin --> AuditLogs
    Admin --> UsersRoles
```

## 🎨 Quick Start Commands

```bash
# Create project structure
npx create-react-app sigmatiq
cd sigmatiq

# Install dependencies
npm install react-router-dom axios react-window

# Create component structure
mkdir -p src/components/{core,analytics,admin,shared}
mkdir -p src/styles src/assets/icons src/layouts
mkdir -p src/contexts src/services src/hooks src/data

# Copy theme CSS
echo "/* Theme tokens */" > src/styles/theme.css

# Create base components
touch src/components/shared/{Logo,Icon,Button}.jsx
touch src/layouts/AppShell.jsx
touch src/components/core/{Header,Sidebar,Dashboard,ModelsList,CreateWizard}.jsx
touch src/components/core/{CommandPalette,QuickAccessDrawer}.jsx

# Create data files
touch src/data/menu.json

# Start development server
npm start
```

## 🚨 Common Pitfalls to Avoid

1. **No 3D Effects**: Absolutely no `translateY`, `translateZ`, or `box-shadow` for depth
2. **Single Header Only**: One header at top - no secondary headers
3. **Auto-Collapse Required**: Only one sidebar menu expanded at a time
4. **Flat Buttons**: All buttons use border-only hover states
5. **Icon-Only Quick Access**: No text labels in quick access buttons
6. **Dashboard Cycling**: Single button that cycles 1→4→1
7. **Accessibility First**: Every interactive element needs ARIA labels
8. **Keyboard Support**: Enter/Space for buttons, Cmd/Ctrl+K for palette
9. **Uniform Background**: Use `--color-surface-1` throughout
10. **Handle WebSocket Reconnection**: Network issues are common
11. **Test with Real Data**: Ensure performance with 1000+ items
12. **Validate API Responses**: Don't assume data structure
13. **Mobile Touch Targets**: Minimum 44px for all interactive elements
14. **Test Theme Switching**: Ensure all components respect theme changes
15. **Form Validation**: Both client and server-side validation required

## 🚀 Migration Notes from Original Design

### What Changed
- **Header**: Single flat header instead of multiple headers
- **3D Effects**: Removed all elevation and shadows
- **Navigation**: Auto-collapse behavior (only one expanded)
- **Dashboard Button**: Cycles through 4 dashboards instead of dropdown
- **Quick Access**: Icon-only buttons with edit at the end
- **Command Palette**: Uses ⌘K symbol instead of icon
- **Borders**: Minimal use, only where essential

### What Stayed
- All P0, P1, P2 component specifications
- API integration patterns
- WebSocket implementation
- State management approach
- Testing strategies
- Performance optimizations
- Accessibility requirements
- Mobile responsiveness
- Component usage examples

## 📞 Support & Resources

- **Design System Documentation**: Refer to the theme.css for all design tokens
- **Component Library**: All components in src/components/
- **Icon Library**: SVG icons in src/assets/icons/
- **Menu Structure**: Navigation hierarchy in src/data/menu.json
- **API Documentation**: Check API integration section
- **Performance Monitoring**: Use React DevTools Profiler
- **Accessibility Testing**: Use axe DevTools extension

---

This implementation guide provides a complete roadmap for building the SIGMATIQ Sigma Lab trading platform UI with all the refinements for a clean, accessible, flat design. Follow the phases in order and refer back to the component examples as needed. Good luck with your implementation!