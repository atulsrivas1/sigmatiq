# Sigmatiq Edge Lab UI Development Guide

## Project Overview

Sigmatiq Edge Lab is an institutional-grade trading platform for retail investors featuring model authoring, backtesting, and automated execution. The UI provides a comprehensive interface for the Build → Train → Backtest (BTB) pipeline with advanced risk management and signal monitoring capabilities.

## Architecture & Technology Stack

- **Frontend**: React-based SPA with TypeScript
- **API**: FastAPI backend with REST endpoints
- **Database**: PostgreSQL with migration support
- **Styling**: CSS-in-JS with semantic design tokens
- **State Management**: Type-safe API client with optimistic updates
- **Testing**: Unit tests + E2E accessibility compliance

## Core UI Principles

### Design Philosophy
- **Evidence over opinion**: All signals carry provenance and expected ranges
- **Transparency first**: Model cards and lineage tracking are standard
- **Risk-aware by default**: Conservative controls enabled; users opt into higher risk
- **Accessibility first**: WCAG AA compliance with keyboard navigation
- **Desktop-first**: Optimized for professional trading workflows

### User Experience Goals
- Intuitive BTB pipeline: Build → Sweeps (Backtests) → Leaderboard → Train
- Clear risk profile management (Conservative/Balanced/Aggressive)
- Real-time monitoring with performance attribution
- Context-aware AI assistant guidance

## Application Structure

### Route Hierarchy
```
/dashboard                    # At-a-glance status and quick actions
/models                      # Browse and manage models
  /new                      # Create model wizard (template picker)
  /:id/designer            # Edit model structure (indicators/policy)
  /:id/composer            # BTB pipeline for model
    /build                # Construct training matrix
    /sweeps               # Configuration grid backtesting
    /leaderboard          # Compare and select results
    /train                # Queue selected configurations
/signals                     # Live signal monitoring
  /leaderboard            # Live performance comparisons
  /log                    # Signal entries with fills/slippage
  /analytics              # Charts and performance visualization
/overlay                     # Options overlay conversion
/health                      # System status and diagnostics
/docs                        # Documentation launcher
/admin                       # Admin-only management interface
```

### Core Components

#### Global UI Elements
- **Risk Profile Selector**: Conservative | Balanced | Aggressive badges
- **Selection Cart**: Persistent drawer for chosen configurations
- **Gate Badges**: Pass/fail chips with tooltip explanations
- **AI Assistant**: Context-aware chat panel with read-only data access
- **Command Palette**: Keyboard-first navigation (Cmd/Ctrl+K)

#### Theme & Styling System
```css
/* Root attributes for theming */
[data-theme="light|dark|slate|paper"]
[data-density="compact|cozy|comfortable"] 
[data-edge="zeroedge|swingedge|longedge|overnightedge|momentumedge"]

/* Semantic tokens */
--surface-1, --surface-2, --bg-primary, --bg-secondary
--text-primary, --text-secondary, --text-muted
--border-color, --border-strong, --ring
--primary-color, --accent, --status-success/warning/error
```

## Page Specifications

### Dashboard (Priority 0)
**Purpose**: At-a-glance status and quick actions
**Components**:
- Recent Models table with quick actions
- Last Runs activity feed
- Quick Actions panel (Create Model, Run Backtest, Sweeps)
- Health status summary
**APIs**: `/models`, `/leaderboard?limit=10`, `/healthz`

### Models - List (Priority 0)
**Purpose**: Browse and manage models
**Features**:
- Search/filter by model_id, pack_id
- Server-side pagination with sortable columns
- Inline actions (Open, Backtest, Sweeps)
- Performance sparklines (model_id, pack_id, updated_at, sharpe, pnl)
**APIs**: `GET /models`, `POST /models`

### Models - Create Wizard (Priority 0)
**Purpose**: Template-driven model creation
**Flow**:
1. Choose Template (pack/horizon/cadence cards)
2. Name & Risk Profile (model name input + risk chips)
3. Create & Navigate (success with Designer/Composer options)
**APIs**: `GET /model_templates`, `POST /models`

### Model Designer (Priority 1)
**Purpose**: Edit model structure and configuration
**Features**:
- Indicator set selection with 90+ built-in technical indicators
- Options flow families configuration (0DTE only)
- Policy editing with validation
- Save prompts rebuild workflow
**APIs**: `/indicators`, `/indicator_sets`, `/validate_policy`

### Composer - Build/Train/Backtest (Priority 0)
**Purpose**: Core BTB pipeline execution
**Build Tab**:
- Date range selection
- Matrix construction with profile link
- Matrix SHA capture and diagnostics
**Train Tab**:
- Allowed hours configuration
- Training queue management
- Artifact tracking
**Backtest Tab**:
- Single backtest execution
- Results visualization with plots
- Parity panel for options

### Sweeps (Priority 0)
**Purpose**: Configuration grid backtesting
**Features**:
- Risk Profile selector with budget controls
- Threshold/hours/top% variant configuration
- What-if panel with delta preview
- Results table with Gate badges and actions
- CSV export with lineage fields
**APIs**: `POST /backtest_sweep`, `GET /leaderboard?tag=...`

### Leaderboard (Priority 0)
**Purpose**: Compare and select backtest results
**Features**:
- Multi-model comparison with filters
- "Pass Gate only" toggle
- Batch selection for training
- Performance sparklines and metrics
- Export capabilities
**APIs**: `GET /leaderboard` with extensive query support

