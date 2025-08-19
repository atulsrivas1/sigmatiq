import { OVERLAY_SAMPLE, MODELS } from '../mocks/mock_data.js';

export function render() {
  const container = document.createElement('div');
  container.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="2" y1="12" x2="6" y2="12"/>
            <line x1="18" y1="12" x2="22" y2="12"/>
            <line x1="12" y1="6" x2="12" y2="2"/>
            <line x1="12" y1="18" x2="12" y2="22"/>
          </svg>
        </span>
        Options Overlay
      </h1>
      <p class="page-description">Transform stock signals into options strategies with parity analysis</p>
    </div>

    <!-- Configuration Panel -->
    <div class="card">
      <h3 class="card-title">
        <span class="card-title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </span>
        Overlay Configuration
      </h3>
      
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Source Model *</label>
          <select class="form-input" id="overlay-model" required>
            <option value="">Select model...</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Signal Date *</label>
          <input type="date" class="form-input" id="overlay-date" required />
        </div>
        <div class="form-group">
          <label class="form-label">Strategy Mode</label>
          <select class="form-input" id="overlay-mode">
            <option value="single">Single Leg</option>
            <option value="vertical">Vertical Spread</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Expiry</label>
          <select class="form-input" id="overlay-expiry">
            <option value="">Select expiry...</option>
            <option value="2025-08-22">2025-08-22 (5 DTE)</option>
            <option value="2025-08-29">2025-08-29 (12 DTE)</option>
            <option value="2025-09-19">2025-09-19 (33 DTE)</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Target Delta</label>
          <input type="number" class="form-input" id="overlay-delta" value="0.30" min="0.05" max="0.95" step="0.05" />
        </div>
        <div class="form-group">
          <label class="form-label">Min Open Interest</label>
          <input type="number" class="form-input" id="overlay-min-oi" value="100" min="1" />
        </div>
      </div>
      
      <div class="form-actions">
        <button class="btn btn-primary" id="run-overlay">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5,3 19,12 5,21"/>
            </svg>
          </span>
          Generate Overlay
        </button>
        <button class="btn btn-secondary" id="reset-overlay">Reset</button>
      </div>
    </div>

    <!-- Results Section -->
    <div class="results-section" id="overlay-results-section" style="display: none;">
      <div class="results-header">
        <h2 class="results-title">
          <span class="results-title-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
            </svg>
          </span>
          Overlay Results
        </h2>
        <div class="results-actions">
          <button class="btn btn-secondary" id="export-overlay-csv">
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

      <!-- Parity Summary -->
      <div class="card">
        <h3 class="card-title">
          <span class="card-title-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
          </span>
          Parity Summary
        </h3>
        <div class="parity-summary" id="parity-summary">
          <div class="parity-metric">
            <div class="parity-value" id="overlay-count">0</div>
            <div class="parity-label">Options Found</div>
          </div>
          <div class="parity-metric">
            <div class="parity-value" id="avg-premium">$0.00</div>
            <div class="parity-label">Avg Premium</div>
          </div>
          <div class="parity-metric">
            <div class="parity-value" id="coverage-rate">0%</div>
            <div class="parity-label">Coverage Rate</div>
          </div>
          <div class="parity-metric">
            <div class="parity-value" id="avg-oi">0</div>
            <div class="parity-label">Avg OI</div>
          </div>
        </div>
      </div>

      <!-- Options Table -->
      <table class="results-table" id="overlay-table">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Strike</th>
            <th>Type</th>
            <th>Expiry</th>
            <th class="cell-right">Delta</th>
            <th class="cell-right">IV</th>
            <th class="cell-right">Bid</th>
            <th class="cell-right">Ask</th>
            <th class="cell-right">Volume</th>
            <th class="cell-right">OI</th>
            <th>OCC Symbol</th>
          </tr>
        </thead>
        <tbody id="overlay-tbody">
          <!-- Options will be rendered here -->
        </tbody>
      </table>
    </div>
  `;

  // Get all form elements
  const modelSelect = container.querySelector('#overlay-model');
  const dateInput = container.querySelector('#overlay-date');
  const modeSelect = container.querySelector('#overlay-mode');
  const expirySelect = container.querySelector('#overlay-expiry');
  const deltaInput = container.querySelector('#overlay-delta');
  const minOiInput = container.querySelector('#overlay-min-oi');
  
  // Get result elements
  const runBtn = container.querySelector('#run-overlay');
  const resetBtn = container.querySelector('#reset-overlay');
  const resultsSection = container.querySelector('#overlay-results-section');
  const tbody = container.querySelector('#overlay-tbody');
  
  // Summary elements
  const overlayCount = container.querySelector('#overlay-count');
  const avgPremium = container.querySelector('#avg-premium');
  const coverageRate = container.querySelector('#coverage-rate');
  const avgOi = container.querySelector('#avg-oi');

  // Populate model options
  modelSelect.innerHTML += MODELS.map(model => 
    `<option value="${model.model_id}">${model.model_id}</option>`
  ).join('');

  // Helper functions
  function formatCurrency(value) {
    return `$${parseFloat(value).toFixed(2)}`;
  }

  function formatPercent(value) {
    return `${(parseFloat(value) * 100).toFixed(1)}%`;
  }

  function getOptionTypeBadge(type) {
    const typeClass = type.toLowerCase() === 'call' ? 'option-call' : 'option-put';
    return `<span class="option-type-badge ${typeClass}">${type}</span>`;
  }

  function validateForm() {
    const model = modelSelect.value;
    const date = dateInput.value;
    
    if (!model || !date) {
      alert('Please select a model and date before generating overlay');
      return false;
    }
    return true;
  }

  function renderResults() {
    if (!validateForm()) return;

    // Show results section
    resultsSection.style.display = 'block';

    // Update summary metrics
    overlayCount.textContent = OVERLAY_SAMPLE.count;
    avgPremium.textContent = '$2.45';
    coverageRate.textContent = '87%';
    avgOi.textContent = '1,247';

    // Render options table
    const rows = OVERLAY_SAMPLE.rows.map(option => `
      <tr>
        <td>
          <span class="ticker-symbol">${option.ticker}</span>
        </td>
        <td>
          <span class="strike-price">$${option.strike}</span>
        </td>
        <td>${getOptionTypeBadge(option.type)}</td>
        <td>${option.expiry}</td>
        <td class="cell-right">${option.delta}</td>
        <td class="cell-right">${formatPercent(option.iv_used)}</td>
        <td class="cell-right">${formatCurrency(option.bid || '2.10')}</td>
        <td class="cell-right">${formatCurrency(option.ask || '2.15')}</td>
        <td class="cell-right">${option.volume || '147'}</td>
        <td class="cell-right">${option.open_interest || '1,247'}</td>
        <td>
          <code class="occ-symbol">${option.occ}</code>
        </td>
      </tr>
    `).join('');

    tbody.innerHTML = rows;

    // Scroll to results
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

  // Event listeners
  runBtn.addEventListener('click', renderResults);
  resetBtn.addEventListener('click', resetForm);
  
  container.querySelector('#export-overlay-csv').addEventListener('click', () => {
    alert('CSV export functionality will be implemented when connected to APIs');
  });

  // Set default date to today
  dateInput.value = new Date().toISOString().split('T')[0];

  return container;
}
