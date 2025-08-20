import React from 'react'
import './Toggle.css'

interface ToggleProps {
  checked?: boolean
  defaultChecked?: boolean
  onChange?: (checked: boolean) => void
  disabled?: boolean
  label?: string
  labelPosition?: 'left' | 'right'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  id?: string
  name?: string
}

export const Toggle: React.FC<ToggleProps> = ({
  checked,
  defaultChecked = false,
  onChange,
  disabled = false,
  label,
  labelPosition = 'right',
  size = 'md',
  className = '',
  id,
  name
}) => {
  const isControlled = checked !== undefined
  const [internalChecked, setInternalChecked] = React.useState(defaultChecked)
  
  const isChecked = isControlled ? checked : internalChecked
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newChecked = e.target.checked
    if (!isControlled) {
      setInternalChecked(newChecked)
    }
    onChange?.(newChecked)
  }
  
  const toggleId = id || `toggle-${Math.random().toString(36).substr(2, 9)}`
  
  const toggleClasses = [
    'toggle-switch',
    `toggle-${size}`,
    disabled && 'toggle-disabled',
    className
  ].filter(Boolean).join(' ')
  
  const content = (
    <>
      {label && labelPosition === 'left' && (
        <label htmlFor={toggleId} className="toggle-label toggle-label-left">
          {label}
        </label>
      )}
      <div className={toggleClasses}>
        <input
          type="checkbox"
          id={toggleId}
          name={name}
          checked={isChecked}
          onChange={handleChange}
          disabled={disabled}
          className="toggle-input"
        />
        <span className="toggle-slider" />
      </div>
      {label && labelPosition === 'right' && (
        <label htmlFor={toggleId} className="toggle-label toggle-label-right">
          {label}
        </label>
      )}
    </>
  )
  
  return (
    <div className="toggle-container">
      {content}
    </div>
  )
}