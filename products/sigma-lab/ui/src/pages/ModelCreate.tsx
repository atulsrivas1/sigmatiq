import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiService } from '../services/api'
import './ModelCreate.css'

interface Template {
  id: string
  name: string
  description: string
  pack: string
  horizon: string
  cadence: string
  icon: string
  recommended: boolean
}

const templates: Template[] = [
  {
    id: 'spy_opt_0dte_hourly',
    name: 'SPY 0DTE Options',
    description: 'Intraday options strategy for SPY with hourly signals',
    pack: 'zerosigma',
    horizon: '0DTE',
    cadence: 'Hourly',
    icon: '⚡',
    recommended: true
  },
  {
    id: 'spy_eq_swing_daily',
    name: 'SPY Swing Trading',
    description: 'Multi-day equity swing trades with daily signals',
    pack: 'swingsigma',
    horizon: '2-5 days',
    cadence: 'Daily',
    icon: '📊',
    recommended: false
  },
  {
    id: 'qqq_opt_0dte_hourly',
    name: 'QQQ 0DTE Options',
    description: 'Tech-focused intraday options with hourly signals',
    pack: 'zerosigma',
    horizon: '0DTE',
    cadence: 'Hourly',
    icon: '💻',
    recommended: false
  },
  {
    id: 'universe_eq_swing_scanner',
    name: 'Universe Scanner',
    description: 'Scan entire market for swing trade opportunities',
    pack: 'swingsigma',
    horizon: '2-10 days',
    cadence: 'Daily',
    icon: '🔍',
    recommended: false
  },
  {
    id: 'spy_eq_long_weekly',
    name: 'Long-term SPY',
    description: 'Position trades with weekly rebalancing',
    pack: 'longsigma',
    horizon: '30+ days',
    cadence: 'Weekly',
    icon: '🎯',
    recommended: false
  },
  {
    id: 'overnight_eq_gap',
    name: 'Overnight Gap Trading',
    description: 'Capture overnight gaps with pre-market signals',
    pack: 'overnightsigma',
    horizon: 'Overnight',
    cadence: 'Daily',
    icon: '🌙',
    recommended: false
  }
]

