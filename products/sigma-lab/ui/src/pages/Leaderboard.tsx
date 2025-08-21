import React, { useEffect, useState } from 'react'
import { apiService } from '../services/api'
import './Leaderboard.css'
import { ErrorBanner } from '../components/common/ErrorBanner'

interface LeaderboardEntry {
  model_id: string
  pack_id: string
  sharpe: number
  trades: number
  win_rate: number
  max_drawdown?: number
  cum_ret?: number
  gate?: {
    pass: boolean
    reasons?: string[]
  }
}

export const Leaderboard: React.FC = () => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState({
    pack: '',
    riskProfile: '',
    passGateOnly: false
  })
  const [selectedEntries, setSelectedEntries] = useState<Set<string>>(new Set())

  useEffect(() => {
    fetchLeaderboard()
  }, [filters])

  const fetchLeaderboard = async () => {
    try {
      setLoading(true)
      setError(null)
      const params: any = {}
      if (filters.pack) params.pack_id = filters.pack
      if (filters.riskProfile) params.risk_profile = filters.riskProfile
      if (filters.passGateOnly) params.pass_gate = true
      
      const response = await apiService.getLeaderboard(params)
      setEntries(response.data.rows || [])
    } catch (err: any) {
      console.error('Error fetching leaderboard:', err)
      setError(err?.message || 'Failed to fetch leaderboard')
    } finally {
      setLoading(false)
    }
  }

  const toggleSelection = (modelId: string) => {
    const newSelection = new Set(selectedEntries)
    if (newSelection.has(modelId)) {
      newSelection.delete(modelId)
    } else {
      newSelection.add(modelId)
    }
    setSelectedEntries(newSelection)
  }

  const handleBatchTrain = () => {
    console.log('Training models:', Array.from(selectedEntries))
    // Implement batch training
  }

  const handleExport = () => {
    console.log('Exporting leaderboard data')
    // Implement CSV export
  }

  return (
    <div className="leaderboard-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Leaderboard</h1>
          <p className="page-description">Compare and select backtest results across models</p>
        </div>
        <div className="page-actions">
          {selectedEntries.size > 0 && (
            <button className="btn btn-primary" onClick={handleBatchTrain}>
              🎯 Train Selected ({selectedEntries.size})
            </button>
          )}
          <button className="btn btn-secondary" onClick={handleExport}>
            📥 Export CSV
          </button>
        </div>
      </div>

      {error && (
        <div style={{ marginBottom: 12 }}>
          <ErrorBanner message={error} />
        </div>
      )}

      {/* Filters */}
      <div className="leaderboard-filters">
        <div className="filter-group">
          <label>Pack</label>
          <select 
            className="input select" 
            value={filters.pack}
            onChange={(e) => setFilters({...filters, pack: e.target.value})}
          >
            <option value="">All Packs</option>
            <option value="zerosigma">ZeroSigma</option>
            <option value="swingsigma">SwingSigma</option>
            <option value="longsigma">LongSigma</option>
            <option value="overnightsigma">OvernightSigma</option>
            <option value="momentumsigma">MomentumSigma</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>Risk Profile</label>
          <select 
            className="input select"
            value={filters.riskProfile}
            onChange={(e) => setFilters({...filters, riskProfile: e.target.value})}
          >
            <option value="">All Profiles</option>
            <option value="Conservative">Conservative</option>
            <option value="Balanced">Balanced</option>
            <option value="Aggressive">Aggressive</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="checkbox-label">
            <input 
              type="checkbox"
              checked={filters.passGateOnly}
              onChange={(e) => setFilters({...filters, passGateOnly: e.target.checked})}
            />
            Pass Gate Only
          </label>
        </div>

        <div className="filter-info">
          {selectedEntries.size > 0 && (
            <span className="selection-count">
              {selectedEntries.size} selected for training
            </span>
          )}
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="leaderboard-container">
        {loading ? (
          <div className="loading-container">
            <div className="spinner spinner-lg"></div>
            <p className="text-muted">Loading leaderboard...</p>
          </div>
        ) : entries.length === 0 ? (
          <div className="empty-state">
            <h3>No results found</h3>
            <p className="text-muted">Try adjusting your filters or run more backtests</p>
          </div>
        ) : (
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th className="checkbox-column">
                  <input 
                    type="checkbox"
                    checked={selectedEntries.size === entries.length && entries.length > 0}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedEntries(new Set(entries.map(e => e.model_id)))
                      } else {
                        setSelectedEntries(new Set())
                      }
                    }}
                  />
                </th>
                <th>Rank</th>
                <th>Model ID</th>
                <th>Pack</th>
                <th>Gate</th>
                <th>Sharpe</th>
                <th>Win Rate</th>
                <th>Trades</th>
                <th>Max DD</th>
                <th>Cum Return</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry, index) => (
                <tr key={entry.model_id} className={selectedEntries.has(entry.model_id) ? 'selected' : ''}>
                  <td className="checkbox-column">
                    <input 
                      type="checkbox"
                      checked={selectedEntries.has(entry.model_id)}
                      onChange={() => toggleSelection(entry.model_id)}
                    />
                  </td>
                  <td className="rank-column">
                    <div className={`rank-badge ${index < 3 ? 'top-rank' : ''}`}>
                      {index + 1}
                    </div>
                  </td>
                  <td className="model-column">
                    <span className="model-id">{entry.model_id}</span>
                  </td>
                  <td>
                    <span className={`badge badge-pack ${entry.pack_id}`}>
                      {entry.pack_id}
                    </span>
                  </td>
                  <td>
                    {entry.gate?.pass ? (
                      <span className="badge badge-success">✓ Pass</span>
                    ) : (
                      <div className="gate-fail">
                        <span className="badge badge-error">✗ Fail</span>
                        {entry.gate?.reasons && (
                          <div className="tooltip">
                            <span className="tooltip-content">
                              {entry.gate.reasons.join(', ')}
                            </span>
                          </div>
                        )}
                      </div>
                    )}
                  </td>
                  <td className={entry.sharpe > 1 ? 'metric-positive' : entry.sharpe < 0 ? 'metric-negative' : ''}>
                    {entry.sharpe.toFixed(2)}
                  </td>
                  <td className={entry.win_rate > 0.5 ? 'metric-positive' : 'metric-negative'}>
                    {(entry.win_rate * 100).toFixed(1)}%
                  </td>
                  <td>{entry.trades}</td>
                  <td className={entry.max_drawdown && entry.max_drawdown > -0.1 ? '' : 'metric-negative'}>
                    {entry.max_drawdown ? `${(entry.max_drawdown * 100).toFixed(1)}%` : '—'}
                  </td>
                  <td className={entry.cum_ret && entry.cum_ret > 0 ? 'metric-positive' : 'metric-negative'}>
                    {entry.cum_ret ? `${(entry.cum_ret * 100).toFixed(1)}%` : '—'}
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button className="btn btn-ghost btn-sm" title="View Details">
                        👁️
                      </button>
                      <button className="btn btn-ghost btn-sm" title="Train">
                        🎯
                      </button>
                      <button className="btn btn-ghost btn-sm" title="Compare">
                        📊
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Performance Summary */}
      {entries.length > 0 && (
        <div className="performance-summary">
          <h3>Performance Summary</h3>
          <div className="summary-stats">
            <div className="summary-stat">
              <span className="stat-label">Avg Sharpe</span>
              <span className="stat-value">
                {(entries.reduce((sum, e) => sum + e.sharpe, 0) / entries.length).toFixed(2)}
              </span>
            </div>
            <div className="summary-stat">
              <span className="stat-label">Avg Win Rate</span>
              <span className="stat-value">
                {(entries.reduce((sum, e) => sum + e.win_rate, 0) / entries.length * 100).toFixed(1)}%
              </span>
            </div>
            <div className="summary-stat">
              <span className="stat-label">Total Trades</span>
              <span className="stat-value">
                {entries.reduce((sum, e) => sum + e.trades, 0)}
              </span>
            </div>
            <div className="summary-stat">
              <span className="stat-label">Pass Rate</span>
              <span className="stat-value">
                {(entries.filter(e => e.gate?.pass).length / entries.length * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
