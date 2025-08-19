export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </span>
        System Health
      </h1>
      <div class="header-actions">
        <button class="btn btn-secondary" id="refresh-health-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23,4 23,10 17,10"/>
              <polyline points="1,20 1,14 7,14"/>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10"/>
              <path d="M3.51 15a9 9 0 0 0 14.85 2.36L23 14"/>
            </svg>
          </span>
          Refresh
        </button>
        <button class="btn btn-primary" id="export-diagnostics-btn">
          <span class="icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7,10 12,15 17,10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
          </span>
          Export Diagnostics
        </button>
      </div>
    </div>

    <div class="page-content">
      <div class="health-overview">
        <div class="health-cards">
          <div class="health-card api-health">
            <div class="health-header">
              <div class="health-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="2" y1="12" x2="6" y2="12"/>
                  <line x1="18" y1="12" x2="22" y2="12"/>
                  <line x1="12" y1="6" x2="12" y2="2"/>
                  <line x1="12" y1="18" x2="12" y2="22"/>
                </svg>
              </div>
              <div class="health-title">
                <h3>API Health</h3>
                <span class="health-status good">Healthy</span>
              </div>
            </div>
            <div class="health-metrics">
              <div class="metric-item">
                <span class="metric-label">Response Time:</span>
                <span class="metric-value">45ms</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Success Rate:</span>
                <span class="metric-value">99.8%</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Uptime:</span>
                <span class="metric-value">99.95%</span>
              </div>
            </div>
          </div>

          <div class="health-card database-health">
            <div class="health-header">
              <div class="health-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <ellipse cx="12" cy="5" rx="9" ry="3"/>
                  <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                  <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
              </div>
              <div class="health-title">
                <h3>Database</h3>
                <span class="health-status good">Healthy</span>
              </div>
            </div>
            <div class="health-metrics">
              <div class="metric-item">
                <span class="metric-label">Connections:</span>
                <span class="metric-value">12/50</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Query Time:</span>
                <span class="metric-value">12ms avg</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Storage:</span>
                <span class="metric-value">68% used</span>
              </div>
            </div>
          </div>

          <div class="health-card data-health">
            <div class="health-header">
              <div class="health-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <line x1="3" y1="9" x2="21" y2="9"/>
                  <line x1="9" y1="21" x2="9" y2="9"/>
                </svg>
              </div>
              <div class="health-title">
                <h3>Data Coverage</h3>
                <span class="health-status warning">Warning</span>
              </div>
            </div>
            <div class="health-metrics">
              <div class="metric-item">
                <span class="metric-label">SPY Coverage:</span>
                <span class="metric-value">99.2%</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Options Data:</span>
                <span class="metric-value">96.8%</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Last Update:</span>
                <span class="metric-value">2 hours ago</span>
              </div>
            </div>
          </div>

          <div class="health-card workers-health">
            <div class="health-header">
              <div class="health-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </div>
              <div class="health-title">
                <h3>Workers</h3>
                <span class="health-status good">Healthy</span>
              </div>
            </div>
            <div class="health-metrics">
              <div class="metric-item">
                <span class="metric-label">Active Workers:</span>
                <span class="metric-value">8/10</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">Queue Depth:</span>
                <span class="metric-value">3 jobs</span>
              </div>
              <div class="metric-item">
                <span class="metric-label">CPU Usage:</span>
                <span class="metric-value">45%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="health-details">
        <div class="health-section">
          <h3 class="section-title">System Dependencies</h3>
          <div class="dependencies-table">
            <table>
              <thead>
                <tr>
                  <th>Service</th>
                  <th>Status</th>
                  <th>Version</th>
                  <th>Last Check</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>PostgreSQL</td>
                  <td><span class="status-badge good">Healthy</span></td>
                  <td>15.3</td>
                  <td>30s ago</td>
                  <td><button class="btn btn-small">Test Connection</button></td>
                </tr>
                <tr>
                  <td>Redis</td>
                  <td><span class="status-badge good">Healthy</span></td>
                  <td>7.2.1</td>
                  <td>30s ago</td>
                  <td><button class="btn btn-small">Test Connection</button></td>
                </tr>
                <tr>
                  <td>Polygon API</td>
                  <td><span class="status-badge good">Healthy</span></td>
                  <td>v3.12</td>
                  <td>1m ago</td>
                  <td><button class="btn btn-small">Test API</button></td>
                </tr>
                <tr>
                  <td>Alpaca API</td>
                  <td><span class="status-badge warning">Degraded</span></td>
                  <td>v2.8</td>
                  <td>5m ago</td>
                  <td><button class="btn btn-small">Test API</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="health-section">
          <h3 class="section-title">Data Freshness</h3>
          <div class="freshness-grid">
            <div class="freshness-item">
              <div class="freshness-header">
                <span class="freshness-label">SPY Minute Data</span>
                <span class="freshness-status fresh">Fresh</span>
              </div>
              <div class="freshness-details">
                <span class="freshness-time">Last: 5 minutes ago</span>
                <span class="freshness-coverage">Coverage: 99.8%</span>
              </div>
            </div>
            
            <div class="freshness-item">
              <div class="freshness-header">
                <span class="freshness-label">Options Chain</span>
                <span class="freshness-status stale">Stale</span>
              </div>
              <div class="freshness-details">
                <span class="freshness-time">Last: 2 hours ago</span>
                <span class="freshness-coverage">Coverage: 96.2%</span>
              </div>
            </div>
            
            <div class="freshness-item">
              <div class="freshness-header">
                <span class="freshness-label">Market Indicators</span>
                <span class="freshness-status fresh">Fresh</span>
              </div>
              <div class="freshness-details">
                <span class="freshness-time">Last: 1 minute ago</span>
                <span class="freshness-coverage">Coverage: 100%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="health-section">
          <h3 class="section-title">Recent Issues</h3>
          <div class="issues-list">
            <div class="issue-item warning">
              <div class="issue-icon">⚠️</div>
              <div class="issue-content">
                <div class="issue-title">Options data delayed</div>
                <div class="issue-description">Alpaca options feed experiencing 2+ hour delays</div>
                <div class="issue-time">Started 3 hours ago</div>
              </div>
              <div class="issue-actions">
                <button class="btn btn-small">View Details</button>
              </div>
            </div>
            
            <div class="issue-item resolved">
              <div class="issue-icon">✅</div>
              <div class="issue-content">
                <div class="issue-title">Database connection timeout</div>
                <div class="issue-description">Resolved by increasing connection pool size</div>
                <div class="issue-time">Resolved 6 hours ago</div>
              </div>
              <div class="issue-actions">
                <button class="btn btn-small">View Details</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Add event listeners
  wrap.querySelector('#refresh-health-btn').addEventListener('click', () => {
    alert('Refreshing health status...');
    // In real implementation, would refresh all health data
  });

  wrap.querySelector('#export-diagnostics-btn').addEventListener('click', () => {
    alert('Exporting diagnostics bundle...');
    // In real implementation, would trigger diagnostics export
  });

  return wrap;
}