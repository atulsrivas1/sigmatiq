# Sigmatiq Sigma — Batch 8: Dashboard Shell

Top bar, collapsible sidebar, and content area with tokenized theming and pack accents.
Includes a sortable, sticky-header **table** pattern and KPI tiles.

## Files
- `components/shell.css` — layout, topbar, sidebar, KPI, utilities
- `components/table.css` — sticky header, hover states, badges, sorting affordances
- `components/shell.js` — theme/pack toggles, responsive sidebar, table sorting
- `tokens/colors.css`, `tokens/typography.css`, `tokens/sigma-pack-themes.css`
- `preview/index.html` — full page demo with KPIs + runs table
- `icons/*.svg` — minimal glyphs

## Usage
1. Include token CSS then shell & table CSS.
2. Add the `.app` grid with `.topbar`, `.sidebar`, and `.main` regions.
3. Wire controls via `components/shell.js` (no dependencies).

### Sorting
Add `class="sort"` + `data-key="<key>"` and optional `data-type="num"` on `<th>`.
Each row must mark cells with `data-col="<key>"` and optional `data-value` for numeric comparisons.

### Theming
- Theme: `<html data-theme="light|dark">`
- Pack accent: `<html data-sigma="zero|swing|long|overnight|custom">`

### Accessibility
- Skip link to main content.
- Sidebar uses `role="navigation"` with aria-label.
- Topbar & main have appropriate roles.

You can now drop in earlier **Batch 7** Alerts & Signal Cards or the **Pack Explorer / Renderer** inside the shell.