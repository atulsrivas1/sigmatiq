import React from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import './Composer.css'

const ComposerBuild: React.FC = () => (
  <div className="composer-content">
    <h2>Build Matrix</h2>
    <p>Configure and build your training matrix.</p>
    <div className="placeholder-content">
      <p>Build interface implementation coming soon...</p>
    </div>
  </div>
)

const ComposerTrain: React.FC = () => (
  <div className="composer-content">
    <h2>Train Model</h2>
    <p>Configure training parameters and queue training jobs.</p>
    <div className="placeholder-content">
      <p>Train interface implementation coming soon...</p>
    </div>
  </div>
)

const ComposerBacktest: React.FC = () => (
  <div className="composer-content">
    <h2>Backtest</h2>
    <p>Run backtests and analyze results.</p>
    <div className="placeholder-content">
      <p>Backtest interface implementation coming soon...</p>
    </div>
  </div>
)

export const Composer: React.FC = () => {
  const location = useLocation()
  const currentPath = location.pathname.split('/').pop()

  return (
    <div className="composer-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Composer</h1>
          <p className="page-description">Build, Train, and Backtest pipeline</p>
        </div>
      </div>

      <div className="composer-tabs">
        <Link 
          to="/composer/build" 
          className={`composer-tab ${currentPath === 'build' || currentPath === 'composer' ? 'active' : ''}`}
        >
          🔨 Build
        </Link>
        <Link 
          to="/composer/train" 
          className={`composer-tab ${currentPath === 'train' ? 'active' : ''}`}
        >
          🎯 Train
        </Link>
        <Link 
          to="/composer/backtest" 
          className={`composer-tab ${currentPath === 'backtest' ? 'active' : ''}`}
        >
          📈 Backtest
        </Link>
      </div>

      <div className="composer-container">
        <Routes>
          <Route index element={<ComposerBuild />} />
          <Route path="build" element={<ComposerBuild />} />
          <Route path="train" element={<ComposerTrain />} />
          <Route path="backtest" element={<ComposerBacktest />} />
        </Routes>
      </div>
    </div>
  )
}