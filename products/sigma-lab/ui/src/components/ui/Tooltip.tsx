import React, { useState, useRef, useEffect } from 'react'
import './Tooltip.css'

export interface TooltipProps {
  content: React.ReactNode
  children: React.ReactElement
  placement?: 'top' | 'bottom' | 'left' | 'right' | 'auto'
  delay?: number
  className?: string
  disabled?: boolean
  trigger?: 'hover' | 'click' | 'focus'
}

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  placement = 'auto',
  delay = 200,
  className = '',
  disabled = false,
  trigger = 'hover'
}) => {
  const [isVisible, setIsVisible] = useState(false)
  const [actualPlacement, setActualPlacement] = useState(placement)
  const triggerRef = useRef<HTMLDivElement>(null)
  const tooltipRef = useRef<HTMLDivElement>(null)
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined)

  const calculatePosition = () => {
    if (!triggerRef.current || !tooltipRef.current) return

    const triggerRect = triggerRef.current.getBoundingClientRect()
    const tooltipRect = tooltipRef.current.getBoundingClientRect()
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight
    const gap = 10

    let top = 0
    let left = 0
    let finalPlacement = placement

    if (placement === 'auto') {
      const spaceAbove = triggerRect.top
      const spaceBelow = viewportHeight - triggerRect.bottom
      const spaceLeft = triggerRect.left
      const spaceRight = viewportWidth - triggerRect.right

      if (spaceAbove > tooltipRect.height + gap) {
        finalPlacement = 'top'
      } else if (spaceBelow > tooltipRect.height + gap) {
        finalPlacement = 'bottom'
      } else if (spaceLeft > tooltipRect.width + gap) {
        finalPlacement = 'left'
      } else if (spaceRight > tooltipRect.width + gap) {
        finalPlacement = 'right'
      } else {
        finalPlacement = 'bottom'
      }
    } else {
      finalPlacement = placement
    }

    switch (finalPlacement) {
      case 'top':
        top = triggerRect.top - tooltipRect.height - gap
        left = triggerRect.left + (triggerRect.width - tooltipRect.width) / 2
        break
      case 'bottom':
        top = triggerRect.bottom + gap
        left = triggerRect.left + (triggerRect.width - tooltipRect.width) / 2
        break
      case 'left':
        top = triggerRect.top + (triggerRect.height - tooltipRect.height) / 2
        left = triggerRect.left - tooltipRect.width - gap
        break
      case 'right':
        top = triggerRect.top + (triggerRect.height - tooltipRect.height) / 2
        left = triggerRect.right + gap
        break
    }

    // Keep tooltip within viewport
    left = Math.max(gap, Math.min(left, viewportWidth - tooltipRect.width - gap))
    top = Math.max(gap, Math.min(top, viewportHeight - tooltipRect.height - gap))

    tooltipRef.current.style.top = `${top}px`
    tooltipRef.current.style.left = `${left}px`
    setActualPlacement(finalPlacement)
  }

  const showTooltip = () => {
    if (disabled || !content) return
    if (timeoutRef.current) clearTimeout(timeoutRef.current)
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true)
    }, delay)
  }

  const hideTooltip = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current)
    timeoutRef.current = setTimeout(() => {
      setIsVisible(false)
    }, 80)
  }

  const toggleTooltip = () => {
    if (isVisible) {
      hideTooltip()
    } else {
      showTooltip()
    }
  }

  useEffect(() => {
    if (isVisible) {
      calculatePosition()
      window.addEventListener('scroll', calculatePosition, true)
      window.addEventListener('resize', calculatePosition)
      return () => {
        window.removeEventListener('scroll', calculatePosition, true)
        window.removeEventListener('resize', calculatePosition)
      }
    }
  }, [isVisible])

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  const childProps: any = {
    ref: triggerRef,
    'aria-describedby': isVisible ? 'tooltip' : undefined
  }

  if (trigger === 'hover') {
    childProps.onMouseEnter = showTooltip
    childProps.onMouseLeave = hideTooltip
    childProps.onFocus = showTooltip
    childProps.onBlur = hideTooltip
  } else if (trigger === 'click') {
    childProps.onClick = toggleTooltip
  } else if (trigger === 'focus') {
    childProps.onFocus = showTooltip
    childProps.onBlur = hideTooltip
  }

  return (
    <>
      {React.cloneElement(children, childProps)}
      {isVisible && content && (
        <div
          ref={tooltipRef}
          id="tooltip"
          role="tooltip"
          className={`tooltip tooltip-${actualPlacement} ${className}`}
          data-show="true"
        >
          {content}
        </div>
      )}
    </>
  )
}