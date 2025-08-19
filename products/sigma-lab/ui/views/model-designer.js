export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <div class="breadcrumb">
        <a href="#/models">Models</a> / <span>Designer</span>
      </div>
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
          </svg>
        </span>
        Model Designer
      </h1>
      <div class="header-actions">
        <button class="btn btn-secondary" id="save-draft-btn">Save Draft</button>
        <button class="btn btn-primary" id="save-and-build-btn">Save & Build Matrix</button>
      </div>
    </div>

    <div class="page-content">
      <div class="designer-layout">
        <div class="designer-main">
          <div class="design-section">
            <h3 class="section-title">Model Configuration</h3>
            <div class="form-grid">
              <div class="form-field">
                <label for="model-name">Model Name</label>
                <input type="text" id="model-name" value="spy_opt_0dte_v2" placeholder="Enter model name">
              </div>
              <div class="form-field">
                <label for="model-pack">Pack</label>
                <select id="model-pack">
                  <option value="zerosigma" selected>ZeroSigma</option>
                  <option value="swingsigma">SwingSigma</option>
                  <option value="longsigma">LongSigma</option>
                  <option value="overnightsigma">OvernightSigma</option>
                  <option value="momentumsigma">MomentumSigma</option>
                </select>
              </div>
              <div class="form-field">
                <label for="model-description">Description</label>
                <textarea id="model-description" placeholder="Describe your model's strategy and purpose">SPY 0DTE options model using intraday momentum and IV signals</textarea>
              </div>
            </div>
          </div>

          <div class="design-section">
            <h3 class="section-title">Indicator Set</h3>
            <div class="indicator-builder">
              <div class="indicator-categories">
                <div class="category-tab active" data-category="price">Price Action</div>
                <div class="category-tab" data-category="volatility">Volatility</div>
                <div class="category-tab" data-category="volume">Volume</div>
                <div class="category-tab" data-category="options">Options</div>
                <div class="category-tab" data-category="time">Time-based</div>
              </div>
              
              <div class="indicator-content">
                <div class="available-indicators">
                  <h4>Available Indicators</h4>
                  <div class="indicator-list">
                    <div class="indicator-item" data-indicator="ema">
                      <span class="indicator-name">EMA</span>
                      <span class="indicator-desc">Exponential Moving Average</span>
                      <button class="add-indicator">+</button>
                    </div>
                    <div class="indicator-item" data-indicator="rsi">
                      <span class="indicator-name">RSI</span>
                      <span class="indicator-desc">Relative Strength Index</span>
                      <button class="add-indicator">+</button>
                    </div>
                    <div class="indicator-item" data-indicator="atr">
                      <span class="indicator-name">ATR</span>
                      <span class="indicator-desc">Average True Range</span>
                      <button class="add-indicator">+</button>
                    </div>
                    <div class="indicator-item" data-indicator="vwap">
                      <span class="indicator-name">VWAP</span>
                      <span class="indicator-desc">Volume Weighted Average Price</span>
                      <button class="add-indicator">+</button>
                    </div>
                  </div>
                </div>
                
                <div class="selected-indicators">
                  <h4>Selected Indicators (5)</h4>
                  <div class="selected-list">
                    <div class="selected-indicator">
                      <span class="indicator-name">EMA(20)</span>
                      <div class="indicator-params">
                        <input type="number" value="20" min="1" max="200">
                      </div>
                      <button class="remove-indicator">×</button>
                    </div>
                    <div class="selected-indicator">
                      <span class="indicator-name">RSI(14)</span>
                      <div class="indicator-params">
                        <input type="number" value="14" min="2" max="50">
                      </div>
                      <button class="remove-indicator">×</button>
                    </div>
                    <div class="selected-indicator">
                      <span class="indicator-name">ATR(14)</span>
                      <div class="indicator-params">
                        <input type="number" value="14" min="2" max="50">
                      </div>
                      <button class="remove-indicator">×</button>
                    </div>
                    <div class="selected-indicator">
                      <span class="indicator-name">VWAP</span>
                      <div class="indicator-params">
                        <span class="param-note">No parameters</span>
                      </div>
                      <button class="remove-indicator">×</button>
                    </div>
                    <div class="selected-indicator">
                      <span class="indicator-name">Options IV</span>
                      <div class="indicator-params">
                        <select>
                          <option>ATM</option>
                          <option>30 Delta</option>
                        </select>
                      </div>
                      <button class="remove-indicator">×</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="design-section">
            <h3 class="section-title">Policy Configuration</h3>
            <div class="policy-builder">
              <div class="form-grid">
                <div class="form-field">
                  <label for="policy-type">Policy Type</label>
                  <select id="policy-type">
                    <option value="threshold" selected>Threshold-based</option>
                    <option value="top_n">Top N%</option>
                    <option value="hybrid">Hybrid</option>
                  </select>
                </div>
                <div class="form-field">
                  <label for="policy-horizon">Horizon</label>
                  <select id="policy-horizon">
                    <option value="intraday" selected>Intraday</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                  </select>
                </div>
                <div class="form-field">
                  <label for="policy-cadence">Cadence</label>
                  <select id="policy-cadence">
                    <option value="hourly" selected>Hourly</option>
                    <option value="daily">Daily</option>
                    <option value="on_signal">On Signal</option>
                  </select>
                </div>
              </div>
              
              <div class="policy-rules">
                <h4>Signal Rules</h4>
                <div class="rule-builder">
                  <div class="rule-item">
                    <span class="rule-desc">RSI &lt; 30 AND EMA_slope &gt; 0.5</span>
                    <button class="edit-rule">Edit</button>
                    <button class="remove-rule">×</button>
                  </div>
                  <div class="rule-item">
                    <span class="rule-desc">ATR &gt; 1.5 * ATR_20d</span>
                    <button class="edit-rule">Edit</button>
                    <button class="remove-rule">×</button>
                  </div>
                  <button class="btn btn-secondary add-rule">+ Add Rule</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="designer-sidebar">
          <div class="sidebar-section">
            <h4>Model Preview</h4>
            <div class="model-preview">
              <div class="preview-item">
                <span class="label">Features:</span>
                <span class="value">12</span>
              </div>
              <div class="preview-item">
                <span class="label">Indicators:</span>
                <span class="value">5</span>
              </div>
              <div class="preview-item">
                <span class="label">Rules:</span>
                <span class="value">2</span>
              </div>
              <div class="preview-item">
                <span class="label">Est. Matrix Size:</span>
                <span class="value">~45K rows</span>
              </div>
            </div>
          </div>

          <div class="sidebar-section">
            <h4>Validation</h4>
            <div class="validation-status">
              <div class="validation-item valid">
                <span class="validation-icon">✓</span>
                <span class="validation-text">Model name unique</span>
              </div>
              <div class="validation-item valid">
                <span class="validation-icon">✓</span>
                <span class="validation-text">Indicators compatible</span>
              </div>
              <div class="validation-item warning">
                <span class="validation-icon">⚠</span>
                <span class="validation-text">High memory usage</span>
              </div>
            </div>
          </div>

          <div class="sidebar-section">
            <h4>Recent Changes</h4>
            <div class="change-log">
              <div class="change-item">
                <span class="change-time">2m ago</span>
                <span class="change-desc">Added RSI indicator</span>
              </div>
              <div class="change-item">
                <span class="change-time">5m ago</span>
                <span class="change-desc">Updated policy horizon</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Add event listeners
  wrap.querySelector('#save-draft-btn').addEventListener('click', () => {
    alert('Draft saved! Changes saved locally.');
  });

  wrap.querySelector('#save-and-build-btn').addEventListener('click', () => {
    alert('Model saved! Redirecting to Composer to build matrix...');
    // In real implementation, would save and navigate to composer/build
  });

  return wrap;
}