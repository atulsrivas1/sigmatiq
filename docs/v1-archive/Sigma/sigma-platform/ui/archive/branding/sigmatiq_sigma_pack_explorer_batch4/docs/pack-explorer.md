# Sigmatiq Sigma – Pack Explorer (Batch 4)

Grid-based explorer for discovering and managing **Sigma Packs** with versioning, tags, and quick actions.

## Features
- **Search & Sort**: client-side filtering + sort by updated/name
- **Cards**: show horizon badge, description, stats (models, signals), tags
- **Version switcher**: per-pack `<select>`
- **Quick actions**: Install / View Panels / Docs
- **Theme-aware** with accent color tied to pack using `data-sigma`

## Markup pattern
```html
<article class="card" data-sigma="zero" role="article" aria-labelledby="title-zero">
  <header class="card-header">
    <div class="card-title">
      <svg class="icon" ...></svg>
      <h3 id="title-zero" class="h4">ZeroSigma</h3>
      <span class="badge">Intraday</span>
    </div>
    <div class="version">
      <label class="small" for="v-zero">Version</label>
      <select id="v-zero" class="input select"> ... </select>
    </div>
  </header>
  <p class="p desc">Description…</p>
  <div class="meta">…</div>
  <div class="tags">
    <span class="tag">microstructure</span>
  </div>
  <div class="card-actions">
    <button class="btn btn-primary">Install</button>
    <button class="btn btn-outline">View Panels</button>
    <button class="btn btn-ghost">Docs</button>
  </div>
</article>
```

## Data model (suggested)
```ts
type SigmaPack = {
  key: string;            // "zero" | "swing" | "long" | "overnight" | "custom"
  name: string;           // "ZeroSigma"
  sigma: string;           // maps to data-sigma
  horizon: string;        // "Intraday" | "Swing" | ...
  desc: string;
  models: number;
  signals: number;
  updated: string;        // ISO (YYYY-MM-DD)
  versions: string[];
  tags: string[];
};
```

## Theming
- Set `data-theme="light|dark"` on `<html>`
- Accent is driven by `data-sigma` on each card; tokens: `--sigma-zero-accent`, `--sigma-swing-accent`, etc.

## Integration tips
- Replace the `packs` array in `preview/index.html` with your registry data or load `data/packs.sample.json` and `render()`.
- Wire **Install** to your backend/CLI for `sigma pack install <name>@<version>`.
- **View Panels** should navigate to the schema-driven UI (coming in Batch 5).
- Use semantic `<article>` and label cards with `aria-labelledby` for accessibility.