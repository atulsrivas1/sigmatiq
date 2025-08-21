import React from 'react'
import { FreshIcon } from '../common/FreshIcon'

export const Pagination: React.FC<{ total?: number }>= ({ total }) => {
  return (
    <div className="pagination-container">
      <div className="pagination-info">Showing 1-6 of {total ?? 42} models</div>
      <div className="pagination-controls">
        <button className="page-btn" disabled><FreshIcon name="chevronLeft" size={14} /></button>
        <button className="page-btn active">1</button>
        <button className="page-btn">2</button>
        <button className="page-btn">3</button>
        <button className="page-btn">4</button>
        <button className="page-btn">5</button>
        <button className="page-btn">6</button>
        <button className="page-btn">7</button>
        <button className="page-btn"><FreshIcon name="chevronRight" size={14} /></button>
      </div>
      <div style={{ display:'flex', alignItems:'center', gap:8 }}>
        <span style={{ fontSize: 13, color: 'var(--color-text-2)' }}>Items:</span>
        <select className="filter-select" style={{ padding: '8px 12px' }}>
          <option>6</option>
          <option>12</option>
          <option>24</option>
          <option>48</option>
        </select>
      </div>
    </div>
  )
}

