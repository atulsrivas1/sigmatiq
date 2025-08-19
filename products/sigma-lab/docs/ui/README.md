# Sigma Lab UI — Getting Started

This short guide shows how to use the AppShell platform (themes, density, and pack accents) and wire a minimal shell for mockups or a future SPA.

## Prereqs
- Open `products/sigma-lab/ui/app_shell_template.html` in a browser to see the shell.
- Tokens and base styles live in `products/sigma-lab/ui/assets/style.css`.
- Platform behaviors are specified in `products/sigma-lab/docs/ui/AppShell_Platform_v1.md`.

## Minimal AppShell (HTML)
Use the template as a starter. It sets `data-theme` and `data-density` on `<html>` and persists preferences to `localStorage`.

```html
<!doctype html>
<html lang="en" data-theme="light" data-density="cozy" data-edge="zeroedge">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sigma Lab — AppShell</title>
    <link rel="stylesheet" href="assets/style.css" />
    <style>
      .app-content { padding: 20px; }
      .topbar-right { display: flex; gap: 10px; align-items: center; }
      .select { background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: 6px; padding: 6px 8px; }
    </style>
  </head>
  <body>
    <div class="app-container">
      <div class="top-bar">
        <div class="logo-section">
          <button class="menu-toggle" aria-label="Toggle menu">☰</button>
          <a href="#" class="logo-container" aria-label="Sigmatiq home">
            <img src="assets/logo.svg" class="logo-mark" alt="Sigmatiq logo" />
            <div class="text-content">
              <div class="sigma-lab">EDGE LAB</div>
              <div class="sigmatiq">SIGMATIQ</div>
              <div class="tagline">EVIDENCE TO GOVERNED ACTION</div>
            </div>
          </a>
        </div>
        <div class="topbar-right">
          <button id="cmdk" class="theme-toggle" aria-label="Open command palette" title="Command Palette (Ctrl/⌘+K)">⌘K</button>
          <button id="themeBtn" class="theme-toggle" aria-label="Toggle theme" title="Theme">◑</button>
          <label>
            <span class="sr-only">Density</span>
            <select id="densitySel" class="select" aria-label="Density">
              <option value="compact">Compact</option>
              <option value="cozy" selected>Cozy</option>
              <option value="comfortable">Comfortable</option>
            </select>
          </label>
          <a class="top-bar-link" href="../INDEX.md" target="_blank" rel="noreferrer">Docs</a>
        </div>
      </div>
      <div class="main-layout">
        <aside class="sidebar">
          <a class="nav-item active" href="#"><span class="nav-icon icon-dashboard"><span></span></span>Dashboard</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-models"><span></span></span>Models</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-build"><span></span></span>Build/Train/Backtest</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-sweeps"><span></span></span>Sweeps</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-leaderboard"><span></span></span>Leaderboard</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-signals"><span></span></span>Signals</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-overlay"><span></span></span>Overlay</a>
          <a class="nav-item" href="#"><span class="nav-icon icon-docs"><span></span></span>Docs</a>
        </aside>
        <main class="content-area">
          <div class="page-container app-content">
            <h1 class="page-title">Welcome</h1>
            <p>Use the theme and density controls in the top bar. Tokens from <code>assets/style.css</code> drive surfaces, text, borders, and status colors.</p>
          </div>
        </main>
      </div>
    </div>
    <script>
      (function () {
        const root = document.documentElement;
        const ls = window.localStorage;
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        const userTheme = ls.getItem('ui.theme');
        const userDensity = ls.getItem('ui.density');
        root.dataset.theme = userTheme || (prefersDark.matches ? 'dark' : 'light');
        root.dataset.density = userDensity || 'cozy';

        document.getElementById('themeBtn').addEventListener('click', () => {
          const order = ['light', 'dark', 'slate', 'paper'];
          const next = order[(order.indexOf(root.dataset.theme) + 1) % order.length];
          root.dataset.theme = next; ls.setItem('ui.theme', next);
        });
        document.getElementById('densitySel').addEventListener('change', (e) => {
          const val = e.target.value; root.dataset.density = val; ls.setItem('ui.density', val);
        });
        // Simple Cmd+K handler (placeholder)
        window.addEventListener('keydown', (e) => {
          const isCmdK = (e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K');
          if (isCmdK) { e.preventDefault(); alert('Command Palette (stub)'); }
        });
      })();
    </script>
  </body>
</html>
```

## Next Steps
- Replace the alert-based Command Palette with a real dialog component.
- Thread the shell into your framework of choice (React/Vite, etc.) and lift theme/density state into context.
- Add Trust HUD, lineage chips, and sweeps components per the wireframes.

