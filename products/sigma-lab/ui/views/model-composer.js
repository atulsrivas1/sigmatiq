export function render() {
  // Extract model ID and tab from the current path
  const path = location.hash.replace(/^#/, '');
  const pathParts = path.split('/');
  const modelId = pathParts[2] || 'spy_opt_0dte_v2';
  const activeTab = pathParts[4] || 'build';

  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <div class="breadcrumb">
        <a href="#/models">Models</a> / <a href="#/models/${modelId}">${modelId}</a> / <span>Composer</span>
      </div>
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polygon points="10,8 16,12 10,16 10,8"/>
          </svg>
        </span>
        Composer: ${modelId}
      </h1>
      <div class="header-actions">
        <div class="risk-profile-display">
          <span class="risk-label">Risk Profile:</span>
          <span class="risk-chip active" id="current-risk">Balanced</span>
        </div>
        <button class="btn btn-secondary" id="designer-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 20h9"/>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
            </svg>
          </span>
          Open Designer
        </button>
      </div>
    </div>

    <div class="composer-tabs">
      <div class="tab-nav">
        <button class="tab-button ${activeTab === 'build' ? 'active' : ''}" data-tab="build">
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            </svg>
          </span>
          Build
        </button>
        <button class="tab-button ${activeTab === 'sweeps' ? 'active' : ''}" data-tab="sweeps">
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <line x1="7" y1="6" x2="7" y2="18"/>
              <line x1="12" y1="6" x2="12" y2="18"/>
              <line x1="17" y1="6" x2="17" y2="18"/>
            </svg>
          </span>
          Sweeps
        </button>
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
        <button class="tab-button ${activeTab === 'train' ? 'active' : ''}" data-tab="train">
          <span class="tab-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
          </span>
          Train
        </button>
      </div>
    </div>

    <div class="tab-content" id="tab-content">
      ${renderTabContent(activeTab, modelId)}
    </div>
  `;

  // Add tab switching functionality
  wrap.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
      const tab = button.dataset.tab;
      const newPath = `#/models/${modelId}/composer/${tab}`;
      
      // Update active tab
      wrap.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
      button.classList.add('active');
      
      // Update content
      wrap.querySelector('#tab-content').innerHTML = renderTabContent(tab, modelId);
      
      // Update URL without triggering full page reload
      history.replaceState(null, '', newPath);
    });
  });

  // Designer button
  wrap.querySelector('#designer-btn').addEventListener('click', () => {
    location.hash = `/models/${modelId}/designer`;
  });

  return wrap;
}

function renderTabContent(tab, modelId) {
  switch (tab) {
    case 'build':
      return renderBuildTab(modelId);
    case 'sweeps':
      return renderSweepsTab(modelId);
    case 'leaderboard':
      return renderLeaderboardTab(modelId);
    case 'train':
      return renderTrainTab(modelId);
    default:
      return renderBuildTab(modelId);
  }
}

