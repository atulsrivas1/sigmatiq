// Mock data constants used across views (no API wiring yet)

// Wizard data
export const TICKERS = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA'];
export const ASSET_TYPES = ['equity', 'options', 'futures'];
export const HORIZONS = ['intraday', 'daily', 'weekly'];
export const CADENCES = ['1min', '5min', '15min', '30min', '1hour', '4hour', 'daily'];

export const INDICATOR_SETS = [
  {
    name: 'zerosigma_core_v2',
    indicators: ['options_gamma', 'options_iv', 'intraday_open', 'vix_level', 'momentum_score']
  },
  {
    name: 'swingsigma_momentum_v1', 
    indicators: ['ema_12', 'ema_26', 'macd', 'rsi_14', 'bollinger_bands', 'volume_sma']
  },
  {
    name: 'longsigma_trend_v1',
    indicators: ['sma_50', 'sma_200', 'atr_14', 'adx_14', 'stochastic']
  }
];

export const POLICY_TEMPLATES = [
  {
    name: 'default_classification',
    params: {
      'target_lookahead': '1h',
      'threshold_pct': '0.5%',
      'min_trades': 10,
      'max_drawdown': '5%'
    }
  },
  {
    name: 'swing_momentum',
    params: {
      'target_lookahead': '1d',
      'threshold_pct': '1.0%', 
      'min_trades': 5,
      'stop_loss': '2%',
      'take_profit': '4%'
    }
  }
];

export const MODELS = [
  { 
    model_id: 'spy_opt_0dte_hourly', 
    pack_id: 'zerosigma', 
    updated_at: '2025-08-16T09:50:00Z',
    sharpe: 2.41,
    return: '24.5%',
    trades: 142,
    ticker: 'SPY',
    current_price: 447.82,
    price_change: 1.25,
    price_change_pct: 0.28
  },
  { 
    model_id: 'spy_eq_swing_daily', 
    pack_id: 'swingsigma', 
    updated_at: '2025-08-15T16:10:00Z',
    sharpe: 1.85,
    return: '18.2%',
    trades: 89,
    ticker: 'SPY',
    current_price: 447.82,
    price_change: 1.25,
    price_change_pct: 0.28
  },
  { 
    model_id: 'aapl_eq_intraday_hourly', 
    pack_id: 'swingsigma', 
    updated_at: '2025-08-14T10:20:00Z',
    sharpe: 1.92,
    return: '15.7%',
    trades: 203,
    ticker: 'AAPL',
    current_price: 224.31,
    price_change: -2.18,
    price_change_pct: -0.96
  },
  { 
    model_id: 'tsla_opt_0dte_5min', 
    pack_id: 'zerosigma', 
    updated_at: '2025-08-13T14:30:00Z',
    sharpe: 2.15,
    return: '31.2%',
    trades: 276,
    ticker: 'TSLA',
    current_price: 358.64,
    price_change: 4.91,
    price_change_pct: 1.39
  },
  { 
    model_id: 'qqq_eq_long_weekly', 
    pack_id: 'swingsigma', 
    updated_at: '2025-08-11T08:15:00Z',
    sharpe: 1.56,
    return: '12.8%',
    trades: 42,
    ticker: 'QQQ',
    current_price: 481.27,
    price_change: 0.93,
    price_change_pct: 0.19
  },
  { 
    model_id: 'nvda_opt_swing_daily', 
    pack_id: 'zerosigma', 
    updated_at: '2025-08-09T12:45:00Z',
    sharpe: 1.73,
    return: '19.4%',
    trades: 67,
    ticker: 'NVDA',
    current_price: 134.85,
    price_change: -1.42,
    price_change_pct: -1.04
  }
];

export const LEADERBOARD_RUNS = [
  {
    id: 1,
    started_at: '2025-08-16T11:50:00Z',
    model_id: 'spy_opt_0dte_hourly',
    pack_id: 'zerosigma',
    best_sharpe_hourly: 2.41,
    best_cum_ret: 0.38,
    trades_total: 120,
    metrics: { win_rate: 0.62 },
    tag: 'smoke'
  },
  {
    id: 2,
    started_at: '2025-08-15T16:10:00Z',
    model_id: 'spy_eq_swing_daily',
    pack_id: 'swingsigma',
    best_sharpe_hourly: 1.82,
    best_cum_ret: 0.24,
    trades_total: 98,
    metrics: { win_rate: 0.57 },
    tag: 'sweep1'
  },
];

