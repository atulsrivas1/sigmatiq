# Sigmatiq Sigma Lab - Complete Development Guide

## Project Overview

Sigmatiq Sigma Lab is an institutional-grade trading platform for retail investors that provides the complete lifecycle: **discover → validate → simulate → subscribe → automate → review**. The platform features model authoring, backtesting, automated execution, and comprehensive risk management through the Build → Train → Backtest (BTB) pipeline.

### Product Ecosystem
- **Sigma Lab**: Model authoring and evaluation (preview, build/train/backtest, sweeps/leaderboard, model cards and lineage)
- **Sigma Sim**: Broker-aware paper trading for validation before capital deployment
- **Sigma Market**: Curated signal feeds from AI models and vetted human traders
- **Sigma Pilot**: Policy-driven execution automation across supported brokers

### Core Principles
1. **Evidence over opinion** - All signals carry provenance, assumptions, and expected ranges
2. **Transparency first** - Model cards, data sheets, and post-trade attribution are standard
3. **Risk-aware by default** - Conservative controls enabled; users opt into higher risk
4. **Human control** - Automation is reversible and bounded by user policies
5. **Continuous learning** - Every trade feeds evaluation loops and improves models

## Project Structure & Conventions

### Repository Layout
```
products/
  sigma-lab/           # Main product directory
    api/               # FastAPI backend
    ui/                # React TypeScript frontend
    docs/              # Comprehensive documentation
    packs/             # Trading strategy packs (zerosigma, swingsigma, etc.)
    matrices/          # Generated training matrices
    artifacts/         # Model artifacts
    live_data/         # Live trading data
    static/            # Static assets and plots
    reports/           # Generated reports
  sigma-core/          # Shared core libraries
  sigma-platform/      # Platform helpers
  mock-api/            # Mock API for UI development
```

### Key Conventions
- **Product root**: `products/sigma-lab/`
- **API**: Runs on port 8001 (`python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`)
- **Mock API**: Development server on port 8010 for UI testing
- **Environment**: `.env` file with POLYGON_API_KEY, DB_* settings
- **Package naming**: `sigma_core` (shared libs), `sigma_platform` (platform helpers)
- **Data caching**: Historical-only cache; today's data always live
- **Naming convention**: Models use `ticker_asset_horizon_cadence` format

## Architecture & Technology Stack

### Backend
- **API Framework**: FastAPI with Pydantic models
- **Database**: PostgreSQL (no container requirement)
- **Data Provider**: Polygon.io for market data
- **Caching**: Historical-only, never cache today's data
- **Testing**: pytest with coverage targets

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast HMR and builds
- **Styling**: CSS-in-JS with semantic design tokens
- **State Management**: React Context + type-safe API client
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

## Trading Packs (Strategy Types)

### Available Packs
1. **ZeroSigma (0DTE)**: Options expiring same day, high frequency trading
2. **SwingSigma**: 2-10 day equity/options swing trades
3. **LongSigma**: 63-252 day long-term positions
4. **OvernightSigma**: Close-to-open overnight gap trading
5. **MomentumSigma**: Vol-scaled momentum strategies

### Pack Configuration
Each pack includes:
- Indicator sets (90+ technical indicators available)
- Policy templates and risk profiles
- Model templates with pre-configured defaults
- Pack-specific ranking metrics and gates

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

## Development Commands

### Start Development Servers
```bash
# Start UI development server (runs on http://localhost:5173)
cd products/sigma-lab/ui
npm install
npm run dev

# Start API server (runs on http://localhost:8001)
python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload

# Start Mock API for UI development (runs on http://localhost:8010)
cd products/mock-api
pip install -r requirements.txt
make dev
```

### Testing
```bash
# Run core tests
pytest products/sigma-core/tests -q

# Run API tests  
pytest products/sigma-lab/api/tests -q

# Run all tests with coverage
pytest --cov=sigma_core --cov=sigma_platform --cov-report term-missing
```

