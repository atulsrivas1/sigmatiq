# Edge Lab UI — AppShell Platform (v1)

Purpose: specify shared UI platform behaviors and tokens for theme, density, accent, and command palette so pages remain consistent.

## Root Attributes
- `data-theme`: `light | dark | slate | paper` (default respects `prefers-color-scheme`).
- `data-density`: `compact | cozy | comfortable` (default `cozy`).
- `data-edge` (optional per-pack accent): e.g., `zeroedge | swingedge | longedge | overnightedge | momentumedge`.

## Persistence
- `localStorage['ui.theme']`: one of the themes above. Empty = follow system.
- `localStorage['ui.density']`: one of the density values above.

## Semantic Tokens (CSS Variables)
- Surfaces: `--surface-1`, `--surface-2`, `--bg-primary`, `--bg-secondary`, `--bg-tertiary`, `--bg-hover`.
- Text: `--text-primary`, `--text-secondary`, `--text-muted`, `--text-inverse`.
- Borders & ring: `--border-color`, `--border-strong`, `--ring`.
- Brand: `--primary-color`, `--primary-dark`, `--accent` (derived from pack via `data-edge`).
- Status: `--status-success`, `--status-warning`, `--status-error`.

## ThemeToggle (Topbar)
- Behavior: cycles or menu of themes. On change, sets `document.documentElement.dataset.theme` and persists `ui.theme`.
- Default: if `ui.theme` not set, initialize from `window.matchMedia('(prefers-color-scheme: dark)')` to `dark` or `light`.
- A11y: toggle is a `button` with `aria-pressed` and label, keyboard-activatable, `:focus-visible` ring.

## DensitySwitch (Topbar)
- Behavior: sets `document.documentElement.dataset.density` and persists `ui.density`.
- Effect: tables/cards consume `--padding` and `--font-size` via selectors keyed on `data-density`.

## CommandPalette (Ctrl/⌘+K)
- Commands (initial):
  - “Build Model…” → open Runs page with Build tab preselected
  - “Train Model…” → Runs/Train
  - “Backtest Model…” → Runs/Backtest
  - “Open Docs” → Docs launcher
  - “Toggle Theme” → ThemeToggle
- A11y: focus trap within palette; ESC to close; `role="dialog"` and labelled title.

## Pack Accent (`--accent`)
- Derive from `data-edge` on the page root or set explicitly per view.
- Suggested mapping:
  - `zeroedge` → `--accent: var(--teal)`
  - `swingedge` → `--accent: #F59E0B`
  - `longedge` → `--accent: #A3BE3C`
  - `overnightedge` → `--accent: #6D28D9`
  - `momentumedge` → `--accent: #3B82F6`
- Use `--accent` for subtle borders, focus outlines, and badges; keep `--primary-color` for brand actions.

## Minimal Wiring (pseudo-code)
```html
<!-- index.html body tag -->
<body data-theme="light" data-density="cozy" data-edge="zeroedge">
  <div id="app"></div>
  <script type="module">
    const root = document.documentElement;
    const ls = window.localStorage;
    const sysDark = window.matchMedia('(prefers-color-scheme: dark)');

    function applyTheme(val){
      root.dataset.theme = val || (sysDark.matches ? 'dark' : 'light');
    }
    function applyDensity(val){ root.dataset.density = val || 'cozy'; }

    applyTheme(ls.getItem('ui.theme'));
    applyDensity(ls.getItem('ui.density'));

    // Theme toggle
    window.toggleTheme = () => {
      const order = ['light','dark','slate','paper'];
      const cur = root.dataset.theme; const next = order[(order.indexOf(cur)+1)%order.length];
      applyTheme(next); ls.setItem('ui.theme', next);
    };

    // Density switch
    window.setDensity = (val) => { applyDensity(val); ls.setItem('ui.density', val); };
  </script>
</body>
```

## CSS Hooks (example)
```css
/* Density-driven values */
[data-density="compact"] { --padding: 6px; --font-size: 12px; }
[data-density="cozy"] { --padding: 12px; --font-size: 14px; }
[data-density="comfortable"] { --padding: 16px; --font-size: 16px; }

/* Accent per pack */
[data-edge="zeroedge"] { --accent: var(--teal); }
[data-edge="swingedge"] { --accent: #F59E0B; }
/* ... */

/* Focus ring (applied across interactive) */
.button:focus-visible, .chip:focus-visible, a:focus-visible { box-shadow: var(--ring); outline: none; }
```

## Accessibility & Performance
- Always show `:focus-visible` outlines on keyboard focus.
- Respect reduced motion for any transitions; avoid large layout shifts.
- Keep palette contrast ≥ WCAG AA; use high-contrast theme for critical workflows.

## Testing
- Unit: Theme/density utilities set root attributes and persist to storage.
- E2E: Keyboard nav through topbar; palette opens on Ctrl/⌘+K; theme toggles and persists across reloads.

