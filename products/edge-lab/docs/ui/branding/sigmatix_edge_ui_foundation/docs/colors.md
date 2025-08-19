# Sigmatiq Edge – Color Tokens

Theme-aware semantic tokens and brand accents for Edge Packs.

## Semantic tokens

- `--color-bg`, `--color-surface-1`, `--color-surface-2`, `--color-border`
- `--color-text-1`, `--color-text-2`
- Status: `--success-*`, `--info-*`, `--warning-*`, `--danger-*`
- Focus: `--focus-ring`
- Elevation: `--shadow-1`, `--shadow-2`

## Edge Pack accents

- `--edge-zero-accent` (ZeroEdge)
- `--edge-swing-accent` (SwingEdge)
- `--edge-long-accent` (LongEdge)
- Reserved: `--edge-overnight-accent`, `--edge-custom-accent`

Use a container attribute to apply an accent:

```html
<section data-edge="zero">
  <h4 class="h4 sig-accent">ZeroEdge</h4>
</section>
```

## Dark mode

Dark mode is enabled by setting `data-theme="dark"` on the `<html>` element.

```html
<html data-theme="dark"> ... </html>
```

## Tailwind mapping (example)

```js
// tailwind.config.js (excerpt)
const withOpacity = (varName) => ({ opacityValue }) => {
  if (opacityValue === undefined) return `rgb(var(${varName}))`;
  return `rgb(var(${varName}) / ${opacityValue})`;
};

module.exports = {
  theme: {
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface: {
          1: 'var(--color-surface-1)',
          2: 'var(--color-surface-2)'
        },
        border: 'var(--color-border)',
        text: {
          1: 'var(--color-text-1)',
          2: 'var(--color-text-2)'
        },
        edge: {
          DEFAULT: 'var(--edge-accent)'
        }
      },
      boxShadow: {
        sig1: 'var(--shadow-1)',
        sig2: 'var(--shadow-2)'
      }
    }
  }
}
```