import React from 'react'

export const CompactSelect: React.FC<React.SelectHTMLAttributes<HTMLSelectElement>> = ({ children, className='', ...rest }) => {
  return (
    <select className={`compact-select ${className}`.trim()} {...rest}>
      {children}
    </select>
  )
}