export const SWEEPS_RUNS = [
  { kind: 'thresholds', thresholds: '0.55,0.60,0.65', allowed_hours: '13,14,15', res: { best_sharpe_hourly: 2.41, best_cum_ret: 0.38, trades_total: 120 } },
  { kind: 'top_pct', top_pct: 0.2, allowed_hours: '13,14', res: { best_sharpe_hourly: 2.12, best_cum_ret: 0.31, trades_total: 98 } },
];

// Enhanced sweeps data for new design
export const SWEEP_RESULTS = [
  {
    id: 1,
    kind: 'top_pct',
    value: '0.10',
    allowed_hours: '13,14',
    sharpe: 0.41,
    cum_return: 0.9999,
    trades: 1,
    parity: null,
    tag: 'demo',
    created_at: '2025-08-16T14:30:00Z'
  },
  {
    id: 2,
    kind: 'thr',
    value: '0.60',
    allowed_hours: '13,14,15',
    sharpe: 0.33,
    cum_return: 0.9999,
    trades: 1,
    parity: null,
    tag: 'demo',
    created_at: '2025-08-16T14:25:00Z'
  },
  {
    id: 3,
    kind: 'thr',
    value: '0.55',
    allowed_hours: '13,14',
    sharpe: 0.28,
    cum_return: 0.8521,
    trades: 3,
    parity: null,
    tag: 'demo',
    created_at: '2025-08-16T14:20:00Z'
  },
  {
    id: 4,
    kind: 'thr',
    value: '0.50,0.52,0.54',
    allowed_hours: '13,14,15',
    sharpe: 1.85,
    cum_return: 0.7234,
    trades: 42,
    parity: 'met',
    tag: 'demo',
    created_at: '2025-08-16T13:15:00Z'
  },
  {
    id: 5,
    kind: 'top_pct',
    value: '0.15',
    allowed_hours: '14,15',
    sharpe: 0.95,
    cum_return: 0.6123,
    trades: 8,
    parity: null,
    tag: 'live',
    created_at: '2025-08-16T12:45:00Z'
  }
];

export const SWEEP_MODELS = [
  'spy_opt_0dte_hourly',
  'spy_eq_swing_daily', 
  'aapl_eq_intraday_hourly',
  'tsla_opt_0dte_5min',
  'qqq_eq_long_weekly',
  'nvda_opt_swing_daily'
];

export const SIGNALS = [
  { 
    date: '2025-08-16', 
    time: '09:30',
    model_id: 'spy_opt_0dte_hourly', 
    pack_id: 'zerosigma',
    ticker: 'SPY', 
    side: 'long', 
    entry_mode: 'market', 
    entry_ref_px: 447.35, 
    stop_px: 442.2, 
    target_px: 455.1, 
    rr: 1.8,
    status: 'filled'
  },
  { 
    date: '2025-08-16', 
    time: '10:15',
    model_id: 'spy_eq_swing_daily', 
    pack_id: 'swingsigma',
    ticker: 'SPY', 
    side: 'long', 
    entry_mode: 'limit', 
    entry_ref_px: 447.35, 
    stop_px: 441.0, 
    target_px: 456.0, 
    rr: 1.6,
    status: 'pending'
  },
  { 
    date: '2025-08-15', 
    time: '15:45',
    model_id: 'aapl_eq_intraday_hourly', 
    pack_id: 'longsigma',
    ticker: 'AAPL', 
    side: 'short', 
    entry_mode: 'stop', 
    entry_ref_px: 191.25, 
    stop_px: 195.8, 
    target_px: 184.3, 
    rr: 1.5,
    status: 'filled'
  },
  { 
    date: '2025-08-15', 
    time: '14:20',
    model_id: 'tsla_opt_0dte_5min', 
    pack_id: 'zerosigma',
    ticker: 'TSLA', 
    side: 'long', 
    entry_mode: 'market', 
    entry_ref_px: 245.67, 
    stop_px: 240.1, 
    target_px: 253.4, 
    rr: 1.4,
    status: 'error'
  },
  { 
    date: '2025-08-14', 
    time: '11:30',
    model_id: 'qqq_eq_long_weekly', 
    pack_id: 'longsigma',
    ticker: 'QQQ', 
    side: 'long', 
    entry_mode: 'limit', 
    entry_ref_px: 372.15, 
    stop_px: 368.2, 
    target_px: 378.9, 
    rr: 1.7,
    status: 'filled'
  }
];

