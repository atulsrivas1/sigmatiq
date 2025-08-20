import React from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'

const SignalsLive: React.FC = () => (
  <div style={{ padding: '2rem' }}>
    <h2>Live Signals</h2>
    <p>Monitor real-time trading signals from your models.</p>
    <div style={{ marginTop: '2rem', padding: '2rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
      <p style={{ color: 'var(--color-text-3)' }}>Live signals interface coming soon...</p>
    </div>
  </div>
)

const SignalsLog: React.FC = () => (
  <div style={{ padding: '2rem' }}>
    <h2>Signal Log</h2>
    <p>Historical log of all signals with execution details.</p>
    <div style={{ marginTop: '2rem', padding: '2rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
      <p style={{ color: 'var(--color-text-3)' }}>Signal log interface coming soon...</p>
    </div>
  </div>
)

const SignalsAnalytics: React.FC = () => (
  <div style={{ padding: '2rem' }}>
    <h2>Signal Analytics</h2>
    <p>Performance analytics and visualizations for your signals.</p>
    <div style={{ marginTop: '2rem', padding: '2rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
      <p style={{ color: 'var(--color-text-3)' }}>Analytics interface coming soon...</p>
    </div>
  </div>
)

export const Signals: React.FC = () => {
  const location = useLocation()
  const currentPath = location.pathname.split('/').pop()

  return (
    <div style={{ padding: 'var(--spacing-lg)', maxWidth: '1400px', margin: '0 auto' }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">Signals</h1>
          <p className="page-description">Monitor and analyze trading signals</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', background: 'var(--color-surface-1)', padding: '4px', borderRadius: '12px' }}>
        <Link 
          to="/signals" 
          className={`btn ${currentPath === 'signals' ? 'btn-primary' : 'btn-ghost'}`}
          style={{ flex: 1 }}
        >
          🔴 Live
        </Link>
        <Link 
          to="/signals/log" 
          className={`btn ${currentPath === 'log' ? 'btn-primary' : 'btn-ghost'}`}
          style={{ flex: 1 }}
        >
          📜 Log
        </Link>
        <Link 
          to="/signals/analytics" 
          className={`btn ${currentPath === 'analytics' ? 'btn-primary' : 'btn-ghost'}`}
          style={{ flex: 1 }}
        >
          📊 Analytics
        </Link>
      </div>

      <div className="card">
        <Routes>
          <Route index element={<SignalsLive />} />
          <Route path="log" element={<SignalsLog />} />
          <Route path="analytics" element={<SignalsAnalytics />} />
        </Routes>
      </div>
    </div>
  )
}