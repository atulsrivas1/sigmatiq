export interface MenuItem {
  title: string
  route: string
  hover?: string
  adminOnly?: boolean
  optional?: boolean
  count?: number
  children?: MenuItem[]
}

// Derived from DevGuide/menu.json (hash removed, paths normalized for React Router)
export const menu: MenuItem[] = [
  {
    title: 'Dashboard',
    route: '/dashboard',
    hover: 'At-a-glance status, quick actions, and system health.',
  },
  {
    title: 'Packs',
    route: '/packs',
    hover: 'Explore packs; view presets, indicator sets, and docs; start create in pack context.',
    children: [
      { title: 'Overview', route: '/packs', hover: 'Pack description, presets, indicator sets, and docs.' },
      { title: 'Templates (Gallery)', route: '/packs/:id/templates', hover: 'Browse pack-filtered templates; use one to prefill Create.' },
      { title: 'Recent Models', route: '/packs/:id', hover: 'Open Composer or Designer for models in this pack.' },
    ],
  },
  {
    title: 'Models',
    route: '/models',
    hover: 'Browse, create, edit, and run models.',
    children: [
      { title: 'List', route: '/models', hover: 'Search and filter all models; open details.' },
      { title: 'Templates (Gallery)', route: '/models/templates', hover: 'Browse templates; filter by pack/horizon; prefill Create.', optional: true },
      { title: 'Create Model', route: '/models/new', hover: 'Pick a template, name it, choose risk.' },
      { title: 'Designer', route: '/models/:id/designer', hover: 'Edit indicator set, policy, and metadata.' },
      {
        title: 'Composer',
        route: '/models/:id/composer',
        hover: 'Build → Sweeps → Leaderboard → Train for this model.',
      },
    ],
  },
  {
    title: 'Signals',
    route: '/signals',
    hover: 'Monitor live signals; compare models by live performance.',
    children: [
      { title: 'Leaderboard', route: '/signals', hover: 'Live period metrics (Sharpe, return, win, trades, etc.)' },
      { title: 'Log', route: '/signals/log', hover: 'Filterable entries/fills with slippage, status, and PnL.' },
      { title: 'Analytics', route: '/signals/analytics', hover: 'Equity/drawdown, heatmaps; parity/capacity charts.' },
    ],
  },
  { title: 'Options Overlay', route: '/overlay', hover: 'Convert stock signals to options with parity checks.' },
  { title: 'Health', route: '/health', hover: 'API/DB/data coverage status and troubleshooting.' },
  { title: 'Docs', route: '/docs', hover: 'Open runbooks, specs, and reference documentation.' },
  {
    title: 'Admin',
    route: '/admin',
    hover: 'Admin-only controls for jobs, quotas, risk, packs, templates, flags, and users.',
    adminOnly: true,
    children: [
      { title: 'Jobs', route: '/admin/jobs', hover: 'Monitor/cancel/retry sweeps and training.' },
      { title: 'Quotas & Limits', route: '/admin/quotas', hover: 'View/edit per-user quotas for sweeps and training.' },
      { title: 'Risk Profiles', route: '/admin/risk-profiles', hover: 'Manage global Conservative/Balanced/Aggressive presets per pack.' },
      { title: 'Packs Manager', route: '/admin/packs', hover: 'Manage packs metadata and indicator sets registry.' },
      { title: 'Templates Manager', route: '/admin/templates', hover: 'CRUD model templates; validate and publish versions.' },
      { title: 'Feature Flags', route: '/admin/flags', hover: 'Toggle non-critical features.' },
      { title: 'Data Health', route: '/admin/health', hover: 'DB/migrations, cache policy, workers; diagnostics.' },
      { title: 'Audit & Logs', route: '/admin/audit', hover: 'Recent admin actions; export tail; link to logs.' },
      { title: 'Users & Roles', route: '/admin/users', hover: 'Assign roles; rotate API tokens.' },
    ],
  },
]

// Known implemented app routes (to disable links for not-yet-implemented paths)
export const implementedPaths: string[] = [
  '/dashboard',
  '/models',
  '/models/new',
  '/models/:id/designer',
  '/composer',
  '/sweeps',
  '/leaderboard',
  '/signals',
  '/signals/log',
  '/signals/analytics',
  '/overlay',
  '/health',
]
