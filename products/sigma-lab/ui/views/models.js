import { MODELS } from '../mocks/mock_data.js';

// ... (renderModelCard function remains the same)

export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
        <h1 class="page-title"><span class="title-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M7 6l3 3"/><path d="M14 9l3-3"/><path d="M7 18l3-3"/><path d="M14 15l3 3"/><path d="M10 10l4 4"/><path d="M10 14l4-4"/></svg></span>Models</h1>
        <div class="header-actions">
            <button class="btn btn-primary" id="create-model-btn"><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></span><span>Create Model</span></button>
        </div>
    </div>
    <div class="filters-bar">
        <div class="filters-left">
            <div class="search-box">
                <input type="text" class="search-input" id="models-search" placeholder="Search models..." \/>
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="7"><\/circle>
                    <line x1="16.65" y1="16.65" x2="21" y2="21"><\/line>
                <\/svg>
            <\/div>
        <\/div>
        <div class="filters-right">
            <div class="filter-chip active" id="filter-all">All<\/div>
            <div class="filter-chip pack-badge zerosigma" id="filter-zerosigma">ZeroSigma<\/div>
            <div class="filter-chip pack-badge swingsigma" id="filter-swingsigma">SwingSigma<\/div>
            <div class="filter-chip pack-badge momentumsigma" id="filter-momentumsigma">MomentumSigma<\/div>
            <div class="filter-chip pack-badge longsigma" id="filter-longsigma">LongSigma<\/div>
        <\/div>
    <\/div>
    <div class="models-grid" id="models-grid">
    <\/div>
  `;
  // ... (rest of the models.js logic) ...

  const searchEl = wrap.querySelector('#models-search');
  const modelsGrid = wrap.querySelector('#models-grid');
  const filterChips = wrap.querySelectorAll('.filter-chip');

  let models = MODELS.slice();
  let currentFilter = 'all';

  function getTimeAgo(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffHours < 1) return 'Updated just now';
    if (diffHours < 24) return `Updated ${diffHours} hour${diffHours === 1 ? '' : 's'} ago`;
    if (diffDays === 1) return 'Updated 1 day ago';
    if (diffDays < 7) return `Updated ${diffDays} days ago`;
    return 'Updated 1 week ago';
  }

  function renderLoadingState() {
    modelsGrid.innerHTML = Array(6).fill(0).map(() => `
      <div class="model-card">
        <div class="model-header">
          <div class="loading-skeleton wide"></div>
          <div class="loading-skeleton medium"></div>
        </div>
        <div class="model-body">
          <div class="model-stats">
            <div class="stat-item">
              <div class="loading-skeleton narrow"></div>
              <div class="loading-skeleton narrow"></div>
            </div>
            <div class="stat-item">
              <div class="loading-skeleton narrow"></div>
              <div class="loading-skeleton narrow"></div>
            </div>
            <div class="stat-item">
              <div class="loading-skeleton narrow"></div>
              <div class="loading-skeleton narrow"></div>
            </div>
          </div>
        </div>
      </div>
    `).join('');
  }

  function renderEmptyState() {
    modelsGrid.innerHTML = `
      <div class="empty-state">
        <h3>No models found</h3>
        <p>Create your first model to get started with Sigma Lab</p>
        <button class="btn btn-primary" onclick="window.location.hash='#/models/new'">
          Create Model
        </button>
      </div>
    `;
  }

  function renderErrorState(error) {
    modelsGrid.innerHTML = `
      <div class="error-banner">
        <div class="error-banner-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        </div>
        <div class="error-banner-content">
          <div class="error-banner-title">Error loading models</div>
          <div class="error-banner-message">${error}</div>
        </div>
        <button class="btn btn-secondary" onclick="location.reload()">Retry</button>
      </div>
    `;
  }

  function renderModels(list) {
    if (list.length === 0) {
      renderEmptyState();
      return;
    }
    
    modelsGrid.innerHTML = list.map(model => {
      const timeAgo = getTimeAgo(model.updated_at);
      const priceChangeClass = model.price_change > 0 ? 'positive' : model.price_change < 0 ? 'negative' : 'neutral';
      const priceChangeSign = model.price_change > 0 ? '+' : '';
      
      return `
        <div class="model-card">
          <div class="model-header">
            <div class="model-id">${model.model_id}</div>
            <div class="model-meta">
              <span class="pack-badge ${model.pack_id}">${model.pack_id}</span>
              <span>${timeAgo}</span>
              <div class="ticker-price">
                <span class="ticker-symbol">${model.ticker}</span>
                <span class="current-price">$${model.current_price}</span>
                <span class="price-change ${priceChangeClass}">(${priceChangeSign}${model.price_change_pct.toFixed(2)}%)</span>
              </div>
            </div>
            <!-- Trust HUD -->
            <div class="trust-hud">
              <div class="trust-badge integrity ${model.trust?.integrity || 'ok'}" title="Data Integrity">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
              </div>
              <div class="trust-badge parity ${model.trust?.parity || 'ok'}" title="Model Parity">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4"/>
                  <circle cx="12" cy="12" r="10"/>
                </svg>
              </div>
              <div class="trust-badge capacity ${model.trust?.capacity || 'warn'}" title="Trade Capacity">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
              </div>
            </div>
            <!-- Lineage Chips -->
            <div class="lineage-chips">
              <button class="lineage-chip" title="Pack SHA: ${model.lineage?.pack_sha || 'abc123ef'}">
                pack_sha • ${(model.lineage?.pack_sha || 'abc123ef').substring(0, 7)}
              </button>
              <button class="lineage-chip" title="Config SHA: ${model.lineage?.config_sha || 'def456gh'}">
                config_sha • ${(model.lineage?.config_sha || 'def456gh').substring(0, 7)}
              </button>
              <button class="lineage-chip" title="Policy SHA: ${model.lineage?.policy_sha || 'ghi789ij'}">
                policy_sha • ${(model.lineage?.policy_sha || 'ghi789ij').substring(0, 7)}
              </button>
            </div>
          </div>
          <div class="model-body">
            <div class="model-stats">
              <div class="stat-item">
                <div class="stat-value">${model.sharpe || 'N/A'}</div>
                <div class="stat-label">Sharpe</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">${model.return || 'N/A'}</div>
                <div class="stat-label">Return</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">${model.trades || 'N/A'}</div>
                <div class="stat-label">Trades</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">PnL Trend</div>
                <div class="sparkline">
                  <svg viewBox="0 0 60 20" class="sparkline-svg">
                    <polyline points="2,18 12,14 22,10 32,12 42,8 52,6 58,4" 
                              stroke="var(--status-success)" 
                              stroke-width="1.5" 
                              fill="none"/>
                    <circle cx="58" cy="4" r="1.5" fill="var(--status-success)"/>
                  </svg>
                </div>
              </div>
            </div>
            <div class="model-actions">
              <button class="btn btn-primary"><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15,3 21,3 21,9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></span>Open</button>
              <button class="btn btn-secondary"><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5,3 19,12 5,21"/></svg></span>Backtest</button>
              <button class="btn btn-secondary"><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5,3 19,12 5,21"/></svg></span>Sweeps</button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  function applyFilters() {
    const query = (searchEl.value || '').toLowerCase();
    let filtered = models;

    // Apply pack filter
    if (currentFilter !== 'all') {
      filtered = filtered.filter(m => m.pack_id === currentFilter);
    }

    // Apply search filter
    if (query) {
      filtered = filtered.filter(m => m.model_id.toLowerCase().includes(query));
    }

    renderModels(filtered);
  }

  // Filter chip event listeners
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilter = chip.id.replace('filter-', '');
      applyFilters();
    });
  });

  searchEl.addEventListener('input', applyFilters);
  
  // Create Model button event handler
  wrap.querySelector('#create-model-btn').addEventListener('click', () => {
    window.location.hash = '#/models/new';
  });
  
  renderModels(models);
  return wrap;
}
