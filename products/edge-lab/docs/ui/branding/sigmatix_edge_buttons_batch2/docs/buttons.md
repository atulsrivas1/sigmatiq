# Sigmatiq Edge – Buttons (Batch 2)

Accessible, theme-aware buttons with Edge Pack accent support.

## Include

```html
<link rel="stylesheet" href="/tokens/colors.css">
<link rel="stylesheet" href="/tokens/typography.css">
<link rel="stylesheet" href="/components/buttons.css">
```

Ensure the `<html>` element has `data-theme="light|dark"` and optionally `data-edge="zero|swing|long|overnight|custom"`.

## Variants
- `.btn-primary` (accented via `--edge-accent`)
- `.btn-secondary` (neutral)
- `.btn-outline` (accent outline)
- `.btn-ghost` (minimal)
- `.btn-soft` (tinted accent)
- Status: `.btn-success`, `.btn-info`, `.btn-warning`, `.btn-danger`

## Sizes
- `.btn-sm`, `.btn-md`, `.btn-lg`

## Icons & Loading
Use inline SVG with `currentColor`. Show a spinner with `[aria-busy="true"]` and an element `[data-spinner]` inside.

```html
<button class="btn btn-primary" aria-busy="true">
  <span data-spinner class="spinner" aria-hidden="true"></span>
  <span class="label">Processing…</span>
</button>
```

## Accessibility
- Provide `aria-label` for icon-only buttons.
- Uses `:focus-visible` ring tied to `--focus-ring` token.
- Disabled state via `disabled` or `aria-disabled="true"`.

## Tailwind Mapping (Optional)
You can map CSS variables into Tailwind theme tokens (`colors.edge`, etc.) as shown in the foundation docs.