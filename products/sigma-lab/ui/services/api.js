// Minimal REST client with stubs that we can replace later

const API_BASE = (window.EDGE_API_BASE || 'http://localhost:8001');

async function request(path, { method = 'GET', body, headers } = {}) {
  const opts = { method, headers: { 'Content-Type': 'application/json', ...(headers||{}) } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, opts).catch(err => ({ ok: false, _err: err }));
  if (!res || res._err) throw new Error('Network error');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Stubs for local development without API
function stub(delay, data) { return new Promise(resolve => setTimeout(() => resolve(data), delay)); }

export const api = {
  request,
  getModels: () => stub(200, { ok: true, rows: [ { model_id: 'spy_opt_0dte_hourly', pack_id: 'zerosigma', updated_at: '2025-08-16T11:50:00Z' } ] }),
  getLeaderboard: () => stub(200, { ok: true, rows: [ { model_id: 'spy_opt_0dte_hourly', best_sharpe: 2.41, best_cum_ret: 0.38, started_at: '2025-08-16T11:50:00Z' } ] }),
  getHealthz: () => stub(150, { ok: true, checks: { api: 'ok', polygon: 'ok' } }),
  // Add more: buildMatrix, train, backtest, backtestSweep, getSignals, optionsOverlay when wiring real API
};

