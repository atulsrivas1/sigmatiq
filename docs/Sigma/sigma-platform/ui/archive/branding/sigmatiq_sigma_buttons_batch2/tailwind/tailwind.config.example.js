/** Example tailwind.config.js mapping to Sigmatiq tokens */
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
        sigma: 'var(--sigma-accent)',
        success: 'var(--success-fg)',
        info: 'var(--info-fg)',
        warning: 'var(--warning-fg)',
        danger: 'var(--danger-fg)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
      boxShadow: {
        sig1: 'var(--shadow-1)',
        sig2: 'var(--shadow-2)',
      }
    }
  }
}