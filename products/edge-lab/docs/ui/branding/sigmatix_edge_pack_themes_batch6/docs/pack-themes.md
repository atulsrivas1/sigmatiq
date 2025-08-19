# Sigmatiq Edge – Pack Themes (Batch 6)

This package adds **visual identities** for additional Edge Packs using a token-first approach.

## Packs & Accents
- ZeroEdge — Electric Blue `#3B82F6` (default)
- SwingEdge — Swing Orange `#F97316`
- LongEdge — Long Green `#22C55E`
- OvernightEdge — Violet `#8B5CF6`
- CustomizedEdge — Teal `#14B8A6` (reserved)

Each pack defines:
- `--edge-accent` — primary accent
- `--edge-grad-start` / `--edge-grad-end` — header/hero gradient stops
- Derived tints: `--edge-tint-12`, `--edge-tint-24`, `--edge-tint-36`

## Usage
```html
<link rel="stylesheet" href="/tokens/colors.css">
<link rel="stylesheet" href="/tokens/typography.css">
<link rel="stylesheet" href="/tokens/edge-pack-themes.css">
<link rel="stylesheet" href="/components/pack-theme-components.css">

<!-- Set on page or section root -->
<section data-edge="swing">
  <!-- components inside pick up SwingEdge theme -->
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
- Add new packs by defining `[data-edge="<key>"]` block with `--edge-accent` + gradient stops.
- Use tints via `color-mix()` for subtle backgrounds.

Refer to `preview/index.html` for a live toggle demo.