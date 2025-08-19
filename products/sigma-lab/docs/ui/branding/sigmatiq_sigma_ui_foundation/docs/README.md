
# Sigmatiq Sigma — UI Foundation (Batch 1)

Generated: 2025-08-15 02:18 UTC

This package contains **real, production-ready** design tokens (no placeholders) for **Sigmatiq Sigma**.

## Contents
- `tokens/` — CSS variables for colors, themes, typography, spacing, radii, shadows
- `visuals/` — SVG previews of the color palettes and type scale
- `samples/` — Minimal HTML pages showing how to use tokens in components

## How to Use (Quick Start)

1. Include the token CSS files as early as possible—ideally in your global CSS:

```html
<link rel="stylesheet" href="/tokens/colors.css" />
<link rel="stylesheet" href="/tokens/typography.css" />
<link rel="stylesheet" href="/tokens/spacing.css" />
<link rel="stylesheet" href="/tokens/radii.css" />
<link rel="stylesheet" href="/tokens/shadows.css" />
```

2. Toggle **light/dark** and **Sigma Pack accent** via attributes on the root element:

```html
<html data-theme="dark" data-pack="zerosigma">
```

3. Use tokens directly in CSS or with Tailwind **arbitrary values**:

```html
<div class="p-6 rounded-[var(--radius-md)] border" style="background:var(--surface); color:var(--text); border-color:var(--border)">
  Hello Sigmatiq Sigma
</div>
```

### Tailwind Integration (Optional)

Add the CSS variables as custom colors in `tailwind.config.js` (v3+):

```js
// tailwind.config.js
module.exports = {
  content: ["./**/*.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
    extend: {
      colors: {
        surface: "var(--surface)",
        bg: "var(--bg)",
        text: "var(--text)",
        border: "var(--border)",
        primary: "var(--primary)",
        accent: "var(--accent)",
        pack: "var(--pack-accent)",
        success: "var(--color-success)",
        info: "var(--color-info)",
        warning: "var(--color-warning)",
        danger: "var(--color-danger)",
      },
      borderRadius: {
        xs: "var(--radius-xs)",
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)",
        "2xl": "var(--radius-2xl)",
      },
      boxShadow: {
        sm: "var(--shadow-sm)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
        ring: "var(--shadow-ring)",
      }
    }
  }
};
```

### Packs
- `data-pack="zerosigma"` → Electric blue accent
- `data-pack="swingsigma"` → Orange accent
- `data-pack="longsigma"` → Green accent

You can define future packs (e.g. `overnightsigma`, `customizededge`) by adding their accents inside `tokens/colors.css` under the pack section.

---

**Next suggested batch:** Buttons and Inputs using these tokens (light/dark) + per-pack accent variants.
