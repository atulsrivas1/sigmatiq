import React, { forwardRef } from 'react'
import { Icon } from '../Icon'
import './Input.css'

interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string
  error?: string
  helpText?: string
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'search'
  leftIcon?: string
  rightIcon?: string
  onRightIconClick?: () => void
  fullWidth?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({
  label,
  error,
  helpText,
  size = 'md',
  variant = 'default',
  leftIcon,
  rightIcon,
  onRightIconClick,
  fullWidth = false,
  className = '',
  disabled,
  ...props
}, ref) => {
  const inputClasses = [
    'input',
    `input-${size}`,
    `input-${variant}`,
    fullWidth && 'input-full-width',
    leftIcon && 'input-with-left-icon',
    rightIcon && 'input-with-right-icon',
    error && 'input-error',
    disabled && 'input-disabled',
    className
  ].filter(Boolean).join(' ')

  return (
    <div className="input-group">
      {label && (
        <label className="input-label">
          {label}
          {props.required && <span className="input-required">*</span>}
        </label>
      )}
      
      <div className="input-wrapper">
        {leftIcon && (
          <Icon 
            name={leftIcon} 
            size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16}
            className="input-left-icon" 
          />
        )}
        
        <input
          ref={ref}
          className={inputClasses}
          disabled={disabled}
          {...props}
        />
        
        {rightIcon && (
          <button
            type="button"
            className="input-right-icon"
            onClick={onRightIconClick}
            disabled={disabled}
            tabIndex={onRightIconClick ? 0 : -1}
          >
            <Icon 
              name={rightIcon} 
              size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16}
            />
          </button>
        )}
      </div>
      
      {error && <span className="input-error-text">{error}</span>}
      {helpText && !error && <span className="input-help-text">{helpText}</span>}
    </div>
  )
})

Input.displayName = 'Input'

// Textarea component
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helpText?: string
  resize?: 'none' | 'both' | 'horizontal' | 'vertical'
  fullWidth?: boolean
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(({
  label,
  error,
  helpText,
  resize = 'vertical',
  fullWidth = false,
  className = '',
  disabled,
  ...props
}, ref) => {
  const textareaClasses = [
    'textarea',
    fullWidth && 'textarea-full-width',
    error && 'textarea-error',
    disabled && 'textarea-disabled',
    className
  ].filter(Boolean).join(' ')

  return (
    <div className="input-group">
      {label && (
        <label className="input-label">
          {label}
          {props.required && <span className="input-required">*</span>}
        </label>
      )}
      
      <textarea
        ref={ref}
        className={textareaClasses}
        style={{ resize }}
        disabled={disabled}
        {...props}
      />
      
      {error && <span className="input-error-text">{error}</span>}
      {helpText && !error && <span className="input-help-text">{helpText}</span>}
    </div>
  )
})

Textarea.displayName = 'Textarea'

// Search Input - specialized variant
interface SearchInputProps extends Omit<InputProps, 'variant' | 'leftIcon'> {
  onClear?: () => void
  showClear?: boolean
}

export const SearchInput: React.FC<SearchInputProps> = ({
  onClear,
  showClear = false,
  value,
  ...props
}) => {
  const handleClear = () => {
    onClear?.()
  }

  return (
    <Input
      {...props}
      variant="search"
      leftIcon="search"
      rightIcon={showClear && value ? "close" : undefined}
      onRightIconClick={showClear && value ? handleClear : undefined}
      value={value}
    />
  )
}