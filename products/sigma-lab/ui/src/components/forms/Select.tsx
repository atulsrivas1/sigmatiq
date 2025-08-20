import React, { forwardRef } from 'react'
import { Icon } from '../Icon'
import './Select.css'

interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string
  error?: string
  helpText?: string
  size?: 'sm' | 'md' | 'lg'
  options?: SelectOption[]
  placeholder?: string
  fullWidth?: boolean
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(({
  label,
  error,
  helpText,
  size = 'md',
  options = [],
  placeholder,
  fullWidth = false,
  className = '',
  disabled,
  children,
  ...props
}, ref) => {
  const selectClasses = [
    'select',
    `select-${size}`,
    fullWidth && 'select-full-width',
    error && 'select-error',
    disabled && 'select-disabled',
    className
  ].filter(Boolean).join(' ')

  return (
    <div className="select-group">
      {label && (
        <label className="select-label">
          {label}
          {props.required && <span className="select-required">*</span>}
        </label>
      )}
      
      <div className="select-wrapper">
        <select
          ref={ref}
          className={selectClasses}
          disabled={disabled}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option
              key={option.value}
              value={option.value}
              disabled={option.disabled}
            >
              {option.label}
            </option>
          ))}
          {children}
        </select>
        
        <div className="select-icon">
          <Icon name="chevronDown" size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16} />
        </div>
      </div>
      
      {error && <span className="select-error-text">{error}</span>}
      {helpText && !error && <span className="select-help-text">{helpText}</span>}
    </div>
  )
})

Select.displayName = 'Select'

// Filter Select - specialized for filtering
interface FilterSelectProps extends Omit<SelectProps, 'label' | 'error' | 'helpText'> {
  onFilterChange?: (value: string) => void
}

export const FilterSelect: React.FC<FilterSelectProps> = ({
  onFilterChange,
  onChange,
  ...props
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value
    onFilterChange?.(value)
    onChange?.(e)
  }

  return (
    <Select
      {...props}
      onChange={handleChange}
      className={`filter-select ${props.className || ''}`}
    />
  )
}