function renderBuildTab(modelId) {
  return `
    <div class="build-tab">
      <div class="build-content">
        <div class="build-section">
          <h3 class="section-title">Matrix Configuration</h3>
          <div class="form-grid">
            <div class="form-field">
              <label for="start-date">Start Date</label>
              <input type="date" id="start-date" value="2024-01-01">
            </div>
            <div class="form-field">
              <label for="end-date">End Date</label>
              <input type="date" id="end-date" value="2024-08-01">
            </div>
            <div class="form-field">
              <label for="universe">Universe</label>
              <select id="universe">
                <option value="spy">SPY</option>
                <option value="qqq">QQQ</option>
                <option value="iwm">IWM</option>
                <option value="custom">Custom...</option>
              </select>
            </div>
          </div>
        </div>

        <div class="build-section">
          <h3 class="section-title">Matrix Status</h3>
          <div class="matrix-status">
            <div class="status-item">
              <span class="status-label">Current Matrix:</span>
              <span class="status-value">matrix_a1b2c3d4</span>
              <button class="btn btn-small">View Profile</button>
            </div>
            <div class="status-item">
              <span class="status-label">Created:</span>
              <span class="status-value">2 hours ago</span>
            </div>
            <div class="status-item">
              <span class="status-label">Rows:</span>
              <span class="status-value">45,234</span>
            </div>
            <div class="status-item">
              <span class="status-label">Features:</span>
              <span class="status-value">28</span>
            </div>
          </div>
        </div>

        <div class="build-actions">
          <button class="btn btn-primary" id="build-matrix-btn">
            <span class="icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5,3 19,12 5,21"/>
              </svg>
            </span>
            Build Matrix
          </button>
          <button class="btn btn-secondary">Download Current</button>
        </div>
      </div>

      <div class="build-sidebar">
        <div class="trust-hud">
          <h4>Trust HUD</h4>
          <div class="trust-metrics">
            <div class="trust-item">
              <span class="trust-label">Data Quality:</span>
              <span class="trust-badge good">Good</span>
            </div>
            <div class="trust-item">
              <span class="trust-label">Coverage:</span>
              <span class="trust-badge excellent">95%</span>
            </div>
            <div class="trust-item">
              <span class="trust-label">Leakage Risk:</span>
              <span class="trust-badge low">Low</span>
            </div>
          </div>
        </div>

        <div class="lineage-chips">
          <h4>Lineage</h4>
          <div class="chip-group">
            <div class="lineage-chip" title="Matrix SHA">
              <span class="chip-label">matrix_sha</span>
              <span class="chip-value">a1b2c3d4</span>
              <button class="chip-copy">📋</button>
            </div>
            <div class="lineage-chip" title="Config SHA">
              <span class="chip-label">config_sha</span>
              <span class="chip-value">e5f6g7h8</span>
              <button class="chip-copy">📋</button>
            </div>
            <div class="lineage-chip" title="Policy SHA">
              <span class="chip-label">policy_sha</span>
              <span class="chip-value">i9j0k1l2</span>
              <button class="chip-copy">📋</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderSweepsTab(modelId) {
  return `
    <div class="sweeps-tab">
      <div class="sweeps-content">
        <div class="sweeps-controls">
          <h3 class="section-title">Sweep Configuration</h3>
          <div class="control-grid">
            <div class="form-field">
              <label for="threshold-variants">Threshold Variants</label>
              <input type="text" id="threshold-variants" value="0.6, 0.7, 0.8" placeholder="0.6, 0.7, 0.8">
            </div>
            <div class="form-field">
              <label for="hours-variants">Allowed Hours</label>
              <input type="text" id="hours-variants" value="13, 14, 15" placeholder="13, 14, 15">
            </div>
            <div class="form-field">
              <label for="top-pct-variants">Top % Variants</label>
              <input type="text" id="top-pct-variants" value="5, 10, 15" placeholder="5, 10, 15">
            </div>
          </div>
        </div>

        <div class="risk-envelope">
          <h3 class="section-title">Risk Envelope</h3>
          <div class="envelope-grid">
            <div class="form-field">
              <label for="min-trades">Min Trades</label>
              <input type="number" id="min-trades" value="50">
            </div>
            <div class="form-field">
              <label for="max-drawdown">Max Drawdown %</label>
              <input type="number" id="max-drawdown" value="15" step="0.1">
            </div>
            <div class="form-field">
              <label for="es95-mult">ES95 Multiplier</label>
              <input type="number" id="es95-mult" value="2.0" step="0.1">
            </div>
            <div class="form-field">
              <label for="min-fill-rate">Min Fill Rate %</label>
              <input type="number" id="min-fill-rate" value="85">
            </div>
          </div>
        </div>

        <div class="sweep-actions">
          <button class="btn btn-primary" id="run-sweep-btn">
            <span class="icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5,3 19,12 5,21"/>
              </svg>
            </span>
            Run Sweep
          </button>
          <button class="btn btn-secondary">Reset to Defaults</button>
        </div>

        <div class="sweep-results" id="sweep-results">
          <h3 class="section-title">Results (12 configurations)</h3>
          <div class="results-table">
            <table>
              <thead>
                <tr>
                  <th>Threshold</th>
                  <th>Hours</th>
                  <th>Sharpe</th>
                  <th>Return %</th>
                  <th>Trades</th>
                  <th>Gate</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>0.7</td>
                  <td>13-15</td>
                  <td>1.24</td>
                  <td>8.7%</td>
                  <td>234</td>
                  <td><span class="gate-badge pass">Pass</span></td>
                  <td>
                    <button class="btn btn-small">Add to Cart</button>
                    <button class="btn btn-small">CSV</button>
                  </td>
                </tr>
                <tr>
                  <td>0.8</td>
                  <td>14-15</td>
                  <td>1.12</td>
                  <td>6.8%</td>
                  <td>156</td>
                  <td><span class="gate-badge pass">Pass</span></td>
                  <td>
                    <button class="btn btn-small">Add to Cart</button>
                    <button class="btn btn-small">CSV</button>
                  </td>
                </tr>
                <tr>
                  <td>0.6</td>
                  <td>13-15</td>
                  <td>0.89</td>
                  <td>12.3%</td>
                  <td>412</td>
                  <td><span class="gate-badge fail">Fail</span></td>
                  <td>
                    <button class="btn btn-small disabled">Add to Cart</button>
                    <button class="btn btn-small">CSV</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderLeaderboardTab(modelId) {
  return `
    <div class="leaderboard-tab">
      <div class="leaderboard-controls">
        <div class="control-row">
          <div class="filters">
            <label>
              <input type="checkbox" id="pass-gate-only" checked>
              Pass Gate Only
            </label>
            <select id="sort-by">
              <option value="sharpe">Sort by Sharpe</option>
              <option value="return">Sort by Return</option>
              <option value="trades">Sort by Trades</option>
            </select>
          </div>
          <div class="batch-actions">
            <button class="btn btn-secondary" id="compare-selected">Compare Selected</button>
            <button class="btn btn-primary" id="train-selected">Train Selected</button>
          </div>
        </div>
      </div>

      <div class="leaderboard-table">
        <table>
          <thead>
            <tr>
              <th><input type="checkbox" id="select-all"></th>
              <th>Started At</th>
              <th>Config</th>
              <th>Sharpe</th>
              <th>Return %</th>
              <th>Trades</th>
              <th>Win Rate</th>
              <th>Gate</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><input type="checkbox" class="row-select"></td>
              <td>Aug 15, 14:23</td>
              <td>thr:0.7, hrs:13-15</td>
              <td>1.24</td>
              <td>8.7%</td>
              <td>234</td>
              <td>67%</td>
              <td><span class="gate-badge pass">Pass</span></td>
              <td>
                <button class="btn btn-small">View</button>
                <button class="btn btn-small">Add to Cart</button>
              </td>
            </tr>
            <tr>
              <td><input type="checkbox" class="row-select"></td>
              <td>Aug 15, 14:18</td>
              <td>thr:0.8, hrs:14-15</td>
              <td>1.12</td>
              <td>6.8%</td>
              <td>156</td>
              <td>71%</td>
              <td><span class="gate-badge pass">Pass</span></td>
              <td>
                <button class="btn btn-small">View</button>
                <button class="btn btn-small">Add to Cart</button>
              </td>
            </tr>
            <tr>
              <td><input type="checkbox" class="row-select"></td>
              <td>Aug 15, 14:15</td>
              <td>thr:0.75, hrs:13-14</td>
              <td>1.08</td>
              <td>7.2%</td>
              <td>189</td>
              <td>69%</td>
              <td><span class="gate-badge pass">Pass</span></td>
              <td>
                <button class="btn btn-small">View</button>
                <button class="btn btn-small">Add to Cart</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderTrainTab(modelId) {
  return `
    <div class="train-tab">
      <div class="selected-configs">
        <h3 class="section-title">Selected Configurations (3)</h3>
        <div class="configs-table">
          <table>
            <thead>
              <tr>
                <th>Model ID</th>
                <th>Matrix SHA</th>
                <th>Config</th>
                <th>Risk Profile</th>
                <th>Gate Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>${modelId}</td>
                <td>a1b2c3d4</td>
                <td>thr:0.7, hrs:13-15</td>
                <td><span class="risk-chip balanced">Balanced</span></td>
                <td><span class="gate-badge pass">Pass</span></td>
                <td><button class="btn btn-small">Remove</button></td>
              </tr>
              <tr>
                <td>${modelId}</td>
                <td>a1b2c3d4</td>
                <td>thr:0.8, hrs:14-15</td>
                <td><span class="risk-chip balanced">Balanced</span></td>
                <td><span class="gate-badge pass">Pass</span></td>
                <td><button class="btn btn-small">Remove</button></td>
              </tr>
              <tr>
                <td>${modelId}</td>
                <td>a1b2c3d4</td>
                <td>thr:0.75, hrs:13-14</td>
                <td><span class="risk-chip balanced">Balanced</span></td>
                <td><span class="gate-badge pass">Pass</span></td>
                <td><button class="btn btn-small">Remove</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="training-options">
        <h3 class="section-title">Training Options</h3>
        <div class="options-grid">
          <div class="form-field">
            <label for="algorithm">Algorithm</label>
            <select id="algorithm">
              <option value="gbm" selected>Gradient Boosting</option>
              <option value="rf">Random Forest</option>
              <option value="nn">Neural Network</option>
            </select>
          </div>
          <div class="form-field">
            <label for="concurrency">Concurrency</label>
            <input type="number" id="concurrency" value="2" min="1" max="4">
          </div>
          <div class="form-field">
            <label for="seed">Random Seed</label>
            <input type="number" id="seed" value="42">
          </div>
          <div class="form-field">
            <label for="tag">Tag</label>
            <input type="text" id="tag" placeholder="experiment_v1">
          </div>
        </div>
      </div>

      <div class="queue-summary">
        <h3 class="section-title">Queue Summary</h3>
        <div class="summary-content">
          <div class="summary-item">
            <span class="label">Jobs to Start:</span>
            <span class="value">3</span>
          </div>
          <div class="summary-item">
            <span class="label">Estimated Duration:</span>
            <span class="value">~45 minutes</span>
          </div>
          <div class="summary-item">
            <span class="label">Total Cores:</span>
            <span class="value">6</span>
          </div>
        </div>
      </div>

      <div class="train-actions">
        <button class="btn btn-primary" id="start-training-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5,3 19,12 5,21"/>
            </svg>
          </span>
          Start Training
        </button>
        <button class="btn btn-secondary">Clear Selection</button>
      </div>

      <div class="training-progress" id="training-progress" style="display: none;">
        <h3 class="section-title">Training Progress</h3>
        <div class="progress-list">
          <div class="progress-item">
            <span class="job-config">thr:0.7, hrs:13-15</span>
            <div class="progress-bar">
              <div class="progress-fill" style="width: 65%"></div>
            </div>
            <span class="progress-text">65% - Training...</span>
          </div>
        </div>
      </div>
    </div>
  `;
}