export const OVERLAY_SAMPLE = {
  date: '2025-08-16',
  count: 4,
  rows: [
    { 
      ticker: 'AAPL', 
      occ: 'AAPL250816C00190000', 
      expiry: '2025-08-16', 
      strike: 190, 
      type: 'Call', 
      delta: 0.35, 
      iv_used: 0.27,
      bid: 2.10,
      ask: 2.15,
      volume: 147,
      open_interest: 1247
    },
    { 
      ticker: 'MSFT', 
      occ: 'MSFT250816C00380000', 
      expiry: '2025-08-16', 
      strike: 380, 
      type: 'Call', 
      delta: 0.36, 
      iv_used: 0.25,
      bid: 3.20,
      ask: 3.25,
      volume: 89,
      open_interest: 892
    },
    { 
      ticker: 'SPY', 
      occ: 'SPY250816P00445000', 
      expiry: '2025-08-16', 
      strike: 445, 
      type: 'Put', 
      delta: -0.32, 
      iv_used: 0.22,
      bid: 1.85,
      ask: 1.90,
      volume: 234,
      open_interest: 1567
    },
    { 
      ticker: 'TSLA', 
      occ: 'TSLA250816C00250000', 
      expiry: '2025-08-16', 
      strike: 250, 
      type: 'Call', 
      delta: 0.38, 
      iv_used: 0.31,
      bid: 4.15,
      ask: 4.25,
      volume: 67,
      open_interest: 543
    }
  ]
};

// Dashboard-specific mock data
export const RECENT_MODELS = [
  {
    model_id: 'spy_opt_0dte_hourly',
    algorithm: 'KNN',
    status: 'training',
    updated_at: '2025-08-16T11:50:00Z',
    dataset: 'SPXL,30 (May 2022 - Nov 2024)',
    signal: 'R/R 3.00, SL 0.5%, TP 1.5%',
    inputs: ['A: C[5]', 'B: C[20]', 'D: C[40]', 'E: H-L'],
    runtime: '00:09',
    ticker: 'SPY',
    current_price: 447.82,
    price_change: 1.25,
    price_change_pct: 0.28
  },
  {
    model_id: 'spy_eq_swing_daily',
    algorithm: 'GBM',
    status: 'completed',
    updated_at: '2025-08-16T10:50:00Z',
    dataset: 'SPY,D (Jan 2020 - Nov 2024)',
    signal: 'R/R 2.50, SL 1.0%, TP 2.5%',
    inputs: ['RSI(14)', 'EMA(20)', 'Vol/MA', 'ADX'],
    runtime: null,
    ticker: 'SPY',
    current_price: 447.82,
    price_change: 1.25,
    price_change_pct: 0.28
  },
  {
    model_id: 'aapl_eq_intraday_h',
    algorithm: 'RF',
    status: 'completed',
    updated_at: '2025-08-16T08:50:00Z',
    dataset: 'AAPL,60 (Jun 2023 - Nov 2024)',
    signal: 'R/R 2.00, SL 0.75%, TP 1.5%',
    inputs: ['MACD', 'BB', 'OBV', 'ATR'],
    runtime: null,
    ticker: 'AAPL',
    current_price: 224.31,
    price_change: -2.18,
    price_change_pct: -0.96
  },
  {
    model_id: 'tsla_opt_0dte_5m',
    algorithm: 'SVM',
    status: 'queued',
    updated_at: '2025-08-16T06:50:00Z',
    dataset: 'TSLA,5 (Oct - Nov 2024)',
    signal: 'R/R 4.00, SL 0.25%, TP 1.0%',
    inputs: ['Mom(5)', 'Vol', 'Alpha', 'Flow'],
    runtime: null,
    ticker: 'TSLA',
    current_price: 358.64,
    price_change: 4.91,
    price_change_pct: 1.39
  }
];

