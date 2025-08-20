import React, { useState, ReactNode } from 'react'
import { Icon } from '../Icon'
import './DataGrid.css'

export interface DataGridColumn {
  key: string
  label: string
  width?: string | number
  align?: 'left' | 'center' | 'right'
  render?: (value: any, item: any) => ReactNode
}

export interface DataGridProps<T = any> {
  data: T[]
  columns?: DataGridColumn[]
  viewMode?: 'card' | 'row'
  defaultView?: 'card' | 'row'
  
  // Card renderer for card view
  renderCard?: (item: T, index: number) => ReactNode
  
  // Row renderer for row view (optional, uses columns if not provided)
  renderRow?: (item: T, index: number) => ReactNode
  
  // Features toggles
  showSearch?: boolean
  showFilters?: boolean
  showViewToggle?: boolean
  showPagination?: boolean
  showItemsPerPage?: boolean
  showSorting?: boolean
  
  // Search
  searchPlaceholder?: string
  onSearch?: (query: string) => void
  
  // Filters
  filters?: Array<{
    key: string
    label: string
    options: Array<{ value: string; label: string }>
    onChange?: (value: string) => void
  }>
  
  // Sorting
  sortOptions?: Array<{ value: string; label: string }>
  defaultSort?: string
  onSort?: (sortBy: string) => void
  
  // Pagination
  itemsPerPage?: number
  itemsPerPageOptions?: number[]
  currentPage?: number
  totalItems?: number
  onPageChange?: (page: number) => void
  onItemsPerPageChange?: (items: number) => void
  
  // Other props
  loading?: boolean
  emptyMessage?: string
  className?: string
  gridClassName?: string
  cardClassName?: string
  rowClassName?: string
}

