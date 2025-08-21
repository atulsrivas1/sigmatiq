import { NavItem, Model, RecentModel, RunItem, QuickAction, HealthItem } from '../types';

export const navigationItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: 'grid', route: '/dashboard', active: true },
  { id: 'models', label: 'Models', icon: 'cube', route: '/models' },
  { id: 'sweeps', label: 'Sweeps', icon: 'nodes', route: '/sweeps' },
  { id: 'leaderboard', label: 'Leaderboard', icon: 'barChart', route: '/leaderboard' },
  { id: 'signals', label: 'Signals', icon: 'dollarSign', route: '/signals' },
  { id: 'docs', label: 'Docs', icon: 'fileText', route: '/docs' }
];

export const recentModels: RecentModel[] = [
  { id: 'spy_opt_0dte_hourly', pack: 'zerosigma', status: 'active', statusColor: 'teal', updatedAt: '2h ago' },
  { id: 'aapl_eq_swing_daily', pack: 'swingsigma', status: 'active', statusColor: 'golden', updatedAt: '5h ago' },
  { id: 'tsla_opt_weekly', pack: 'weeklysigma', status: 'active', statusColor: 'tealDark', updatedAt: '1d ago' }
];

export const lastRuns: RunItem[] = [
  { name: 'Backtest Complete', model: 'spy_opt_0dte', time: '11:50 AM', status: 'success', statusLabel: 'Success', icon: 'check' },
  { name: 'Train Running', model: 'aapl_eq_swing', time: '10:30 AM', status: 'running', statusLabel: 'Running', icon: 'spinner' },
  { name: 'Build Failed', model: 'tsla_opt_weekly', time: '9:15 AM', status: 'failed', statusLabel: 'Failed', icon: 'alert' }
];

export const quickActions: QuickAction[] = [
  { label: 'Create Model', icon: 'plus', route: '/models/create', primary: true },
  { label: 'Run Backtest', icon: 'play', route: '/backtest' },
  { label: 'Open Sweeps', icon: 'nodes', route: '/sweeps' },
  { label: 'View Docs', icon: 'file', route: '/docs' }
];

export const systemHealth: HealthItem[] = [
  { label: 'API', status: 'OPERATIONAL', statusClass: 'ok', icon: 'shield' },
  { label: 'Database', status: 'DEGRADED', statusClass: 'warn', icon: 'database' },
  { label: 'Data Feed', status: 'CONNECTED', statusClass: 'ok', icon: 'globe' }
];

export const modelsList: Model[] = [
  {
    id: '1',
    name: 'spy_opt_0dte_hourly',
    pack: 'ZeroSigma',
    type: '0DTE',
    status: 'active',
    badgeColor: 'success',
    icon: { type: 'trendUp', bgColor: 'var(--sigmatiq-bright-teal)' },
    stats: {
      sharpe: '2.41',
      return: { value: '+24.5%', trend: 'positive' },
      winRate: '58%',
      trades: '142'
    },
    meta: { updatedAt: '2h ago', risk: 'Balanced' },
    chartData: 'uptrend',
    actions: [
      { label: 'Open', primary: true },
      { label: 'Sweeps' },
      { label: 'Train' }
    ]
  },
  {
    id: '2',
    name: 'aapl_eq_swing_daily',
    pack: 'SwingSigma',
    type: 'Swing',
    status: 'training',
    badgeColor: 'warning',
    icon: { type: 'chart', bgColor: 'var(--sigmatiq-golden)' },
    stats: {
      sharpe: '1.85',
      return: { value: '+18.2%', trend: 'positive' },
      winRate: '52%',
      trades: '87'
    },
    meta: { updatedAt: '5h ago', risk: 'Conservative' },
    chartData: 'uptrend',
    actions: [
      { label: 'Open', primary: true },
      { label: 'Sweeps' },
      { label: 'Train' }
    ]
  }
];
