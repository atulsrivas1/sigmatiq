import Button from './components/Button'
import { setTheme, setPack } from './brand/theme'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { BRAND_NAME } from './brand/brand'

export default function App() {
  const loc = useLocation()
  return (
    <div className="min-h-full bg-bg text-text1">
      <header className="border-b border-border bg-surface1">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-3">
          <img src="/favicon.svg" alt="logo" className="w-6 h-6" />
          <h1 className="font-display text-lg font-bold">{BRAND_NAME}</h1>
          <nav className="ml-6 flex gap-4 text-sm">
            <NavLink to="/" active={loc.pathname === '/'}>Models</NavLink>
            <NavLink to="/signals" active={loc.pathname.startsWith('/signals')}>Signals</NavLink>
            <NavLink to="/sweep" active={loc.pathname.startsWith('/sweep')}>Backtest Sweep</NavLink>
          </nav>
          <div className="ml-auto flex items-center gap-2">
            <select className="input" onChange={(e)=> setTheme(e.target.value as any)} defaultValue="dark">
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
            <select className="input" onChange={(e)=> setPack(e.target.value as any)} defaultValue="zero">
              <option value="zero">Zero</option>
              <option value="swing">Swing</option>
              <option value="long">Long</option>
              <option value="overnight">Overnight</option>
              <option value="custom">Custom</option>
            </select>
            <button className="btn btn-accent" onClick={()=>window.location.reload()}>Refresh</button>
          </div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}

function NavLink({ to, active, children }: { to: string, active: boolean, children: any }){
  return (
    <Link to={to} className={`px-2 py-1 rounded ${active ? 'text-accent' : 'text-text2 hover:text-text1'}`}>{children}</Link>
  )}