export const ModelCreate: React.FC = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null)
  const [modelName, setModelName] = useState('')
  const [riskProfile, setRiskProfile] = useState<'Conservative' | 'Balanced' | 'Aggressive'>('Balanced')
  const [creating, setCreating] = useState(false)

  const handleTemplateSelect = (template: Template) => {
    setSelectedTemplate(template)
    setModelName(`${template.id}_custom_${Date.now()}`)
  }

  const handleCreate = async () => {
    if (!selectedTemplate || !modelName) return

    try {
      setCreating(true)
      await apiService.createModel({
        template_id: selectedTemplate.id,
        name: modelName,
        risk_profile: riskProfile
      })
      
      // Navigate to the model designer or composer
      navigate(`/models/${modelName}/designer`)
    } catch (error) {
      console.error('Error creating model:', error)
      // In a real app, show error message
    } finally {
      setCreating(false)
    }
  }

  const renderStep1 = () => (
    <div className="wizard-step">
      <div className="step-header">
        <h2>Choose a Template</h2>
        <p className="text-muted">Select a pre-configured model template to get started quickly</p>
      </div>
      
      <div className="templates-grid">
        {templates.map(template => (
          <div
            key={template.id}
            className={`template-card ${selectedTemplate?.id === template.id ? 'selected' : ''}`}
            onClick={() => handleTemplateSelect(template)}
          >
            {template.recommended && (
              <div className="template-badge">Recommended</div>
            )}
            <div className="template-icon">{template.icon}</div>
            <div className="template-content">
              <h3 className="template-name">{template.name}</h3>
              <p className="template-description">{template.description}</p>
              <div className="template-meta">
                <span className="meta-item">
                  <span className="meta-label">Pack:</span>
                  <span className="badge badge-neutral">{template.pack}</span>
                </span>
                <span className="meta-item">
                  <span className="meta-label">Horizon:</span>
                  <span>{template.horizon}</span>
                </span>
                <span className="meta-item">
                  <span className="meta-label">Cadence:</span>
                  <span>{template.cadence}</span>
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="wizard-actions">
        <button className="btn btn-secondary" onClick={() => navigate('/models')}>
          Cancel
        </button>
        <button 
          className="btn btn-primary" 
          disabled={!selectedTemplate}
          onClick={() => setStep(2)}
        >
          Continue →
        </button>
      </div>
    </div>
  )

  const renderStep2 = () => (
    <div className="wizard-step">
      <div className="step-header">
        <h2>Configure Your Model</h2>
        <p className="text-muted">Name your model and select a risk profile</p>
      </div>

      <div className="config-form">
        <div className="form-group">
          <label htmlFor="model-name">Model Name</label>
          <input
            id="model-name"
            type="text"
            className="input"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            placeholder="Enter a unique model name"
          />
          <p className="form-hint">
            Use lowercase letters, numbers, and underscores only
          </p>
        </div>

        <div className="form-group">
          <label>Risk Profile</label>
          <div className="risk-options">
            <button
              className={`risk-option ${riskProfile === 'Conservative' ? 'selected' : ''}`}
              onClick={() => setRiskProfile('Conservative')}
            >
              <div className="risk-icon">🛡️</div>
              <div className="risk-details">
                <h4>Conservative</h4>
                <p>Lower risk, steady returns</p>
                <ul>
                  <li>Strict position sizing</li>
                  <li>Higher win rate targets</li>
                  <li>Tighter stop losses</li>
                </ul>
              </div>
            </button>
            
            <button
              className={`risk-option ${riskProfile === 'Balanced' ? 'selected' : ''}`}
              onClick={() => setRiskProfile('Balanced')}
            >
              <div className="risk-icon">⚖️</div>
              <div className="risk-details">
                <h4>Balanced</h4>
                <p>Moderate risk and returns</p>
                <ul>
                  <li>Standard position sizing</li>
                  <li>Balanced risk/reward</li>
                  <li>Adaptive stops</li>
                </ul>
              </div>
            </button>
            
            <button
              className={`risk-option ${riskProfile === 'Aggressive' ? 'selected' : ''}`}
              onClick={() => setRiskProfile('Aggressive')}
            >
              <div className="risk-icon">🚀</div>
              <div className="risk-details">
                <h4>Aggressive</h4>
                <p>Higher risk, higher returns</p>
                <ul>
                  <li>Larger position sizes</li>
                  <li>Higher leverage allowed</li>
                  <li>Wider stop losses</li>
                </ul>
              </div>
            </button>
          </div>
        </div>

        {selectedTemplate && (
          <div className="template-summary">
            <h3>Selected Template</h3>
            <div className="summary-card">
              <div className="summary-icon">{selectedTemplate.icon}</div>
              <div className="summary-details">
                <h4>{selectedTemplate.name}</h4>
                <p>{selectedTemplate.description}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="wizard-actions">
        <button className="btn btn-secondary" onClick={() => setStep(1)}>
          ← Back
        </button>
        <button 
          className="btn btn-primary" 
          disabled={!modelName || creating}
          onClick={() => setStep(3)}
        >
          Review & Create →
        </button>
      </div>
    </div>
  )

  const renderStep3 = () => (
    <div className="wizard-step">
      <div className="step-header">
        <h2>Review & Create</h2>
        <p className="text-muted">Confirm your model configuration</p>
      </div>

      <div className="review-container">
        <div className="review-section">
          <h3>Model Configuration</h3>
          <div className="review-items">
            <div className="review-item">
              <span className="review-label">Model Name:</span>
              <span className="review-value">{modelName}</span>
            </div>
            <div className="review-item">
              <span className="review-label">Template:</span>
              <span className="review-value">{selectedTemplate?.name}</span>
            </div>
            <div className="review-item">
              <span className="review-label">Pack:</span>
              <span className="badge badge-neutral">{selectedTemplate?.pack}</span>
            </div>
            <div className="review-item">
              <span className="review-label">Risk Profile:</span>
              <span className={`badge badge-${riskProfile.toLowerCase()}`}>
                {riskProfile === 'Conservative' && '🛡️'} 
                {riskProfile === 'Balanced' && '⚖️'} 
                {riskProfile === 'Aggressive' && '🚀'} 
                {riskProfile}
              </span>
            </div>
          </div>
        </div>

        <div className="next-steps">
          <h3>What happens next?</h3>
          <div className="steps-list">
            <div className="step-item">
              <div className="step-number">1</div>
              <div className="step-content">
                <h4>Model Designer</h4>
                <p>Configure indicators and policy settings</p>
              </div>
            </div>
            <div className="step-item">
              <div className="step-number">2</div>
              <div className="step-content">
                <h4>Composer</h4>
                <p>Build training matrix and run backtests</p>
              </div>
            </div>
            <div className="step-item">
              <div className="step-number">3</div>
              <div className="step-content">
                <h4>Deploy</h4>
                <p>Activate your model for live signals</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="wizard-actions">
        <button className="btn btn-secondary" onClick={() => setStep(2)}>
          ← Back
        </button>
        <button 
          className="btn btn-primary" 
          disabled={creating}
          onClick={handleCreate}
        >
          {creating ? (
            <>
              <span className="spinner"></span>
              Creating...
            </>
          ) : (
            '✅ Create Model'
          )}
        </button>
      </div>
    </div>
  )

  return (
    <div className="model-create-page">
      <div className="wizard-container">
        <div className="wizard-progress">
          <div className={`progress-step ${step >= 1 ? 'active' : ''}`}>
            <div className="progress-number">1</div>
            <div className="progress-label">Choose Template</div>
          </div>
          <div className={`progress-line ${step >= 2 ? 'active' : ''}`}></div>
          <div className={`progress-step ${step >= 2 ? 'active' : ''}`}>
            <div className="progress-number">2</div>
            <div className="progress-label">Configure</div>
          </div>
          <div className={`progress-line ${step >= 3 ? 'active' : ''}`}></div>
          <div className={`progress-step ${step >= 3 ? 'active' : ''}`}>
            <div className="progress-number">3</div>
            <div className="progress-label">Review & Create</div>
          </div>
        </div>

        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
      </div>
    </div>
  )
}