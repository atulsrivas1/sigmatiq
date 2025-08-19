# Icons — Guidelines

Location: `products/sigma-lab/ui/assets/icons`

## Style Guide
- Size: `viewBox="0 0 24 24"`; render at 20–24px in UI.
- Stroke: `stroke="currentColor"`, `stroke-width="2"`, `stroke-linecap="round"`, `stroke-linejoin="round"`.
- Fill: prefer `fill="none"` for line icons; avoid solid fills unless needed.
- Theming: icons inherit color from parent via `currentColor`.
- Accessibility: decorative icons should be `aria-hidden="true"`; only add `<title>` for informative icons.
- Geometry: snap to whole or .5 coordinates to avoid blur; keep shapes simple enough for 24px.

## Naming
- Kebab-case descriptive names, e.g., `leaderboard.svg`, `open-sweeps.svg`.
- Alternate variants live under `_alternates/` (e.g., `/_alternates/models_css.svg`). Prefer a single canonical icon per concept; use alternates sparingly and document their use.

## Do/Don’t
- Do keep stroke and cap/join consistent across all icons.
- Do avoid inline `style` attributes; use attributes like `opacity="0.6"` instead.
- Don’t mix rounded and sharp corners arbitrarily; stay consistent within families (e.g., bars with `rx="1"`).

## Checklists
- [ ] 24×24 viewBox
- [ ] Uses `currentColor`
- [ ] stroke-width=2, round caps/joins
- [ ] No invalid path data; no inline styles
- [ ] Simple and legible at 24px
- [ ] Name follows convention

## Notes
- CSS-driven states (hover/active) should set `color` on the container rather than altering the SVG.
- If experimenting with alternates, place them in `_alternates/` and reference usage in UI docs.
