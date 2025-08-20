import React, { useState } from 'react'
import './Sweeps.css'

export const Sweeps: React.FC = () => {
  const [riskProfile, setRiskProfile] = useState<'Conservative' | 'Balanced' | 'Aggressive'>('Balanced')
  const [sweepType, setSweepType] = useState<'thresholds' | 'hours' | 'top_pct'>('thresholds')

  return (
    <div className="sweeps-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Sweeps</h1>
          <p className="page-description">Configuration grid backtesting for optimal parameters</p>
        </div>
        <div className="page-actions">
          <button className="btn btn-primary">
            ▶️ Run Sweep
          </button>
        </div>
      </div>

      <div className="sweeps-container">
        <div className="sweep-configuration">
          <h2>Configuration</h2>
          
          <div className="config-section">
            <h3>Risk Profile</h3>
            <div className="risk-selector">
              <button
                className={`risk-btn ${riskProfile === 'Conservative' ? 'active' : ''}`}
                onClick={() => setRiskProfile('Conservative')}
              >
                🛡️ Conservative
              </button>
              <button
                className={`risk-btn ${riskProfile === 'Balanced' ? 'active' : ''}`}
                onClick={() => setRiskProfile('Balanced')}
              >
                ⚖️ Balanced
              </button>
              <button
                className={`risk-btn ${riskProfile === 'Aggressive' ? 'active' : ''}`}
                onClick={() => setRiskProfile('Aggressive')}
              >
                🚀 Aggressive
              </button>
            </div>
          </div>

          <div className="config-section">
            <h3>Sweep Type</h3>
            <select 
              className="input select" 
              value={sweepType} 
              onChange={(e) => setSweepType(e.target.value as any)}
            >
              <option value="thresholds">Thresholds</option>
              <option value="hours">Allowed Hours</option>
              <option value="top_pct">Top Percentage</option>
            </select>
          </div>

          <div className="config-section">
            <h3>What-if Analysis</h3>
            <div className="what-if-panel">
              <p>Configure parameters to preview sweep impact</p>
              <div className="placeholder-content">
                What-if panel implementation coming soon...
              </div>
            </div>
          </div>
        </div>

        <div className="sweep-results">
          <h2>Results</h2>
          <div className="placeholder-content">
            <p>Run a sweep to see results here</p>
            <p>Results will include Gate badges, performance metrics, and export options</p>
          </div>
        </div>
      </div>
    </div>
  )
}