### Signals Monitoring (Priority 1)
**Purpose**: Live signal performance tracking
**Tabs**:
- **Leaderboard**: Live period metrics comparison
- **Log**: Filterable signal entries with slippage data
- **Analytics**: Equity curves, calendar/hour heatmaps
**APIs**: `/signals/leaderboard`, `/signals`, `/signals/summary`

## Technical Implementation

### API Integration
- Type-safe client with centralized error handling
- Optimistic updates with rollback capability
- Streaming support for long-running operations
- File download handling for CSV/plot exports

### State Management
- Persistent selection cart across sessions
- Risk profile preferences per user
- Theme and density settings in localStorage
- Form state with validation and error recovery

### Accessibility Requirements
- WCAG AA compliance (AAA for critical text)
- Keyboard navigation with focus management
- Screen reader support with ARIA labels
- High contrast theme option
- No keyboard traps in modals/drawers

### Performance Considerations
- Table virtualization for large datasets
- Lazy loading for charts and heavy components
- Debounced search and filtering
- Optimized bundle splitting by route

## Data Contracts

### Core Models
```typescript
interface Model {
  model_id: string;
  pack_id: string;
  updated_at: string;
  sharpe?: number;
  lineage: {
    matrix_sha: string;
    config_sha: string;
    policy_sha: string;
    risk_profile: 'Conservative' | 'Balanced' | 'Aggressive';
  };
}

interface BacktestResult {
  id: string;
  model_id: string;
  metrics: {
    sharpe: number;
    cum_ret: number;
    trades: number;
    win_rate: number;
    max_drawdown: number;
  };
  gate: {
    pass: boolean;
    reasons: string[];
  };
  config: {
    kind: 'thresholds' | 'top_pct';
    value: number;
    allowed_hours: number[];
    splits: number;
  };
}
```

### API Endpoints
```typescript
// Core operations
GET /models?model_id&pack_id&limit&offset
POST /models { template_id, name, risk_profile }
GET /leaderboard?model_id&pack_id&tag&risk_profile&pass_gate&limit&offset
POST /backtest_sweep { model_id, risk_profile, sweep, tag }

// Pipeline operations  
POST /build_matrix { model_id, start_date, end_date }
POST /train { model_id, allowed_hours }
POST /backtest { model_id, config, matrix_sha }

// Monitoring
GET /signals?model_id&start&end&status&limit&offset
GET /signals/leaderboard?pack&risk_profile&start&end
GET /healthz?ticker&pack_id&model_id
```

## Development Workflow

### Component Development
1. **Design Tokens**: Use semantic CSS variables for consistent theming
2. **Accessibility**: Implement keyboard navigation and screen reader support
3. **Loading States**: Skeleton screens for tables, shimmer for cards
4. **Error Handling**: Inline field errors + banner notifications
5. **Empty States**: Helpful messaging with clear next actions

### Testing Strategy
- Unit tests for utilities and isolated components
- Integration tests for API client and state management
- E2E tests for critical user flows (BTB pipeline)
- Accessibility testing with automated tools
- Performance benchmarks for data-heavy components

### Quality Gates
- TypeScript strict mode compliance
- Lighthouse performance scores (desktop focus)
- WCAG AA accessibility validation
- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- Mobile responsiveness for key workflows

## Feature Priorities

### Phase 0 (P0) - Core BTB Pipeline
- Dashboard with quick actions
- Models list and create wizard  
- Build/Train/Backtest interface
- Sweeps configuration and results
- Leaderboard with selection
- Basic theming and accessibility

### Phase 1 (P1) - Enhanced Monitoring
- Signals monitoring suite
- Model Designer interface
- Options overlay functionality
- AI Assistant integration
- Performance drawer/modals
- Advanced filtering and export

### Phase 2 (P2) - Advanced Features
- Admin interface for system management
- Advanced charting and visualization
- Real-time streaming updates
- Collaborative features
- Mobile-optimized flows

## Risk Management UI

### Gate System
- Visual badges indicating pass/fail status
- Hover tooltips explaining failure reasons
- Budget visualization with progress bars
- Risk profile impact preview

### Selection Cart
- Persistent across sessions and pages
- Batch operations (compare, train, export)
- Lineage tracking for each selection
- Capacity warnings for large selections

### Audit Trail
- Action logging with timestamps
- Configuration change tracking
- Performance attribution chain
- Export capabilities for compliance

## AI Assistant Integration

### Capabilities
- Context-aware guidance based on current page/model
- Read-only access to database and reports
- Documentation search and citation
- Next action suggestions with one-click execution
- Validation and error explanation

### Safety Measures
- Explicit confirmation required for compute operations
- Read-only mode by default
- Parameter validation before execution
- Clear source attribution for all responses

### UI Integration
- Docked drawer with expand/collapse
- Message threading with action chips
- File preview capabilities
- Integration with command palette

## Deployment Considerations

### Environment Configuration
- API base URL configuration
- Feature flag support for gradual rollout
- Authentication integration
- Error reporting and monitoring

### Performance Optimization
- CDN integration for static assets
- Service worker for offline capabilities
- Progressive loading for large datasets
- Caching strategy for frequently accessed data

### Monitoring & Analytics
- User interaction tracking
- Performance monitoring
- Error rate tracking
- Feature usage analytics

---

This guide provides the foundation for building the Sigmatiq Edge Lab UI. Focus on the P0 features first, ensuring solid accessibility and performance foundations before expanding to advanced features.