import { RECENT_MODELS, RECENT_RUNS, SYSTEM_HEALTH } from '../mocks/mock_data.js';

export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <line x1="12" y1="3" x2="12" y2="21"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
          </svg>
        </span>
        Dashboard
      </h1>
      <div class="header-actions">
        <button class="btn btn-primary" id="create-model-header-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </span>
          Create Model
        </button>
        <a class="btn btn-secondary" href="#/models">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="5,3 19,12 5,21"/>
            </svg>
          </span>
          Open Composer
        </a>
      </div>
    </div>

    <div class="dashboard-grid">
      <!-- Recent Models Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-title-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="2"/>
                <circle cx="5" cy="5" r="2"/>
                <circle cx="19" cy="5" r="2"/>
                <circle cx="5" cy="19" r="2"/>
                <circle cx="19" cy="19" r="2"/>
                <path d="M7 6l3 3"/>
                <path d="M14 9l3-3"/>
                <path d="M7 18l3-3"/>
                <path d="M14 15l3 3"/>
                <path d="M10 10l4 4"/>
                <path d="M10 14l4-4"/>
              </svg>
            </span>
            Recent Models
          </h3>
          <a href="#/models" class="section-link">
            <span class="icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15,3 21,3 21,9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </span>
            View All
          </a>
        </div>
        <div class="recent-models-list" id="recent-models">
          <!-- Models will be rendered here -->
        </div>
      </div>

      <!-- Last Runs Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-title-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12,6 12,12 16,14"/>
              </svg>
            </span>
            Last Runs
          </h3>
          <a href="#/models" class="section-link">
            <span class="icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15,3 21,3 21,9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </span>
            View All
          </a>
        </div>
        <div class="recent-runs-list" id="recent-runs">
          <!-- Runs will be rendered here -->
        </div>
      </div>

      <!-- Quick Actions Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-title-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6"/>
                <path d="m18.5 5.5-4.24 4.24m-4.52 4.52L5.5 18.5"/>
                <path d="m5.5 5.5 4.24 4.24m4.52 4.52L18.5 18.5"/>
              </svg>
            </span>
            Quick Actions
          </h3>
        </div>
        <div class="quick-actions-grid">
          <button class="quick-action-card" id="create-model-quick-btn">
            <span class="quick-action-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            </span>
            <span class="quick-action-label">Create Model</span>
          </button>
          <a href="#/models" class="quick-action-card">
            <span class="quick-action-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polygon points="10,8 16,12 10,16 10,8"/>
              </svg>
            </span>
            <span class="quick-action-label">Open Composer</span>
          </a>
          <a href="#/packs" class="quick-action-card">
            <span class="quick-action-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <path d="M3 9h18"/>
                <path d="M9 21V9"/>
              </svg>
            </span>
            <span class="quick-action-label">Explore Packs</span>
          </a>
          <a href="#/signals" class="quick-action-card">
            <span class="quick-action-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </span>
            <span class="quick-action-label">View Signals</span>
          </a>
        </div>
      </div>

      <!-- System Health Section -->
      <div class="dashboard-section">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-title-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </span>
            System Health
          </h3>
          <a href="#/health" class="section-link">
            <span class="icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15,3 21,3 21,9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </span>
            View Details
          </a>
        </div>
        <div class="system-health-grid" id="system-health">
          <!-- Health status will be rendered here -->
        </div>
      </div>
    </div>
  `;

  // Render Recent Models
  const recentModelsContainer = wrap.querySelector('#recent-models');
  const recentModelsHtml = RECENT_MODELS.map(model => {
    const algorithmBadge = getAlgorithmBadge(model.algorithm);
    const statusBadge = getStatusBadge(model.status);
    const timeAgo = getTimeAgo(model.updated_at);
    const priceChangeClass = model.price_change > 0 ? 'positive' : model.price_change < 0 ? 'negative' : 'neutral';
    const priceChangeSign = model.price_change > 0 ? '+' : '';
    
    return `
      <div class="recent-model-item">
        <div class="model-header-compact">
          <div class="model-id-compact">${model.model_id}</div>
          <div class="model-badges">
            ${algorithmBadge}
            ${statusBadge}
          </div>
        </div>
        <div class="model-details">
          <div class="ticker-price">
            <span class="ticker-symbol">${model.ticker}</span>
            <span class="current-price">$${model.current_price}</span>
            <span class="price-change ${priceChangeClass}">(${priceChangeSign}${model.price_change_pct.toFixed(2)}%)</span>
          </div>
          <div class="model-dataset">${model.dataset}</div>
          <div class="model-signal">${model.signal}</div>
          <div class="model-inputs">${model.inputs.join(', ')}</div>
        </div>
        <div class="model-footer">
          <span class="model-time">${timeAgo}</span>
          ${model.runtime ? `<span class="model-runtime">${model.runtime}</span>` : ''}
        </div>
      </div>
    `;
  }).join('');
  recentModelsContainer.innerHTML = recentModelsHtml;

  // Render Recent Runs
  const recentRunsContainer = wrap.querySelector('#recent-runs');
  const recentRunsHtml = RECENT_RUNS.map(run => {
    const typeBadge = getRunTypeBadge(run.type);
    const statusBadge = getStatusBadge(run.status);
    const timeAgo = getTimeAgo(run.started_at);
    const metricsHtml = getRunMetricsHtml(run);
    
    return `
      <div class="recent-run-item">
        <div class="run-header-compact">
          <div class="run-model-id">${run.model_id}</div>
          <div class="run-badges">
            ${typeBadge}
            ${statusBadge}
          </div>
        </div>
        <div class="run-metrics">
          ${metricsHtml}
        </div>
        <div class="run-footer">
          <span class="run-time">${timeAgo}</span>
        </div>
      </div>
    `;
  }).join('');
  recentRunsContainer.innerHTML = recentRunsHtml;

  // Render System Health
  const systemHealthContainer = wrap.querySelector('#system-health');
  const healthItems = ['api', 'database', 'data_coverage'];
  const healthLabels = { api: 'API', database: 'Database', data_coverage: 'Data Coverage' };
  const systemHealthHtml = healthItems.map(key => {
    const health = SYSTEM_HEALTH[key];
    const statusClass = getHealthStatusClass(health.status);
    const label = healthLabels[key];
    
    return `
      <div class="health-item">
        <div class="health-label">${label}</div>
        <div class="health-status ${statusClass}">${health.message}</div>
      </div>
    `;
  }).join('');
  systemHealthContainer.innerHTML = systemHealthHtml;

  // Create Model button event handlers
  function handleCreateModel() {
    window.location.hash = '#/models/new';
  }
  
  wrap.querySelector('#create-model-header-btn').addEventListener('click', handleCreateModel);
  wrap.querySelector('#create-model-quick-btn').addEventListener('click', handleCreateModel);

  return wrap;
}

function getAlgorithmBadge(algorithm) {
  const badgeClass = algorithm.toLowerCase();
  return `<span class="algorithm-badge ${badgeClass}">${algorithm}</span>`;
}

function getStatusBadge(status) {
  const statusClass = status === 'completed' ? 'status-success' :
                     status === 'running' || status === 'training' ? 'status-warning' :
                     status === 'queued' ? 'status-info' : 'status-default';
  return `<span class="status-badge ${statusClass}">${status}</span>`;
}

function getRunTypeBadge(type) {
  const typeColors = {
    backtest: 'type-backtest',
    train: 'type-train', 
    build: 'type-build',
    sweep: 'type-sweep'
  };
  return `<span class="run-type-badge ${typeColors[type] || 'type-default'}">${type}</span>`;
}

function getTimeAgo(dateStr) {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffHours < 1) return 'Just now';
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays === 1) return '1d ago';
  if (diffDays < 7) return `${diffDays}d ago`;
  return '1w ago';
}

function getHealthStatusClass(status) {
  return status === 'ok' ? 'status-success' :
         status === 'warning' ? 'status-warning' : 'status-error';
}

function getRunMetricsHtml(run) {
  const metrics = run.metrics;
  
  switch (run.type) {
    case 'backtest':
      return `
        <div class="metric-item">
          <span class="metric-label">Sharpe:</span>
          <span class="metric-value">${metrics.sharpe}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Return:</span>
          <span class="metric-value">${metrics.return}%</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Trades:</span>
          <span class="metric-value">${metrics.trades}</span>
        </div>
      `;
    case 'train':
      return `
        <div class="metric-item">
          <span class="metric-label">Accuracy:</span>
          <span class="metric-value">${metrics.accuracy}%</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">F1:</span>
          <span class="metric-value">${metrics.f1_score}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Time:</span>
          <span class="metric-value">${metrics.time_minutes}m</span>
        </div>
      `;
    case 'build':
      return `
        <div class="metric-item">
          <span class="metric-label">Features:</span>
          <span class="metric-value">${metrics.features}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Rows:</span>
          <span class="metric-value">${metrics.rows}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">NaN:</span>
          <span class="metric-value">${metrics.nan_percent}%</span>
        </div>
      `;
    case 'sweep':
      return `
        <div class="metric-item">
          <span class="metric-label">Progress:</span>
          <span class="metric-value">${metrics.progress}%</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">Combos:</span>
          <span class="metric-value">${metrics.combos_completed}/${metrics.combos_total}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">ETA:</span>
          <span class="metric-value">${metrics.eta_minutes}m</span>
        </div>
      `;
    default:
      return '';
  }
}
