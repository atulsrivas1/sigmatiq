# Sigmatiq Sigma – Pack Themes (Batch 6)

This package adds **visual identities** for additional Sigma Packs using a token-first approach.

## Packs & Accents
- ZeroSigma — Electric Blue `#3B82F6` (default)
- SwingSigma — Swing Orange `#F97316`
- LongSigma — Long Green `#22C55E`
- OvernightSigma — Violet `#8B5CF6`
- CustomizedSigma — Teal `#14B8A6` (reserved)

Each pack defines:
- `--sigma-accent` — primary accent
- `--sigma-grad-start` / `--sigma-grad-end` — header/hero gradient stops
- Derived tints: `--sigma-tint-12`, `--sigma-tint-24`, `--sigma-tint-36`

## Usage
```html
<link rel="stylesheet" href="/tokens/colors.css">
<link rel="stylesheet" href="/tokens/typography.css">
<link rel="stylesheet" href="/tokens/sigma-pack-themes.css">
<link rel="stylesheet" href="/components/pack-theme-components.css">

<!-- Set on page or section root -->
<section data-sigma="swing">
  <!-- components inside pick up SwingSigma theme -->
</section>
```

## Components
- `.pack-hero` — uses gradient tokens for a themed header
- `.btn-accent`, `.btn-outline` — accent-aware CTA styles
- `.tab[aria-selected="true"]` — accent border
- `.tag-accent` — tinted tag background

## Accessibility
- Accent-on-white text is white by default for contrast (`#fff` on gradient).
- Maintain AA contrast on body text; the tokens keep neutral surfaces for content density.

## Extend
- Add new packs by defining `[data-sigma="<key>"]` block with `--sigma-accent` + gradient stops.
- Use tints via `color-mix()` for subtle backgrounds.

Refer to `preview/index.html` for a live toggle demo.