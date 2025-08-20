export type Theme = 'light' | 'dark'
export type Pack = 'zero' | 'swing' | 'long' | 'overnight' | 'custom'

export function setTheme(theme: Theme) {
  document.documentElement.setAttribute('data-theme', theme)
}

export function setPack(pack: Pack) {
  document.documentElement.setAttribute('data-edge', pack)
}

export function initBrand() {
  if (!document.documentElement.getAttribute('data-theme')) setTheme('dark')
  if (!document.documentElement.getAttribute('data-edge')) setPack('zero')
  document.title = 'Sigmatiq Sigma'
}