export const RECENT_RUNS = [
  {
    id: 1,
    type: 'backtest',
    model_id: 'spy_opt_0dte_hourly',
    started_at: '2025-08-16T11:48:00Z',
    status: 'completed',
    metrics: {
      sharpe: 2.41,
      return: 24.5,
      trades: 142
    }
  },
  {
    id: 2,
    type: 'train',
    model_id: 'spy_eq_swing_daily',
    started_at: '2025-08-16T10:48:00Z',
    status: 'completed',
    metrics: {
      accuracy: 87.3,
      f1_score: 0.84,
      time_minutes: 12
    }
  },
  {
    id: 3,
    type: 'build',
    model_id: 'aapl_eq_intraday_hourly',
    started_at: '2025-08-16T08:48:00Z',
    status: 'completed',
    metrics: {
      features: 24,
      rows: '15.2k',
      nan_percent: 0.1
    }
  },
  {
    id: 4,
    type: 'sweep',
    model_id: 'tsla_opt_0dte_5min',
    started_at: '2025-08-16T11:45:00Z',
    status: 'running',
    metrics: {
      progress: 45,
      combos_completed: 18,
      combos_total: 40,
      eta_minutes: 5
    }
  }
];

export const SYSTEM_HEALTH = {
  api: { status: 'ok', message: 'OK' },
  database: { status: 'warning', message: 'WARN' },
  data_coverage: { status: 'ok', message: '98%' }
};

// Sweeps page specific mock data
export const SWEEP_MODELS_LIST = [
  'spy_opt_0dte_hourly',
  'spy_eq_swing_daily', 
  'aapl_eq_intraday_hourly',
  'tsla_opt_0dte_5min',
  'qqq_eq_long_weekly',
  'nvda_opt_swing_daily'
];

export const SWEEP_CONFIGURATION_DEFAULTS = {
  model: 'spy_opt_0dte_hourly',
  threshold_variants: [
    '0.50,0.52,0.54',
    '0.55,0.60,0.65'
  ],
  hours_variants: [
    '13,14',
    '13,14,15'
  ],
  top_pct_variants: [
    '0.10,0.15'
  ],
  guards: {
    min_trades: 5,
    min_sharpe: 0.30,
    tag: 'demo'
  }
};

// Enhanced sweep results matching mock table structure
export const SWEEP_RESULTS_DETAILED = [
  {
    id: 1,
    kind: 'top_pct',
    value: '0.10',
    allowed_hours: '13,14',
    sharpe: 0.41,
    cum_return: 0.9999,
    trades: 1,
    parity: null,
    tag: 'demo',
    created_at: '2025-08-16T14:30:00Z',
    model_id: 'spy_opt_0dte_hourly'
  },
  {
    id: 2,
    kind: 'thr',
    value: '0.60',
    allowed_hours: '13,14,15',
    sharpe: 0.33,
    cum_return: 0.9999,
    trades: 1,
    parity: null,
    tag: 'demo',
    created_at: '2025-08-16T14:25:00Z',
    model_id: 'spy_opt_0dte_hourly'
  },
  {
    id: 3,
    kind: 'thr',
    value: '0.55',
    allowed_hours: '13,14',
    sharpe: 0.28,
    cum_return: 0.8521,
    trades: 3,
    parity: null,
    tag: 'demo',
    created_at: '2025-08-16T14:20:00Z',
    model_id: 'spy_opt_0dte_hourly'
  },
  {
    id: 4,
    kind: 'thr',
    value: '0.50,0.52,0.54',
    allowed_hours: '13,14,15',
    sharpe: 1.85,
    cum_return: 0.7234,
    trades: 42,
    parity: 'met',
    tag: 'demo',
    created_at: '2025-08-16T13:15:00Z',
    model_id: 'spy_opt_0dte_hourly'
  },
  {
    id: 5,
    kind: 'top_pct',
    value: '0.15',
    allowed_hours: '14,15',
    sharpe: 0.95,
    cum_return: 0.6123,
    trades: 8,
    parity: null,
    tag: 'live',
    created_at: '2025-08-16T12:45:00Z',
    model_id: 'spy_opt_0dte_hourly'
  }
];

