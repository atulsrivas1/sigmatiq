import React from 'react'

export const ErrorBanner: React.FC<{ message: string }>= ({ message }) => (
  <div className="error-banner" role="alert" style={{ marginBottom: 12 }}>
    <strong>Request failed:</strong> <span style={{ marginLeft: 6 }}>{message}</span>
  </div>
)

