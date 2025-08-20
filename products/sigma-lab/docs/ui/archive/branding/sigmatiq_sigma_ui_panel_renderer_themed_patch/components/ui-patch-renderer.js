(function(){
  function el(tag, attrs={}, children=[]){
    const node = document.createElement(tag);
    for (const [k,v] of Object.entries(attrs||{})){
      if (k === 'class') node.className = v;
      else if (k === 'text') node.textContent = v;
      else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v);
    }
    (children||[]).forEach(c => node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c));
    return node;
  }
  function render(root, schema){
    root.innerHTML='';
    const hero = el('header', { class: 'pack-hero' }, [
      el('div', { class: 'inner' }, [
        el('div', {}, [ el('div', { class: 'small', text: 'Sigmatiq Sigma' }), el('h1', { class: 'h3', text: 'UI Panel Renderer — Themed' }) ]),
        el('div', { class: 'row' }, [
          el('button', { class: 'btn', text: 'Toggle Theme', onclick: () => {
            const html = document.documentElement;
            html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
          }}),
          (() => {
            const sel = el('select', { class: 'btn', id: 'packSel' });
            [['zero','ZeroSigma'],['swing','SwingSigma'],['long','LongSigma'],['overnight','OvernightSigma'],['custom','CustomizedSigma']].forEach(([k,v])=>{
              sel.appendChild(el('option', { value: k, text: v }));
            });
            sel.addEventListener('change', e => document.documentElement.setAttribute('data-sigma', e.target.value));
            return sel;
          })()
        ])
      ])
    ]);
    root.appendChild(hero);

    const grid = el('div', { class: 'container grid' });
    const left = el('div', { class: 'col-5 panel' });
    const right = el('div', { class: 'col-7 panel' });
    grid.append(left, right);
    root.appendChild(grid);

    // Simple form
    left.append(
      el('div', { class: 'small', text: 'Configuration' }),
      el('label', { class: 'small', for: 'symbol', text: 'Symbol' }),
      el('input', { id:'symbol', class:'input', placeholder:'SPY' }),
      el('div', { style:'height:10px' }),
      el('label', { class: 'small', for: 'lookback', text: 'Lookback (bars)' }),
      el('input', { id:'lookback', class:'input', type:'number', value:'120' }),
      el('div', { style:'height:10px' }),
      el('button', { class: 'btn btn-primary', id:'run', text:'Run Backtest' })
    );

    // Tabs & outputs
    const tabs = el('div', { class: 'tabs' }, [
      el('button', { class: 'tab', id:'tab-eq', 'aria-selected':'true', text:'Equity Curve', onclick: ()=>sel('eq') }),
      el('button', { class: 'tab', id:'tab-m', 'aria-selected':'false', text:'Metrics', onclick: ()=>sel('m') }),
    ]);
    const eq = el('canvas', { id:'chart', class:'chart', width:800, height:240 });
    const table = el('table', { class:'table', hidden:'' }, [
      el('thead', {}, [ el('tr', {}, [ el('th',{text:'Metric'}), el('th',{text:'Value'}) ]) ]),
      el('tbody')
    ]);
    right.append(tabs, eq, table);

    function sel(which){
      tabs.querySelectorAll('.tab').forEach(b => b.setAttribute('aria-selected','false'));
      if (which==='eq'){ document.getElementById('tab-eq').setAttribute('aria-selected','true'); eq.hidden=false; table.hidden=true; }
      else { document.getElementById('tab-m').setAttribute('aria-selected','true'); eq.hidden=true; table.hidden=false; }
    }

    function draw(data){
      const ctx = eq.getContext('2d');
      const w = eq.width, h = eq.height;
      ctx.clearRect(0,0,w,h);
      // grid
      ctx.strokeStyle = 'rgba(148,163,184,0.3)'; ctx.lineWidth = 1;
      for (let y=0; y<=4; y++){ const yy = (h-20)*y/4 + 10; ctx.beginPath(); ctx.moveTo(40,yy); ctx.lineTo(w-10,yy); ctx.stroke(); }
      // axes
      ctx.strokeStyle = 'rgba(107,114,128,0.8)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(40,10); ctx.lineTo(40,h-10); ctx.lineTo(w-10,h-10); ctx.stroke();
      // line color = accent
      ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--sigma-accent') || '#3B82F6';
      ctx.lineWidth = 2;
      ctx.beginPath();
      const min = Math.min(...data), max = Math.max(...data);
      const sx = (w-60)/(data.length-1), sy = (h-40)/((max-min)||1);
      data.forEach((v,i)=>{ const x=40+i*sx, y=h-10-(v-min)*sy; if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y); });
      ctx.stroke();
    }

    function run(){
      const arr = Array.from({length: 120}, (_,i) => 100 + Math.sin(i/8)*2 + (Math.random()-0.48)*1.2);
      draw(arr);
      const metrics = [
        ['CAGR', '27.1%'],
        ['Sharpe', '1.45'],
        ['Max Drawdown', '-12.0%']
      ];
      const tbody = table.querySelector('tbody'); tbody.innerHTML='';
      metrics.forEach(([k,v]) => {
        const tr = document.createElement('tr'); tr.appendChild(el('td',{text:k})); tr.appendChild(el('td',{text:v})); tbody.appendChild(tr);
      });
    }

    document.getElementById('run').addEventListener('click', run);
    run();
  }
  window.SigPatchRenderer = { render };
})();