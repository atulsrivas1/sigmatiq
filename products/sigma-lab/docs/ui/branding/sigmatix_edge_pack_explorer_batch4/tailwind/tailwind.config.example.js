/** Example tailwind.config.js mapping to Sigmatiq tokens (used by Pack Explorer too) */
module.exports = {
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        border: 'var(--color-border)',
        text: {
          1: 'var(--color-text-1)',
          2: 'var(--color-text-2)',
        },
        edge: 'var(--sigma-accent)',
      },
      boxShadow: {
        sig1: 'var(--shadow-1)',
        sig2: 'var(--shadow-2)',
      },
      borderRadius: {
        md: '10px',
        lg: '12px',
      }
    }
  }
}