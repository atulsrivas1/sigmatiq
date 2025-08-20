# Sigmatiq Sigma – Inputs (Batch 3)

Accessible, theme-aware inputs aligned with the Sigmatiq token system.

## Include
```html
<link rel="stylesheet" href="/tokens/colors.css">
<link rel="stylesheet" href="/tokens/typography.css">
<link rel="stylesheet" href="/components/inputs.css">
```

Ensure the `<html>` element has `data-theme="light|dark"` and optionally `data-sigma="zero|swing|long|overnight|custom"`.

## Components
- `.input` text, number, search, textarea
- `.select` (custom arrow icon via `.select-arrow`)
- `.switch` (checkbox-based toggle)
- `.checkbox` / `.radio` (custom, accent-aware)
- `.field` layout with `.label`, `.help`, `.error`

## States
- Error: set `aria-invalid="true"` and pair with `aria-describedby="…-error"`
- Success (optional class): `.valid`
- Disabled: `disabled` or `aria-disabled="true"`
- Read-only: `readonly`

## Icons & adornments
Add `.has-leading` / `.has-trailing` to the `.input` when placing icons inside `.input-wrap`. Use `.adornment` for units (e.g., `%`).

## Accessibility
- Always use `<label for="...">` and input `id` pairs or wrap input inside label.
- Use `aria-describedby` for hint/error text.
- Keep native HTML semantics where possible for improved AT support.
- Icon-only controls require `aria-label`.

## Tailwind mapping
Reuse the mapping from foundations (colors, shadows, radii). Class strategy can be hybrid: Tailwind for layout + these component styles for consistency.