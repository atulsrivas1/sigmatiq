import React from 'react'
import { FreshIcon } from '../common/FreshIcon'

export type TemplateMeta = { label: string; value: string }

export const TemplateCard: React.FC<{
  icon?: 'grid'|'cube'|'nodes'|'barChart'|'dollarSign'|'fileText'
  name: string
  description?: string
  meta?: TemplateMeta[]
  tags?: string[]
  featured?: boolean
  onPrimary?: () => void
  onSecondary?: () => void
}> = ({ icon='barChart', name, description, meta=[], tags=[], featured, onPrimary, onSecondary }) => {
  return (
    <div className={`template-card${featured ? ' featured' : ''}`}>
      <div className="template-icon"><FreshIcon name={icon} size={24} /></div>
      <div className="template-name">{name}</div>
      {description && <div className="template-description">{description}</div>}
      {!!meta.length && (
        <div className="template-meta">
          {meta.map((m, i) => (
            <div className="template-meta-item" key={i}>
              <div className="template-meta-label">{m.label}</div>
              <div className="template-meta-value">{m.value}</div>
            </div>
          ))}
        </div>
      )}
      {!!tags.length && (
        <div className="template-tags">
          {tags.map((t, i) => (<span className="template-tag" key={i}>{t}</span>))}
        </div>
      )}
      <div className="template-actions">
        <button className="btn" onClick={onPrimary}>Use Template</button>
        <button className="btn" onClick={onSecondary}>View Details</button>
      </div>
    </div>
  )
}

export const TemplatesGrid: React.FC<{ children: React.ReactNode }>= ({ children }) => (
  <div className="templates-grid">{children}</div>
)

