export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </span>
        Administration
      </h1>
      <div class="admin-badge">Admin Only</div>
    </div>

    <div class="page-content">
      <div class="admin-grid">
        <div class="admin-card" data-section="jobs">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
                <line x1="7" y1="2" x2="7" y2="22"/>
                <line x1="17" y1="2" x2="17" y2="22"/>
                <line x1="2" y1="12" x2="22" y2="12"/>
                <line x1="2" y1="7" x2="7" y2="7"/>
                <line x1="2" y1="17" x2="7" y2="17"/>
                <line x1="17" y1="17" x2="22" y2="17"/>
                <line x1="17" y1="7" x2="22" y2="7"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Jobs Management</h3>
              <p>Monitor, retry, and cancel training and sweep jobs</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">8 active</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Queue Depth:</span>
              <span class="stat-value">12</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Failed (24h):</span>
              <span class="stat-value">3</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Workers:</span>
              <span class="stat-value">8/10</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Manage Jobs</button>
          </div>
        </div>

        <div class="admin-card" data-section="quotas">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 6L9 17l-5-5"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Quotas & Limits</h3>
              <p>Manage per-user quotas and resource limits</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">5 users</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Avg Usage:</span>
              <span class="stat-value">68%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Quota Hits:</span>
              <span class="stat-value">2 (week)</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Overrides:</span>
              <span class="stat-value">1 active</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Manage Quotas</button>
          </div>
        </div>

        <div class="admin-card" data-section="risk-profiles">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Risk Profiles</h3>
              <p>Configure Conservative/Balanced/Aggressive presets</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">3 profiles</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Last Updated:</span>
              <span class="stat-value">2 days ago</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Version:</span>
              <span class="stat-value">v2.1</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Active:</span>
              <span class="stat-value">3/3</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Edit Profiles</button>
          </div>
        </div>

        <div class="admin-card" data-section="packs">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <path d="M3 9h18"/>
                <path d="M9 21V9"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Packs Manager</h3>
              <p>Manage packs, indicator sets, and metadata</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">5 packs</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Total Indicators:</span>
              <span class="stat-value">127</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Coverage Issues:</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Active Packs:</span>
              <span class="stat-value">4/5</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Manage Packs</button>
          </div>
        </div>

        <div class="admin-card" data-section="templates">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <line x1="9" y1="9" x2="15" y2="9"/>
                <line x1="9" y1="12" x2="15" y2="12"/>
                <line x1="9" y1="15" x2="13" y2="15"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Templates Manager</h3>
              <p>Create, edit, and publish model templates</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">14 templates</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Published:</span>
              <span class="stat-value">12</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Drafts:</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Usage (30d):</span>
              <span class="stat-value">45 models</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Manage Templates</button>
          </div>
        </div>

        <div class="admin-card" data-section="flags">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>
                <line x1="4" y1="22" x2="4" y2="15"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Feature Flags</h3>
              <p>Toggle experimental and optional features</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">8 flags</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Enabled:</span>
              <span class="stat-value">5</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Disabled:</span>
              <span class="stat-value">3</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Changed Today:</span>
              <span class="stat-value">1</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Manage Flags</button>
          </div>
        </div>

        <div class="admin-card" data-section="data-health">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Data Health</h3>
              <p>Monitor database, cache, and data pipeline health</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator warning">2 warnings</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">DB Status:</span>
              <span class="stat-value">Healthy</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Cache Hit Rate:</span>
              <span class="stat-value">94%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Data Lag:</span>
              <span class="stat-value">5 minutes</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">View Details</button>
          </div>
        </div>

        <div class="admin-card" data-section="audit">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Audit & Logs</h3>
              <p>View admin actions, system logs, and audit trail</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">123 today</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Actions (24h):</span>
              <span class="stat-value">45</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Errors (24h):</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Log Size:</span>
              <span class="stat-value">2.3 GB</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">View Logs</button>
          </div>
        </div>

        <div class="admin-card" data-section="users">
          <div class="admin-card-header">
            <div class="admin-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div class="admin-card-title">
              <h3>Users & Roles</h3>
              <p>Manage user accounts, roles, and API tokens</p>
            </div>
            <div class="admin-card-status">
              <span class="status-indicator">5 users</span>
            </div>
          </div>
          <div class="admin-card-stats">
            <div class="stat-item">
              <span class="stat-label">Admins:</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Editors:</span>
              <span class="stat-value">2</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Viewers:</span>
              <span class="stat-value">1</span>
            </div>
          </div>
          <div class="admin-card-actions">
            <button class="btn btn-primary">Manage Users</button>
          </div>
        </div>
      </div>

      <div class="admin-actions">
        <h3 class="section-title">Quick Actions</h3>
        <div class="quick-actions-row">
          <button class="btn btn-secondary" id="export-config-btn">Export System Config</button>
          <button class="btn btn-secondary" id="backup-data-btn">Backup Data</button>
          <button class="btn btn-secondary" id="clear-cache-btn">Clear Cache</button>
          <button class="btn btn-warning" id="restart-workers-btn">Restart Workers</button>
        </div>
      </div>
    </div>
  `;

  // Add event listeners for admin actions
  wrap.querySelector('#export-config-btn').addEventListener('click', () => {
    alert('Exporting system configuration...');
  });

  wrap.querySelector('#backup-data-btn').addEventListener('click', () => {
    if (confirm('Start data backup? This may take several minutes.')) {
      alert('Backup started. You will be notified when complete.');
    }
  });

  wrap.querySelector('#clear-cache-btn').addEventListener('click', () => {
    if (confirm('Clear all cache? This may temporarily slow down responses.')) {
      alert('Cache cleared successfully.');
    }
  });

  wrap.querySelector('#restart-workers-btn').addEventListener('click', () => {
    if (confirm('Restart all workers? This will cancel running jobs.')) {
      alert('Workers restarted. Jobs will resume shortly.');
    }
  });

  // Add event listeners for admin cards
  wrap.querySelectorAll('.admin-card').forEach(card => {
    card.addEventListener('click', () => {
      const section = card.dataset.section;
      alert(`Opening ${section} management interface...`);
      // In real implementation, would navigate to specific admin section
    });
  });

  return wrap;
}