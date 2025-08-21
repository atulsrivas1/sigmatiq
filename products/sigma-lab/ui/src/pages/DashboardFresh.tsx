import React from 'react'
import { FreshRecentModels } from '../fresh/components/dashboard/RecentModels'
import { FreshLastRuns } from '../fresh/components/dashboard/LastRuns'
import { FreshQuickActions } from '../fresh/components/dashboard/QuickActions'
import { FreshSystemHealth } from '../fresh/components/dashboard/SystemHealth'
import { FreshControlsBar } from '../fresh/components/models/ControlsBar'
import { FreshModelsContainer } from '../fresh/components/models/ModelsContainer'
import { FreshPagination } from '../fresh/components/models/Pagination'
import { freshRecentModels, freshRuns, freshHealth } from '../fresh/data/dashboard'
import { freshModels } from '../fresh/data/models'
import './Dashboard.css'

export const DashboardFresh: React.FC = () => {
  const [view, setView] = React.useState<'card'|'row'>('card')
  return (
    <div className="dashboard-page">
      <div className="container">
        <section className="section">
          <div className="section-header">
            <h2 className="section-title">Dashboard</h2>
          </div>
          <div className="dashboard-grid">
            <FreshRecentModels items={freshRecentModels} />
            <FreshLastRuns runs={freshRuns} />
            <FreshQuickActions />
            <FreshSystemHealth items={freshHealth as any} />
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2 className="section-title">Models</h2>
          </div>
          <FreshControlsBar view={view} setView={setView} />
          <FreshModelsContainer view={view} models={freshModels} />
          <FreshPagination total={freshModels.length} />
        </section>
      </div>
    </div>
  )
}

