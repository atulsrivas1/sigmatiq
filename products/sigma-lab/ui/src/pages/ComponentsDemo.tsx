import React from 'react'
import { GateBadge } from '../components/trust/GateBadge'
import { HealthTile, HealthTiles } from '../components/health/HealthTile'
import { TemplatesGrid, TemplateCard } from '../components/templates/TemplateCard'
import { FiltersRow } from '../components/filters/FiltersRow'
import { SearchInput } from '../components/filters/SearchInput'
import { CompactSelect } from '../components/filters/CompactSelect'
import { FilterChip } from '../components/filters/FilterChip'
import { SignalsTable, type SignalsRow } from '../components/signals/SignalsTable'
import { JobsTable } from '../components/admin/JobsTable'
import { JobStatusPill } from '../components/admin/JobStatusPill'
import { ChartHeader } from '../components/charts/ChartHeader'
import { ChartContainer } from '../components/charts/ChartContainer'
import { KPIStat } from '../components/common/KPIStat'
import { Sparkline } from '../components/common/Sparkline'
import { StatusBadge } from '../components/common/StatusBadge'
import { ModelIdLink } from '../components/common/ModelIdLink'
import { ConfidenceBadge } from '../components/signals/ConfidenceBadge'
import { SidePill } from '../components/signals/SidePill'
import { TickerBadge } from '../components/signals/TickerBadge'

export const ComponentsDemo: React.FC = () => {
  const signalRows: SignalsRow[] = [
    { ts: '2025-08-19T15:30:00Z', model: 'spy_opt_0dte_hourly', ticker: 'SPY', side: 'Long', conf: 0.78, pack: 'zerosigma' },
    { ts: '2025-08-19T15:31:00Z', model: 'aapl_eq_swing_daily', ticker: 'AAPL', side: 'Short', conf: 0.61, pack: 'swingsigma' },
  ]

  return (
    <div className="dashboard-page">
      <div className="container">
        <section className="section">
          <div className="section-header"><h2 className="section-title">Components Demo</h2></div>

          {/* Trust Gate + Health Tiles */}
          <div className="panel" style={{ marginBottom: 20 }}>
            <h3 className="panel-title">Gate + Health</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
              <GateBadge pass={true} reasons={["✓ Min trades: 10 ≥ 5", "✓ Max DD: 8% ≤ 20%"]} />
              <GateBadge pass={false} reasons={["✗ Min trades: 3 < 5"]} />
            </div>
            <HealthTiles>
              <HealthTile label="API" value="OPERATIONAL" status="ok" />
              <HealthTile label="Database" value="DEGRADED" status="warn" />
              <HealthTile label="Data Feed" value="CONNECTED" status="ok" />
            </HealthTiles>
          </div>

          {/* Templates */}
          <div className="panel" style={{ marginBottom: 20 }}>
            <h3 className="panel-title">Template Cards</h3>
            <TemplatesGrid>
              <TemplateCard name="Breakout Scanner" description="Equity daily breakout with momentum alignment" meta={[{label:'Sharpe', value:'1.8'}]} tags={['Equity','Daily']} featured />
              <TemplateCard name="0DTE Options" description="Intraday SPY scalper with risk controls" meta={[{label:'Sharpe', value:'2.1'}]} tags={['Options','Intraday']} />
            </TemplatesGrid>
          </div>

          {/* Filters Bar */}
          <div className="panel" style={{ marginBottom: 20 }}>
            <h3 className="panel-title">Filters Row</h3>
            <FiltersRow
              left={<SearchInput placeholder="Search..." />}
              right={<CompactSelect><option>All Packs</option><option>zerosigma</option></CompactSelect>}
            >
              <FilterChip>Active</FilterChip>
              <FilterChip active>Training</FilterChip>
              <FilterChip>Paused</FilterChip>
            </FiltersRow>
          </div>

          {/* Signals + Cells */}
          <div className="panel" style={{ marginBottom: 20 }}>
            <h3 className="panel-title">Signals Table</h3>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 12 }}>
              <ModelIdLink id="spy_opt_0dte_hourly" />
              <TickerBadge ticker="SPY" />
              <SidePill side="Long" />
              <ConfidenceBadge value={0.72} />
              <StatusBadge variant="info">Info</StatusBadge>
            </div>
            <SignalsTable rows={signalRows} />
          </div>

          {/* Jobs Table */}
          <div className="panel" style={{ marginBottom: 20 }}>
            <h3 className="panel-title">Jobs Table</h3>
            <JobsTable headers={["Job ID","Type","Submitted","Status","Actions"]}>
              <tr>
                <td><span className="job-id">job_abc123</span></td>
                <td>Backtest</td>
                <td>2025-08-19 11:30</td>
                <td><JobStatusPill status="running" /></td>
                <td className="job-actions"><button className="btn btn-sm">Cancel</button><button className="btn btn-sm">Details</button></td>
              </tr>
              <tr>
                <td><span className="job-id">job_def456</span></td>
                <td>Train</td>
                <td>2025-08-18 09:10</td>
                <td><JobStatusPill status="completed" /></td>
                <td className="job-actions"><button className="btn btn-sm">Logs</button></td>
              </tr>
            </JobsTable>
          </div>

          {/* Charts */}
          <div className="charts-grid">
            <ChartContainer>
              <ChartHeader title="Equity Curve" right={<>
                <button className="chart-control-btn active">Day</button>
                <button className="chart-control-btn">Week</button>
                <button className="chart-control-btn">Month</button>
              </>} />
              <Sparkline />
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2,1fr)', gap: 12, marginTop: 12 }}>
                <KPIStat label="Sharpe" value={1.92} trend="positive" />
                <KPIStat label="Max DD" value={'-12%'} trend="negative" />
              </div>
            </ChartContainer>
            <ChartContainer>
              <ChartHeader title="Capacity" />
              <div className="card-chart" style={{ height: 80, marginTop: 8 }} />
            </ChartContainer>
          </div>

        </section>
      </div>
    </div>
  )
}

