import React, { useEffect, useMemo, useState } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { Logo } from '../components/Logo'
import { Icon } from '../components/Icon'
import { menu as menuConfig, MenuItem, implementedPaths } from '../config/menu'
import './AppShell.css'
import { useUIContext } from '../contexts/UIContext'
import { useTheme } from '../contexts/ThemeContext'
import { CommandPalette } from '../components/CommandPalette'

interface NavItem {
  id: string
  label: string
  path: string
  icon: string
  hover?: string
  adminOnly?: boolean
  implemented: boolean
  count?: number
  children?: NavItem[]
}

// Simple icon selection based on menu title/route keywords
const pickIcon = (item: MenuItem): string => {
  const t = item.title.toLowerCase()
  const r = item.route.toLowerCase()
  if (t.includes('dashboard')) return 'dashboard'
  if (t.includes('pack') || r.startsWith('/packs')) return 'packsLayered'
  if (t.includes('model') || r.startsWith('/models')) return 'models'
  if (t.includes('signal') || r.startsWith('/signals')) return 'signals'
  if (t.includes('overlay') || r.includes('overlay')) return 'overlay'
  if (t.includes('health')) return 'health'
  if (t.includes('doc')) return 'docs'
  if (t.includes('quota') || t.includes('flag') || t.includes('template')) return 'settings'
  if (t.includes('user')) return 'user'
  if (t.includes('leaderboard')) return 'leaderboard'
  if (t.includes('sweep')) return 'sweeps'
  if (t.includes('train')) return 'train'
  if (t.includes('build')) return 'build'
  return 'grid'
}

