import React from 'react'

export const FiltersRow: React.FC<{ left?: React.ReactNode; children?: React.ReactNode; right?: React.ReactNode }>= ({ left, children, right }) => {
  return (
    <div className="filters-row">
      <div className="filters-left">{left}</div>
      <div className="filters-center">{children}</div>
      <div className="filters-right">{right}</div>
    </div>
  )
}

