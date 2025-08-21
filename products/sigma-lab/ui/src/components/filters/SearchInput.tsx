import React from 'react'

export const SearchInput: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = ({ className='', ...rest }) => {
  return (
    <div className={`search-box ${className}`.trim()}>
      <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
      </svg>
      <input className="search-input" {...rest} />
    </div>
  )
}