const normalizePath = (p: string) => p.replace(/^#/, '')

// Flatten implemented paths matcher with simple dynamic segment awareness
const pathMatches = (pattern: string, path: string) => {
  const partsP = pattern.split('/')
  const parts = path.split('/')
  if (partsP.length !== parts.length) return false
  for (let i = 0; i < partsP.length; i++) {
    const a = partsP[i]
    const b = parts[i]
    if (a.startsWith(':')) continue
    if (a !== b) return false
  }
  return true
}

const isImplemented = (to: string) => {
  const path = normalizePath(to)
  return implementedPaths.some(p => pathMatches(p, path))
}

export const AppShell: React.FC = () => {
  const location = useLocation()
  const { sidebarCollapsed: collapsed, setSidebarCollapsed, expandedNavIds, setExpandedNavIds } = useUIContext()
  const { cycleTheme, currentThemeConfig } = useTheme()
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false)
  
  // Add keyboard shortcut for command palette
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setCommandPaletteOpen(prev => !prev)
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Build navigation model from DevGuide config
  const navigation = useMemo(() => {
    const build = (items: MenuItem[], parentKey = ''): NavItem[] =>
      items.map((it, idx) => {
        const id = `${parentKey}${idx}-${it.title.toLowerCase().replace(/\s+/g, '-')}`
        const path = normalizePath(it.route)
        return {
          id,
          label: it.title,
          path,
          icon: pickIcon(it),
          hover: it.hover,
          adminOnly: it.adminOnly,
          implemented: isImplemented(path),
          count: (it as any).count,
          children: it.children ? build(it.children, id + '.') : undefined,
        }
      })
    return build(menuConfig)
  }, [])

  // Helpers for nested expand/collapse (only-one-open per level, keep ancestors)
  const getParentId = (id: string) => (id.includes('.') ? id.slice(0, id.lastIndexOf('.')) : null)
  const isDescendantOf = (id: string, ancestorId: string) => id.startsWith(ancestorId + '.')
  const getAncestorIds = (id: string): string[] => {
    const ids: string[] = []
    let current = getParentId(id)
    while (current) {
      ids.unshift(current)
      current = getParentId(current)
    }
    return ids
  }

  const toggleExpanded = (itemId: string) => {
    const parentId = getParentId(itemId)
    const prev = expandedNavIds
    const isOpen = prev.includes(itemId)
    if (isOpen) {
      const next = prev.filter(id => !(id === itemId || isDescendantOf(id, itemId)))
      setExpandedNavIds(next)
      return
    }
    const ancestors = getAncestorIds(itemId)
    const withoutSiblings = prev.filter(id => getParentId(id) !== parentId)
    const withAncestors = ancestors.reduce<string[]>((acc, a) => (acc.includes(a) ? acc : acc.concat(a)), withoutSiblings)
    const next = withAncestors.includes(itemId) ? withAncestors : withAncestors.concat(itemId)
    setExpandedNavIds(next)
  }

  // Exact-match active to avoid multiple items appearing selected
  const isActive = (path: string) => location.pathname === path

  // Auto-expand ancestor chain for active route
  useEffect(() => {
    const findActiveChain = (items: NavItem[], chain: NavItem[] = []): NavItem[] | null => {
      for (const it of items) {
        const here = [...chain, it]
        if (isActive(it.path)) return here
        if (it.children) {
          const deeper = findActiveChain(it.children, here)
          if (deeper) return deeper
        }
      }
      return null
    }
    const chain = findActiveChain(navigation) || []
    const ancestorIds = chain.slice(0, -1).map(n => n.id)
    // Always keep ancestors open of the active route
    setExpandedNavIds(ancestorIds)
  }, [location.pathname, navigation])

  const renderNavItem = (item: NavItem, depth = 0) => {
    const hasChildren = item.children && item.children.length > 0
    const isExpanded = expandedNavIds.includes(item.id)
    const active = isActive(item.path)
    const disabled = !item.implemented
    const paddingLeft = (collapsed ? 16 : 16 + depth * 16) + 'px'
    const itemClass = depth === 0 ? 'nav-item' : 'nav-child'
    const depthClass = depth > 0 ? `depth-${depth}` : ''

    // decide badge: if explicit count provided, use it; otherwise show children count for any item with children
    const badgeCount = typeof item.count === 'number' ? item.count : (hasChildren ? item.children!.length : undefined)
    return (
      <div key={item.id}>
        {hasChildren ? (
          <button
            className={`${itemClass} ${depthClass} ${active ? 'active' : ''} ${hasChildren ? 'has-children' : ''} ${isExpanded ? 'expanded' : ''}`}
            onClick={() => toggleExpanded(item.id)}
            style={{ paddingLeft }}
            title={item.hover || ''}
          >
            {depth === 0 && (
              <span className="nav-icon"><Icon name={item.icon} size={18} /></span>
            )}
            <span className="nav-text">{item.label}</span>
            {typeof badgeCount === 'number' && (
              <span className="nav-badge" aria-label={`Count ${badgeCount}`}>{badgeCount}</span>
            )}
          </button>
        ) : (
          disabled ? (
            <button
              className={`${itemClass} ${depthClass} ${active ? 'active' : ''} disabled`}
              style={{ paddingLeft }}
              title={(item.hover ? item.hover + ' — ' : '') + 'Coming soon'}
              aria-disabled
            >
              {depth === 0 && (
                <span className="nav-icon"><Icon name={item.icon} size={18} /></span>
              )}
              <span className="nav-text">{item.label}</span>
              {typeof badgeCount === 'number' && (
                <span className="nav-badge" aria-label={`Count ${badgeCount}`}>{badgeCount}</span>
              )}
            </button>
          ) : (
            <Link
              to={item.path}
              className={`${itemClass} ${depthClass} ${active ? 'active' : ''}`}
              style={{ paddingLeft }}
              title={item.hover || ''}
              aria-current={active ? 'page' : undefined}
            >
              {depth === 0 && (
                <span className="nav-icon"><Icon name={item.icon} size={18} /></span>
              )}
              <span className="nav-text">{item.label}</span>
              {typeof badgeCount === 'number' && (
                <span className="nav-badge" aria-label={`Count ${badgeCount}`}>{badgeCount}</span>
              )}
            </Link>
          )
        )}
        {hasChildren && (
          <div className={`nav-children ${isExpanded ? 'expanded' : ''}`}>
            {item.children!.map((child: NavItem) => renderNavItem(child, depth + 1))}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="app-shell">
      <a href="#main-content" className="skip-link">Skip to main content</a>
      {/* Header */}
      <header className="main-header">
        <div className="header-left">
          <Logo size={44} showText={true} />
        </div>
        
        <div className="header-right">
          <button className="icon-btn" aria-label="Switch Dashboard" title="Switch Dashboard">
            <Icon name="grid" size={18} />
          </button>
          <button 
            className="icon-btn theme-btn" 
            aria-label="Toggle Theme" 
            title={`Current theme: ${currentThemeConfig.name}`}
            onClick={cycleTheme}
            style={{ color: currentThemeConfig.color }}
          >
            <Icon name="sun" size={18} />
          </button>
          <button 
            className="icon-btn" 
            aria-label="Open Command Palette" 
            title="Command Palette (⌘K)"
            onClick={() => setCommandPaletteOpen(true)}
          >
            <span className="cmd-k">⌘K</span>
          </button>
        </div>
      </header>

      {/* Main Layout */}
      <div className="main-layout">
        {/* Sidebar */}
        <aside className={`sidebar${collapsed ? ' collapsed' : ''}`} role="navigation" aria-label="Primary">
          <div className="sidebar-content">
            {navigation.map(item => renderNavItem(item))}
          </div>
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarCollapsed(!collapsed)}
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            title={collapsed ? 'Expand' : 'Collapse'}
          >
            <Icon name="menu" size={20} />
          </button>
        </aside>

        {/* Main Content */}
        <main className="main-content" role="main" id="main-content">
          <Outlet />
        </main>
      </div>

      <QuickAccessDrawer />
      {commandPaletteOpen && (
        <CommandPalette 
          isOpen={commandPaletteOpen} 
          onClose={() => setCommandPaletteOpen(false)} 
        />
      )}
    </div>
  )
}

const QuickAccessDrawer: React.FC = () => {
  const [open, setOpen] = useState(false)
  return (
    <div className={`quick-access-drawer ${open ? 'open' : ''}`}>
      <button className="drawer-handle" onClick={() => setOpen(!open)} aria-label={open ? 'Close Quick Access' : 'Open Quick Access'}>
        <span>Quick Access</span>
        <Icon name="chevronDown" size={12} />
      </button>
      <div className="drawer-content">
        <div className="quick-actions">
          <button className="quick-action-btn" aria-label="Dashboard">
            <Icon name="grid" size={18} />
          </button>
          <button className="quick-action-btn" aria-label="Info">
            <Icon name="info" size={18} />
          </button>
          <button className="quick-action-btn" aria-label="Activity">
            <Icon name="signals" size={18} />
          </button>
          <button className="quick-action-btn" aria-label="Export">
            <Icon name="export" size={18} />
          </button>
          <button className="quick-action-btn" aria-label="Refresh">
            <Icon name="refresh" size={18} />
          </button>
          <button className="quick-action-btn" aria-label="Settings">
            <Icon name="settings" size={18} />
          </button>
          <button className="quick-action-btn" aria-label="Add">
            <Icon name="plus" size={18} />
          </button>
          <button className="quick-action-btn edit-btn" aria-label="Edit">
            <Icon name="edit" size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}
