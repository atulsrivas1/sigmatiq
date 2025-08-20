import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiService } from '../services/api'
import './Models.css'

interface Model {
  id?: string
  model_id: string
  pack_id: string
  config?: any
  sharpe?: number
  trades?: number
  win_rate?: number
  updated_at?: string
}

export const Models: React.FC = () => {
  const [models, setModels] = useState<Model[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterPack, setFilterPack] = useState('')
  const [sortBy, setSortBy] = useState<'model_id' | 'pack_id' | 'sharpe' | 'updated_at'>('updated_at')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  useEffect(() => {
    fetchModels()
  }, [])

  const fetchModels = async () => {
    try {
      setLoading(true)
      const response = await apiService.getModels()
      setModels(response.data.models || [])
    } catch (error) {
      console.error('Error fetching models:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSort = (column: typeof sortBy) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('desc')
    }
  }

  const filteredModels = models.filter(model => {
    const matchesSearch = model.model_id.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesPack = !filterPack || model.pack_id === filterPack
    return matchesSearch && matchesPack
  })

  const sortedModels = [...filteredModels].sort((a, b) => {
    let aVal = a[sortBy] || ''
    let bVal = b[sortBy] || ''
    
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortOrder === 'asc' ? aVal - bVal : bVal - aVal
    }
    
    const comparison = String(aVal).localeCompare(String(bVal))
    return sortOrder === 'asc' ? comparison : -comparison
  })

  const uniquePacks = Array.from(new Set(models.map(m => m.pack_id)))

  return (
    <div className="models-page">
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Models</h1>
          <p className="page-description">Browse and manage your trading models</p>
        </div>
        <div className="page-actions">
          <Link to="/models/new" className="btn btn-primary">
            ➕ Create New Model
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-bar">
        <div className="filter-group">
          <input
            type="text"
            className="input"
            placeholder="Search models..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="filter-group">
          <select
            className="input select"
            value={filterPack}
            onChange={(e) => setFilterPack(e.target.value)}
          >
            <option value="">All Packs</option>
            {uniquePacks.map(pack => (
              <option key={pack} value={pack}>{pack}</option>
            ))}
          </select>
        </div>
        <div className="filter-info">
          Showing {sortedModels.length} of {models.length} models
        </div>
      </div>

      {/* Models Table */}
      <div className="card">
        {loading ? (
          <div className="loading-container">
            <div className="spinner spinner-lg"></div>
            <p className="text-muted">Loading models...</p>
          </div>
        ) : sortedModels.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🧠</div>
            <h3>No models found</h3>
            <p className="text-muted">
              {searchTerm || filterPack 
                ? 'Try adjusting your filters' 
                : 'Create your first model to get started'}
            </p>
            {!searchTerm && !filterPack && (
              <Link to="/models/new" className="btn btn-primary">
                Create Your First Model
              </Link>
            )}
          </div>
        ) : (
          <div className="table-container">
            <table className="table models-table">
              <thead>
                <tr>
                  <th onClick={() => handleSort('model_id')} className="sortable">
                    Model ID
                    {sortBy === 'model_id' && (
                      <span className="sort-indicator">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </th>
                  <th onClick={() => handleSort('pack_id')} className="sortable">
                    Pack
                    {sortBy === 'pack_id' && (
                      <span className="sort-indicator">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </th>
                  <th onClick={() => handleSort('sharpe')} className="sortable">
                    Sharpe
                    {sortBy === 'sharpe' && (
                      <span className="sort-indicator">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </th>
                  <th>Win Rate</th>
                  <th>Trades</th>
                  <th onClick={() => handleSort('updated_at')} className="sortable">
                    Updated
                    {sortBy === 'updated_at' && (
                      <span className="sort-indicator">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedModels.map((model) => (
                  <tr key={model.model_id}>
                    <td>
                      <Link to={`/models/${model.model_id}/designer`} className="model-link">
                        <span className="model-name">{model.model_id}</span>
                      </Link>
                    </td>
                    <td>
                      <span className={`badge badge-pack ${model.pack_id}`}>
                        {model.pack_id}
                      </span>
                    </td>
                    <td>
                      {model.sharpe ? (
                        <span className={`metric ${model.sharpe > 1 ? 'positive' : model.sharpe < 0 ? 'negative' : ''}`}>
                          {model.sharpe.toFixed(2)}
                        </span>
                      ) : (
                        <span className="text-dim">—</span>
                      )}
                    </td>
                    <td>
                      {model.win_rate ? (
                        <span className={`metric ${model.win_rate > 0.5 ? 'positive' : 'negative'}`}>
                          {(model.win_rate * 100).toFixed(0)}%
                        </span>
                      ) : (
                        <span className="text-dim">—</span>
                      )}
                    </td>
                    <td>
                      {model.trades || <span className="text-dim">—</span>}
                    </td>
                    <td>
                      <span className="text-muted">
                        {model.updated_at || 'Recently'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <Link 
                          to={`/models/${model.model_id}/designer`} 
                          className="btn btn-ghost btn-sm"
                          title="Open in Designer"
                        >
                          ✏️
                        </Link>
                        <Link 
                          to={`/composer/build?model=${model.model_id}`} 
                          className="btn btn-ghost btn-sm"
                          title="Open in Composer"
                        >
                          🎼
                        </Link>
                        <Link 
                          to={`/composer/backtest?model=${model.model_id}`} 
                          className="btn btn-ghost btn-sm"
                          title="Run Backtest"
                        >
                          📈
                        </Link>
                        <Link 
                          to={`/sweeps?model=${model.model_id}`} 
                          className="btn btn-ghost btn-sm"
                          title="Configure Sweep"
                        >
                          🔄
                        </Link>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Performance Sparklines (Optional Enhancement) */}
      <div className="models-insights">
        <div className="insight-card">
          <h3>Model Statistics</h3>
          <div className="stats-row">
            <div className="stat">
              <span className="stat-label">Total Models</span>
              <span className="stat-value">{models.length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Avg Sharpe</span>
              <span className="stat-value">
                {models.length > 0 
                  ? (models.reduce((sum, m) => sum + (m.sharpe || 0), 0) / models.length).toFixed(2)
                  : '—'}
              </span>
            </div>
            <div className="stat">
              <span className="stat-label">Active Packs</span>
              <span className="stat-value">{uniquePacks.length}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}