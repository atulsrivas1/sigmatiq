(function(){
  // services/api.js (stubs)
  var API_BASE = (window.EDGE_API_BASE || 'http://localhost:8001');
  async function request(path, opts){
    opts = opts || {}; var method = opts.method || 'GET';
    var headers = Object.assign({'Content-Type':'application/json'}, opts.headers||{});
    var body = opts.body ? JSON.stringify(opts.body) : undefined;
    var res;
    try { res = await fetch(API_BASE + path, { method, headers, body }); } catch(e){ throw new Error('Network error'); }
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return res.json();
  }
  function stub(delay, data){ return new Promise(r=>setTimeout(()=>r(data), delay)); }
  var api = {
    request,
    getModels: () => stub(200, { ok:true, rows:[{ model_id:'spy_opt_0dte_hourly', pack_id:'zerosigma', updated_at:'2025-08-16T11:50:00Z' }] }),
    getLeaderboard: () => stub(200, { ok:true, rows:[{ model_id:'spy_opt_0dte_hourly', best_sharpe:2.41, best_cum_ret:0.38, started_at:'2025-08-16T11:50:00Z' }] }),
    getHealthz: () => stub(150, { ok:true, checks:{ api:'ok', polygon:'ok' } }),
  };

  // ---- Mock data (UI-first, no API wiring) ----
  var MODELS = [
    { model_id: 'spy_opt_0dte_hourly', pack_id: 'zerosigma', updated_at: '2025-08-16T09:50:00Z', sharpe: 2.41, return: '24.5%', trades: 142, ticker: 'SPY', current_price: 447.82, price_change: 1.25, price_change_pct: 0.28, trust: {integrity: 'ok', parity: 'ok', capacity: 'warn'}, lineage: {pack_sha: 'abc123ef', config_sha: 'def456gh', policy_sha: 'ghi789ij'} },
    { model_id: 'spy_eq_swing_daily', pack_id: 'swingsigma', updated_at: '2025-08-15T16:10:00Z', sharpe: 1.85, return: '18.2%', trades: 89, ticker: 'SPY', current_price: 447.82, price_change: 1.25, price_change_pct: 0.28, trust: {integrity: 'ok', parity: 'warn', capacity: 'ok'}, lineage: {pack_sha: 'bcd234fg', config_sha: 'efg567hi', policy_sha: 'hij890jk'} },
    { model_id: 'aapl_eq_intraday_hourly', pack_id: 'swingsigma', updated_at: '2025-08-14T10:20:00Z', sharpe: 1.92, return: '15.7%', trades: 203, ticker: 'AAPL', current_price: 224.31, price_change: -2.18, price_change_pct: -0.96, trust: {integrity: 'ok', parity: 'ok', capacity: 'ok'}, lineage: {pack_sha: 'cde345gh', config_sha: 'fgh678ij', policy_sha: 'ijk901kl'} },
    { model_id: 'tsla_opt_0dte_5min', pack_id: 'zerosigma', updated_at: '2025-08-13T14:30:00Z', sharpe: 2.15, return: '31.2%', trades: 276, ticker: 'TSLA', current_price: 358.64, price_change: 4.91, price_change_pct: 1.39, trust: {integrity: 'warn', parity: 'ok', capacity: 'error'}, lineage: {pack_sha: 'def456hi', config_sha: 'ghi789jk', policy_sha: 'jkl012lm'} },
    { model_id: 'qqq_eq_long_weekly', pack_id: 'swingsigma', updated_at: '2025-08-11T08:15:00Z', sharpe: 1.56, return: '12.8%', trades: 42, ticker: 'QQQ', current_price: 481.27, price_change: 0.93, price_change_pct: 0.19, trust: {integrity: 'ok', parity: 'ok', capacity: 'ok'}, lineage: {pack_sha: 'efg567ij', config_sha: 'hij890kl', policy_sha: 'klm123mn'} },
    { model_id: 'nvda_opt_swing_daily', pack_id: 'zerosigma', updated_at: '2025-08-09T12:45:00Z', sharpe: 1.73, return: '19.4%', trades: 67, ticker: 'NVDA', current_price: 134.85, price_change: -1.42, price_change_pct: -1.04, trust: {integrity: 'error', parity: 'warn', capacity: 'warn'}, lineage: {pack_sha: 'fgh678jk', config_sha: 'ijk901lm', policy_sha: 'lmn234no'} }
  ];

  var SIGNALS = [
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

  var OVERLAY_SAMPLE = {
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

  var RECENT_MODELS = [
    { model_id: 'spy_opt_0dte_hourly', algorithm: 'KNN', status: 'training', updated_at: '2025-08-16T11:50:00Z', dataset: 'SPXL,30 (May 2022 - Nov 2024)', signal: 'R/R 3.00, SL 0.5%, TP 1.5%', inputs: ['A: C[5]', 'B: C[20]', 'D: C[40]', 'E: H-L'], runtime: '00:09', ticker: 'SPY', current_price: 447.82, price_change: 1.25, price_change_pct: 0.28 },
    { model_id: 'spy_eq_swing_daily', algorithm: 'GBM', status: 'completed', updated_at: '2025-08-16T10:50:00Z', dataset: 'SPY,D (Jan 2020 - Nov 2024)', signal: 'R/R 2.50, SL 1.0%, TP 2.5%', inputs: ['RSI(14)', 'EMA(20)', 'Vol/MA', 'ADX'], runtime: null, ticker: 'SPY', current_price: 447.82, price_change: 1.25, price_change_pct: 0.28 },
    { model_id: 'aapl_eq_intraday_h', algorithm: 'RF', status: 'completed', updated_at: '2025-08-16T08:50:00Z', dataset: 'AAPL,60 (Jun 2023 - Nov 2024)', signal: 'R/R 2.00, SL 0.75%, TP 1.5%', inputs: ['MACD', 'BB', 'OBV', 'ATR'], runtime: null, ticker: 'AAPL', current_price: 224.31, price_change: -2.18, price_change_pct: -0.96 },
    { model_id: 'tsla_opt_0dte_5m', algorithm: 'SVM', status: 'queued', updated_at: '2025-08-16T06:50:00Z', dataset: 'TSLA,5 (Oct - Nov 2024)', signal: 'R/R 4.00, SL 0.25%, TP 1.0%', inputs: ['Mom(5)', 'Vol', 'Alpha', 'Flow'], runtime: null, ticker: 'TSLA', current_price: 358.64, price_change: 4.91, price_change_pct: 1.39 }
  ];

  var RECENT_RUNS = [
    { id: 1, type: 'backtest', model_id: 'spy_opt_0dte_hourly', started_at: '2025-08-16T11:48:00Z', status: 'completed', metrics: { sharpe: 2.41, return: 24.5, trades: 142 } },
    { id: 2, type: 'train', model_id: 'spy_eq_swing_daily', started_at: '2025-08-16T10:48:00Z', status: 'completed', metrics: { accuracy: 87.3, f1_score: 0.84, time_minutes: 12 } },
    { id: 3, type: 'build', model_id: 'aapl_eq_intraday_hourly', started_at: '2025-08-16T08:48:00Z', status: 'completed', metrics: { features: 24, rows: '15.2k', nan_percent: 0.1 } },
    { id: 4, type: 'sweep', model_id: 'tsla_opt_0dte_5min', started_at: '2025-08-16T11:45:00Z', status: 'running', metrics: { progress: 45, combos_completed: 18, combos_total: 40, eta_minutes: 5 } }
  ];

  var SYSTEM_HEALTH = {
    api: { status: 'ok', message: 'OK' },
    database: { status: 'warning', message: 'WARN' },
    data_coverage: { status: 'ok', message: '98%' }
  };

  var SWEEP_MODELS_LIST = [
    'spy_opt_0dte_hourly',
    'spy_eq_swing_daily', 
    'aapl_eq_intraday_hourly',
    'tsla_opt_0dte_5min',
    'qqq_eq_long_weekly',
    'nvda_opt_swing_daily'
  ];

  var SWEEP_CONFIGURATION_DEFAULTS = {
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
      '0.10,0.15',
      '0.12,0.18'
    ],
    guards: {
      min_trades: 5,
      min_sharpe: 0.50,
      tag: 'live'
    }
  };

  var SWEEP_RESULTS_DETAILED = [
    { id: 1, kind: 'threshold', value: '0.50', allowed_hours: '14,15', sharpe: 0.95, cum_return: 0.6123, trades: 8, parity: null, tag: 'live', created_at: '2025-08-16T12:45:00Z' },
    { id: 2, kind: 'threshold', value: '0.52', allowed_hours: '14,15', sharpe: 1.12, cum_return: 0.7834, trades: 12, parity: null, tag: 'live', created_at: '2025-08-16T12:45:00Z' },
    { id: 3, kind: 'top_pct', value: '0.10', allowed_hours: '13,14', sharpe: 1.45, cum_return: 0.8234, trades: 15, parity: null, tag: 'live', created_at: '2025-08-16T12:45:00Z' },
    { id: 4, kind: 'top_pct', value: '0.12', allowed_hours: '13,14,15', sharpe: 1.78, cum_return: 0.9456, trades: 18, parity: null, tag: 'live', created_at: '2025-08-16T12:45:00Z' },
    { id: 5, kind: 'top_pct', value: '0.15', allowed_hours: '14,15', sharpe: 0.95, cum_return: 0.6123, trades: 8, parity: null, tag: 'live', created_at: '2025-08-16T12:45:00Z' }
  ];

  // ---- Helper Functions ----
  function formatCurrency(value) {
    return '$' + parseFloat(value).toFixed(2);
  }

  function formatPercent(value) {
    return (parseFloat(value) * 100).toFixed(1) + '%';
  }

  function getStatusBadge(status) {
    var statusClass = status === 'filled' ? 'status-success' : 
                     status === 'pending' ? 'status-warning' : 'status-error';
    return '<span class="status-badge ' + statusClass + '">' + status + '</span>';
  }

  function getSideBadge(side) {
    var sideClass = side.toLowerCase() === 'long' ? 'side-long' : 'side-short';
    return '<span class="side-badge ' + sideClass + '">' + side + '</span>';
  }

  function getOptionTypeBadge(type) {
    var typeClass = type.toLowerCase() === 'call' ? 'option-call' : 'option-put';
    return '<span class="option-type-badge ' + typeClass + '">' + type + '</span>';
  }

  function formatPrice(price) {
    return price ? formatCurrency(price) : '-';
  }

  function formatRiskReward(rr) {
    return rr ? parseFloat(rr).toFixed(2) + ':1' : '-';
  }

  // ---- View Functions ----
  function viewSignals() {
    var container = document.createElement('div');
    container.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>' +
            '</svg>' +
          '</span>' +
          'Live Signals' +
        '</h1>' +
        '<p class="page-description">Latest trading signals with bracket details</p>' +
        '<div class="page-actions">' +
          '<button class="btn btn-secondary" id="export-signals-csv">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>' +
                '<polyline points="7,10 12,15 17,10"/>' +
                '<line x1="12" y1="15" x2="12" y2="3"/>' +
              '</svg>' +
            '</span>' +
            'Export CSV' +
          '</button>' +
        '</div>' +
      '</div>' +
      '<div class="filters-bar">' +
        '<div class="filter-group">' +
          '<label class="filter-label">Model</label>' +
          '<select class="filter-select" id="signals-model">' +
            '<option value="">All Models</option>' +
          '</select>' +
        '</div>' +
        '<div class="filter-group">' +
          '<label class="filter-label">Date</label>' +
          '<input type="date" class="filter-input" id="signals-date" />' +
        '</div>' +
        '<div class="filter-group">' +
          '<label class="filter-label">Ticker</label>' +
          '<input type="text" class="filter-input" id="signals-ticker" placeholder="Filter by ticker..." />' +
        '</div>' +
        '<div class="filter-group">' +
          '<label class="filter-label">Entry Mode</label>' +
          '<select class="filter-select" id="signals-entry-mode">' +
            '<option value="">All</option>' +
            '<option value="market">Market</option>' +
            '<option value="limit">Limit</option>' +
            '<option value="stop">Stop</option>' +
          '</select>' +
        '</div>' +
      '</div>' +
      '<div class="results-section">' +
        '<div class="results-header">' +
          '<h2 class="results-title">' +
            '<span class="results-title-icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>' +
                '<line x1="16" y1="2" x2="16" y2="6"/>' +
                '<line x1="8" y1="2" x2="8" y2="6"/>' +
                '<line x1="3" y1="10" x2="21" y2="10"/>' +
              '</svg>' +
            '</span>' +
            'Signals (<span id="signals-count">0</span>)' +
          '</h2>' +
        '</div>' +
        '<table class="results-table" id="signals-table">' +
          '<thead>' +
            '<tr>' +
              '<th>Date/Time</th>' +
              '<th>Model</th>' +
              '<th>Ticker</th>' +
              '<th>Side</th>' +
              '<th>Entry Mode</th>' +
              '<th class="cell-right">Entry Price</th>' +
              '<th class="cell-right">Stop</th>' +
              '<th class="cell-right">Target</th>' +
              '<th class="cell-right">R:R</th>' +
              '<th>Status</th>' +
            '</tr>' +
          '</thead>' +
          '<tbody id="signals-tbody">' +
          '</tbody>' +
        '</table>' +
        '<div class="empty-state" id="signals-empty-state" style="display: none;">' +
          '<h3>No signals found</h3>' +
          '<p>No signals match your current filters. Try adjusting the date range or model selection.</p>' +
          '<button class="btn btn-secondary" id="clear-filters-btn">Clear Filters</button>' +
        '</div>' +
      '</div>';

    var modelSelect = container.querySelector('#signals-model');
    var dateInput = container.querySelector('#signals-date');
    var tickerInput = container.querySelector('#signals-ticker');
    var entryModeSelect = container.querySelector('#signals-entry-mode');
    var tbody = container.querySelector('#signals-tbody');
    var emptyState = container.querySelector('#signals-empty-state');
    var table = container.querySelector('#signals-table');
    var signalsCount = container.querySelector('#signals-count');

    var uniqueModels = [...new Set(MODELS.map(function(m) { return m.model_id; }))];
    modelSelect.innerHTML += uniqueModels.map(function(model) {
      return '<option value="' + model + '">' + model + '</option>';
    }).join('');

    function renderSignals(signals) {
      if (signals.length === 0) {
        table.style.display = 'none';
        emptyState.style.display = 'block';
        signalsCount.textContent = '0';
        return;
      }

      table.style.display = 'table';
      emptyState.style.display = 'none';
      signalsCount.textContent = signals.length;

      tbody.innerHTML = signals.map(function(signal) {
        return '<tr class="signal-row">' +
          '<td>' + signal.date + ' ' + (signal.time || '09:30') + '</td>' +
          '<td>' +
            '<span class="pack-badge ' + (signal.pack_id || 'zerosigma') + '">' + (signal.pack_id || 'zerosigma') + '</span>' +
            '<div class="signal-model">' + signal.model_id + '</div>' +
          '</td>' +
          '<td><span class="ticker-symbol">' + signal.ticker + '</span></td>' +
          '<td>' + getSideBadge(signal.side) + '</td>' +
          '<td><span class="entry-mode-badge">' + (signal.entry_mode || 'market') + '</span></td>' +
          '<td class="cell-right">' + formatPrice(signal.entry_ref_px) + '</td>' +
          '<td class="cell-right">' + formatPrice(signal.stop_px) + '</td>' +
          '<td class="cell-right">' + formatPrice(signal.target_px) + '</td>' +
          '<td class="cell-right">' + formatRiskReward(signal.rr) + '</td>' +
          '<td>' + getStatusBadge(signal.status || 'pending') + '</td>' +
        '</tr>';
      }).join('');
    }

    function applyFilters() {
      var modelFilter = modelSelect.value;
      var dateFilter = dateInput.value;
      var tickerFilter = tickerInput.value.toUpperCase();
      var entryModeFilter = entryModeSelect.value;

      var filtered = SIGNALS.filter(function(signal) {
        return (!modelFilter || signal.model_id === modelFilter) &&
               (!dateFilter || signal.date === dateFilter) &&
               (!tickerFilter || signal.ticker.includes(tickerFilter)) &&
               (!entryModeFilter || (signal.entry_mode || 'market') === entryModeFilter);
      });

      renderSignals(filtered);
    }

    function clearFilters() {
      modelSelect.value = '';
      dateInput.value = '';
      tickerInput.value = '';
      entryModeSelect.value = '';
      renderSignals(SIGNALS);
    }

    modelSelect.addEventListener('change', applyFilters);
    dateInput.addEventListener('change', applyFilters);
    tickerInput.addEventListener('input', applyFilters);
    entryModeSelect.addEventListener('change', applyFilters);
    
    container.querySelector('#clear-filters-btn').addEventListener('click', clearFilters);
    
    container.querySelector('#export-signals-csv').addEventListener('click', function() {
      alert('CSV export functionality will be implemented when connected to APIs');
    });

    renderSignals(SIGNALS);
    
    return container;
  }

  function viewOverlay() {
    var container = document.createElement('div');
    container.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="12" cy="12" r="10"/>' +
              '<line x1="2" y1="12" x2="6" y2="12"/>' +
              '<line x1="18" y1="12" x2="22" y2="12"/>' +
              '<line x1="12" y1="6" x2="12" y2="2"/>' +
              '<line x1="12" y1="18" x2="12" y2="22"/>' +
            '</svg>' +
          '</span>' +
          'Options Overlay' +
        '</h1>' +
        '<p class="page-description">Transform stock signals into options strategies with parity analysis</p>' +
      '</div>' +
      '<div class="card">' +
        '<h3 class="card-title">' +
          '<span class="card-title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
              '<circle cx="12" cy="12" r="3"/>' +
              '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>' +
            '</svg>' +
          '</span>' +
          'Overlay Configuration' +
        '</h3>' +
        '<div class="form-grid">' +
          '<div class="form-group">' +
            '<label class="form-label">Source Model *</label>' +
            '<select class="form-input" id="overlay-model" required>' +
              '<option value="">Select model...</option>' +
            '</select>' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Signal Date *</label>' +
            '<input type="date" class="form-input" id="overlay-date" required />' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Strategy Mode</label>' +
            '<select class="form-input" id="overlay-mode">' +
              '<option value="single">Single Leg</option>' +
              '<option value="vertical">Vertical Spread</option>' +
            '</select>' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Expiry</label>' +
            '<select class="form-input" id="overlay-expiry">' +
              '<option value="">Select expiry...</option>' +
              '<option value="2025-08-22">2025-08-22 (5 DTE)</option>' +
              '<option value="2025-08-29">2025-08-29 (12 DTE)</option>' +
              '<option value="2025-09-19">2025-09-19 (33 DTE)</option>' +
            '</select>' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Target Delta</label>' +
            '<input type="number" class="form-input" id="overlay-delta" value="0.30" min="0.05" max="0.95" step="0.05" />' +
          '</div>' +
          '<div class="form-group">' +
            '<label class="form-label">Min Open Interest</label>' +
            '<input type="number" class="form-input" id="overlay-min-oi" value="100" min="1" />' +
          '</div>' +
        '</div>' +
        '<div class="form-actions">' +
          '<button class="btn btn-primary" id="run-overlay">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<polygon points="5,3 19,12 5,21"/>' +
              '</svg>' +
            '</span>' +
            'Generate Overlay' +
          '</button>' +
          '<button class="btn btn-secondary" id="reset-overlay">Reset</button>' +
        '</div>' +
      '</div>' +
      '<div class="results-section" id="overlay-results-section" style="display: none;">' +
        '<div class="results-header">' +
          '<h2 class="results-title">' +
            '<span class="results-title-icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>' +
              '</svg>' +
            '</span>' +
            'Overlay Results' +
          '</h2>' +
          '<div class="results-actions">' +
            '<button class="btn btn-secondary" id="export-overlay-csv">' +
              '<span class="icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                  '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>' +
                  '<polyline points="7,10 12,15 17,10"/>' +
                  '<line x1="12" y1="15" x2="12" y2="3"/>' +
                '</svg>' +
              '</span>' +
              'Export CSV' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<div class="card">' +
          '<h3 class="card-title">' +
            '<span class="card-title-icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<path d="M9 12l2 2 4-4"/>' +
                '<circle cx="12" cy="12" r="10"/>' +
              '</svg>' +
            '</span>' +
            'Parity Summary' +
          '</h3>' +
          '<div class="parity-summary" id="parity-summary">' +
            '<div class="parity-metric">' +
              '<div class="parity-value" id="overlay-count">0</div>' +
              '<div class="parity-label">Options Found</div>' +
            '</div>' +
            '<div class="parity-metric">' +
              '<div class="parity-value" id="avg-premium">$0.00</div>' +
              '<div class="parity-label">Avg Premium</div>' +
            '</div>' +
            '<div class="parity-metric">' +
              '<div class="parity-value" id="coverage-rate">0%</div>' +
              '<div class="parity-label">Coverage Rate</div>' +
            '</div>' +
            '<div class="parity-metric">' +
              '<div class="parity-value" id="avg-oi">0</div>' +
              '<div class="parity-label">Avg OI</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<table class="results-table" id="overlay-table">' +
          '<thead>' +
            '<tr>' +
              '<th>Ticker</th>' +
              '<th>Strike</th>' +
              '<th>Type</th>' +
              '<th>Expiry</th>' +
              '<th class="cell-right">Delta</th>' +
              '<th class="cell-right">IV</th>' +
              '<th class="cell-right">Bid</th>' +
              '<th class="cell-right">Ask</th>' +
              '<th class="cell-right">Volume</th>' +
              '<th class="cell-right">OI</th>' +
              '<th>OCC Symbol</th>' +
            '</tr>' +
          '</thead>' +
          '<tbody id="overlay-tbody">' +
          '</tbody>' +
        '</table>' +
      '</div>';

    var modelSelect = container.querySelector('#overlay-model');
    var dateInput = container.querySelector('#overlay-date');
    var modeSelect = container.querySelector('#overlay-mode');
    var expirySelect = container.querySelector('#overlay-expiry');
    var deltaInput = container.querySelector('#overlay-delta');
    var minOiInput = container.querySelector('#overlay-min-oi');
    
    var runBtn = container.querySelector('#run-overlay');
    var resetBtn = container.querySelector('#reset-overlay');
    var resultsSection = container.querySelector('#overlay-results-section');
    var tbody = container.querySelector('#overlay-tbody');
    
    var overlayCount = container.querySelector('#overlay-count');
    var avgPremium = container.querySelector('#avg-premium');
    var coverageRate = container.querySelector('#coverage-rate');
    var avgOi = container.querySelector('#avg-oi');

    modelSelect.innerHTML += MODELS.map(function(model) {
      return '<option value="' + model.model_id + '">' + model.model_id + '</option>';
    }).join('');

    function validateForm() {
      var model = modelSelect.value;
      var date = dateInput.value;
      
      if (!model || !date) {
        alert('Please select a model and date before generating overlay');
        return false;
      }
      return true;
    }

    function renderResults() {
      if (!validateForm()) return;

      resultsSection.style.display = 'block';

      overlayCount.textContent = OVERLAY_SAMPLE.count;
      avgPremium.textContent = '$2.45';
      coverageRate.textContent = '87%';
      avgOi.textContent = '1,247';

      var rows = OVERLAY_SAMPLE.rows.map(function(option) {
        return '<tr>' +
          '<td><span class="ticker-symbol">' + option.ticker + '</span></td>' +
          '<td><span class="strike-price">$' + option.strike + '</span></td>' +
          '<td>' + getOptionTypeBadge(option.type) + '</td>' +
          '<td>' + option.expiry + '</td>' +
          '<td class="cell-right">' + option.delta + '</td>' +
          '<td class="cell-right">' + formatPercent(option.iv_used) + '</td>' +
          '<td class="cell-right">' + formatCurrency(option.bid || '2.10') + '</td>' +
          '<td class="cell-right">' + formatCurrency(option.ask || '2.15') + '</td>' +
          '<td class="cell-right">' + (option.volume || '147') + '</td>' +
          '<td class="cell-right">' + (option.open_interest || '1,247') + '</td>' +
          '<td><code class="occ-symbol">' + option.occ + '</code></td>' +
        '</tr>';
      }).join('');

      tbody.innerHTML = rows;
      resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function resetForm() {
      modelSelect.value = '';
      dateInput.value = '';
      modeSelect.value = 'single';
      expirySelect.value = '';
      deltaInput.value = '0.30';
      minOiInput.value = '100';
      resultsSection.style.display = 'none';
    }

    runBtn.addEventListener('click', renderResults);
    resetBtn.addEventListener('click', resetForm);
    
    container.querySelector('#export-overlay-csv').addEventListener('click', function() {
      alert('CSV export functionality will be implemented when connected to APIs');
    });

    dateInput.value = new Date().toISOString().split('T')[0];

    return container;
  }

  // ---- Complete View Functions ----
  function viewDashboard() {
    var wrap = document.createElement('div');
    wrap.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<rect x="3" y="3" width="18" height="18" rx="2"/>' +
              '<line x1="12" y1="3" x2="12" y2="21"/>' +
              '<line x1="3" y1="12" x2="21" y2="12"/>' +
            '</svg>' +
          '</span>' +
          'Dashboard' +
        '</h1>' +
        '<div class="header-actions">' +
          '<button class="btn btn-primary" id="create-model-header-btn">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                '<line x1="12" y1="5" x2="12" y2="19"/>' +
                '<line x1="5" y1="12" x2="19" y2="12"/>' +
              '</svg>' +
            '</span>' +
            'Create Model' +
          '</button>' +
          '<a class="btn btn-secondary" href="#/sweeps">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                '<polygon points="5,3 19,12 5,21"/>' +
              '</svg>' +
            '</span>' +
            'Run Sweeps' +
          '</a>' +
        '</div>' +
      '</div>' +
      '<div class="dashboard-grid">' +
        // Recent Models Section
        '<div class="dashboard-section">' +
          '<div class="section-header">' +
            '<h3 class="section-title">' +
              '<span class="section-title-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<circle cx="12" cy="12" r="2"/>' +
                  '<circle cx="5" cy="5" r="2"/>' +
                  '<circle cx="19" cy="5" r="2"/>' +
                  '<circle cx="5" cy="19" r="2"/>' +
                  '<circle cx="19" cy="19" r="2"/>' +
                  '<path d="M7 6l3 3"/>' +
                  '<path d="M14 9l3-3"/>' +
                  '<path d="M7 18l3-3"/>' +
                  '<path d="M14 15l3 3"/>' +
                  '<path d="M10 10l4 4"/>' +
                  '<path d="M10 14l4-4"/>' +
                '</svg>' +
              '</span>' +
              'Recent Models' +
            '</h3>' +
            '<a href="#/models" class="section-link">' +
              '<span class="icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>' +
                  '<polyline points="15,3 21,3 21,9"/>' +
                  '<line x1="10" y1="14" x2="21" y2="3"/>' +
                '</svg>' +
              '</span>' +
              'View All' +
            '</a>' +
          '</div>' +
          '<div class="recent-models-list" id="recent-models"></div>' +
        '</div>' +
        // Last Runs Section
        '<div class="dashboard-section">' +
          '<div class="section-header">' +
            '<h3 class="section-title">' +
              '<span class="section-title-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<circle cx="12" cy="12" r="10"/>' +
                  '<polyline points="12,6 12,12 16,14"/>' +
                '</svg>' +
              '</span>' +
              'Last Runs' +
            '</h3>' +
            '<a href="#/runs" class="section-link">' +
              '<span class="icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>' +
                  '<polyline points="15,3 21,3 21,9"/>' +
                  '<line x1="10" y1="14" x2="21" y2="3"/>' +
                '</svg>' +
              '</span>' +
              'View All' +
            '</a>' +
          '</div>' +
          '<div class="recent-runs-list" id="recent-runs"></div>' +
        '</div>' +
        // Quick Actions Section
        '<div class="dashboard-section">' +
          '<div class="section-header">' +
            '<h3 class="section-title">' +
              '<span class="section-title-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<circle cx="12" cy="12" r="3"/>' +
                  '<path d="M12 1v6m0 6v6"/>' +
                  '<path d="m18.5 5.5-4.24 4.24m-4.52 4.52L5.5 18.5"/>' +
                  '<path d="m5.5 5.5 4.24 4.24m4.52 4.52L18.5 18.5"/>' +
                '</svg>' +
              '</span>' +
              'Quick Actions' +
            '</h3>' +
          '</div>' +
          '<div class="quick-actions-grid">' +
            '<button class="quick-action-card" id="create-model-quick-btn">' +
              '<span class="quick-action-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<line x1="12" y1="5" x2="12" y2="19"/>' +
                  '<line x1="5" y1="12" x2="19" y2="12"/>' +
                '</svg>' +
              '</span>' +
              '<span class="quick-action-label">Create Model</span>' +
            '</button>' +
            '<a href="#/runs" class="quick-action-card">' +
              '<span class="quick-action-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<polygon points="5,3 19,12 5,21"/>' +
                '</svg>' +
              '</span>' +
              '<span class="quick-action-label">Run Backtest</span>' +
            '</a>' +
            '<a href="#/sweeps" class="quick-action-card">' +
              '<span class="quick-action-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<polygon points="5,3 19,12 5,21"/>' +
                '</svg>' +
              '</span>' +
              '<span class="quick-action-label">Run Sweeps</span>' +
            '</a>' +
            '<a href="#/signals" class="quick-action-card">' +
              '<span class="quick-action-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>' +
                  '<circle cx="12" cy="12" r="3"/>' +
                '</svg>' +
              '</span>' +
              '<span class="quick-action-label">View Signals</span>' +
            '</a>' +
          '</div>' +
        '</div>' +
        // System Health Section
        '<div class="dashboard-section">' +
          '<div class="section-header">' +
            '<h3 class="section-title">' +
              '<span class="section-title-icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>' +
                '</svg>' +
              '</span>' +
              'System Health' +
            '</h3>' +
            '<a href="#/health" class="section-link">' +
              '<span class="icon">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                  '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>' +
                  '<polyline points="15,3 21,3 21,9"/>' +
                  '<line x1="10" y1="14" x2="21" y2="3"/>' +
                '</svg>' +
              '</span>' +
              'View Details' +
            '</a>' +
          '</div>' +
          '<div class="system-health-grid" id="system-health"></div>' +
        '</div>' +
      '</div>';

    // Helper functions
    function getAlgorithmBadge(algo) {
      var badgeClass = algo === 'KNN' ? 'badge-purple' : 
                      algo === 'GBM' ? 'badge-green' :
                      algo === 'RF' ? 'badge-blue' :
                      algo === 'SVM' ? 'badge-orange' : 'badge-gray';
      return '<span class="algorithm-badge ' + badgeClass + '">' + algo + '</span>';
    }

    function getStatusBadge(status) {
      var statusClass = status === 'completed' ? 'status-success' : 
                       status === 'training' || status === 'running' ? 'status-warning' : 
                       status === 'queued' ? 'status-info' : 'status-default';
      return '<span class="status-badge ' + statusClass + '">' + status + '</span>';
    }

    function getRunTypeBadge(type) {
      var typeColors = {
        backtest: 'type-backtest',
        train: 'type-train', 
        build: 'type-build',
        sweep: 'type-sweep'
      };
      return '<span class="run-type-badge ' + (typeColors[type] || 'type-default') + '">' + type + '</span>';
    }

    function getHealthStatusClass(status) {
      return status === 'ok' ? 'status-success' :
             status === 'warning' ? 'status-warning' : 'status-error';
    }

    function getRunMetricsHtml(run) {
      var metrics = run.metrics;
      
      switch (run.type) {
        case 'backtest':
          return '<div class="metric-item">' +
            '<span class="metric-label">Sharpe:</span>' +
            '<span class="metric-value">' + metrics.sharpe + '</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">Return:</span>' +
            '<span class="metric-value">' + metrics.return + '%</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">Trades:</span>' +
            '<span class="metric-value">' + metrics.trades + '</span>' +
          '</div>';
        case 'train':
          return '<div class="metric-item">' +
            '<span class="metric-label">Accuracy:</span>' +
            '<span class="metric-value">' + metrics.accuracy + '%</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">F1:</span>' +
            '<span class="metric-value">' + metrics.f1_score + '</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">Time:</span>' +
            '<span class="metric-value">' + metrics.time_minutes + 'm</span>' +
          '</div>';
        case 'build':
          return '<div class="metric-item">' +
            '<span class="metric-label">Features:</span>' +
            '<span class="metric-value">' + metrics.features + '</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">Rows:</span>' +
            '<span class="metric-value">' + metrics.rows + '</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">NaN:</span>' +
            '<span class="metric-value">' + metrics.nan_percent + '%</span>' +
          '</div>';
        case 'sweep':
          return '<div class="metric-item">' +
            '<span class="metric-label">Progress:</span>' +
            '<span class="metric-value">' + metrics.progress + '%</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">Combos:</span>' +
            '<span class="metric-value">' + metrics.combos_completed + '/' + metrics.combos_total + '</span>' +
          '</div>' +
          '<div class="metric-item">' +
            '<span class="metric-label">ETA:</span>' +
            '<span class="metric-value">' + metrics.eta_minutes + 'm</span>' +
          '</div>';
        default:
          return '';
      }
    }

    function getTimeAgo(dateStr) {
      var date = new Date(dateStr);
      var now = new Date();
      var diffMs = now - date;
      var diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      if (diffHours < 1) return 'Just now';
      if (diffHours < 24) return diffHours + 'h ago';
      var diffDays = Math.floor(diffHours / 24);
      if (diffDays === 1) return '1d ago';
      if (diffDays < 7) return diffDays + 'd ago';
      return '1w ago';
    }

    // Render recent models with proper structure
    var recentModels = wrap.querySelector('#recent-models');
    recentModels.innerHTML = RECENT_MODELS.map(function(model) {
      var algorithmBadge = getAlgorithmBadge(model.algorithm);
      var statusBadge = getStatusBadge(model.status);
      var timeAgo = getTimeAgo(model.updated_at);
      var priceChangeClass = model.price_change > 0 ? 'positive' : model.price_change < 0 ? 'negative' : 'neutral';
      var priceChangeSign = model.price_change > 0 ? '+' : '';
      
      return '<div class="recent-model-item">' +
        '<div class="model-header-compact">' +
          '<div class="model-id-compact">' + model.model_id + '</div>' +
          '<div class="model-badges">' +
            algorithmBadge +
            statusBadge +
          '</div>' +
        '</div>' +
        '<div class="model-details">' +
          '<div class="ticker-price">' +
            '<span class="ticker-symbol">' + model.ticker + '</span>' +
            '<span class="current-price">$' + model.current_price + '</span>' +
            '<span class="price-change ' + priceChangeClass + '">(' + priceChangeSign + model.price_change_pct.toFixed(2) + '%)</span>' +
          '</div>' +
          '<div class="model-dataset">' + model.dataset + '</div>' +
          '<div class="model-signal">' + model.signal + '</div>' +
          '<div class="model-inputs">' + model.inputs.join(', ') + '</div>' +
        '</div>' +
        '<div class="model-footer">' +
          '<span class="model-time">' + timeAgo + '</span>' +
          (model.runtime ? '<span class="model-runtime">' + model.runtime + '</span>' : '') +
        '</div>' +
      '</div>';
    }).join('');

    // Render recent runs with proper structure
    var recentRuns = wrap.querySelector('#recent-runs');
    recentRuns.innerHTML = RECENT_RUNS.map(function(run) {
      var typeBadge = getRunTypeBadge(run.type);
      var statusBadge = getStatusBadge(run.status);
      var timeAgo = getTimeAgo(run.started_at);
      var metricsHtml = getRunMetricsHtml(run);
      
      return '<div class="recent-run-item">' +
        '<div class="run-header-compact">' +
          '<div class="run-model-id">' + run.model_id + '</div>' +
          '<div class="run-badges">' +
            typeBadge +
            statusBadge +
          '</div>' +
        '</div>' +
        '<div class="run-metrics">' +
          metricsHtml +
        '</div>' +
        '<div class="run-footer">' +
          '<span class="run-time">' + timeAgo + '</span>' +
        '</div>' +
      '</div>';
    }).join('');

    // Render system health
    var systemHealthContainer = wrap.querySelector('#system-health');
    var healthItems = ['api', 'database', 'data_coverage'];
    var healthLabels = { api: 'API', database: 'Database', data_coverage: 'Data Coverage' };
    systemHealthContainer.innerHTML = healthItems.map(function(key) {
      var health = SYSTEM_HEALTH[key];
      var statusClass = getHealthStatusClass(health.status);
      var label = healthLabels[key];
      
      return '<div class="health-item">' +
        '<div class="health-label">' + label + '</div>' +
        '<div class="health-status ' + statusClass + '">' + health.message + '</div>' +
      '</div>';
    }).join('');

    // Create Model button event handlers
    function handleCreateModel() {
      // For now, show a simple alert indicating this is a mock
      // In a real implementation, this would navigate to a model creation form
      alert('Model creation form coming soon! This is currently a mock interface.');
    }
    
    wrap.querySelector('#create-model-header-btn').addEventListener('click', handleCreateModel);
    wrap.querySelector('#create-model-quick-btn').addEventListener('click', handleCreateModel);

    return wrap;
  }

  function viewModels() {
    var wrap = document.createElement('div');
    wrap.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="12" cy="12" r="2"/>' +
              '<circle cx="5" cy="5" r="2"/>' +
              '<circle cx="19" cy="5" r="2"/>' +
              '<circle cx="5" cy="19" r="2"/>' +
              '<circle cx="19" cy="19" r="2"/>' +
            '</svg>' +
          '</span>' +
          'Models' +
        '</h1>' +
        '<div class="header-actions">' +
          '<button class="btn btn-primary" id="create-model-btn">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                '<line x1="12" y1="5" x2="12" y2="19"/>' +
                '<line x1="5" y1="12" x2="19" y2="12"/>' +
              '</svg>' +
            '</span>' +
            'Create Model' +
          '</button>' +
        '</div>' +
      '</div>' +
      '<div class="filters-bar">' +
        '<div class="filters-left">' +
          '<div class="search-box">' +
            '<input type="text" class="search-input" id="models-search" placeholder="Search models..." />' +
            '<svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="11" cy="11" r="7"></circle>' +
              '<line x1="16.65" y1="16.65" x2="21" y2="21"></line>' +
            '</svg>' +
          '</div>' +
        '</div>' +
        '<div class="filters-right">' +
          '<div class="filter-chip active" id="filter-all">All</div>' +
          '<div class="filter-chip pack-badge zerosigma" id="filter-zerosigma">ZeroSigma</div>' +
          '<div class="filter-chip pack-badge swingsigma" id="filter-swingsigma">SwingSigma</div>' +
          '<div class="filter-chip pack-badge momentumsigma" id="filter-momentumsigma">MomentumSigma</div>' +
          '<div class="filter-chip pack-badge longsigma" id="filter-longsigma">LongSigma</div>' +
        '</div>' +
      '</div>' +
      '<div class="models-grid" id="models-grid"></div>';
    
    var searchEl = wrap.querySelector('#models-search');
    var modelsGrid = wrap.querySelector('#models-grid');
    var filterChips = wrap.querySelectorAll('.filter-chip');
    var currentFilter = 'all';

    function getTimeAgo(dateStr) {
      var date = new Date(dateStr);
      var now = new Date();
      var diffMs = now - date;
      var diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      var diffDays = Math.floor(diffHours / 24);
      
      if (diffHours < 1) return 'Updated just now';
      if (diffHours < 24) return 'Updated ' + diffHours + ' hour' + (diffHours === 1 ? '' : 's') + ' ago';
      if (diffDays === 1) return 'Updated 1 day ago';
      if (diffDays < 7) return 'Updated ' + diffDays + ' days ago';
      return 'Updated 1 week ago';
    }
    
    function renderModels(list) {
      modelsGrid.innerHTML = list.map(function(model) {
        var timeAgo = getTimeAgo(model.updated_at);
        var priceChangeClass = model.price_change > 0 ? 'positive' : model.price_change < 0 ? 'negative' : 'neutral';
        var priceChangeSign = model.price_change > 0 ? '+' : '';
        
        return '<div class="model-card">' +
          '<div class="model-header">' +
            '<div class="model-id">' + model.model_id + '</div>' +
            '<div class="model-meta">' +
              '<span class="pack-badge ' + model.pack_id + '">' + model.pack_id + '</span>' +
              '<span>' + timeAgo + '</span>' +
              '<div class="ticker-price">' +
                '<span class="ticker-symbol">' + model.ticker + '</span>' +
                '<span class="current-price">$' + model.current_price + '</span>' +
                '<span class="price-change ' + priceChangeClass + '">(' + priceChangeSign + model.price_change_pct.toFixed(2) + '%)</span>' +
              '</div>' +
            '</div>' +
            '<div class="trust-hud">' +
              '<div class="trust-badge integrity ' + (model.trust.integrity || 'ok') + '" title="Data Integrity">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                  '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>' +
                '</svg>' +
              '</div>' +
              '<div class="trust-badge parity ' + (model.trust.parity || 'ok') + '" title="Model Parity">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                  '<path d="M9 12l2 2 4-4"/>' +
                  '<circle cx="12" cy="12" r="10"/>' +
                '</svg>' +
              '</div>' +
              '<div class="trust-badge capacity ' + (model.trust.capacity || 'warn') + '" title="Trade Capacity">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                  '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>' +
                '</svg>' +
              '</div>' +
            '</div>' +
            '<div class="lineage-chips">' +
              '<button class="lineage-chip" title="Pack SHA: ' + (model.lineage.pack_sha || 'abc123ef') + '">' +
                'pack_sha • ' + (model.lineage.pack_sha || 'abc123ef').substring(0, 7) +
              '</button>' +
              '<button class="lineage-chip" title="Config SHA: ' + (model.lineage.config_sha || 'def456gh') + '">' +
                'config_sha • ' + (model.lineage.config_sha || 'def456gh').substring(0, 7) +
              '</button>' +
              '<button class="lineage-chip" title="Policy SHA: ' + (model.lineage.policy_sha || 'ghi789ij') + '">' +
                'policy_sha • ' + (model.lineage.policy_sha || 'ghi789ij').substring(0, 7) +
              '</button>' +
            '</div>' +
          '</div>' +
          '<div class="model-body">' +
            '<div class="model-stats">' +
              '<div class="stat-item">' +
                '<div class="stat-value">' + (model.sharpe || 'N/A') + '</div>' +
                '<div class="stat-label">Sharpe</div>' +
              '</div>' +
              '<div class="stat-item">' +
                '<div class="stat-value">' + (model.return || 'N/A') + '</div>' +
                '<div class="stat-label">Return</div>' +
              '</div>' +
              '<div class="stat-item">' +
                '<div class="stat-value">' + (model.trades || 'N/A') + '</div>' +
                '<div class="stat-label">Trades</div>' +
              '</div>' +
              '<div class="stat-item">' +
                '<div class="stat-label">PnL Trend</div>' +
                '<div class="sparkline">' +
                  '<svg viewBox="0 0 60 20" class="sparkline-svg">' +
                    '<polyline points="2,18 12,14 22,10 32,12 42,8 52,6 58,4" ' +
                              'stroke="var(--status-success)" ' +
                              'stroke-width="1.5" ' +
                              'fill="none"/>' +
                    '<circle cx="58" cy="4" r="1.5" fill="var(--status-success)"/>' +
                  '</svg>' +
                '</div>' +
              '</div>' +
            '</div>' +
            '<div class="model-actions">' +
              '<button class="btn btn-primary">' +
                '<span class="icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>' +
                    '<polyline points="15,3 21,3 21,9"/>' +
                    '<line x1="10" y1="14" x2="21" y2="3"/>' +
                  '</svg>' +
                '</span>' +
                'Open' +
              '</button>' +
              '<button class="btn btn-secondary">' +
                '<span class="icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<polygon points="5,3 19,12 5,21"/>' +
                  '</svg>' +
                '</span>' +
                'Backtest' +
              '</button>' +
              '<button class="btn btn-secondary">' +
                '<span class="icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<polygon points="5,3 19,12 5,21"/>' +
                  '</svg>' +
                '</span>' +
                'Sweeps' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>';
      }).join('');
    }

    function applyFilters() {
      var query = (searchEl.value || '').toLowerCase();
      var filtered = MODELS;

      if (currentFilter !== 'all') {
        filtered = filtered.filter(function(m) { return m.pack_id === currentFilter; });
      }

      if (query) {
        filtered = filtered.filter(function(m) { return m.model_id.toLowerCase().includes(query); });
      }

      renderModels(filtered);
    }

    filterChips.forEach(function(chip) {
      chip.addEventListener('click', function() {
        filterChips.forEach(function(c) { c.classList.remove('active'); });
        chip.classList.add('active');
        currentFilter = chip.id.replace('filter-', '');
        applyFilters();
      });
    });

    searchEl.addEventListener('input', applyFilters);
    
    wrap.querySelector('#create-model-btn').addEventListener('click', function() {
      window.location.hash = '#/models/new';
    });
    
    renderModels(MODELS);
    return wrap;
  }

  function viewLeaderboard() {
    var wrap = document.createElement('div');
    wrap.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<rect x="4" y="11" width="3" height="7" rx="1"/>' +
              '<rect x="10.5" y="7" width="3" height="11" rx="1"/>' +
              '<rect x="17" y="9" width="3" height="9" rx="1"/>' +
            '</svg>' +
          '</span>' +
          'Leaderboard' +
        '</h1>' +
      '</div>' +
      '<table class="leaderboard-table">' +
        '<thead>' +
          '<tr>' +
            '<th>Rank</th>' +
            '<th>Model</th>' +
            '<th>Pack</th>' +
            '<th class="cell-right">Sharpe</th>' +
            '<th class="cell-right">Return</th>' +
            '<th class="cell-right">Trades</th>' +
            '<th>Updated</th>' +
          '</tr>' +
        '</thead>' +
        '<tbody id="leaderboard-tbody">' +
        '</tbody>' +
      '</table>';

    var tbody = wrap.querySelector('#leaderboard-tbody');
    var sortedModels = MODELS.slice().sort(function(a, b) {
      return parseFloat(b.sharpe || 0) - parseFloat(a.sharpe || 0);
    });

    tbody.innerHTML = sortedModels.map(function(model, index) {
      var rankClass = index === 0 ? 'rank-gold' : index === 1 ? 'rank-silver' : index === 2 ? 'rank-bronze' : '';
      return '<tr class="' + rankClass + '">' +
        '<td class="rank">' + (index + 1) + '</td>' +
        '<td>' + model.model_id + '</td>' +
        '<td><span class="pack-badge ' + model.pack_id + '">' + model.pack_id + '</span></td>' +
        '<td class="cell-right metric-positive">' + (model.sharpe || 'N/A') + '</td>' +
        '<td class="cell-right metric-positive">' + (model.return || 'N/A') + '</td>' +
        '<td class="cell-right">' + (model.trades || 'N/A') + '</td>' +
        '<td>' + new Date(model.updated_at).toLocaleDateString() + '</td>' +
      '</tr>';
    }).join('');

    return wrap;
  }

  function viewRuns() {
    var wrap = document.createElement('div');
    wrap.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<polygon points="5,3 19,12 5,21"/>' +
            '</svg>' +
          '</span>' +
          'Build/Train/Backtest' +
        '</h1>' +
        '<p class="page-description">Model pipeline orchestration and execution</p>' +
        '<div class="page-actions">' +
          '<button class="btn btn-secondary" id="queue-status-btn">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<circle cx="12" cy="12" r="10"/>' +
                '<polyline points="12,6 12,12 16,14"/>' +
              '</svg>' +
            '</span>' +
            'Queue Status' +
          '</button>' +
          '<button class="btn btn-secondary" id="run-history-btn">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                '<path d="M3 3v18l18-9-18-9z"/>' +
              '</svg>' +
            '</span>' +
            'Run History' +
          '</button>' +
        '</div>' +
      '</div>' +
      
      '<div class="tab-nav">' +
        '<button class="tab-btn active" data-tab="build">' +
          '<span class="tab-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
              '<path d="M12 2L2 7l10 5 10-5-10-5z"/>' +
              '<path d="M2 17l10 5 10-5"/>' +
              '<path d="M2 12l10 5 10-5"/>' +
            '</svg>' +
          '</span>' +
          'Build' +
        '</button>' +
        '<button class="tab-btn" data-tab="train">' +
          '<span class="tab-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
              '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>' +
              '<polyline points="14,2 14,8 20,8"/>' +
              '<line x1="16" y1="13" x2="8" y2="13"/>' +
              '<line x1="16" y1="17" x2="8" y2="17"/>' +
            '</svg>' +
          '</span>' +
          'Train' +
        '</button>' +
        '<button class="tab-btn" data-tab="backtest">' +
          '<span class="tab-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
              '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>' +
            '</svg>' +
          '</span>' +
          'Backtest' +
        '</button>' +
      '</div>' +
      
      '<div class="tab-content" id="tab-content">' +
        // BUILD TAB
        '<div id="build-tab" class="tab-panel active">' +
          '<div class="pipeline-grid">' +
            '<div class="card">' +
              '<h3 class="card-title">' +
                '<span class="card-title-icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<path d="M12 2L2 7l10 5 10-5-10-5z"/>' +
                  '</svg>' +
                '</span>' +
                'Build Configuration' +
              '</h3>' +
              '<div class="form-grid">' +
                '<div class="form-group">' +
                  '<label class="form-label">Model ID</label>' +
                  '<input type="text" class="form-input" id="build-model-id" placeholder="spy_opt_0dte_hourly_v2" value="spy_opt_0dte_hourly_v2" />' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Pack</label>' +
                  '<select class="form-input" id="build-pack">' +
                    '<option value="zerosigma" selected>ZeroSigma</option>' +
                    '<option value="swingsigma">SwingSigma</option>' +
                    '<option value="longsigma">LongSigma</option>' +
                    '<option value="overnightsigma">OvernightSigma</option>' +
                    '<option value="momentumsigma">MomentumSigma</option>' +
                  '</select>' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Universe</label>' +
                  '<select class="form-input" id="build-universe">' +
                    '<option value="sp500">S&P 500</option>' +
                    '<option value="nasdaq100" selected>NASDAQ 100</option>' +
                    '<option value="russell1000">Russell 1000</option>' +
                    '<option value="custom">Custom List</option>' +
                  '</select>' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Timeframe</label>' +
                  '<select class="form-input" id="build-timeframe">' +
                    '<option value="1m">1 Minute</option>' +
                    '<option value="5m">5 Minutes</option>' +
                    '<option value="1h" selected>1 Hour</option>' +
                    '<option value="1d">1 Day</option>' +
                  '</select>' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Date Range</label>' +
                  '<div class="date-range">' +
                    '<input type="date" class="form-input" id="build-start-date" value="2022-01-01" />' +
                    '<span class="date-separator">to</span>' +
                    '<input type="date" class="form-input" id="build-end-date" value="2024-11-01" />' +
                  '</div>' +
                '</div>' +
                '<div class="form-group span-2">' +
                  '<label class="form-label">Features</label>' +
                  '<div class="feature-tags" id="build-features">' +
                    '<span class="feature-tag active">RSI(14)</span>' +
                    '<span class="feature-tag active">MACD</span>' +
                    '<span class="feature-tag active">BB(20)</span>' +
                    '<span class="feature-tag">ATR</span>' +
                    '<span class="feature-tag">EMA(50)</span>' +
                    '<span class="feature-tag">Volume</span>' +
                    '<span class="feature-tag">IV</span>' +
                    '<span class="feature-tag">Greeks</span>' +
                  '</div>' +
                '</div>' +
              '</div>' +
              '<div class="form-actions">' +
                '<button class="btn btn-secondary" id="validate-build-btn">Validate</button>' +
                '<button class="btn btn-primary" id="start-build-btn">' +
                  '<span class="icon">' +
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                      '<polygon points="5,3 19,12 5,21"/>' +
                    '</svg>' +
                  '</span>' +
                  'Start Build' +
                '</button>' +
              '</div>' +
            '</div>' +
            
            '<div class="card">' +
              '<h3 class="card-title">' +
                '<span class="card-title-icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<circle cx="12" cy="12" r="10"/>' +
                    '<polyline points="12,6 12,12 16,14"/>' +
                  '</svg>' +
                '</span>' +
                'Current Build Progress' +
              '</h3>' +
              '<div class="progress-section" id="build-progress">' +
                '<div class="progress-item">' +
                  '<div class="progress-header">' +
                    '<span class="progress-label">Data Fetching</span>' +
                    '<span class="progress-percentage">100%</span>' +
                  '</div>' +
                  '<div class="progress-bar">' +
                    '<div class="progress-fill" style="width: 100%;"></div>' +
                  '</div>' +
                '</div>' +
                '<div class="progress-item">' +
                  '<div class="progress-header">' +
                    '<span class="progress-label">Feature Engineering</span>' +
                    '<span class="progress-percentage">75%</span>' +
                  '</div>' +
                  '<div class="progress-bar">' +
                    '<div class="progress-fill" style="width: 75%;"></div>' +
                  '</div>' +
                '</div>' +
                '<div class="progress-item">' +
                  '<div class="progress-header">' +
                    '<span class="progress-label">Data Validation</span>' +
                    '<span class="progress-percentage">25%</span>' +
                  '</div>' +
                  '<div class="progress-bar">' +
                    '<div class="progress-fill" style="width: 25%;"></div>' +
                  '</div>' +
                '</div>' +
                '<div class="progress-item">' +
                  '<div class="progress-header">' +
                    '<span class="progress-label">Export Dataset</span>' +
                    '<span class="progress-percentage">0%</span>' +
                  '</div>' +
                  '<div class="progress-bar">' +
                    '<div class="progress-fill" style="width: 0%;"></div>' +
                  '</div>' +
                '</div>' +
              '</div>' +
              '<div class="progress-stats">' +
                '<div class="stat-item">' +
                  '<div class="stat-value">156,432</div>' +
                  '<div class="stat-label">Rows Processed</div>' +
                '</div>' +
                '<div class="stat-item">' +
                  '<div class="stat-value">24</div>' +
                  '<div class="stat-label">Features</div>' +
                '</div>' +
                '<div class="stat-item">' +
                  '<div class="stat-value">2.1%</div>' +
                  '<div class="stat-label">NaN Rate</div>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        
        // TRAIN TAB  
        '<div id="train-tab" class="tab-panel">' +
          '<div class="pipeline-grid">' +
            '<div class="card">' +
              '<h3 class="card-title">' +
                '<span class="card-title-icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>' +
                    '<polyline points="14,2 14,8 20,8"/>' +
                  '</svg>' +
                '</span>' +
                'Training Configuration' +
              '</h3>' +
              '<div class="form-grid">' +
                '<div class="form-group">' +
                  '<label class="form-label">Algorithm</label>' +
                  '<select class="form-input" id="train-algorithm">' +
                    '<option value="gbm" selected>Gradient Boosting</option>' +
                    '<option value="rf">Random Forest</option>' +
                    '<option value="xgb">XGBoost</option>' +
                    '<option value="lgb">LightGBM</option>' +
                    '<option value="svm">SVM</option>' +
                    '<option value="knn">K-Nearest Neighbors</option>' +
                  '</select>' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Cross-Validation</label>' +
                  '<select class="form-input" id="train-cv">' +
                    '<option value="timeseries" selected>Time Series Split</option>' +
                    '<option value="kfold">K-Fold</option>' +
                    '<option value="stratified">Stratified K-Fold</option>' +
                  '</select>' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Test Size</label>' +
                  '<input type="number" class="form-input" id="train-test-size" value="0.2" min="0.1" max="0.5" step="0.05" />' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Max Iterations</label>' +
                  '<input type="number" class="form-input" id="train-max-iter" value="1000" min="100" max="5000" step="100" />' +
                '</div>' +
                '<div class="form-group span-2">' +
                  '<label class="form-label">Hyperparameter Tuning</label>' +
                  '<div class="checkbox-group">' +
                    '<label class="checkbox-label">' +
                      '<input type="checkbox" class="checkbox-input" id="tune-learning-rate" checked />' +
                      '<span class="checkbox-text">Learning Rate</span>' +
                    '</label>' +
                    '<label class="checkbox-label">' +
                      '<input type="checkbox" class="checkbox-input" id="tune-depth" checked />' +
                      '<span class="checkbox-text">Max Depth</span>' +
                    '</label>' +
                    '<label class="checkbox-label">' +
                      '<input type="checkbox" class="checkbox-input" id="tune-estimators" />' +
                      '<span class="checkbox-text">N Estimators</span>' +
                    '</label>' +
                  '</div>' +
                '</div>' +
              '</div>' +
              '<div class="form-actions">' +
                '<button class="btn btn-secondary" id="validate-train-btn">Validate</button>' +
                '<button class="btn btn-primary" id="start-train-btn">' +
                  '<span class="icon">' +
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                      '<polygon points="5,3 19,12 5,21"/>' +
                    '</svg>' +
                  '</span>' +
                  'Start Training' +
                '</button>' +
              '</div>' +
            '</div>' +
            
            '<div class="card">' +
              '<h3 class="card-title">' +
                '<span class="card-title-icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>' +
                  '</svg>' +
                '</span>' +
                'Training Metrics' +
              '</h3>' +
              '<div class="metrics-grid" id="train-metrics">' +
                '<div class="metric-card">' +
                  '<div class="metric-value">87.3%</div>' +
                  '<div class="metric-label">Accuracy</div>' +
                  '<div class="metric-change positive">+2.1%</div>' +
                '</div>' +
                '<div class="metric-card">' +
                  '<div class="metric-value">0.841</div>' +
                  '<div class="metric-label">F1 Score</div>' +
                  '<div class="metric-change positive">+0.05</div>' +
                '</div>' +
                '<div class="metric-card">' +
                  '<div class="metric-value">0.923</div>' +
                  '<div class="metric-label">AUC-ROC</div>' +
                  '<div class="metric-change neutral">-0.01</div>' +
                '</div>' +
                '<div class="metric-card">' +
                  '<div class="metric-value">0.156</div>' +
                  '<div class="metric-label">Log Loss</div>' +
                  '<div class="metric-change positive">-0.02</div>' +
                '</div>' +
              '</div>' +
              '<div class="training-chart">' +
                '<h4 class="chart-title">Loss Curves</h4>' +
                '<div class="chart-container">' +
                  '<svg viewBox="0 0 300 150" class="loss-chart">' +
                    '<polyline points="10,140 30,120 50,110 70,100 90,95 110,90 130,88 150,85 170,83 190,82 210,81 230,80 250,80 270,79 290,79" stroke="var(--primary-color)" stroke-width="2" fill="none" opacity="0.8"/>' +
                    '<polyline points="10,130 30,125 50,115 70,108 90,105 110,102 130,100 150,99 170,98 190,97 210,97 230,96 250,96 270,96 290,95" stroke="var(--status-warning)" stroke-width="2" fill="none" opacity="0.8"/>' +
                    '<text x="10" y="15" fill="var(--text-secondary)" font-size="12">Training Loss</text>' +
                    '<text x="10" y="30" fill="var(--text-secondary)" font-size="12">Validation Loss</text>' +
                  '</svg>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        
        // BACKTEST TAB
        '<div id="backtest-tab" class="tab-panel">' +
          '<div class="pipeline-grid">' +
            '<div class="card">' +
              '<h3 class="card-title">' +
                '<span class="card-title-icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>' +
                  '</svg>' +
                '</span>' +
                'Backtest Configuration' +
              '</h3>' +
              '<div class="form-grid">' +
                '<div class="form-group">' +
                  '<label class="form-label">Model</label>' +
                  '<select class="form-input" id="backtest-model">' +
                    '<option value="spy_opt_0dte_hourly" selected>spy_opt_0dte_hourly</option>' +
                    '<option value="spy_eq_swing_daily">spy_eq_swing_daily</option>' +
                    '<option value="aapl_eq_intraday_hourly">aapl_eq_intraday_hourly</option>' +
                  '</select>' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Initial Capital</label>' +
                  '<input type="number" class="form-input" id="backtest-capital" value="100000" min="1000" step="1000" />' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Commission</label>' +
                  '<input type="number" class="form-input" id="backtest-commission" value="1.0" min="0" step="0.1" />' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Slippage</label>' +
                  '<input type="number" class="form-input" id="backtest-slippage" value="0.001" min="0" step="0.0001" />' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Risk Per Trade</label>' +
                  '<input type="number" class="form-input" id="backtest-risk" value="2.0" min="0.1" max="10" step="0.1" />' +
                '</div>' +
                '<div class="form-group">' +
                  '<label class="form-label">Max Drawdown</label>' +
                  '<input type="number" class="form-input" id="backtest-drawdown" value="20.0" min="5" max="50" step="1" />' +
                '</div>' +
              '</div>' +
              '<div class="form-actions">' +
                '<button class="btn btn-secondary" id="validate-backtest-btn">Validate</button>' +
                '<button class="btn btn-primary" id="start-backtest-btn">' +
                  '<span class="icon">' +
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                      '<polygon points="5,3 19,12 5,21"/>' +
                    '</svg>' +
                  '</span>' +
                  'Start Backtest' +
                '</button>' +
              '</div>' +
            '</div>' +
            
            '<div class="card">' +
              '<h3 class="card-title">' +
                '<span class="card-title-icon">' +
                  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
                    '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>' +
                    '<rect x="7" y="7" width="3" height="9"/>' +
                    '<rect x="14" y="7" width="3" height="5"/>' +
                  '</svg>' +
                '</span>' +
                'Backtest Results' +
              '</h3>' +
              '<div class="results-grid" id="backtest-results">' +
                '<div class="result-card featured">' +
                  '<div class="result-value">2.41</div>' +
                  '<div class="result-label">Sharpe Ratio</div>' +
                  '<div class="result-benchmark">vs 1.85 benchmark</div>' +
                '</div>' +
                '<div class="result-card">' +
                  '<div class="result-value">+24.5%</div>' +
                  '<div class="result-label">Total Return</div>' +
                  '<div class="result-trend positive">↗</div>' +
                '</div>' +
                '<div class="result-card">' +
                  '<div class="result-value">142</div>' +
                  '<div class="result-label">Total Trades</div>' +
                  '<div class="result-info">67% Win Rate</div>' +
                '</div>' +
                '<div class="result-card">' +
                  '<div class="result-value">-5.2%</div>' +
                  '<div class="result-label">Max Drawdown</div>' +
                  '<div class="result-trend positive">↗</div>' +
                '</div>' +
              '</div>' +
              '<div class="equity-curve">' +
                '<h4 class="chart-title">Equity Curve</h4>' +
                '<div class="chart-container">' +
                  '<svg viewBox="0 0 300 150" class="equity-chart">' +
                    '<polyline points="10,140 25,138 40,135 55,130 70,125 85,122 100,118 115,115 130,110 145,105 160,102 175,98 190,95 205,90 220,85 235,80 250,75 265,70 280,65 295,60" stroke="var(--status-success)" stroke-width="3" fill="none"/>' +
                    '<circle cx="295" cy="60" r="3" fill="var(--status-success)"/>' +
                  '</svg>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';

    // Add interactive functionality
    function setupTabSwitching() {
      var tabBtns = wrap.querySelectorAll('.tab-btn');
      var tabPanels = wrap.querySelectorAll('.tab-panel');
      
      tabBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
          var tabId = btn.dataset.tab;
          
          // Remove active class from all buttons and panels
          tabBtns.forEach(function(b) { b.classList.remove('active'); });
          tabPanels.forEach(function(p) { p.classList.remove('active'); });
          
          // Add active class to clicked button and corresponding panel
          btn.classList.add('active');
          wrap.querySelector('#' + tabId + '-tab').classList.add('active');
        });
      });
    }
    
    function setupFeatureTags() {
      var featureTags = wrap.querySelectorAll('.feature-tag');
      featureTags.forEach(function(tag) {
        tag.addEventListener('click', function() {
          tag.classList.toggle('active');
        });
      });
    }
    
    function setupFormValidation() {
      // Build validation
      var validateBuildBtn = wrap.querySelector('#validate-build-btn');
      if (validateBuildBtn) {
        validateBuildBtn.addEventListener('click', function() {
          alert('Build configuration validated successfully!');
        });
      }
      
      // Train validation  
      var validateTrainBtn = wrap.querySelector('#validate-train-btn');
      if (validateTrainBtn) {
        validateTrainBtn.addEventListener('click', function() {
          alert('Training configuration validated successfully!');
        });
      }
      
      // Backtest validation
      var validateBacktestBtn = wrap.querySelector('#validate-backtest-btn');
      if (validateBacktestBtn) {
        validateBacktestBtn.addEventListener('click', function() {
          alert('Backtest configuration validated successfully!');
        });
      }
    }
    
    function setupRunButtons() {
      // Start Build
      var startBuildBtn = wrap.querySelector('#start-build-btn');
      if (startBuildBtn) {
        startBuildBtn.addEventListener('click', function() {
          alert('Build process started! Check progress in the panel above.');
        });
      }
      
      // Start Training
      var startTrainBtn = wrap.querySelector('#start-train-btn');
      if (startTrainBtn) {
        startTrainBtn.addEventListener('click', function() {
          alert('Training process started! Monitor metrics in the panel above.');
        });
      }
      
      // Start Backtest
      var startBacktestBtn = wrap.querySelector('#start-backtest-btn');
      if (startBacktestBtn) {
        startBacktestBtn.addEventListener('click', function() {
          alert('Backtest process started! Results will appear in the panel above.');
        });
      }
    }
    
    function setupPageActions() {
      var queueStatusBtn = wrap.querySelector('#queue-status-btn');
      if (queueStatusBtn) {
        queueStatusBtn.addEventListener('click', function() {
          alert('Queue Status: 2 builds running, 1 training queued, 0 backtests pending');
        });
      }
      
      var runHistoryBtn = wrap.querySelector('#run-history-btn');
      if (runHistoryBtn) {
        runHistoryBtn.addEventListener('click', function() {
          alert('Run History will show detailed logs and past execution results');
        });
      }
    }
    
    // Initialize all functionality
    setupTabSwitching();
    setupFeatureTags();
    setupFormValidation();
    setupRunButtons();
    setupPageActions();

    return wrap;
  }

  function viewSweeps() {
    var container = document.createElement('div');
    container.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">' +
          '<span class="title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<rect x="3" y="3" width="18" height="18" rx="2"/>' +
              '<line x1="7" y1="6" x2="7" y2="18"/>' +
              '<line x1="12" y1="6" x2="12" y2="18"/>' +
              '<line x1="17" y1="6" x2="17" y2="18"/>' +
              '<line x1="5" y1="10" x2="9" y2="10"/>' +
              '<line x1="10" y1="14" x2="14" y2="14"/>' +
              '<line x1="15" y1="8" x2="19" y2="8"/>' +
            '</svg>' +
          '</span>' +
          'Sweeps' +
        '</h1>' +
        '<p class="page-description">Grid search across thresholds, hours, and top percentages</p>' +
      '</div>' +
      '<div class="control-panel">' +
        '<h2 class="control-title">' +
          '<span class="control-title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="12" cy="12" r="3"/>' +
              '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>' +
            '</svg>' +
          '</span>' +
          'Sweep Configuration' +
        '</h2>' +
        '<div class="control-group">' +
          '<label class="control-label">Model</label>' +
          '<select class="control-input" id="model-select">' +
            SWEEP_MODELS_LIST.map(function(model) {
              return '<option value="' + model + '"' + (model === SWEEP_CONFIGURATION_DEFAULTS.model ? ' selected' : '') + '>' + model + '</option>';
            }).join('') +
          '</select>' +
        '</div>' +
        '<div class="control-grid">' +
          '<div class="control-group">' +
            '<label class="control-label">Thresholds Variants</label>' +
            '<div id="threshold-variants">' +
              SWEEP_CONFIGURATION_DEFAULTS.threshold_variants.map(function(variant) {
                return '<div class="variant-input">' +
                  '<input type="text" class="control-input" value="' + variant + '" placeholder="e.g., 0.50,0.52,0.54">' +
                '</div>';
              }).join('') +
            '</div>' +
            '<button class="add-variant-btn" data-target="threshold-variants">+ Add Variant</button>' +
          '</div>' +
          '<div class="control-group">' +
            '<label class="control-label">Allowed Hours Variants</label>' +
            '<div id="hours-variants">' +
              SWEEP_CONFIGURATION_DEFAULTS.hours_variants.map(function(variant) {
                return '<div class="variant-input">' +
                  '<input type="text" class="control-input" value="' + variant + '" placeholder="e.g., 13,14">' +
                '</div>';
              }).join('') +
            '</div>' +
            '<button class="add-variant-btn" data-target="hours-variants">+ Add Variant</button>' +
          '</div>' +
        '</div>' +
        '<div class="control-group">' +
          '<label class="control-label">Top % Variants</label>' +
          '<div id="top-pct-variants">' +
            SWEEP_CONFIGURATION_DEFAULTS.top_pct_variants.map(function(variant) {
              return '<div class="variant-input">' +
                '<input type="text" class="control-input" value="' + variant + '" placeholder="e.g., 0.10,0.15">' +
              '</div>';
            }).join('') +
          '</div>' +
          '<button class="add-variant-btn" data-target="top-pct-variants">+ Add Variant</button>' +
        '</div>' +
        '<div class="control-group">' +
          '<label class="control-label">Guards</label>' +
          '<div class="guards-row">' +
            '<div>' +
              '<label class="control-label" style="font-size: 12px; text-transform: none;">Min Trades</label>' +
              '<input type="number" class="control-input" value="' + SWEEP_CONFIGURATION_DEFAULTS.guards.min_trades + '" min="0">' +
            '</div>' +
            '<div>' +
              '<label class="control-label" style="font-size: 12px; text-transform: none;">Min Sharpe</label>' +
              '<input type="number" class="control-input" value="' + SWEEP_CONFIGURATION_DEFAULTS.guards.min_sharpe + '" min="0" step="0.01">' +
            '</div>' +
            '<div>' +
              '<label class="control-label" style="font-size: 12px; text-transform: none;">Tag</label>' +
              '<input type="text" class="control-input" value="' + SWEEP_CONFIGURATION_DEFAULTS.guards.tag + '" placeholder="e.g., demo">' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="action-row">' +
          '<button class="btn btn-secondary" id="reset-btn">Reset</button>' +
          '<button class="btn btn-secondary" id="run-sweep-btn">' +
            '<span class="icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                '<polygon points="5,3 19,12 5,21"/>' +
              '</svg>' +
            '</span>' +
            'Run Sweep' +
          '</button>' +
        '</div>' +
      '</div>' +
      '<div class="whatif-panel">' +
        '<h3 class="card-title">' +
          '<span class="card-title-icon">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="12" cy="12" r="10"/>' +
              '<line x1="10" y1="8" x2="10" y2="16"/>' +
              '<line x1="14" y1="8" x2="14" y2="16"/>' +
            '</svg>' +
          '</span>' +
          'What-If Analysis' +
        '</h3>' +
        '<div class="whatif-controls">' +
          '<div class="control-group">' +
            '<label class="control-label">Threshold: <span id="threshold-value">0.50</span></label>' +
            '<input type="range" class="whatif-slider" id="threshold-slider" min="0.30" max="0.80" step="0.01" value="0.50">' +
          '</div>' +
          '<div class="control-group">' +
            '<label class="control-label">Top N: <span id="topn-value">20</span></label>' +
            '<input type="range" class="whatif-slider" id="topn-slider" min="5" max="50" step="1" value="20">' +
          '</div>' +
        '</div>' +
        '<div class="whatif-deltas">' +
          '<div class="delta-chip" id="sharpe-delta">' +
            '<div class="delta-label">Sharpe Δ</div>' +
            '<div class="delta-value">+0.12</div>' +
          '</div>' +
          '<div class="delta-chip" id="trades-delta">' +
            '<div class="delta-label">Trades Δ</div>' +
            '<div class="delta-value">-8</div>' +
          '</div>' +
          '<div class="delta-chip" id="return-delta">' +
            '<div class="delta-label">Return Δ</div>' +
            '<div class="delta-value">+2.1%</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="results-section">' +
        '<div class="results-header">' +
          '<h2 class="results-title">' +
            '<span class="results-title-icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
                '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>' +
              '</svg>' +
            '</span>' +
            'Results' +
          '</h2>' +
          '<div class="results-actions">' +
            '<button class="btn btn-secondary">Export All CSV</button>' +
          '</div>' +
        '</div>' +
        '<table class="results-table" id="results-table">' +
          '<thead>' +
            '<tr>' +
              '<th>Kind</th>' +
              '<th>Thr/Top%</th>' +
              '<th>Allowed Hours</th>' +
              '<th class="cell-right">Sharpe</th>' +
              '<th class="cell-right">Cum Return</th>' +
              '<th class="cell-right">Trades</th>' +
              '<th>Parity</th>' +
              '<th>Tag</th>' +
              '<th>Actions</th>' +
            '</tr>' +
          '</thead>' +
          '<tbody id="results-tbody">' +
          '</tbody>' +
        '</table>' +
        '<div class="empty-state" id="empty-state" style="display: none;">' +
          '<h3>No results yet</h3>' +
          '<p>Run a sweep to see results. Adjust variants or relax guards if needed.</p>' +
        '</div>' +
      '</div>';

    // Add event listeners for What-if sliders
    var thresholdSlider = container.querySelector('#threshold-slider');
    var topnSlider = container.querySelector('#topn-slider');
    var thresholdValue = container.querySelector('#threshold-value');
    var topnValue = container.querySelector('#topn-value');
    var sharpeDeltas = container.querySelector('#sharpe-delta');
    var tradesDeltas = container.querySelector('#trades-delta');
    var returnDeltas = container.querySelector('#return-delta');

    function updateWhatIfDeltas() {
      var threshold = parseFloat(thresholdSlider.value);
      var topn = parseInt(topnSlider.value);
      
      // Simple delta calculations (in real implementation, this would call API)
      var sharpeDelta = (threshold - 0.5) * 0.24 + (topn - 20) * 0.008;
      var tradesDelta = Math.round((threshold - 0.5) * -40 + (topn - 20) * 1.2);
      var returnDelta = (threshold - 0.5) * 4.2 + (topn - 20) * 0.15;
      
      thresholdValue.textContent = threshold.toFixed(2);
      topnValue.textContent = topn;
      
      sharpeDeltas.querySelector('.delta-value').textContent = (sharpeDelta >= 0 ? '+' : '') + sharpeDelta.toFixed(2);
      tradesDeltas.querySelector('.delta-value').textContent = (tradesDelta >= 0 ? '+' : '') + tradesDelta;
      returnDeltas.querySelector('.delta-value').textContent = (returnDelta >= 0 ? '+' : '') + returnDelta.toFixed(1) + '%';
      
      sharpeDeltas.className = 'delta-chip ' + (sharpeDelta >= 0 ? 'positive' : 'negative');
      tradesDeltas.className = 'delta-chip ' + (tradesDelta >= 0 ? 'positive' : 'negative');
      returnDeltas.className = 'delta-chip ' + (returnDelta >= 0 ? 'positive' : 'negative');
    }

    thresholdSlider.addEventListener('input', updateWhatIfDeltas);
    topnSlider.addEventListener('input', updateWhatIfDeltas);

    // Render initial results
    var tbody = container.querySelector('#results-tbody');
    tbody.innerHTML = SWEEP_RESULTS_DETAILED.map(function(result) {
      return '<tr>' +
        '<td>' + result.kind + '</td>' +
        '<td>' + result.value + '</td>' +
        '<td>' + result.allowed_hours + '</td>' +
        '<td class="cell-right metric-positive">' + result.sharpe.toFixed(2) + '</td>' +
        '<td class="cell-right metric-positive">' + (result.cum_return * 100).toFixed(1) + '%</td>' +
        '<td class="cell-right">' + result.trades + '</td>' +
        '<td>' + (result.parity || 'N/A') + '</td>' +
        '<td>' + result.tag + '</td>' +
        '<td><button class="btn btn-sm view-btn">View</button></td>' +
      '</tr>';
    }).join('');

    return container;
  }

  function viewDocs() {
    var wrap = document.createElement('div');
    wrap.innerHTML = 
      '<div class="page-header">' +
        '<h1 class="page-title">Documentation</h1>' +
        '<p class="page-description">Sigma Lab guides and API reference</p>' +
      '</div>' +
      '<div class="docs-grid">' +
        '<div class="doc-card">' +
          '<h3>Getting Started</h3>' +
          '<p>Learn the basics of Sigma Lab and create your first model.</p>' +
        '</div>' +
        '<div class="doc-card">' +
          '<h3>API Reference</h3>' +
          '<p>Complete API documentation for all endpoints.</p>' +
        '</div>' +
        '<div class="doc-card">' +
          '<h3>Tutorials</h3>' +
          '<p>Step-by-step tutorials for common workflows.</p>' +
        '</div>' +
      '</div>';
    
    return wrap;
  }

  // ---- Router ----
  var app = document.getElementById('app');
  var routes = {
    '/': viewDashboard,
    '/dashboard': viewDashboard,
    '/packs': viewModels, // Using viewModels as placeholder
    '/models': viewModels,
    '/models/new': viewModels,
    '/models/templates': viewModels,
    '/models/:id/designer': viewModels,
    '/models/:id/composer': viewModels,
    '/models/:id/composer/build': viewModels,
    '/models/:id/composer/sweeps': viewSweeps,
    '/models/:id/composer/leaderboard': viewLeaderboard,
    '/models/:id/composer/backtest': viewModels,
    '/models/:id/composer/train': viewModels,
    '/runs': viewRuns,
    '/sweeps': viewSweeps,
    '/leaderboard': viewLeaderboard,
    '/signals': viewSignals,
    '/overlay': viewOverlay,
    '/health': viewModels, // Using viewModels as placeholder
    '/docs': viewDocs,
    '/admin': viewModels, // Using viewModels as placeholder
  };

  function setActiveNav(path){
    document.querySelectorAll('.nav-item').forEach(function(a){ a.classList.toggle('active', a.getAttribute('data-route')==='#'+path); });
  }

  function render(path){ 
    var view = routes[path] || routes['/dashboard']; 
    app.innerHTML=''; 
    var node = view(); 
    if(node) app.appendChild(node); 
    setActiveNav(path); 
  }

  function navigate(hash){ 
    var path = (hash || '#/dashboard').replace('#',''); 
    render(path); 
  }

  window.addEventListener('hashchange', function(){ navigate(location.hash); });
  navigate(location.hash);

  // ---- Theme and UI Interactions ----
  var root = document.documentElement;
  var ls = window.localStorage;
  var themeBtn = document.getElementById('themeBtn');
  var densitySelect = document.getElementById('densitySelect');
  var sidebar = document.getElementById('sidebar');
  var menuBtn = document.getElementById('menu-toggle-btn');
  var overlay = document.getElementById('overlay');
  var cmdk = document.getElementById('cmdkDialog');
  var cmdkInput = document.getElementById('cmdkInput');
  
  var isSidebarOpen = false;
  var isCmdkOpen = false;

  // Theme switcher
  function applyTheme(theme) { 
    root.dataset.theme = theme; 
    ls.setItem('ui.theme', theme); 
  }
  
  function applyDensity(density) { 
    root.dataset.density = density; 
    ls.setItem('ui.density', density); 
  }
  
  if (themeBtn) {
    themeBtn.addEventListener('click', function() {
      var order = ['light', 'dark', 'slate', 'paper'];
      var next = order[(order.indexOf(root.dataset.theme) + 1) % order.length];
      applyTheme(next);
    });
  }
  
  if (densitySelect) {
    densitySelect.addEventListener('change', function(e) {
      applyDensity(e.target.value);
    });
  }
  
  var savedTheme = ls.getItem('ui.theme');
  var savedDensity = ls.getItem('ui.density');
  
  applyTheme(savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  applyDensity(savedDensity || 'cozy');
  
  if (densitySelect) {
    densitySelect.value = root.dataset.density;
  }

  // Sidebar toggle
  function updateOverlay() {
    var shouldShow = isSidebarOpen || isCmdkOpen;
    if (overlay) {
      overlay.style.display = shouldShow ? 'block' : 'none';
      overlay.setAttribute('aria-hidden', shouldShow ? 'false' : 'true');
    }
  }

  if (menuBtn) {
    menuBtn.addEventListener('click', function() {
      var isMobile = window.matchMedia('(max-width: 1024px)').matches;
      if (isMobile) {
        isSidebarOpen = sidebar.classList.toggle('open');
        updateOverlay();
      } else {
        var isCollapsing = !sidebar.classList.contains('collapsed');
        sidebar.classList.toggle('collapsed');
        
        // Close all submenus when collapsing
        if (isCollapsing) {
          closeAllSubmenus();
        }
      }
    });
  }
  
  if (overlay) {
    overlay.addEventListener('click', function() {
      if (isSidebarOpen) {
        sidebar.classList.remove('open');
        isSidebarOpen = false;
      }
      if (isCmdkOpen) {
        cmdk.setAttribute('aria-hidden', 'true');
        isCmdkOpen = false;
      }
      if (isCartOpen) closeCart();
      if (isAssistantOpen) closeAssistant();
      updateOverlayForDrawers();
    });
  }
  
  // Command palette
  var cmdkBtn = document.getElementById('cmdk');
  if (cmdkBtn) {
    cmdkBtn.addEventListener('click', function() {
      if (cmdk) {
        cmdk.setAttribute('aria-hidden', 'false');
        isCmdkOpen = true;
        updateOverlay();
        if (cmdkInput) {
          setTimeout(function() {
            cmdkInput.focus();
          }, 150);
        }
      }
    });
  }

  // Keyboard shortcuts
  window.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      if (isSidebarOpen) {
        sidebar.classList.remove('open');
        isSidebarOpen = false;
      }
      if (isCmdkOpen) {
        cmdk.setAttribute('aria-hidden', 'true');
        isCmdkOpen = false;
      }
      if (isCartOpen) closeCart();
      if (isAssistantOpen) closeAssistant();
      updateOverlayForDrawers();
    }
    
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      if (cmdk) {
        cmdk.setAttribute('aria-hidden', 'false');
        isCmdkOpen = true;
        updateOverlay();
        if (cmdkInput) {
          setTimeout(function() {
            cmdkInput.focus();
          }, 150);
        }
      }
    }
  });

  // --- Drawer Management ---
  var selectionCart = document.getElementById('selectionCart');
  var aiAssistant = document.getElementById('aiAssistant');
  var cartToggle = document.getElementById('cartToggle');
  var assistantToggle = document.getElementById('assistantToggle');
  var cartClose = document.getElementById('cartClose');
  var assistantClose = document.getElementById('assistantClose');
  
  var isCartOpen = false;
  var isAssistantOpen = false;
  
  function updateOverlayForDrawers() {
    var shouldShow = isSidebarOpen || isCartOpen || isAssistantOpen;
    if (overlay) {
      overlay.style.display = shouldShow ? 'block' : 'none';
      overlay.setAttribute('aria-hidden', shouldShow ? 'false' : 'true');
    }
  }
  
  function openCart() {
    isCartOpen = true;
    isAssistantOpen = false;
    if (selectionCart) selectionCart.setAttribute('aria-hidden', 'false');
    if (aiAssistant) aiAssistant.setAttribute('aria-hidden', 'true');
    updateOverlayForDrawers();
  }
  
  function closeCart() {
    isCartOpen = false;
    if (selectionCart) selectionCart.setAttribute('aria-hidden', 'true');
    updateOverlayForDrawers();
  }
  
  function openAssistant() {
    isAssistantOpen = true;
    isCartOpen = false;
    if (aiAssistant) aiAssistant.setAttribute('aria-hidden', 'false');
    if (selectionCart) selectionCart.setAttribute('aria-hidden', 'true');
    updateOverlayForDrawers();
  }
  
  function closeAssistant() {
    isAssistantOpen = false;
    if (aiAssistant) aiAssistant.setAttribute('aria-hidden', 'true');
    updateOverlayForDrawers();
  }
  
  // Drawer event listeners
  if (cartToggle) {
    cartToggle.addEventListener('click', function() {
      if (isCartOpen) closeCart(); else openCart();
    });
  }
  
  if (assistantToggle) {
    assistantToggle.addEventListener('click', function() {
      if (isAssistantOpen) closeAssistant(); else openAssistant();
    });
  }
  
  if (cartClose) cartClose.addEventListener('click', closeCart);
  if (assistantClose) assistantClose.addEventListener('click', closeAssistant);
  
  // --- Risk Profile Management ---
  var riskProfileChips = document.getElementById('riskProfileChips');
  var currentRiskProfile = (localStorage && localStorage.getItem('ui.riskProfile')) || 'balanced';
  
  function updateRiskProfile(profile) {
    currentRiskProfile = profile;
    if (localStorage) localStorage.setItem('ui.riskProfile', profile);
    if (riskProfileChips) {
      var chips = riskProfileChips.querySelectorAll('.risk-chip');
      chips.forEach(function(chip) {
        if (chip.dataset.profile === profile) {
          chip.classList.add('active');
        } else {
          chip.classList.remove('active');
        }
      });
    }
    // Dispatch custom event for components to listen to
    if (window.CustomEvent) {
      window.dispatchEvent(new CustomEvent('riskProfileChanged', { detail: { profile: profile } }));
    }
  }
  
  // Initialize risk profile
  updateRiskProfile(currentRiskProfile);
  
  // Risk profile chip event listeners
  if (riskProfileChips) {
    riskProfileChips.addEventListener('click', function(e) {
      if (e.target.classList.contains('risk-chip')) {
        updateRiskProfile(e.target.dataset.profile);
      }
    });
  }
  
  // Expose risk profile globally
  window.getCurrentRiskProfile = function() { return currentRiskProfile; };

  // --- Expandable Navigation ---
  function initExpandableNavigation() {
    var navParents = document.querySelectorAll('.nav-parent');
    
    navParents.forEach(function(parent) {
      parent.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Don't expand if sidebar is collapsed
        if (sidebar && sidebar.classList.contains('collapsed')) {
          return;
        }
        
        var toggleId = parent.getAttribute('data-toggle');
        var submenu = document.getElementById(toggleId + '-submenu');
        var chevron = parent.querySelector('.nav-chevron');
        var isNested = parent.closest('.nav-nested');
        
        if (submenu) {
          var isExpanded = submenu.classList.contains('expanded');
          
          // For nested menus, only close other nested menus in the same parent
          // For top-level menus, close all other top-level menus
          if (isNested) {
            // Close other nested submenus in the same parent
            var parentSubmenu = parent.closest('.nav-submenu');
            if (parentSubmenu) {
              parentSubmenu.querySelectorAll('.nav-nested-submenu.expanded').forEach(function(menu) {
                if (menu !== submenu) {
                  menu.classList.remove('expanded');
                  var otherParent = parentSubmenu.querySelector('[data-toggle="' + menu.id.replace('-submenu', '') + '"]');
                  if (otherParent) {
                    otherParent.classList.remove('expanded');
                    var otherChevron = otherParent.querySelector('.nav-chevron');
                    if (otherChevron) {
                      otherChevron.style.transform = '';
                    }
                  }
                }
              });
            }
          } else {
            // Close all other top-level submenus
            document.querySelectorAll('.nav-submenu.expanded').forEach(function(menu) {
              if (menu !== submenu && !menu.classList.contains('nav-nested-submenu')) {
                menu.classList.remove('expanded');
                var otherParent = document.querySelector('[data-toggle="' + menu.id.replace('-submenu', '') + '"]');
                if (otherParent && !otherParent.closest('.nav-nested')) {
                  otherParent.classList.remove('expanded');
                  var otherChevron = otherParent.querySelector('.nav-chevron');
                  if (otherChevron) {
                    otherChevron.style.transform = '';
                  }
                }
              }
            });
          }
          
          // Toggle current submenu
          if (isExpanded) {
            submenu.classList.remove('expanded');
            parent.classList.remove('expanded');
            if (chevron) chevron.style.transform = '';
          } else {
            submenu.classList.add('expanded');
            parent.classList.add('expanded');
            if (chevron) chevron.style.transform = 'rotate(90deg)';
          }
        }
      });
    });
  }
  
  // Function to close all expanded submenus
  function closeAllSubmenus() {
    document.querySelectorAll('.nav-submenu.expanded').forEach(function(menu) {
      menu.classList.remove('expanded');
      var parent = document.querySelector('[data-toggle="' + menu.id.replace('-submenu', '') + '"]');
      if (parent) {
        parent.classList.remove('expanded');
        var chevron = parent.querySelector('.nav-chevron');
        if (chevron) {
          chevron.style.transform = '';
        }
      }
    });
  }
  
  // Initialize expandable navigation
  setTimeout(function() {
    initExpandableNavigation();
  }, 100);

  // Command palette actions
  if (cmdk && cmdkInput) {
    var cmdkItems = cmdk.querySelectorAll('.cmdk-item');
    var selectedIndex = 0;
    
    function updateSelection() {
      cmdkItems.forEach(function(item, index) {
        if (index === selectedIndex) {
          item.setAttribute('aria-selected', 'true');
        } else {
          item.setAttribute('aria-selected', 'false');
        }
      });
    }
    
    function executeCommand(item) {
      var action = item.dataset.action;
      if (action.startsWith('route:')) {
        var route = action.replace('route:', '');
        window.location.hash = '#' + route;
      } else if (action === 'theme') {
        if (themeBtn) themeBtn.click();
      } else if (action === 'docs') {
        window.location.hash = '#/docs';
      } else if (action.startsWith('drawer:')) {
        var drawer = action.replace('drawer:', '');
        if (drawer === 'cart') {
          openCart();
        } else if (drawer === 'assistant') {
          openAssistant();
        }
      }
      
      cmdk.setAttribute('aria-hidden', 'true');
      isCmdkOpen = false;
      updateOverlayForDrawers();
    }
    
    // Click handlers
    cmdkItems.forEach(function(item, index) {
      item.addEventListener('click', function() {
        executeCommand(item);
      });
      
      item.addEventListener('mouseenter', function() {
        selectedIndex = index;
        updateSelection();
      });
    });
    
    // Keyboard navigation
    cmdkInput.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, cmdkItems.length - 1);
        updateSelection();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, 0);
        updateSelection();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (cmdkItems[selectedIndex]) {
          executeCommand(cmdkItems[selectedIndex]);
        }
      }
    });
    
    // Search filtering (basic)
    cmdkInput.addEventListener('input', function() {
      var query = this.value.toLowerCase();
      var visibleIndex = 0;
      
      cmdkItems.forEach(function(item) {
        var text = item.textContent.toLowerCase();
        if (query === '' || text.includes(query)) {
          item.style.display = 'flex';
          if (visibleIndex === 0) {
            selectedIndex = Array.from(cmdkItems).indexOf(item);
          }
          visibleIndex++;
        } else {
          item.style.display = 'none';
        }
      });
      
      updateSelection();
    });
    
    // Reset when opening
    cmdk.addEventListener('transitionend', function() {
      if (cmdk.getAttribute('aria-hidden') === 'false') {
        selectedIndex = 0;
        updateSelection();
        cmdkInput.value = '';
        cmdkItems.forEach(function(item) {
          item.style.display = 'flex';
        });
      }
    });
  }

})();