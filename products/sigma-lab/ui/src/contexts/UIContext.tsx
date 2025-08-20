import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

type UIContextState = {
  sidebarCollapsed: boolean
  setSidebarCollapsed: (v: boolean) => void
  expandedNavIds: string[]
  setExpandedNavIds: (ids: string[]) => void
}

const UIContext = createContext<UIContextState | undefined>(undefined)

const LS_COLLAPSED_KEY = 'ui.sidebarCollapsed'
const LS_EXPANDED_KEY = 'ui.expandedNavIds'

export const UIProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sidebarCollapsed, setSidebarCollapsedState] = useState<boolean>(() => {
    try {
      const v = localStorage.getItem(LS_COLLAPSED_KEY)
      return v ? JSON.parse(v) : false
    } catch {
      return false
    }
  })

  const [expandedNavIds, setExpandedNavIdsState] = useState<string[]>(() => {
    try {
      const v = localStorage.getItem(LS_EXPANDED_KEY)
      return v ? JSON.parse(v) : []
    } catch {
      return []
    }
  })

  useEffect(() => {
    try { localStorage.setItem(LS_COLLAPSED_KEY, JSON.stringify(sidebarCollapsed)) } catch {}
  }, [sidebarCollapsed])

  useEffect(() => {
    try { localStorage.setItem(LS_EXPANDED_KEY, JSON.stringify(expandedNavIds)) } catch {}
  }, [expandedNavIds])

  const setSidebarCollapsed = useCallback((v: boolean) => setSidebarCollapsedState(v), [])
  const setExpandedNavIds = useCallback((ids: string[]) => setExpandedNavIdsState(ids), [])

  const value = useMemo<UIContextState>(() => ({
    sidebarCollapsed,
    setSidebarCollapsed,
    expandedNavIds,
    setExpandedNavIds,
  }), [sidebarCollapsed, expandedNavIds, setSidebarCollapsed, setExpandedNavIds])

  return <UIContext.Provider value={value}>{children}</UIContext.Provider>
}

export const useUIContext = () => {
  const ctx = useContext(UIContext)
  if (!ctx) throw new Error('useUIContext must be used within UIProvider')
  return ctx
}
