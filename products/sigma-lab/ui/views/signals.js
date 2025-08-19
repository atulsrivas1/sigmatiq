import { SIGNALS, MODELS } from '../mocks/mock_data.js';

export function render() {
  const wrap = document.createElement('div');
  
  // Get active tab from hash or default to leaderboard
  const hash = window.location.hash;
  const activeTab = hash.includes('/signals/') ? hash.split('/signals/')[1] : 'leaderboard';
  
  wrap.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
          </svg>
        </span>
        Signals
      </h1>
      <div class="header-actions">
        <button class="btn btn-secondary" id="export-signals-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7,10 12,15 17,10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
          </span>
          Export CSV
        </button>
      </div>
    </div>

    <div class="signals-tabs">
      <div class="tab-nav">
        <button class="tab-button ${activeTab === 'leaderboard' ? 'active' : ''}" data-tab="leaderboard">
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="4" y="11" width="3" height="7" rx="1"/>
              <rect x="10.5" y="7" width="3" height="11" rx="1"/>
              <rect x="17" y="9" width="3" height="9" rx="1"/>
            </svg>
          </span>
          Leaderboard
        </button>
        <button class="tab-button ${activeTab === 'log' ? 'active' : ''}" data-tab="log">
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
          </span>
          Log
        </button>
        <button class="tab-button ${activeTab === 'analytics' ? 'active' : ''}" data-tab="analytics">
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 20V10"/>
              <path d="M12 20V4"/>
              <path d="M6 20v-6"/>
            </svg>
          </span>
          Analytics
        </button>
      </div>
    </div>

    <div class="tab-content" id="signals-tab-content">
      ${renderTabContent(activeTab)}
    </div>
  `;

  // Add tab switching functionality
  wrap.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
      const tab = button.dataset.tab;
      
      // Update active tab
      wrap.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
      button.classList.add('active');
      
      // Update content
      wrap.querySelector('#signals-tab-content').innerHTML = renderTabContent(tab);
      
      // Update URL without triggering full page reload
      history.replaceState(null, '', `#/signals/${tab}`);
    });
  });

  // Export button
  wrap.querySelector('#export-signals-btn').addEventListener('click', () => {
    alert('Exporting signals data to CSV...');
  });

  return wrap;
}

function renderTabContent(tab) {
  switch (tab) {
    case 'leaderboard':
      return renderLeaderboardTab();
    case 'log':
      return renderLogTab();
    case 'analytics':
      return renderAnalyticsTab();
    default:
      return renderLeaderboardTab();
  }
}

