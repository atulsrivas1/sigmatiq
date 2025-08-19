import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './styles/global.css'
import { initBrand } from './brand/theme'
import App from './App'
import Dashboard from './routes/Dashboard'
import Models from './routes/Models'
import Signals from './routes/Signals'
import BacktestSweep from './routes/BacktestSweep'

initBrand()

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'signals', element: <Signals /> },
      { path: 'sweep', element: <BacktestSweep /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
