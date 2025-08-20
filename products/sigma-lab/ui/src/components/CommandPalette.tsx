import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import { Icon } from './Icon'
import './CommandPalette.css'

interface Command {
  id: string
  label: string
  shortcut?: string[]
  icon?: string
  action: () => void
  group?: string
}

interface CommandPaletteProps {
  isOpen: boolean
  onClose: () => void
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose }) => {
  const [search, setSearch] = useState('')
  const [selectedIndex, setSelectedIndex] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()
  const { setTheme, themes } = useTheme()

  const commands: Command[] = [
    // Actions
    { id: 'new-model', label: 'Create New Model', shortcut: ['⌘', 'N'], icon: 'plus', group: 'Actions', action: () => { navigate('/models/new'); onClose() } },
    { id: 'run-backtest', label: 'Run Backtest', shortcut: ['⌘', 'R'], icon: 'backtest', group: 'Actions', action: () => { navigate('/backtest'); onClose() } },
    { id: 'sweeps', label: 'Open Sweeps', icon: 'sweeps', group: 'Actions', action: () => { navigate('/sweeps'); onClose() } },
    
    // Navigation
    { id: 'dashboard', label: 'Go to Dashboard', icon: 'dashboard', group: 'Navigation', action: () => { navigate('/dashboard'); onClose() } },
    { id: 'models', label: 'Go to Models', icon: 'models', group: 'Navigation', action: () => { navigate('/models'); onClose() } },
    { id: 'leaderboard', label: 'Go to Leaderboard', icon: 'leaderboard', group: 'Navigation', action: () => { navigate('/leaderboard'); onClose() } },
    { id: 'signals', label: 'Go to Signals', icon: 'signals', group: 'Navigation', action: () => { navigate('/signals'); onClose() } },
    { id: 'health', label: 'Go to Health', icon: 'health', group: 'Navigation', action: () => { navigate('/health'); onClose() } },
    
    // Theme
    { id: 'theme-dark', label: 'Dark Theme', icon: 'theme', group: 'Theme', action: () => { setTheme('dark'); onClose() } },
    { id: 'theme-midnight', label: 'Midnight Theme', icon: 'theme', group: 'Theme', action: () => { setTheme('midnight'); onClose() } },
    { id: 'theme-light', label: 'Light Theme', icon: 'theme', group: 'Theme', action: () => { setTheme('light'); onClose() } },
    { id: 'theme-slate', label: 'Slate Theme', icon: 'theme', group: 'Theme', action: () => { setTheme('slate'); onClose() } },
  ]

  const filteredCommands = commands.filter(cmd =>
    cmd.label.toLowerCase().includes(search.toLowerCase())
  )

  // Group commands
  const groupedCommands = filteredCommands.reduce((acc, cmd) => {
    const group = cmd.group || 'Other'
    if (!acc[group]) acc[group] = []
    acc[group].push(cmd)
    return acc
  }, {} as Record<string, Command[]>)

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus()
      setSearch('')
      setSelectedIndex(0)
    }
  }, [isOpen])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return

      if (e.key === 'Escape') {
        onClose()
      } else if (e.key === 'ArrowDown') {
        e.preventDefault()
        setSelectedIndex(prev => (prev + 1) % filteredCommands.length)
      } else if (e.key === 'ArrowUp') {
        e.preventDefault()
        setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % filteredCommands.length)
      } else if (e.key === 'Enter') {
        e.preventDefault()
        if (filteredCommands[selectedIndex]) {
          filteredCommands[selectedIndex].action()
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, selectedIndex, filteredCommands, onClose])

  if (!isOpen) return null

  return (
    <>
      <div className="command-palette-backdrop" onClick={onClose} />
      <div className="command-palette">
        <div className="command-header">
          <input
            ref={inputRef}
            type="text"
            className="command-input"
            placeholder="Type a command or search..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value)
              setSelectedIndex(0)
            }}
          />
          <span className="command-key">ESC</span>
        </div>
        <div className="command-results">
          {filteredCommands.length === 0 ? (
            <div className="command-group">
              <div className="command-group-label">No results</div>
              <div className="command-item">No commands found</div>
            </div>
          ) : (
            Object.entries(groupedCommands).map(([group, cmds]) => {
              let cmdIndex = -1
              return (
                <div key={group} className="command-group">
                  <div className="command-group-label">{group}</div>
                  {cmds.map((cmd) => {
                    cmdIndex++
                    const globalIndex = filteredCommands.indexOf(cmd)
                    return (
                      <button
                        key={cmd.id}
                        className={`command-item ${globalIndex === selectedIndex ? 'active' : ''}`}
                        onClick={cmd.action}
                        onMouseEnter={() => setSelectedIndex(globalIndex)}
                      >
                        {cmd.icon && (
                          <div className="command-icon">
                            <Icon name={cmd.icon} size={20} />
                          </div>
                        )}
                        <span className="command-text">{cmd.label}</span>
                        {cmd.shortcut && (
                          <div className="command-shortcut">
                            {cmd.shortcut.map((key, i) => (
                              <kbd key={i}>{key}</kbd>
                            ))}
                          </div>
                        )}
                      </button>
                    )
                  })}
                </div>
              )
            })
          )}
        </div>
      </div>
    </>
  )
}