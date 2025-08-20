import React, { useState } from 'react'
import './Tabs.css'

interface Tab {
  id: string
  label: string
  icon?: React.ReactNode
  disabled?: boolean
  badge?: string | number
}

interface TabsProps {
  tabs: Tab[]
  activeTab?: string
  defaultTab?: string
  onChange?: (tabId: string) => void
  variant?: 'default' | 'pills' | 'underline'
  size?: 'sm' | 'md' | 'lg'
  fullWidth?: boolean
  className?: string
  children?: React.ReactNode
}

export const Tabs: React.FC<TabsProps> = ({
  tabs,
  activeTab,
  defaultTab,
  onChange,
  variant = 'default',
  size = 'md',
  fullWidth = false,
  className = '',
  children
}) => {
  const [internalActiveTab, setInternalActiveTab] = useState(defaultTab || tabs[0]?.id)
  const currentTab = activeTab !== undefined ? activeTab : internalActiveTab
  
  const handleTabClick = (tabId: string) => {
    if (activeTab === undefined) {
      setInternalActiveTab(tabId)
    }
    onChange?.(tabId)
  }
  
  const tabsClasses = [
    'tabs',
    `tabs-${variant}`,
    `tabs-${size}`,
    fullWidth && 'tabs-full-width',
    className
  ].filter(Boolean).join(' ')
  
  return (
    <div className="tabs-container">
      <div className={tabsClasses} role="tablist">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab ${currentTab === tab.id ? 'tab-active' : ''} ${tab.disabled ? 'tab-disabled' : ''}`}
            onClick={() => !tab.disabled && handleTabClick(tab.id)}
            disabled={tab.disabled}
            role="tab"
            aria-selected={currentTab === tab.id}
            aria-controls={`tabpanel-${tab.id}`}
          >
            {tab.icon && <span className="tab-icon">{tab.icon}</span>}
            <span className="tab-label">{tab.label}</span>
            {tab.badge && (
              <span className="tab-badge">{tab.badge}</span>
            )}
          </button>
        ))}
      </div>
      
      {children && (
        <div className="tabs-content">
          {React.Children.map(children, (child) => {
            if (React.isValidElement(child) && (child.props as any).tabId === currentTab) {
              return (
                <div
                  role="tabpanel"
                  id={`tabpanel-${currentTab}`}
                  aria-labelledby={`tab-${currentTab}`}
                >
                  {child}
                </div>
              )
            }
            return null
          })}
        </div>
      )}
    </div>
  )
}

// Tab Panel component for content
interface TabPanelProps {
  tabId: string
  children: React.ReactNode
  className?: string
}

export const TabPanel: React.FC<TabPanelProps> = ({
  children,
  className = ''
}) => {
  return (
    <div className={`tab-panel ${className}`}>
      {children}
    </div>
  )
}

// Period Selector - specialized tabs for time periods
interface PeriodSelectorProps {
  periods?: Array<{ id: string; label: string }>
  activePeriod?: string
  defaultPeriod?: string
  onChange?: (period: string) => void
  className?: string
}

export const PeriodSelector: React.FC<PeriodSelectorProps> = ({
  periods = [
    { id: '1d', label: '1D' },
    { id: '1w', label: '1W' },
    { id: '1m', label: '1M' },
    { id: '3m', label: '3M' },
    { id: 'ytd', label: 'YTD' },
    { id: '1y', label: '1Y' }
  ],
  activePeriod,
  defaultPeriod = '1m',
  onChange,
  className = ''
}) => {
  const [internalPeriod, setInternalPeriod] = useState(defaultPeriod)
  const currentPeriod = activePeriod !== undefined ? activePeriod : internalPeriod
  
  const handlePeriodClick = (periodId: string) => {
    if (activePeriod === undefined) {
      setInternalPeriod(periodId)
    }
    onChange?.(periodId)
  }
  
  return (
    <div className={`period-selector ${className}`}>
      {periods.map(period => (
        <button
          key={period.id}
          className={`period-option ${currentPeriod === period.id ? 'active' : ''}`}
          onClick={() => handlePeriodClick(period.id)}
        >
          {period.label}
        </button>
      ))}
    </div>
  )
}