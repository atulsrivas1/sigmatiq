import axios from 'axios'

// Allow overriding API base via Vite env (useful when not using Vite dev proxy)
// Preferred: keep UI on relative '/api' and route via proxy or gateway
const API_BASE_URL = (import.meta as any)?.env?.VITE_API_BASE_URL || '/api'

// Dev trace to confirm effective base
try {
  const MODE = (import.meta as any)?.env?.MODE
  if (MODE === 'development') {
    // eslint-disable-next-line no-console
    console.log(`[api] base: ${API_BASE_URL}`)
  }
} catch {}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    const msg = (error?.response?.data?.error as string) || error?.message || 'Unknown error'
    return Promise.reject(new Error(msg))
  }
)

// API Methods
export const apiService = {
  // Health & Status
  getHealth: () => api.get('/health'),
  
  // Models
  getModels: (params?: { model_id?: string; pack_id?: string; limit?: number; offset?: number }) =>
    api.get('/models', { params }),
  
  getModelDetail: (model_id: string, pack_id: string) =>
    api.get('/model_detail', { params: { model_id, pack_id } }),
  
  createModel: (data: { template_id: string; name: string; risk_profile: string }) =>
    api.post('/models', data),
  
  // Leaderboard
  getLeaderboard: (params?: {
    model_id?: string
    pack_id?: string
    tag?: string
    risk_profile?: string
    pass_gate?: boolean
    limit?: number
    offset?: number
  }) => api.get('/leaderboard', { params }),
  
  // Signals
  getSignals: (params?: {
    model_id?: string
    start?: string
    end?: string
    status?: string
    limit?: number
    offset?: number
  }) => api.get('/signals', { params }),
  
  getOptionSignals: (params?: { limit?: number; offset?: number }) =>
    api.get('/option_signals', { params }),
  
  // Indicators
  getIndicatorSets: () => api.get('/indicator_sets'),
  
  // Pipeline Operations
  buildMatrix: (data: { model_id: string; pack_id: string; start: string; end: string }) =>
    api.post('/build_matrix', data),
  
  previewMatrix: (data: { model_id: string; pack_id: string; start: string; end: string }) =>
    api.post('/preview_matrix', data),
  
  train: (data: { model_id: string; pack_id: string; csv?: string; calibration?: any }) =>
    api.post('/train', data),
  
  backtest: (data: { model_id: string; pack_id: string; config?: any; matrix_sha?: string }) =>
    api.post('/backtest', data),
  
  backtestSweep: (data: { model_id: string; risk_profile: string; sweep: any; tag?: string }) =>
    api.post('/backtest_sweep', data),
  
  // Calibration
  calibrateThresholds: (data: { model_id: string; grid?: string; top_n?: number }) =>
    api.post('/calibrate_thresholds', data),
  
  // Scanning
  scan: (data: {
    pack_id: string
    model_id: string
    indicator_set: string
    start: string
    end: string
    tickers?: string
    universe_csv?: string
    top_n?: number
  }) => api.post('/scan', data),
  
  // Policy
  explainPolicy: (model_id: string, pack_id: string) =>
    api.get('/policy/explain', { params: { model_id, pack_id } }),
}

export default api
