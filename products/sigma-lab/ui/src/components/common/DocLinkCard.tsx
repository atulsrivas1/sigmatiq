import React from 'react'

export const DocLinkCard: React.FC<{ href?: string; icon?: React.ReactNode; title: string; description?: string }>= ({ href='#', icon, title, description }) => {
  return (
    <a href={href} className="doc-link" style={{ textDecoration: 'none' }}>
      <div className="doc-icon" aria-hidden>{icon}</div>
      <div className="doc-title">{title}</div>
      {description && <div className="doc-description">{description}</div>}
    </a>
  )
}

