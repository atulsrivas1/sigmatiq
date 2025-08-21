export const freshRecentModels = [
  { id: 'spy_opt_0dte_hourly', pack: 'zerosigma', color: 'var(--sigmatiq-bright-teal)', updatedAt: '2h ago' },
  { id: 'aapl_eq_swing_daily', pack: 'swingsigma', color: 'var(--sigmatiq-golden)', updatedAt: '1h ago' },
  { id: 'tsla_opt_weekly', pack: 'weeklysigma', color: 'var(--sigmatiq-teal-dark)', updatedAt: 'recently' },
]

export const freshRuns = [
  { name: 'Backtest Complete', sub: 'spy_opt_0dte • 11:50 AM', type: 'success' as const },
  { name: 'Train Running', sub: 'aapl_eq_swing • 10:30 AM', type: 'running' as const },
  { name: 'Build Failed', sub: 'tsla_opt_weekly • 9:15 AM', type: 'failed' as const },
]

export const freshHealth = [
  { label: 'API', value: 'OPERATIONAL', className: 'ok' as const, color: 'var(--status-success)', icon: 'shield' as const },
  { label: 'Database', value: 'DEGRADED', className: 'warn' as const, color: 'var(--status-warning)', icon: 'rows' as const },
  { label: 'Data Feed', value: 'CONNECTED', className: 'ok' as const, color: 'var(--status-success)', icon: 'globe' as const },
]

