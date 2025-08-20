import React from 'react'

export const Overlay: React.FC = () => {
  return (
    <div style={{ padding: 'var(--spacing-lg)', maxWidth: '1400px', margin: '0 auto' }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">Options Overlay</h1>
          <p className="page-description">Convert equity signals to options strategies</p>
        </div>
      </div>

      <div className="card">
        <div style={{ padding: '2rem' }}>
          <h2 style={{ marginBottom: '1rem' }}>Options Overlay Conversion</h2>
          <p style={{ color: 'var(--color-text-2)', marginBottom: '2rem' }}>
            Transform your equity trading signals into sophisticated options strategies with automatic strike selection, 
            expiration optimization, and risk management.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            <div style={{ padding: '1.5rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
              <div style={{ fontSize: '32px', marginBottom: '1rem' }}>🎯</div>
              <h3 style={{ marginBottom: '0.5rem' }}>Strike Selection</h3>
              <p style={{ fontSize: '13px', color: 'var(--color-text-3)' }}>
                Automatic strike price selection based on delta targets and market conditions
              </p>
            </div>

            <div style={{ padding: '1.5rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
              <div style={{ fontSize: '32px', marginBottom: '1rem' }}>📅</div>
              <h3 style={{ marginBottom: '0.5rem' }}>Expiration Optimization</h3>
              <p style={{ fontSize: '13px', color: 'var(--color-text-3)' }}>
                Smart expiration date selection based on signal horizon and volatility
              </p>
            </div>

            <div style={{ padding: '1.5rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
              <div style={{ fontSize: '32px', marginBottom: '1rem' }}>🛡️</div>
              <h3 style={{ marginBottom: '0.5rem' }}>Risk Management</h3>
              <p style={{ fontSize: '13px', color: 'var(--color-text-3)' }}>
                Built-in position sizing and Greeks-based risk controls
              </p>
            </div>
          </div>

          <div style={{ marginTop: '2rem', padding: '2rem', background: 'var(--color-surface-1)', borderRadius: '8px', textAlign: 'center' }}>
            <p style={{ color: 'var(--color-text-3)' }}>Options overlay interface coming soon...</p>
          </div>
        </div>
      </div>
    </div>
  )
}