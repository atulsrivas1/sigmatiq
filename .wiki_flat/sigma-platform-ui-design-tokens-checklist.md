# Design Tokens Checklist (Align with UI assets/style.css)

Purpose
- Ensure consistent appearance across pages by reusing the token system defined in `products/sigma-lab/ui/assets/style.css`.

Core Tokens
- Colors: `--navy`, `--teal`, `--slate`, `--gray`, `--ivory`.
- Status: `--status-success`, `--status-warning`, `--status-error`.
- Surfaces: `--bg-primary`, `--bg-secondary`, `--bg-tertiary`, `--surface-1`, `--surface-2`.
- Text: `--text-primary`, `--text-secondary`, `--text-muted`, `--text-inverse`.
- Borders: `--border-color`, `--border-strong`.
- Primary: `--primary-color`, `--primary-dark`.
- Shadows/Ring: `--shadow-sm`, `--shadow-md`, `--ring`.
- Controls: `--btn-h`, `--btn-px`, `--btn-radius`, `--btn-font`, `--icon-size`.

Themes
- Supported: `data-theme="light|dark|slate|paper"`.
- Component backgrounds and text must rely on theme tokens rather than hardcoded values.

Pack Accent
- `data-sigma="zerosigma|swingsigma|longsigma|overnightsigma|momentumsigma"` → sets `--accent` for subtle accents.

Component Mapping
- Buttons `.btn-primary`/`.btn-secondary`: use `--primary-color`, borders from `--border-color`, hover `--bg-hover`.
- Cards `.card, .sample-card`: backgrounds `--surface-1`, borders `--border-color`, text `--text-secondary`.
- Navigation `.nav-item.active`: border-left and text use `--primary-color`.
- Badges (Gate): pass → `--status-success`; warn → `--status-warning`; fail → `--status-error`; n/a → `--text-muted`.
- Tables: headers `--text-secondary`, zebra rows using `--bg-secondary`.

Interactions
- Focus: use `--ring` on focus-visible for keyboard accessibility.
- Hover: use `--bg-hover` surfaces.

Density & Typography
- Density controlled by `data-density="compact|cozy|comfortable"`.
- Typography: headers 16px/26px; body 14px; tables 13–14px; rely on `--font-sans`.

Checklist
- [ ] No hardcoded colors; all from tokens.
- [ ] Respect theme/density attributes on `<html>`.
- [ ] Gate badges and status chips use status tokens consistently.
- [ ] Buttons use hover and focus-visible treatments.
- [ ] Sticky table headers and responsive card grids align with tokens.

