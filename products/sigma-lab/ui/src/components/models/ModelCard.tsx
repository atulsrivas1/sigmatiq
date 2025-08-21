import React from 'react'
import { FreshIcon } from '../common/FreshIcon'

export type ModelCardModel = {
  id: string
  title: string
  subtitle: string
  iconName: 'grid'|'cube'|'nodes'|'barChart'|'dollarSign'|'fileText'
  iconBg: string
  badge: string
  badgeClass: 'success'|'warning'|'error'
  stats: { label: string; value: string; trend?: 'positive'|'negative' }[]
  chart: 'g1'|'g2'|'line-red'|'line-teal'|'line-cream'
  updated: string
  risk: string
  actions: string[]
}

const Chart: React.FC<{ kind: ModelCardModel['chart'] }> = ({ kind }) => {
  if (kind === 'g1') {
    return (
      <svg className="mini-chart" viewBox="0 0 200 40">
        <defs>
          <linearGradient id="g1" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style={{ stopColor:'var(--sigmatiq-bright-teal)', stopOpacity:0.3 }} />
            <stop offset="100%" style={{ stopColor:'var(--sigmatiq-bright-teal)', stopOpacity:0 }} />
          </linearGradient>
        </defs>
        <path d="M 0 30 Q 40 25 80 20 T 160 10 L 200 8" stroke="var(--sigmatiq-bright-teal)" strokeWidth="1.5" fill="none"/>
        <path d="M 0 30 Q 40 25 80 20 T 160 10 L 200 8 L 200 40 L 0 40 Z" fill="url(#g1)"/>
      </svg>
    )
  }
  if (kind === 'g2') {
    return (
      <svg className="mini-chart" viewBox="0 0 200 40">
        <defs>
          <linearGradient id="g2" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style={{ stopColor:'var(--sigmatiq-golden)', stopOpacity:0.3 }} />
            <stop offset="100%" style={{ stopColor:'var(--sigmatiq-golden)', stopOpacity:0 }} />
          </linearGradient>
        </defs>
        <path d="M 0 25 Q 50 20 100 15 T 200 10" stroke="var(--sigmatiq-golden)" strokeWidth="1.5" fill="none"/>
        <path d="M 0 25 Q 50 20 100 15 T 200 10 L 200 40 L 0 40 Z" fill="url(#g2)"/>
      </svg>
    )
  }
  if (kind === 'line-red') {
    return (
      <svg className="mini-chart" viewBox="0 0 200 40">
        <path d="M 0 20 Q 50 25 100 30 T 200 25" stroke="var(--status-error)" strokeWidth="1.5" fill="none" strokeDasharray="2,2"/>
      </svg>
    )
  }
  if (kind === 'line-teal') {
    return (
      <svg className="mini-chart" viewBox="0 0 200 40">
        <path d="M 0 28 Q 50 22 100 18 T 200 12" stroke="var(--sigmatiq-bright-teal)" strokeWidth="1.5" fill="none"/>
      </svg>
    )
  }
  if (kind === 'line-cream') {
    return (
      <svg className="mini-chart" viewBox="0 0 200 40">
        <path d="M 0 20 Q 50 15 100 22 T 200 18" stroke="var(--sigmatiq-cream)" strokeWidth="1.5" fill="none"/>
      </svg>
    )
  }
  return null
}

export const ModelCard: React.FC<{ model: ModelCardModel; view: 'card'|'row' }> = ({ model, view }) => {
  return (
    <div className="model-card">
      <div className="card-header">
        <div className="card-icon" style={{ background: model.iconBg }}>
          <FreshIcon name={model.iconName} />
        </div>
        <div className="card-header-info">
          <div className="card-title">{model.title}</div>
          <div className="card-subtitle">{model.subtitle}</div>
        </div>
        <span className={`card-badge ${model.badgeClass}`}>{model.badge}</span>
      </div>

      <div className="card-content">
        <div className={`card-stats ${view==='row' ? 'row-stats' : ''}`}>
          {model.stats.map((s, i) => (
            <div className="stat-item" key={i}>
              <span className="stat-label">{s.label}</span>
              <span className={`stat-value ${s.trend==='positive' ? 'positive' : ''} ${s.trend==='negative' ? 'negative' : ''}`}>{s.value}</span>
            </div>
          ))}
        </div>

        <div className="card-chart">
          <Chart kind={model.chart} />
        </div>

        <div className="card-meta">
          <span>Updated {model.updated}</span>
          <span>Risk: {model.risk}</span>
        </div>
      </div>

      <div className="card-actions">
        {model.actions.map((a, i) => (
          <button className={`card-btn ${i===0 ? 'primary' : ''}`} key={i}>{a}</button>
        ))}
      </div>
    </div>
  )
}

