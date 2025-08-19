export const api = {
  async get<T=any>(path: string): Promise<T> {
    const url = path.startsWith('/api') ? path : `/api${path.startsWith('/')? '': '/'}${path}`
    const res = await fetch(url)
    const txt = await res.text()
    try { return JSON.parse(txt) } catch { throw new Error(`Invalid JSON: ${txt.slice(0,160)}`) }
  },
  async post<T=any>(path: string, body: any): Promise<T> {
    const url = path.startsWith('/api') ? path : `/api${path.startsWith('/')? '': '/'}${path}`
    const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body||{}) })
    const txt = await res.text()
    try { return JSON.parse(txt) } catch { throw new Error(`Invalid JSON: ${txt.slice(0,160)}`) }
  }
}
