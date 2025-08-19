/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{ts,tsx,js,jsx}'
  ],
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface1: 'var(--color-surface-1)',
        surface2: 'var(--color-surface-2)',
        border: 'var(--color-border)',
        text1: 'var(--color-text-1)',
        text2: 'var(--color-text-2)',
        accent: 'var(--sigma-accent)'
      },
      fontFamily: {
        display: 'var(--font-display)',
        body: 'var(--font-body)'
      },
      boxShadow: {
        base: 'var(--shadow-1)'
      }
    }
  },
  plugins: []
}

