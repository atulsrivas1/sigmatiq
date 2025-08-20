import React, { createContext, useContext, useState, useEffect } from 'react'

export type ThemeName = 'dark' | 'light' | 'slate' | 'midnight'

interface ThemeConfig {
  name: ThemeName
  color: string
}

export const themes: ThemeConfig[] = [
  { name: 'dark', color: '#00c4a7' },      // Dark theme 1
  { name: 'midnight', color: '#14b8a6' },  // Dark theme 2
  { name: 'light', color: '#00a693' },     // Light theme 1
  { name: 'slate', color: '#0891b2' }      // Light theme 2
]

interface ThemeContextType {
  theme: ThemeName
  setTheme: (theme: ThemeName) => void
  cycleTheme: () => void
  currentThemeConfig: ThemeConfig
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<ThemeName>(() => {
    const saved = localStorage.getItem('theme')
    return (saved as ThemeName) || 'dark'
  })

  const currentThemeConfig = themes.find(t => t.name === theme) || themes[0]

  useEffect(() => {
    localStorage.setItem('theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const cycleTheme = () => {
    const currentIndex = themes.findIndex(t => t.name === theme)
    const nextIndex = (currentIndex + 1) % themes.length
    setTheme(themes[nextIndex].name)
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme, cycleTheme, currentThemeConfig }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}