function renderLeaderboardTab() {
  return `
    <div class="signals-leaderboard">
      <div class="leaderboard-controls">
        <div class="control-row">
          <div class="filters">
            <select id="period-filter">
              <option value="24h">Last 24 Hours</option>
              <option value="7d" selected>Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="ytd">Year to Date</option>
            </select>
            <select id="pack-filter">
              <option value="all">All Packs</option>
              <option value="zeroedge">ZeroSigma</option>
              <option value="swingedge">SwingSigma</option>
              <option value="longedge">LongSigma</option>
              <option value="overnightedge">OvernightSigma</option>
              <option value="momentumedge">MomentumSigma</option>
            </select>
            <label>
              <input type="checkbox" id="pass-gate-only">
              Pass Gate Only
            </label>
          </div>
        </div>
      </div>

      <div class="leaderboard-table">
        <table>
          <thead>
            <tr>
              <th>Model ID</th>
              <th>Pack</th>
              <th>Sharpe</th>
              <th>Return %</th>
              <th>Win Rate</th>
              <th>Trades</th>
              <th>Fill Rate</th>
              <th>Avg Slippage</th>
              <th>Capacity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${MODELS.slice(0, 5).map(model => `
              <tr>
                <td>${model.model_id}</td>
                <td><span class="pack-badge ${model.pack_id}">${model.pack_id}</span></td>
                <td>${model.sharpe || '2.41'}</td>
                <td class="${parseFloat(model.return) > 0 ? 'positive' : 'negative'}">${model.return}</td>
                <td>67%</td>
                <td>${model.trades}</td>
                <td>94%</td>
                <td>0.02%</td>
                <td><span class="capacity-badge high">High</span></td>
                <td>
                  <button class="btn btn-small">View Performance</button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderLogTab() {
  return `
    <div class="signals-log">
      <div class="log-controls">
        <div class="control-row">
          <div class="filters">
            <input type="date" id="date-filter" value="2025-08-16">
            <select id="model-filter">
              <option value="all">All Models</option>
              ${MODELS.map(m => `<option value="${m.model_id}">${m.model_id}</option>`).join('')}
            </select>
            <select id="status-filter">
              <option value="all">All Status</option>
              <option value="filled">Filled</option>
              <option value="pending">Pending</option>
              <option value="cancelled">Cancelled</option>
              <option value="stopped">Stopped Out</option>
            </select>
            <input type="text" id="ticker-filter" placeholder="Ticker..." style="width: 100px;">
          </div>
        </div>
      </div>

      <div class="log-table">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Model</th>
              <th>Ticker</th>
              <th>Side</th>
              <th>Entry Ref</th>
              <th>Fill Px</th>
              <th>Slippage</th>
              <th>Status</th>
              <th>R:R</th>
              <th>P&L</th>
              <th>Tag</th>
            </tr>
          </thead>
          <tbody>
            ${SIGNALS.map(signal => `
              <tr>
                <td>${signal.date} ${signal.time}</td>
                <td>${signal.model_id}</td>
                <td>${signal.ticker}</td>
                <td class="${signal.side === 'long' ? 'long-side' : 'short-side'}">${signal.side}</td>
                <td>$${signal.entry_ref_px}</td>
                <td>$${(signal.entry_ref_px + 0.05).toFixed(2)}</td>
                <td class="neutral">0.01%</td>
                <td><span class="status-badge ${signal.status}">${signal.status}</span></td>
                <td>${signal.rr}</td>
                <td class="${signal.side === 'long' ? 'positive' : 'negative'}">
                  ${signal.side === 'long' ? '+' : '-'}$${Math.abs(Math.random() * 500).toFixed(2)}
                </td>
                <td>${signal.tag || '-'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderAnalyticsTab() {
  return `
    <div class="signals-analytics">
      <div class="analytics-controls">
        <div class="control-row">
          <div class="filters">
            <select id="model-select">
              <option value="all">All Models</option>
              ${MODELS.map(m => `<option value="${m.model_id}">${m.model_id}</option>`).join('')}
            </select>
            <select id="period-select">
              <option value="7d">Last 7 Days</option>
              <option value="30d" selected>Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
            <div class="risk-profile-display">
              <span class="risk-label">Risk Profile:</span>
              <span class="risk-chip active">Balanced</span>
            </div>
          </div>
        </div>
      </div>

      <div class="analytics-grid">
        <div class="analytics-card">
          <h4>Performance Metrics</h4>
          <div class="metrics-grid">
            <div class="metric-item">
              <span class="metric-label">Sharpe Ratio</span>
              <span class="metric-value">2.14</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Sortino Ratio</span>
              <span class="metric-value">3.21</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Cum Return</span>
              <span class="metric-value positive">+18.7%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Win Rate</span>
              <span class="metric-value">68%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Avg Win/Loss</span>
              <span class="metric-value">1.85</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Max Drawdown</span>
              <span class="metric-value negative">-8.4%</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Total Trades</span>
              <span class="metric-value">342</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">Fill Rate</span>
              <span class="metric-value">94.2%</span>
            </div>
          </div>
        </div>

        <div class="analytics-card">
          <h4>Equity Curve</h4>
          <div class="chart-placeholder">
            <svg viewBox="0 0 400 200" style="width: 100%; height: 200px;">
              <polyline points="0,180 40,170 80,160 120,165 160,140 200,130 240,125 280,110 320,100 360,90 400,85" 
                        fill="none" stroke="var(--primary-color)" stroke-width="2"/>
              <line x1="0" y1="180" x2="400" y2="180" stroke="var(--border-color)" stroke-width="1"/>
            </svg>
          </div>
        </div>

        <div class="analytics-card">
          <h4>Hour-wise Performance</h4>
          <div class="heatmap-grid">
            ${Array.from({length: 7}, (_, i) => `
              <div class="heatmap-row">
                <span class="hour-label">${9 + i}:00</span>
                ${Array.from({length: 5}, (_, j) => `
                  <div class="heatmap-cell" style="background: rgba(26, 188, 156, ${Math.random() * 0.8 + 0.2})"></div>
                `).join('')}
              </div>
            `).join('')}
          </div>
        </div>

        <div class="analytics-card">
          <h4>Parity & Capacity</h4>
          <div class="parity-metrics">
            <div class="parity-item">
              <span class="parity-label">Underlying vs Premium:</span>
              <span class="parity-value good">98.2%</span>
            </div>
            <div class="parity-item">
              <span class="parity-label">Capacity Utilization:</span>
              <span class="parity-value warning">78%</span>
            </div>
            <div class="parity-item">
              <span class="parity-label">Spread Impact:</span>
              <span class="parity-value good">0.12%</span>
            </div>
            <div class="parity-item">
              <span class="parity-label">OI Coverage:</span>
              <span class="parity-value good">94%</span>
            </div>
          </div>
        </div>
      </div>

      <div class="data-freshness">
        <span class="freshness-label">Data Freshness:</span>
        <span class="freshness-value">Last updated 5 minutes ago</span>
        <span class="coverage-label">Coverage:</span>
        <span class="coverage-value">98.5%</span>
      </div>
    </div>
  `;
}