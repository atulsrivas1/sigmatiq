import React, { useEffect, useState } from 'react'
import { apiService } from '../services/api'

export const Health: React.FC = () => {
  const [health, setHealth] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHealth()
  }, [])

  const fetchHealth = async () => {
    try {
      const response = await apiService.getHealth()
      setHealth(response.data)
    } catch (error) {
      console.error('Error fetching health:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 'var(--spacing-lg)', maxWidth: '1400px', margin: '0 auto' }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">System Health</h1>
          <p className="page-description">Monitor system status and diagnostics</p>
        </div>
      </div>

      <div className="card">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <div className="spinner spinner-lg"></div>
            <p className="text-muted" style={{ marginTop: '1rem' }}>Checking system health...</p>
          </div>
        ) : (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
              <span style={{ fontSize: '32px' }}>💚</span>
              <div>
                <h2 style={{ color: 'var(--status-success)' }}>
                  {health?.ok ? 'All Systems Operational' : 'System Issues Detected'}
                </h2>
                <p className="text-muted">Last checked: {new Date().toLocaleString()}</p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
              <div style={{ padding: '1rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
                <h3 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text-3)', marginBottom: '0.5rem' }}>
                  Service Status
                </h3>
                <p style={{ fontSize: '18px', fontWeight: 600, color: health?.ok ? 'var(--status-success)' : 'var(--status-error)' }}>
                  {health?.service || 'Unknown'}
                </p>
              </div>

              <div style={{ padding: '1rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
                <h3 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text-3)', marginBottom: '0.5rem' }}>
                  Version
                </h3>
                <p style={{ fontSize: '18px', fontWeight: 600 }}>
                  {health?.version || '0.0.0'}
                </p>
              </div>

              <div style={{ padding: '1rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
                <h3 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text-3)', marginBottom: '0.5rem' }}>
                  Database
                </h3>
                <p style={{ fontSize: '18px', fontWeight: 600, color: 'var(--status-success)' }}>
                  {health?.deps?.db || 'Unknown'}
                </p>
              </div>

              <div style={{ padding: '1rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
                <h3 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--color-text-3)', marginBottom: '0.5rem' }}>
                  FastAPI
                </h3>
                <p style={{ fontSize: '18px', fontWeight: 600, color: 'var(--status-success)' }}>
                  {health?.deps?.fastapi || 'Unknown'}
                </p>
              </div>
            </div>

            <div style={{ marginTop: '2rem', padding: '1rem', background: 'var(--color-surface-1)', borderRadius: '8px' }}>
              <h3 style={{ marginBottom: '1rem' }}>Health Check Details</h3>
              <pre style={{ fontSize: '12px', color: 'var(--color-text-2)', overflow: 'auto' }}>
                {JSON.stringify(health, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}