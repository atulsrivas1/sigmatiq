// model-create.js - Multi-step Model Creation Wizard
import { 
  INDICATOR_SETS, 
  POLICY_TEMPLATES,
  TICKERS,
  ASSET_TYPES,
  HORIZONS,
  CADENCES
} from '../mocks/mock_data.js';

export function render() {
  const container = document.createElement('div');
  let currentStep = 1;
  let wizardData = {
    basics: {},
    indicators: {},
    policy: {},
    preview: {}
  };

  container.innerHTML = `
    <div class="wizard-container">
      <div class="page-header">
        <h1 class="page-title">
          <span class="title-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </span>
          Create Model
        </h1>
        <p class="page-description">5-step wizard to create a new trading model</p>
      </div>

      <!-- Progress Bar -->
      <div class="wizard-progress">
        <div class="progress-steps">
          <div class="step active" data-step="1">
            <div class="step-circle">1</div>
            <div class="step-label">Basics</div>
          </div>
          <div class="step-separator"></div>
          <div class="step" data-step="2">
            <div class="step-circle">2</div>
            <div class="step-label">Indicators</div>
          </div>
          <div class="step-separator"></div>
          <div class="step" data-step="3">
            <div class="step-circle">3</div>
            <div class="step-label">Policy</div>
          </div>
          <div class="step-separator"></div>
          <div class="step" data-step="4">
            <div class="step-circle">4</div>
            <div class="step-label">Preview</div>
          </div>
          <div class="step-separator"></div>
          <div class="step" data-step="5">
            <div class="step-circle">5</div>
            <div class="step-label">Save</div>
          </div>
        </div>
      </div>

      <!-- Step Content -->
      <div class="wizard-content">
        <!-- Step 1: Basics -->
        <div class="wizard-step" id="step-1">
          <div class="card">
            <h2 class="card-title">
              <span class="card-title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                </svg>
              </span>
              Model Basics
            </h2>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Ticker *</label>
                <select class="form-input" id="ticker-select" required>
                  <option value="">Select ticker...</option>
                  ${TICKERS.map(ticker => `<option value="${ticker}">${ticker}</option>`).join('')}
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Asset Type *</label>
                <select class="form-input" id="asset-type-select" required>
                  <option value="">Select asset type...</option>
                  ${ASSET_TYPES.map(type => `<option value="${type}">${type}</option>`).join('')}
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Horizon *</label>
                <select class="form-input" id="horizon-select" required>
                  <option value="">Select horizon...</option>
                  ${HORIZONS.map(horizon => `<option value="${horizon}">${horizon}</option>`).join('')}
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Cadence *</label>
                <select class="form-input" id="cadence-select" required>
                  <option value="">Select cadence...</option>
                  ${CADENCES.map(cadence => `<option value="${cadence}">${cadence}</option>`).join('')}
                </select>
              </div>
            </div>
            <div class="preview-section">
              <h3>Preview Model ID</h3>
              <div class="model-id-preview" id="model-id-preview">
                <em>Select fields above to generate model ID</em>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2: Indicators -->
        <div class="wizard-step" id="step-2" style="display: none;">
          <div class="card">
            <h2 class="card-title">
              <span class="card-title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
              </span>
              Indicator Set
            </h2>
            <div class="form-group">
              <label class="form-label">Indicator Set Template *</label>
              <select class="form-input" id="indicator-set-select" required>
                <option value="">Select indicator set...</option>
                ${INDICATOR_SETS.map(set => 
                  `<option value="${set.name}">${set.name} (${set.indicators.length} indicators)</option>`
                ).join('')}
              </select>
            </div>
            <div class="indicator-details" id="indicator-details">
              <h3>Indicators in Set</h3>
              <div class="indicator-list" id="indicator-list">
                <em>Select an indicator set to see details</em>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Policy -->
        <div class="wizard-step" id="step-3" style="display: none;">
          <div class="card">
            <h2 class="card-title">
              <span class="card-title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </span>
              Policy Configuration
            </h2>
            <div class="form-group">
              <label class="form-label">Policy Template *</label>
              <select class="form-input" id="policy-template-select" required>
                <option value="">Select policy template...</option>
                ${POLICY_TEMPLATES.map(template => 
                  `<option value="${template.name}">${template.name}</option>`
                ).join('')}
              </select>
            </div>
            <div class="policy-details" id="policy-details">
              <h3>Policy Parameters</h3>
              <div class="policy-params" id="policy-params">
                <em>Select a policy template to configure parameters</em>
              </div>
            </div>
            <div class="validation-status" id="validation-status">
              <!-- Validation results will appear here -->
            </div>
          </div>
        </div>

        <!-- Step 4: Preview -->
        <div class="wizard-step" id="step-4" style="display: none;">
          <div class="card">
            <h2 class="card-title">
              <span class="card-title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </span>
              Preview Matrix
            </h2>
            <div class="preview-controls">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">Preview Start Date</label>
                  <input type="date" class="form-input" id="preview-start-date" value="2024-01-01">
                </div>
                <div class="form-group">
                  <label class="form-label">Preview End Date</label>
                  <input type="date" class="form-input" id="preview-end-date" value="2024-01-31">
                </div>
                <div class="form-group">
                  <button class="btn btn-secondary" id="generate-preview-btn">Generate Preview</button>
                </div>
              </div>
            </div>
            <div class="preview-results" id="preview-results">
              <div class="metric-grid">
                <div class="metric-item">
                  <div class="metric-value" id="preview-features">-</div>
                  <div class="metric-label">Features</div>
                </div>
                <div class="metric-item">
                  <div class="metric-value" id="preview-rows">-</div>
                  <div class="metric-label">Rows</div>
                </div>
                <div class="metric-item">
                  <div class="metric-value" id="preview-coverage">-</div>
                  <div class="metric-label">Coverage</div>
                </div>
                <div class="metric-item">
                  <div class="metric-value" id="preview-nan-pct">-</div>
                  <div class="metric-label">NaN %</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 5: Save -->
        <div class="wizard-step" id="step-5" style="display: none;">
          <div class="card">
            <h2 class="card-title">
              <span class="card-title-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                  <polyline points="17,21 17,13 7,13 7,21"/>
                  <polyline points="7,3 7,8 15,8"/>
                </svg>
              </span>
              Save Model
            </h2>
            <div class="model-summary" id="model-summary">
              <h3>Model Summary</h3>
              <div class="summary-grid">
                <div class="summary-item">
                  <div class="summary-label">Model ID</div>
                  <div class="summary-value" id="final-model-id">-</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Pack</div>
                  <div class="summary-value" id="final-pack">-</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Indicators</div>
                  <div class="summary-value" id="final-indicators">-</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Policy</div>
                  <div class="summary-value" id="final-policy">-</div>
                </div>
              </div>
            </div>
            <div class="save-status" id="save-status">
              <!-- Save status will appear here -->
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="wizard-navigation">
        <button class="btn btn-secondary" id="prev-btn" disabled>Previous</button>
        <div class="step-info">
          Step <span id="current-step">1</span> of 5
        </div>
        <button class="btn btn-primary" id="next-btn">Next</button>
        <button class="btn btn-primary" id="save-btn" style="display: none;">Create Model</button>
      </div>
    </div>
  `;

  // Helper functions
  function updateStepIndicators() {
    container.querySelectorAll('.step').forEach((step, index) => {
      const stepNum = index + 1;
      step.classList.toggle('active', stepNum === currentStep);
      step.classList.toggle('completed', stepNum < currentStep);
    });
  }

  function showStep(step) {
    container.querySelectorAll('.wizard-step').forEach(s => s.style.display = 'none');
    container.querySelector(`#step-${step}`).style.display = 'block';
    
    const prevBtn = container.querySelector('#prev-btn');
    const nextBtn = container.querySelector('#next-btn');
    const saveBtn = container.querySelector('#save-btn');
    
    prevBtn.disabled = step === 1;
    
    if (step === 5) {
      nextBtn.style.display = 'none';
      saveBtn.style.display = 'inline-flex';
    } else {
      nextBtn.style.display = 'inline-flex';
      saveBtn.style.display = 'none';
    }
    
    updateStepIndicators();
    container.querySelector('#current-step').textContent = step;
  }

  function generateModelId() {
    const ticker = container.querySelector('#ticker-select').value;
    const assetType = container.querySelector('#asset-type-select').value;
    const horizon = container.querySelector('#horizon-select').value;
    const cadence = container.querySelector('#cadence-select').value;
    
    if (ticker && assetType && horizon && cadence) {
      const modelId = `${ticker.toLowerCase()}_${assetType.toLowerCase()}_${horizon.toLowerCase()}_${cadence.toLowerCase()}`;
      container.querySelector('#model-id-preview').innerHTML = `<code>${modelId}</code>`;
      return modelId;
    } else {
      container.querySelector('#model-id-preview').innerHTML = '<em>Select fields above to generate model ID</em>';
      return null;
    }
  }

  function validateStep(step) {
    switch(step) {
      case 1:
        return container.querySelector('#ticker-select').value &&
               container.querySelector('#asset-type-select').value &&
               container.querySelector('#horizon-select').value &&
               container.querySelector('#cadence-select').value;
      case 2:
        return container.querySelector('#indicator-set-select').value;
      case 3:
        return container.querySelector('#policy-template-select').value;
      case 4:
        return true; // Preview is optional
      case 5:
        return true;
      default:
        return false;
    }
  }

  // Event listeners
  container.addEventListener('change', function(e) {
    if (e.target.matches('#ticker-select, #asset-type-select, #horizon-select, #cadence-select')) {
      generateModelId();
      wizardData.basics = {
        ticker: container.querySelector('#ticker-select').value,
        assetType: container.querySelector('#asset-type-select').value,
        horizon: container.querySelector('#horizon-select').value,
        cadence: container.querySelector('#cadence-select').value,
        modelId: generateModelId()
      };
    }
    
    if (e.target.id === 'indicator-set-select') {
      const selectedSet = INDICATOR_SETS.find(set => set.name === e.target.value);
      if (selectedSet) {
        const indicatorList = container.querySelector('#indicator-list');
        indicatorList.innerHTML = selectedSet.indicators.map(ind => 
          `<div class="chip">${ind}</div>`
        ).join('');
        
        wizardData.indicators = {
          setName: selectedSet.name,
          indicators: selectedSet.indicators
        };
      }
    }
    
    if (e.target.id === 'policy-template-select') {
      const selectedPolicy = POLICY_TEMPLATES.find(p => p.name === e.target.value);
      if (selectedPolicy) {
        const policyParams = container.querySelector('#policy-params');
        policyParams.innerHTML = Object.entries(selectedPolicy.params).map(([key, value]) =>
          `<div class="param-item"><strong>${key}:</strong> ${value}</div>`
        ).join('');
        
        // Show validation status
        const validationStatus = container.querySelector('#validation-status');
        validationStatus.innerHTML = `
          <div class="validation-success">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20,6 9,17 4,12"/>
            </svg>
            Policy validation passed
          </div>
        `;
        
        wizardData.policy = {
          templateName: selectedPolicy.name,
          params: selectedPolicy.params
        };
      }
    }
  });

  container.querySelector('#prev-btn').addEventListener('click', () => {
    if (currentStep > 1) {
      currentStep--;
      showStep(currentStep);
    }
  });

  container.querySelector('#next-btn').addEventListener('click', () => {
    if (validateStep(currentStep) && currentStep < 5) {
      currentStep++;
      showStep(currentStep);
      
      // Update final summary on step 5
      if (currentStep === 5) {
        container.querySelector('#final-model-id').textContent = wizardData.basics.modelId || '-';
        container.querySelector('#final-pack').textContent = 'zeroedge'; // Default pack
        container.querySelector('#final-indicators').textContent = wizardData.indicators.setName || '-';
        container.querySelector('#final-policy').textContent = wizardData.policy.templateName || '-';
      }
    }
  });

  container.querySelector('#generate-preview-btn').addEventListener('click', () => {
    // Simulate preview generation
    container.querySelector('#preview-features').textContent = '42';
    container.querySelector('#preview-rows').textContent = '8,760';
    container.querySelector('#preview-coverage').textContent = '98.5%';
    container.querySelector('#preview-nan-pct').textContent = '1.5%';
  });

  container.querySelector('#save-btn').addEventListener('click', () => {
    const saveStatus = container.querySelector('#save-status');
    saveStatus.innerHTML = `
      <div class="save-progress">
        <div class="progress-bar">
          <div class="progress-fill" style="width: 100%; transition: width 2s ease;"></div>
        </div>
        <div class="save-steps">
          <div class="save-step completed">✓ Created model configuration</div>
          <div class="save-step completed">✓ Saved indicator set</div>
          <div class="save-step completed">✓ Generated policy file</div>
          <div class="save-step completed">✓ Model ready for training</div>
        </div>
      </div>
    `;
    
    setTimeout(() => {
      window.location.hash = '#/models';
    }, 3000);
  });

  // Initialize
  showStep(1);
  
  return container;
}