export function DataGrid<T = any>({
  data,
  columns = [],
  viewMode: controlledView,
  defaultView = 'card',
  renderCard,
  renderRow,
  showSearch = true,
  showFilters = true,
  showViewToggle = true,
  showPagination = true,
  showItemsPerPage = true,
  showSorting = true,
  searchPlaceholder = 'Search...',
  onSearch,
  filters = [],
  sortOptions = [],
  defaultSort,
  onSort,
  itemsPerPage = 12,
  itemsPerPageOptions = [12, 24, 48],
  currentPage = 1,
  totalItems,
  onPageChange,
  onItemsPerPageChange,
  loading = false,
  emptyMessage = 'No items found',
  className = '',
  gridClassName = '',
  cardClassName = '',
  rowClassName = ''
}: DataGridProps<T>) {
  const [internalView, setInternalView] = useState<'card' | 'row'>(defaultView)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedSort, setSelectedSort] = useState(defaultSort || '')
  const [selectedItemsPerPage, setSelectedItemsPerPage] = useState(itemsPerPage)
  
  const view = controlledView || internalView
  const total = totalItems || data.length
  const totalPages = Math.ceil(total / selectedItemsPerPage)
  
  const handleViewChange = (newView: 'card' | 'row') => {
    setInternalView(newView)
  }
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value
    setSearchQuery(query)
    onSearch?.(query)
  }
  
  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const sortBy = e.target.value
    setSelectedSort(sortBy)
    onSort?.(sortBy)
  }
  
  const handleItemsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const items = parseInt(e.target.value)
    setSelectedItemsPerPage(items)
    onItemsPerPageChange?.(items)
  }
  
  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      onPageChange?.(page)
    }
  }
  
  // Calculate displayed items range
  const startItem = (currentPage - 1) * selectedItemsPerPage + 1
  const endItem = Math.min(currentPage * selectedItemsPerPage, total)
  
  return (
    <div className={`data-grid-container ${className}`}>
      {/* Controls Bar */}
      {(showSearch || showFilters || showViewToggle) && (
        <div className="controls-bar">
          {showSearch && (
            <div className="search-box">
              <Icon name="search" size={16} className="search-icon" />
              <input
                type="text"
                className="search-input"
                placeholder={searchPlaceholder}
                value={searchQuery}
                onChange={handleSearchChange}
              />
            </div>
          )}
          
          {showFilters && (
            <div className="filter-group">
              {filters.map(filter => (
                <select
                  key={filter.key}
                  className="filter-select"
                  onChange={(e) => filter.onChange?.(e.target.value)}
                >
                  {filter.options.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              ))}
              
              {showSorting && sortOptions.length > 0 && (
                <select
                  className="filter-select"
                  value={selectedSort}
                  onChange={handleSortChange}
                >
                  {sortOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              )}
            </div>
          )}
          
          {showViewToggle && (
            <div className="view-toggle">
              <button
                className={`view-option ${view === 'card' ? 'active' : ''}`}
                onClick={() => handleViewChange('card')}
              >
                <Icon name="grid" size={14} />
                <span>Cards</span>
              </button>
              <button
                className={`view-option ${view === 'row' ? 'active' : ''}`}
                onClick={() => handleViewChange('row')}
              >
                <Icon name="menu" size={14} />
                <span>Rows</span>
              </button>
            </div>
          )}
        </div>
      )}
      
      {/* Grid Content */}
      {loading ? (
        <div className="grid-loading">
          <div className="spinner"></div>
          <span>Loading...</span>
        </div>
      ) : data.length === 0 ? (
        <div className="grid-empty">
          <p>{emptyMessage}</p>
        </div>
      ) : (
        <div className={`cards-container ${view}-view ${gridClassName}`}>
          {view === 'card' ? (
            // Card View
            data.map((item, index) => (
              <div key={index} className={`grid-card ${cardClassName}`}>
                {renderCard ? renderCard(item, index) : (
                  <div className="default-card">
                    <pre>{JSON.stringify(item, null, 2)}</pre>
                  </div>
                )}
              </div>
            ))
          ) : (
            // Row View
            data.map((item, index) => (
              <div key={index} className={`grid-row ${rowClassName}`}>
                {renderRow ? renderRow(item, index) : (
                  columns.length > 0 ? (
                    <div className="default-row">
                      {columns.map(col => (
                        <div
                          key={col.key}
                          className={`row-cell row-cell-${col.align || 'left'}`}
                          style={{ width: col.width }}
                        >
                          {col.render ? 
                            col.render(item[col.key as keyof T], item) : 
                            String(item[col.key as keyof T] || '')}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="default-row">
                      <pre>{JSON.stringify(item, null, 2)}</pre>
                    </div>
                  )
                )}
              </div>
            ))
          )}
        </div>
      )}
      
      {/* Pagination */}
      {showPagination && totalPages > 1 && (
        <div className="pagination-container">
          <div className="pagination-info">
            Showing {startItem}-{endItem} of {total} items
          </div>
          
          <div className="pagination-controls">
            <button
              className="page-btn"
              disabled={currentPage === 1}
              onClick={() => handlePageChange(currentPage - 1)}
            >
              <Icon name="chevronLeft" size={14} />
            </button>
            
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              let pageNum = i + 1
              
              // Smart pagination logic
              if (totalPages > 5) {
                if (currentPage <= 3) {
                  pageNum = i + 1
                } else if (currentPage >= totalPages - 2) {
                  pageNum = totalPages - 4 + i
                } else {
                  pageNum = currentPage - 2 + i
                }
              }
              
              return (
                <button
                  key={pageNum}
                  className={`page-btn ${currentPage === pageNum ? 'active' : ''}`}
                  onClick={() => handlePageChange(pageNum)}
                >
                  {pageNum}
                </button>
              )
            })}
            
            <button
              className="page-btn"
              disabled={currentPage === totalPages}
              onClick={() => handlePageChange(currentPage + 1)}
            >
              <Icon name="chevronRight" size={14} />
            </button>
          </div>
          
          {showItemsPerPage && (
            <div className="items-per-page">
              <span>Items:</span>
              <select
                className="filter-select"
                value={selectedItemsPerPage}
                onChange={handleItemsPerPageChange}
              >
                {itemsPerPageOptions.map(option => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}
    </div>
  )
}