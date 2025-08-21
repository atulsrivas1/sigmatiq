import React from 'react'

export const FilterChip: React.FC<{ active?: boolean; onClick?: () => void; children: React.ReactNode }>= ({ active, onClick, children }) => {
  return (
    <button type="button" className={`chip${active ? ' active' : ''}`} onClick={onClick}>
      {children}
    </button>
  )
}