### Build & Deploy
```bash
# Build UI for production
cd products/sigma-lab/ui
npm run build

# Run database migrations
psql -U user -d sigmalab -f products/sigma-lab/api/migrations/0001_init.sql
```

## Current Implementation Status

### ✅ Completed Features
- React TypeScript application structure with routing
- 4-theme system (2 dark: dark/midnight, 2 light: light/slate) with persistence
- Command palette (Cmd/Ctrl+K) with grouped commands and smooth animations
- Sidebar navigation with hamburger menu icon
- Logo alignment with sidebar icons
- Consistent font sizing and styling across all menu levels
- Active state indicators (green line on left, no background change)
- Component library (buttons, forms, data display, tooltips)
- Mock API integration for development
- Vite configuration with hot module replacement

### 🚧 In Progress (Backlog P0)
1. Tests for /backtest_sweep endpoint
2. UI Sweeps: tag filter, CSV export, parity columns
3. Parity computation and rendering in sweeps
4. Gate badges with improved tooltips
5. Selection cart persistence across sessions

### 📋 Next Priorities (P1)
- Signals monitoring UI (leaderboard, log, analytics tabs)
- Model Designer interface for indicator selection
- Options overlay UI for conversion workflows
- AI Assistant integration with context-aware help
- Structured logging and observability improvements

## Key Documentation References

### Essential Docs
- `docs/INDEX.md` - Complete documentation index
- `docs/CONTRACT.md` - API contract specifications
- `docs/CONVENTIONS.md` - Project conventions
- `docs/STATUS_AND_PLANS.md` - Current status and roadmap
- `docs/BACKLOG.md` - Prioritized task list
- `docs/ENGINEERING_STATUS.md` - Recent engineering updates

### Architecture Decision Records (ADRs)
- `0001-architectural-overview.md` - System architecture
- `0005-btb-pipeline-and-risk-profiles.md` - BTB pipeline design
- `0006-template-first-create-and-split-designer-composer.md` - UI workflow

### API Specifications
- `docs/api/BTB_API_Spec_v1.md` - BTB pipeline API
- `docs/api/Signals_API_Spec_v1.md` - Signals monitoring API
- `docs/api/Assistant_API_Spec_v1.md` - AI assistant API

### UI Specifications
- `docs/ui/Sigma_Lab_UI_Requirements_v1.md` - Detailed UI requirements
- `docs/ui/BTB_UI_Spec_v1.md` - BTB pipeline UI specification
- `docs/ui/AI_Assistant_Spec_v1.md` - AI assistant integration

## Important Notes

### Security & Best Practices
- Never commit secrets or API keys
- Use environment variables for configuration
- Follow security best practices for all code
- Implement proper input validation
- Use parameterized queries for database access

### Performance Guidelines
- Table virtualization for datasets >1000 rows
- Lazy loading for heavy components
- Debounced search (300ms default)
- Historical data caching only (never cache today's data)
- Bundle splitting by route

### Accessibility Requirements
- WCAG AA compliance (AAA for critical text)
- Keyboard navigation for all interactive elements
- Screen reader support with proper ARIA labels
- Focus management in modals and drawers
- High contrast theme support

## Git Information

### Current Branch
- Branch: main
- Recent commits include complete UI implementation with themes and command palette
- All code has been committed and is ready for deployment

### Recent Changes
- Implemented 4-theme system with theme toggle
- Added command palette with keyboard shortcuts
- Fixed TypeScript errors in showcase route
- Aligned logo and sidebar icons properly
- Made sidebar background consistent with page
- Removed sidebar border for cleaner look
- Changed to hamburger menu icon for sidebar toggle
- Implemented single-icon theme button with color changes

---

**Last Updated**: 2025-08-20
**Current Focus**: UI implementation complete, ready for P0 backlog items
**Development Server**: Running on http://localhost:5173