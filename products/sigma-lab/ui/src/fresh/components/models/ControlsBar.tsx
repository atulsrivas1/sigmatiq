import React from 'react'
import { FreshIcon } from '../common/Icon'

export const FreshControlsBar: React.FC<{view: 'card'|'row'; setView: (v:'card'|'row')=>void;}> = ({ view, setView }) => {
  return (
    <div className="controls-bar">
      <div className="search-box">
        <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="M21 21l-4.35-4.35"/>
        </svg>
        <input className="search-input" placeholder="Search models..." />
      </div>

      <div className="filter-group">
        <select className="filter-select">
          <option>All Packs</option>
          <option>zerosigma</option>
          <option>swingsigma</option>
          <option>weeklysigma</option>
        </select>

        <select className="filter-select">
          <option>All Status</option>
          <option>Active</option>
          <option>Training</option>
          <option>Paused</option>
        </select>

        <select className="filter-select">
          <option>Sort: Updated</option>
          <option>Sort: Sharpe</option>
          <option>Sort: Return</option>
          <option>Sort: Trades</option>
        </select>
      </div>

      <div className="view-toggle">
        <button
          className={`view-option ${view==='card' ? 'active' : ''}`}
          onClick={() => setView('card')}
        >
          <FreshIcon name="grid" />
          <span>Cards</span>
        </button>
        <button
          className={`view-option ${view==='row' ? 'active' : ''}`}
          onClick={() => setView('row')}
        >
          <FreshIcon name="rows" />
          <span>Rows</span>
        </button>
      </div>
    </div>
  )
}
