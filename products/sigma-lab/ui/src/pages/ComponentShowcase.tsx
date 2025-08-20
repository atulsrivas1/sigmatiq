import React, { useState } from 'react'
import {
  // Core
  Icon,
  Logo,
  // UI Components
  Card,
  CardHeader,
  CardIcon,
  CardHeaderInfo,
  CardBadge,
  CardContent,
  CardStats,
  StatItem,
  CardChart,
  CardMeta,
  CardActions,
  CardButton,
  Button,
  IconButton,
  Badge,
  StatusBadge,
  RiskBadge,
  PackBadge,
  GateBadge,
  TrustBadge,
  Tooltip,
  ProgressBar,
  CapacityBar,
  // Form Components
  Input,
  Textarea,
  SearchInput,
  Select,
  FilterSelect,
  Toggle,
  // Navigation
  Tabs,
  TabPanel,
  PeriodSelector,
  Pagination,
  // Data Display
  DataGrid,
  // Feedback
  Alert,
  Toast,
  EmptyState,
  ErrorState,
  ErrorBanner
} from '../components'
import './ComponentShowcase.css'

export const ComponentShowcase: React.FC = () => {
  const [toggleValue, setToggleValue] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const [selectValue, setSelectValue] = useState('')
  const [activeTab, setActiveTab] = useState('tab1')
  const [activePeriod, setActivePeriod] = useState('1m')
  const [currentPage, setCurrentPage] = useState(1)
  const [showToast, setShowToast] = useState(false)
  const [gridView, setGridView] = useState<'card' | 'row'>('card')

  const sampleData = [
    { id: 1, model_id: 'zerosigma_v1_0dte', pack_id: 'zerosigma', sharpe: 1.82, cum_ret: 12.5, trades: 142, win_rate: 68.2 },
    { id: 2, model_id: 'swingsigma_v2_5d', pack_id: 'swingsigma', sharpe: 1.45, cum_ret: 8.3, trades: 89, win_rate: 62.1 },
    { id: 3, model_id: 'longsigma_v1_30d', pack_id: 'longsigma', sharpe: 2.13, cum_ret: 18.7, trades: 203, win_rate: 71.5 }
  ]

  return (
    <div className="showcase-container">
      <div className="showcase-header">
        <h1>Sigmatiq Component Showcase</h1>
        <p>All components from the design system</p>
      </div>

      {/* Core Components */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Core Components</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Logo</h3>
            <Logo />
          </div>
          <div className="showcase-item">
            <h3>Icons</h3>
            <div className="icon-grid">
              <Icon name="check" />
              <Icon name="x" />
              <Icon name="alert-triangle" />
              <Icon name="info" />
              <Icon name="chevron-right" />
              <Icon name="search" />
            </div>
          </div>
        </div>
      </section>

      {/* Buttons */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Buttons</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Button Variants</h3>
            <div className="button-group">
              <Button variant="primary">Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="danger">Danger</Button>
              <Button disabled>Disabled</Button>
            </div>
          </div>
          <div className="showcase-item">
            <h3>Button Sizes</h3>
            <div className="button-group">
              <Button size="sm">Small</Button>
              <Button size="md">Medium</Button>
              <Button size="lg">Large</Button>
            </div>
          </div>
          <div className="showcase-item">
            <h3>Icon Buttons</h3>
            <div className="button-group">
              <IconButton icon="check" aria-label="Check" />
              <IconButton icon="x" variant="danger" aria-label="Close" />
              <IconButton icon="search" variant="ghost" aria-label="Search" />
            </div>
          </div>
        </div>
      </section>

      {/* Badges */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Badges</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Basic Badges</h3>
            <div className="badge-group">
              <Badge>Default</Badge>
              <Badge variant="success">Success</Badge>
              <Badge variant="warning">Warning</Badge>
              <Badge variant="error">Error</Badge>
              <Badge variant="info">Info</Badge>
            </div>
          </div>
          <div className="showcase-item">
            <h3>Status Badges</h3>
            <div className="badge-group">
              <StatusBadge status="active" />
              <StatusBadge status="pending" />
              <StatusBadge status="inactive" />
              <StatusBadge status="error" />
            </div>
          </div>
          <div className="showcase-item">
            <h3>Risk Badges</h3>
            <div className="badge-group">
              <RiskBadge risk="conservative" />
              <RiskBadge risk="balanced" />
              <RiskBadge risk="aggressive" />
            </div>
          </div>
          <div className="showcase-item">
            <h3>Pack Badges</h3>
            <div className="badge-group">
              <PackBadge pack="zerosigma" />
              <PackBadge pack="swingsigma" />
              <PackBadge pack="longsigma" />
            </div>
          </div>
        </div>
      </section>

      {/* Gate & Trust Badges */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Gate & Trust Badges</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Gate Badges</h3>
            <div className="badge-group">
              <GateBadge 
                status="pass" 
                items={[
                  { rule: 'Min trades', passed: true, message: 'Min trades: 142 ≥ 5' },
                  { rule: 'Max DD', passed: true, message: 'Max DD: 8.2% ≤ 20%' }
                ]}
              />
              <GateBadge 
                status="fail" 
                violations={2}
                items={[
                  { rule: 'Min trades', passed: false, message: 'Min trades not met: 3 < 5' },
                  { rule: 'Max DD', passed: false, message: 'Max DD exceeded: 25% > 20%' }
                ]}
              />
            </div>
          </div>
          <div className="showcase-item">
            <h3>Trust Badges</h3>
            <div className="badge-group">
              <TrustBadge 
                type="integrity" 
                status="success" 
                label="Integrity OK"
                description="All data verified"
              />
              <TrustBadge 
                type="parity" 
                status="warning" 
                label="Parity Drift"
                description="2% variance detected"
              />
              <TrustBadge 
                type="capacity" 
                status="error" 
                label="Low Capacity"
                description="Limited liquidity available"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Form Components */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Form Components</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Input Fields</h3>
            <div className="form-stack">
              <Input 
                label="Model ID" 
                placeholder="Enter model ID"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
              />
              <SearchInput 
                placeholder="Search models..."
                value=""
                onChange={() => {}}
              />
              <Textarea 
                label="Description" 
                placeholder="Enter description..."
                rows={3}
              />
            </div>
          </div>
          <div className="showcase-item">
            <h3>Select & Toggle</h3>
            <div className="form-stack">
              <Select 
                label="Risk Profile"
                value={selectValue}
                onChange={(e) => setSelectValue(e.target.value)}
                options={[
                  { value: '', label: 'Select risk profile' },
                  { value: 'conservative', label: 'Conservative' },
                  { value: 'balanced', label: 'Balanced' },
                  { value: 'aggressive', label: 'Aggressive' }
                ]}
              />
              <FilterSelect 
                options={[
                  { value: 'all', label: 'All Packs' },
                  { value: 'zerosigma', label: 'zerosigma' },
                  { value: 'swingsigma', label: 'swingsigma' }
                ]}
              />
              <Toggle 
                label="Enable notifications"
                checked={toggleValue}
                onChange={setToggleValue}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Navigation Components */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Navigation Components</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Tabs</h3>
            <Tabs
              tabs={[
                { id: 'tab1', label: 'Overview' },
                { id: 'tab2', label: 'Analytics', badge: '3' },
                { id: 'tab3', label: 'Settings' },
                { id: 'tab4', label: 'Disabled', disabled: true }
              ]}
              activeTab={activeTab}
              onChange={setActiveTab}
            >
              <TabPanel tabId="tab1">Overview content</TabPanel>
              <TabPanel tabId="tab2">Analytics content</TabPanel>
              <TabPanel tabId="tab3">Settings content</TabPanel>
            </Tabs>
          </div>
          <div className="showcase-item">
            <h3>Period Selector</h3>
            <PeriodSelector 
              activePeriod={activePeriod}
              onChange={setActivePeriod}
            />
          </div>
          <div className="showcase-item">
            <h3>Pagination</h3>
            <Pagination 
              currentPage={currentPage}
              totalPages={10}
              totalItems={95}
              itemsPerPage={10}
              onPageChange={setCurrentPage}
              showItemInfo
            />
          </div>
        </div>
      </section>

      {/* Progress Bars */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Progress & Capacity Bars</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Progress Bars</h3>
            <div className="progress-stack">
              <ProgressBar value={25} label="Processing" showValue />
              <ProgressBar value={50} variant="warning" label="Memory Usage" />
              <ProgressBar value={75} variant="error" label="Disk Space" />
              <ProgressBar value={90} variant="gradient" label="Complete" animated />
            </div>
          </div>
          <div className="showcase-item">
            <h3>Capacity Bars</h3>
            <div className="progress-stack">
              <CapacityBar used={250} total={1000} label="Positions" />
              <CapacityBar used={750} total={1000} label="Memory" />
              <CapacityBar used={950} total={1000} label="Storage" />
            </div>
          </div>
        </div>
      </section>

      {/* Cards */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Cards</h2>
        <div className="card-grid">
          <Card>
            <CardHeader>
              <CardIcon>📊</CardIcon>
              <CardHeaderInfo title="zerosigma_v1_0dte" subtitle="Last updated: 2 hours ago" />
              <CardBadge variant="success">Active</CardBadge>
            </CardHeader>
            <CardContent>
              <CardStats>
                <StatItem label="Sharpe" value="1.82" variant="positive" />
                <StatItem label="Return" value="12.5%" variant="positive" />
                <StatItem label="Trades" value="142" />
                <StatItem label="Win Rate" value="68.2%" />
              </CardStats>
              <CardChart>
                <div style={{ height: '100px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px dashed var(--color-border)', borderRadius: '4px' }}>
                  Chart Placeholder
                </div>
              </CardChart>
            </CardContent>
            <CardMeta>
              <span>Conservative</span>
              <span>zerosigma pack</span>
            </CardMeta>
            <CardActions>
              <CardButton primary>View Details</CardButton>
              <CardButton>Run Backtest</CardButton>
            </CardActions>
          </Card>

          <Card>
            <CardHeader>
              <CardIcon>🎯</CardIcon>
              <CardHeaderInfo title="swingsigma_v2_5d" subtitle="Last updated: 1 day ago" />
              <CardBadge variant="warning">Pending</CardBadge>
            </CardHeader>
            <CardContent>
              <CardStats>
                <StatItem label="Sharpe" value="1.45" />
                <StatItem label="Return" value="8.3%" variant="negative" />
                <StatItem label="Trades" value="89" />
                <StatItem label="Win Rate" value="62.1%" />
              </CardStats>
            </CardContent>
            <CardActions>
              <CardButton primary>Configure</CardButton>
            </CardActions>
          </Card>
        </div>
      </section>

      {/* Data Grid */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Data Grid</h2>
        <div className="showcase-items">
          <div className="view-toggle-container">
            <Button 
              variant={gridView === 'card' ? 'primary' : 'secondary'}
              size="sm"
              onClick={() => setGridView('card')}
            >
              Card View
            </Button>
            <Button 
              variant={gridView === 'row' ? 'primary' : 'secondary'}
              size="sm"
              onClick={() => setGridView('row')}
            >
              Row View
            </Button>
          </div>
          <DataGrid
            data={sampleData}
            viewMode={gridView}
            columns={[
              { key: 'model_id', label: 'Model ID' },
              { key: 'pack_id', label: 'Pack' },
              { key: 'sharpe', label: 'Sharpe' },
              { key: 'cum_ret', label: 'Return %' },
              { key: 'trades', label: 'Trades' },
              { key: 'win_rate', label: 'Win Rate %' }
            ]}
            showSearch
            showFilters
            showPagination
            renderCard={(item) => (
              <Card key={item.id}>
                <CardHeader>
                  <CardHeaderInfo title={item.model_id} subtitle={item.pack_id} />
                </CardHeader>
                <CardContent>
                  <CardStats>
                    <StatItem label="Sharpe" value={item.sharpe.toString()} />
                    <StatItem label="Return" value={`${item.cum_ret}%`} />
                    <StatItem label="Trades" value={item.trades.toString()} />
                    <StatItem label="Win Rate" value={`${item.win_rate}%`} />
                  </CardStats>
                </CardContent>
              </Card>
            )}
          />
        </div>
      </section>

      {/* Tooltips */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Tooltips</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Tooltip Positions</h3>
            <div className="tooltip-group">
              <Tooltip content="Top tooltip" placement="top">
                <Button variant="secondary">Top</Button>
              </Tooltip>
              <Tooltip content="Bottom tooltip" placement="bottom">
                <Button variant="secondary">Bottom</Button>
              </Tooltip>
              <Tooltip content="Left tooltip" placement="left">
                <Button variant="secondary">Left</Button>
              </Tooltip>
              <Tooltip content="Right tooltip" placement="right">
                <Button variant="secondary">Right</Button>
              </Tooltip>
              <Tooltip content="This tooltip will automatically position itself to stay within the viewport" placement="auto">
                <Button variant="secondary">Auto</Button>
              </Tooltip>
            </div>
          </div>
        </div>
      </section>

      {/* Feedback Components */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Feedback Components</h2>
        <div className="showcase-items">
          <div className="showcase-item">
            <h3>Alerts</h3>
            <div className="alert-stack">
              <Alert variant="info" title="Information">
                This is an informational message.
              </Alert>
              <Alert variant="success" title="Success">
                Operation completed successfully!
              </Alert>
              <Alert variant="warning" title="Warning">
                Please review before proceeding.
              </Alert>
              <Alert variant="error" title="Error">
                An error occurred while processing.
              </Alert>
            </div>
          </div>
          <div className="showcase-item">
            <h3>Error Banners</h3>
            <div className="alert-stack">
              <ErrorBanner 
                variant="critical" 
                message="Failed to save changes. Please try again."
                onDismiss={() => console.log('Dismissed')}
              />
              <ErrorBanner 
                variant="warning" 
                message="Sync delayed. Retrying in the background."
                onDismiss={() => console.log('Dismissed')}
              />
              <ErrorBanner 
                variant="info" 
                message="New version available. Refresh to update."
                onDismiss={() => console.log('Dismissed')}
              />
            </div>
          </div>
          <div className="showcase-item">
            <h3>Toast</h3>
            <Button onClick={() => setShowToast(true)}>Show Toast</Button>
            {showToast && (
              <Toast 
                variant="success"
                onDismiss={() => setShowToast(false)}
              >
                Operation completed successfully!
              </Toast>
            )}
          </div>
        </div>
      </section>

      {/* Empty & Error States */}
      <section className="showcase-section">
        <h2 className="showcase-section-title">Empty & Error States</h2>
        <div className="state-grid">
          <div className="state-card">
            <EmptyState 
              variant="no-data"
              title="No data available"
              message="Start by creating your first model"
              action={<Button variant="primary">Create Model</Button>}
            />
          </div>
          <div className="state-card">
            <EmptyState 
              variant="no-results"
              title="No results found"
              message="Try adjusting your filters or search terms"
              action={<Button>Clear Filters</Button>}
            />
          </div>
          <div className="state-card">
            <EmptyState 
              variant="first-time"
              title="Welcome to Sigmatiq"
              message="Start with a template or take the product tour"
              action={
                <div style={{ display: 'flex', gap: '12px' }}>
                  <Button variant="primary">Start Tour</Button>
                  <Button>Browse Templates</Button>
                </div>
              }
            />
          </div>
          <div className="state-card">
            <ErrorState 
              variant="connection"
              title="Connection Failed"
              message="Unable to connect to the server"
              details="Error: ECONNREFUSED 127.0.0.1:8080"
              actions={<Button>Retry Connection</Button>}
            />
          </div>
          <div className="state-card">
            <ErrorState 
              variant="validation"
              title="Validation Failed"
              message="Please fix the following errors:"
              details={[
                'Model ID is required',
                'Start date must be before end date',
                'Threshold must be between 0 and 1'
              ]}
              actions={<Button>Review Form</Button>}
            />
          </div>
          <div className="state-card">
            <ErrorState 
              variant="server"
              title="Server Error (500)"
              message="Something went wrong on our end"
              details="Request ID: abc123-def456"
              actions={
                <div style={{ display: 'flex', gap: '12px' }}>
                  <Button>Retry</Button>
                  <Button variant="secondary">Contact Support</Button>
                </div>
              }
            />
          </div>
        </div>
      </section>
    </div>
  )
}