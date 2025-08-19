export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-header">
      <div class="page-title">Docs</div>
    </div>
    <div class="sample-card">
      Open docs in a new tab: <a class="top-bar-link" href="../docs/ui/README.md" target="_blank" rel="noreferrer">UI README</a>
    </div>
  `;
  return wrap;
}

