# Brand Tokens

Core CSS design tokens used across the Sigma suite, extracted from `docs/Sigma/sigma-platform/ui/archive/branding/sigmatiq_sigma_ui_foundation/tokens` and related theme files.

## Brand Colors
- `--brand-primary`: Base brand navy (e.g., `#0A2540`).
- `--brand-teal`, `--brand-green`, `--brand-blue`, `--brand-yellow`, `--brand-red`: Accent palette.

## Sigma Pack Accents
- `--sigma-zero-accent`, `--sigma-swing-accent`, `--sigma-long-accent`, `--sigma-overnight-accent`, `--sigma-custom-accent` → per-pack accent hooks.
- Active accent: `--sigma-accent` (scoped via `[data-sigma="{pack}"]`).

## Surfaces & Text (Light)
- `--color-bg`, `--color-surface-1`, `--color-surface-2`, `--color-border`.
- `--color-text-1`, `--color-text-2`.

## Surfaces & Text (Dark overrides)
- Under `html[data-theme="dark"]`: overrides for bg/surfaces/border/text and status tokens.

## Status
- `--success-bg`/`-fg`/`-border`, `--info-*`, `--warning-*`, `--danger-*` (both themes).

## Elevation & Focus
- `--shadow-1`, `--shadow-2` (foundation); also `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-ring` in shadows pack.
- `--focus-ring` focus outline.

## Typography
- Families: `--font-display`, `--font-body`, `--font-mono`.
- Scale: `--fs-12,14,16,18,20,24,28,32,40`.
- Line height: `--lh-tight`, `--lh-normal`, `--lh-relaxed`.
- Tracking: `--tracking-tight`, `--tracking-normal`, `--tracking-wide`.

## Spacing
- 8pt-derived scale: `--space-0,1,2,3,4,5,6,7,8,10,12,16,20,24,32`.

## Radii
- `--radius-xs, -sm, -md, -lg, -xl, -2xl, -full`.

## Gradients (Icons/Brand)
- `--sigma-grad-start`, `--sigma-grad-end`, `--sigma-grad` with per-pack overrides.

## Utilities (Examples)
- `.sig-*` helpers: `sig-bg`, `sig-surface-1`, `sig-surface-2`, `sig-text-1`, `sig-text-2`, `sig-border`, `sig-elev-1`, `sig-elev-2`, `.sig-focus`.
- Brand icon helpers: `.icon`, `.accent-text`, `.accent-bg`.

Notes
- Tokens are declared under `:root` and themed via `[data-theme]` and `[data-sigma]` scopes.
- Keep UI mocks and CSS in sync with these names; prefer consuming tokens over hard-coded values.

