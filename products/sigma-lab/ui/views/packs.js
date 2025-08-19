export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <path d="M3 9h18"/>
            <path d="M9 21V9"/>
          </svg>
        </span>
        Packs
      </h1>
      <div class="header-actions">
        <button class="btn btn-secondary" id="create-pack-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </span>
          Create Pack
        </button>
      </div>
    </div>

    <div class="page-content">
      <div class="packs-grid">
        <div class="pack-card" data-pack="zeroedge">
          <div class="pack-header">
            <div class="pack-icon zeroedge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="6"/>
                <circle cx="12" cy="12" r="2"/>
              </svg>
            </div>
            <div class="pack-info">
              <h3 class="pack-name">ZeroSigma</h3>
              <p class="pack-description">0DTE options strategies with intraday timing</p>
            </div>
            <div class="pack-status active">Active</div>
          </div>
          <div class="pack-stats">
            <div class="stat-item">
              <span class="stat-label">Models:</span>
              <span class="stat-value">12</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Templates:</span>
              <span class="stat-value">4</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Indicators:</span>
              <span class="stat-value">28</span>
            </div>
          </div>
          <div class="pack-actions">
            <a href="#/packs/zeroedge" class="btn btn-primary">Open Pack</a>
            <button class="btn btn-secondary">View Models</button>
          </div>
        </div>

        <div class="pack-card" data-pack="swingedge">
          <div class="pack-header">
            <div class="pack-icon swingedge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </div>
            <div class="pack-info">
              <h3 class="pack-name">SwingSigma</h3>
              <p class="pack-description">Multi-day swing trading with momentum signals</p>
            </div>
            <div class="pack-status active">Active</div>
          </div>
          <div class="pack-stats">
            <div class="stat-item">
              <span class="stat-label">Models:</span>
              <span class="stat-value">8</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Templates:</span>
              <span class="stat-value">3</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Indicators:</span>
              <span class="stat-value">24</span>
            </div>
          </div>
          <div class="pack-actions">
            <a href="#/packs/swingedge" class="btn btn-primary">Open Pack</a>
            <button class="btn btn-secondary">View Models</button>
          </div>
        </div>

        <div class="pack-card" data-pack="longedge">
          <div class="pack-header">
            <div class="pack-icon longedge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
              </svg>
            </div>
            <div class="pack-info">
              <h3 class="pack-name">LongSigma</h3>
              <p class="pack-description">Long-term position strategies</p>
            </div>
            <div class="pack-status active">Active</div>
          </div>
          <div class="pack-stats">
            <div class="stat-item">
              <span class="stat-label">Models:</span>
              <span class="stat-value">6</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Templates:</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Indicators:</span>
              <span class="stat-value">18</span>
            </div>
          </div>
          <div class="pack-actions">
            <a href="#/packs/longedge" class="btn btn-primary">Open Pack</a>
            <button class="btn btn-secondary">View Models</button>
          </div>
        </div>

        <div class="pack-card" data-pack="overnightedge">
          <div class="pack-header">
            <div class="pack-icon overnightedge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            </div>
            <div class="pack-info">
              <h3 class="pack-name">OvernightSigma</h3>
              <p class="pack-description">Overnight gap and momentum strategies</p>
            </div>
            <div class="pack-status beta">Beta</div>
          </div>
          <div class="pack-stats">
            <div class="stat-item">
              <span class="stat-label">Models:</span>
              <span class="stat-value">4</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Templates:</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Indicators:</span>
              <span class="stat-value">15</span>
            </div>
          </div>
          <div class="pack-actions">
            <a href="#/packs/overnightedge" class="btn btn-primary">Open Pack</a>
            <button class="btn btn-secondary">View Models</button>
          </div>
        </div>

        <div class="pack-card" data-pack="momentumedge">
          <div class="pack-header">
            <div class="pack-icon momentumedge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 20V10"/>
                <path d="M12 20V4"/>
                <path d="M6 20v-6"/>
              </svg>
            </div>
            <div class="pack-info">
              <h3 class="pack-name">MomentumSigma</h3>
              <p class="pack-description">Intraday momentum and breakout strategies</p>
            </div>
            <div class="pack-status active">Active</div>
          </div>
          <div class="pack-stats">
            <div class="stat-item">
              <span class="stat-label">Models:</span>
              <span class="stat-value">10</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Templates:</span>
              <span class="stat-value">3</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Indicators:</span>
              <span class="stat-value">22</span>
            </div>
          </div>
          <div class="pack-actions">
            <a href="#/packs/momentumedge" class="btn btn-primary">Open Pack</a>
            <button class="btn btn-secondary">View Models</button>
          </div>
        </div>
      </div>
    </div>
  `;

  // Add event listeners
  wrap.querySelector('#create-pack-btn').addEventListener('click', () => {
    alert('Pack creation coming soon! This is currently a mock interface.');
  });

  return wrap;
}