// Build/Train/Backtest page specific mock data
export const BUILD_TRAIN_BACKTEST_MODELS = [
  'spy_opt_0dte_hourly',
  'spy_eq_swing_daily', 
  'aapl_eq_intraday_hourly',
  'tsla_opt_0dte_5min',
  'qqq_eq_long_weekly',
  'nvda_opt_swing_daily'
];

export const BUILD_DEFAULTS = {
  model: 'spy_opt_0dte_hourly',
  start_date: '2024-01-01',
  end_date: '2024-12-31',
  features: ['RSI', 'MACD', 'Volume', 'BB', 'ATR'],
  selected_features: ['RSI', 'MACD', 'Volume']
};

export const BUILD_METRICS = {
  features: 24,
  rows: '15.2k',
  nan_percent: '0.1%',
  size: '2.3MB'
};

export const BUILD_CONSOLE_LOG = [
  { timestamp: '2025-01-15 10:30:45', message: 'Starting build process...', type: 'info' },
  { timestamp: '2025-01-15 10:30:46', message: 'Data loaded successfully', type: 'success' },
  { timestamp: '2025-01-15 10:30:47', message: 'Computing features...', type: 'info' },
  { timestamp: '2025-01-15 10:30:52', message: 'Build completed', type: 'success' }
];

export const TRAIN_DEFAULTS = {
  model_type: 'Gradient Boosting',
  allowed_hours: '13, 14, 15',
  split_ratio: 0.8,
  random_seed: 42,
  model_types: ['Gradient Boosting', 'Random Forest', 'Neural Network']
};

export const TRAIN_METRICS = {
  accuracy: '87.3%',
  f1_score: '0.84',
  precision: '0.91',
  duration: '12m',
  progress: 65
};

export const BACKTEST_DEFAULTS = {
  mode: 'Thresholds',
  thresholds: '0.55, 0.60, 0.65',
  splits: 5,
  size_by_confidence: 'No',
  modes: ['Thresholds', 'Top %']
};

export const BACKTEST_METRICS = {
  sharpe: 2.41,
  return: '24.5%',
  trades: 142,
  win_rate: '62%'
};

export const RECENT_RUNS_BTB = [
  {
    id: 1,
    model_id: 'spy_opt_0dte_hourly',
    type: 'Backtest',
    status: 'Completed',
    metrics: {
      sharpe: 2.41,
      return: '24.5%',
      trades: 142
    },
    started_at: '2025-08-16T11:48:00Z',
    completed_at: '2025-08-16T11:50:00Z'
  },
  {
    id: 2,
    model_id: 'spy_eq_swing_daily',
    type: 'Training',
    status: 'Running',
    progress: 45,
    started_at: '2025-08-16T11:45:00Z',
    estimated_completion: '2025-08-16T12:00:00Z'
  },
  {
    id: 3,
    model_id: 'aapl_eq_intraday_hourly',
    type: 'Build',
    status: 'Completed',
    metrics: {
      features: 24,
      rows: '15.2k',
      nan_percent: '0.1%'
    },
    started_at: '2025-08-16T11:40:00Z',
    completed_at: '2025-08-16T11:42:00Z'
  },
  {
    id: 4,
    model_id: 'tsla_opt_0dte_5min',
    type: 'Training',
    status: 'Completed',
    metrics: {
      accuracy: '89.2%',
      f1_score: '0.87',
      duration: '8m'
    },
    started_at: '2025-08-16T11:30:00Z',
    completed_at: '2025-08-16T11:38:00Z'
  }
];

