/* Sigmatiq Sigma – UI Panel Renderer (schema-driven) */
(function(){
  function el(tag, attrs={}, children=[]){
    const node = document.createElement(tag);
    for (const [k,v] of Object.entries(attrs||{})){
      if (k === 'class') node.className = v;
      else if (k === 'text') node.textContent = v;
      else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v);
    }
    for (const c of (children||[])){
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    }
    return node;
  }

  function fieldControl(f){
    const wrap = el('div', { class: 'field' });
    if (f.inline) wrap.classList.add('inline');
    if (f.label) wrap.appendChild(el('label', { class: 'label', for: f.id, text: f.label }));

    let ctrl;
    const baseAttrs = { class: 'input', id: f.id, name: f.id };
    if (f.placeholder) baseAttrs.placeholder = f.placeholder;
    if (f.value !== undefined && f.type !== 'checkbox-group' && f.type !== 'radio-group' && f.type !== 'switch') baseAttrs.value = f.value;
    if (f.min !== undefined) baseAttrs.min = f.min;
    if (f.max !== undefined) baseAttrs.max = f.max;
    if (f.step !== undefined) baseAttrs.step = f.step;
    if (f.required) baseAttrs.required = 'true';

    switch(f.type){
      case 'text':
      case 'number':
      case 'search':
        baseAttrs.type = f.type;
        ctrl = el('input', baseAttrs);
        break;
      case 'textarea':
        ctrl = el('textarea', Object.assign({}, baseAttrs, { class: 'input textarea' }));
        break;
      case 'select':
        ctrl = el('select', Object.assign({}, baseAttrs, { class: 'input select' }));
        (f.options||[]).forEach(([val,label]) => {
          const opt = el('option', { value: val, text: label });
          if (f.value === val) opt.selected = true;
          ctrl.appendChild(opt);
        });
        break;
      case 'switch':
        const sw = el('label', { class: 'switch' });
        const inp = el('input', { type: 'checkbox', id: f.id, name: f.id });
        if (f.value) inp.checked = true;
        const track = el('span', { class: 'track' });
        const thumb = el('span', { class: 'thumb' });
        sw.append(inp, track, thumb);
        ctrl = sw;
        break;
      case 'checkbox-group':
        ctrl = el('div', { class: 'row' });
        (f.options||[]).forEach(([val,label]) => {
          const id = `${f.id}-${val}`;
          const l = el('label', { class: 'row', for: id });
          const c = el('input', { type: 'checkbox', class: 'input', id, name: f.id, value: val });
          c.classList.remove('input'); c.classList.add('checkbox');
          if ((f.value||[]).includes(val)) c.checked = true;
          l.append(c, document.createTextNode(' ' + label));
          ctrl.appendChild(l);
        });
        break;
      case 'radio-group':
        ctrl = el('div', { class: 'row' });
        (f.options||[]).forEach(([val,label]) => {
          const id = `${f.id}-${val}`;
          const l = el('label', { class: 'row', for: id });
          const r = el('input', { type: 'radio', class: 'input', id, name: f.id, value: val });
          r.classList.remove('input'); r.classList.add('radio');
          if (f.value === val) r.checked = true;
          l.append(r, document.createTextNode(' ' + label));
          ctrl.appendChild(l);
        });
        break;
      default:
        ctrl = el('div', { class: 'p' }, [ 'Unsupported field type: ' + f.type ]);
    }

    if (f.adornment){
      const wrap2 = el('div', { class: 'input-wrap', style: 'position:relative; display:grid; align-items:center;' });
      if (ctrl.tagName === 'INPUT' || ctrl.tagName === 'TEXTAREA' || ctrl.tagName === 'SELECT'){
        ctrl.classList.add('has-adornment');
      }
      const ad = el('span', { class: 'adornment' }, [ f.adornment ]);
      wrap2.append(ctrl, ad);
      ctrl = wrap2;
    }

    if (f.hint) wrap.appendChild(el('div', { class: 'help', text: f.hint }));
    wrap.appendChild(ctrl);
    return wrap;
  }

  function renderForm(container, panel){
    const form = el('form', { class: 'panel', id: `form-${panel.id}` });
    const grid = el('div', { class: 'grid' });
    (panel.fields||[]).forEach(f => {
      const col = el('div', { class: f.full ? 'col-12' : 'col-6' });
      col.appendChild(fieldControl(f));
      grid.appendChild(col);
    });
    form.appendChild(grid);

    if (panel.actions && panel.actions.length){
      const actions = el('div', { class: 'row', style: 'justify-content:flex-end; margin-top:12px;' });
      panel.actions.forEach(a => {
        const cls = a.kind === 'primary' ? 'btn btn-primary' : a.kind === 'outline' ? 'btn btn-outline' : 'btn btn-secondary';
        const btn = el('button', { type: 'button', class: cls, id: a.id, text: a.label });
        actions.appendChild(btn);
      });
      form.appendChild(actions);
    }

    container.appendChild(form);
  }

  function renderResults(container, panel){
    const wrap = el('section', { class: 'panel' });
    const tabs = el('div', { class: 'tabs', role: 'tablist' });
    const views = el('div');
    (panel.tabs||[]).forEach((t, idx) => {
      const btn = el('button', { class: 'tab', role:'tab', id:`tab-${t.id}`, 'aria-selected': idx===0?'true':'false', 'aria-controls':`view-${t.id}`, text: t.label, onclick: () => {
        tabs.querySelectorAll('.tab').forEach(b => b.setAttribute('aria-selected', 'false'));
        btn.setAttribute('aria-selected', 'true');
        views.querySelectorAll('[data-view]').forEach(v => v.hidden = true);
        views.querySelector(`#view-${t.id}`).hidden = false;
      }});
      tabs.appendChild(btn);

      let view;
      if (t.type === 'chart'){
        view = el('canvas', { id: `chart-${t.id}`, class: 'chart', width: 800, height: 260, 'data-view': 'chart' });
      } else if (t.type === 'table'){
        view = el('div', { class: 'table-wrap', id:`view-${t.id}`, 'data-view':'table' });
        const table = el('table', { class: 'table', 'aria-describedby': `cap-${t.id}` });
        const cap = el('caption', { id: `cap-${t.id}`, text: t.label });
        table.appendChild(cap);
        const thead = el('thead'); const tr = el('tr');
        (t.columns || []).forEach(col => tr.appendChild(el('th', { text: col.label || col.key })));
        thead.appendChild(tr); table.appendChild(thead);
        table.appendChild(el('tbody'));
        view.appendChild(table);
      } else {
        view = el('div', { class: 'alert', id:`view-${t.id}`, 'data-view':'alert' }, [ 'Unsupported tab type: ' + t.type ]);
      }
      if (t.type === 'chart'){
        const wrapper = el('div', { id:`view-${t.id}` });
        wrapper.appendChild(view);
        views.appendChild(wrapper);
      } else {
        views.appendChild(view);
      }
      if (idx !== 0) views.lastChild.hidden = true;
    });

    wrap.append(tabs, views);
    container.appendChild(wrap);
  }

  function drawLineChart(canvas, data){
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0,0,w,h);
    // background grid
    ctx.strokeStyle = 'rgba(148,163,184,0.3)';
    ctx.lineWidth = 1;
    for (let y=0; y<=5; y++){ const yy = (h-20) * y/5 + 10; ctx.beginPath(); ctx.moveTo(40, yy); ctx.lineTo(w-10, yy); ctx.stroke(); }
    // axes
    ctx.strokeStyle = 'rgba(107,114,128,0.8)'; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(40,10); ctx.lineTo(40,h-10); ctx.lineTo(w-10,h-10); ctx.stroke();
    // data
    const values = data || [];
    const min = Math.min(...values), max = Math.max(...values);
    const scaleX = (w-60) / (values.length-1);
    const scaleY = (h-40) / (max-min || 1);
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--sigma-accent') || '#3B82F6';
    ctx.lineWidth = 2;
    ctx.beginPath();
    values.forEach((v,i) => {
      const x = 40 + i*scaleX;
      const y = h-10 - (v - min) * scaleY;
      if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.stroke();
  }

  function populateTable(root, rows, columns){
    const tbody = root.querySelector('tbody');
    tbody.innerHTML = '';
    rows.forEach(r => {
      const tr = document.createElement('tr');
      columns.forEach(col => {
        const td = document.createElement('td');
        let v = r[col.key];
        if (typeof v === 'number' && col.format === 'percent') v = (v*100).toFixed(2) + '%';
        if (typeof v === 'number' && col.format === 'float') v = v.toFixed(2);
        if (typeof v === 'number' && col.format === 'int') v = String(Math.round(v));
        td.textContent = v;
        if (typeof r[col.key] === 'number') td.classList.add('num');
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  }

  function generateDemoBacktest(){
    // simple seeded-like generator for repeatability per load
    const n = 120; const base = 100;
    const eq = []; let v = base;
    for (let i=0;i<n;i++){ v *= (1 + (Math.random()-0.48)/100); eq.push(v); }
    const metrics = [
      { metric: 'CAGR', value: 0.27, note: 'Annualized' },
      { metric: 'Sharpe', value: 1.45 },
      { metric: 'Sortino', value: 2.10 },
      { metric: 'Max Drawdown', value: -0.12, note: 'Peak-to-trough' },
      { metric: 'Win Rate', value: 0.56 },
      { metric: 'Avg Trade', value: 0.003 },
    ];
    const trades = [];
    for (let i=0;i<12;i++){
      trades.push({
        id: i+1, symbol: ['SPY','QQQ','NVDA','AAPL','TSLA'][i%5],
        entry: (100 + Math.random()*100).toFixed(2),
        exit: (100 + Math.random()*100).toFixed(2),
        pnl: (Math.random()-0.45)*2
      });
    }
    return { equity: eq, metrics, trades };
  }

  function renderUIPanels(root, schema){
    root.innerHTML = '';
    const header = el('div', { class: 'header' }, [
      el('div', {}, [
        el('div', { class: 'small', text: 'Sigmatiq Sigma – UI Panel Renderer' }),
        el('h1', { class: 'h3', text: schema.pack + ' — v' + schema.version })
      ]),
      el('div', { class: 'row' }, [
        el('button', { class: 'btn', text: 'Toggle Theme', onclick: () => {
          const html = document.documentElement;
          html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
        }}),
        el('a', { class: 'btn', href: '../data/ui_panels.sample.json', download: '', text: 'Download ui_panels.json' })
      ])
    ]);
    root.appendChild(header);

    const grid = el('div', { class: 'grid' });
    root.appendChild(grid);

    // First panel assumed to be config
    const configPanel = schema.panels.find(p => p.layout && p.layout.startsWith('form'));
    const resultsPanel = schema.panels.find(p => p.layout === 'tabs');

    const leftCol = el('div', { class: 'col-5' });
    const rightCol = el('div', { class: 'col-7' });
    grid.append(leftCol, rightCol);

    if (configPanel){
      leftCol.appendChild(el('h2', { class: 'h4', text: configPanel.title }));
      renderForm(leftCol, configPanel);
    }

    // Live preview area
    const preview = el('section', { class: 'panel' }, [
      el('div', { class: 'small', text: 'Preview' }),
      el('p', { class: 'p', text: 'Adjust configuration on the left, then run a backtest to populate results.' }),
      el('canvas', { id: 'preview-spark', class: 'chart', width: 800, height: 160 }),
    ]);
    rightCol.appendChild(preview);

    // Results
    if (resultsPanel){
      rightCol.appendChild(el('h2', { class: 'h4', text: resultsPanel.title }));
      renderResults(rightCol, resultsPanel);
    }

    // Wire actions
    const runBtn = document.getElementById('run_backtest');
    if (runBtn){
      runBtn.addEventListener('click', () => {
        const out = generateDemoBacktest();
        const eq = out.equity;
        const chartTab = document.getElementById('chart-equity');
        if (chartTab){
          drawLineChart(chartTab, eq);
          // ensure Results -> Equity tab visible
          const equityView = document.querySelector('#view-equity');
          if (equityView){ equityView.hidden = false; }
          document.querySelectorAll('.tabs .tab').forEach(t => t.setAttribute('aria-selected','false'));
          const equityTabBtn = document.querySelector('#tab-equity');
          if (equityTabBtn) equityTabBtn.setAttribute('aria-selected','true');
          document.querySelectorAll('[id^="view-"]').forEach(v => v.hidden = true);
          if (equityView) equityView.hidden = false;
        }
        // metrics table
        const metricsTable = document.querySelector('#view-metrics table');
        if (metricsTable){
          const columns = [
            { key: 'metric', label: 'Metric' },
            { key: 'value', label: 'Value', format: 'float' },
            { key: 'note', label: 'Note' }
          ];
          populateTable(metricsTable, out.metrics, columns);
        }
        // trades table
        const tradesTable = document.querySelector('#view-trades table');
        if (tradesTable){
          const columns = [
            { key: 'id', label: '#', format: 'int' },
            { key: 'symbol', label: 'Symbol' },
            { key: 'entry', label: 'Entry' },
            { key: 'exit', label: 'Exit' },
            { key: 'pnl', label: 'PnL', format: 'float' }
          ];
          populateTable(tradesTable, out.trades, columns);
        }
      });
    }

    // Sparkline in preview
    const spark = document.getElementById('preview-spark');
    if (spark){
      const arr = Array.from({length: 60}, (_,i) => 100 + Math.sin(i/6)*2 + Math.random()*1.5);
      drawLineChart(spark, arr);
    }
  }

  // expose
  window.SigmatiqUIPanels = { renderUIPanels };
})();