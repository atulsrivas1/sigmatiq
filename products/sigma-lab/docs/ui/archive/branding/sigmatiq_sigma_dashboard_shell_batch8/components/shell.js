(function(){
  const $ = sel => document.querySelector(sel);

  function initToggles(){
    const themeBtn = $('#themeToggle'), packSel = $('#packSel'), menuBtn = $('#menuToggle');
    if (themeBtn){
      themeBtn.addEventListener('click', () => {
        const html = document.documentElement;
        const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        try { localStorage.setItem('sig_theme', next); } catch {}
      });
      try { const saved = localStorage.getItem('sig_theme'); if (saved) document.documentElement.setAttribute('data-theme', saved); } catch {}
    }
    if (packSel){
      packSel.addEventListener('change', e => {
        document.documentElement.setAttribute('data-sigma', e.target.value);
        try { localStorage.setItem('sig_edge', e.target.value); } catch {}
      });
      try { const saved = localStorage.getItem('sig_edge'); if (saved) { document.documentElement.setAttribute('data-sigma', saved); packSel.value = saved; } } catch {}
    }
    if (menuBtn){
      menuBtn.addEventListener('click', () => {
        $('#sidebar').classList.toggle('open');
      });
    }
  }

  function initNav(){
    const current = location.hash.replace('#','') || 'overview';
    document.querySelectorAll('.nav a').forEach(a => {
      const key = a.getAttribute('data-key');
      a.setAttribute('aria-current', key === current ? 'page' : 'false');
    });
  }

  function sortTable(table, key, numeric=false){
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const th = table.querySelector('th[data-key="'+key+'"]');
    const dir = th.classList.contains('asc') ? 'desc' : 'asc';
    table.querySelectorAll('th.sort').forEach(h => h.classList.remove('asc','desc'));
    th.classList.add(dir);
    rows.sort((a,b) => {
      const av = a.querySelector('[data-col="'+key+'"]').dataset.value || a.querySelector('[data-col="'+key+'"]').textContent.trim();
      const bv = b.querySelector('[data-col="'+key+'"]').dataset.value || b.querySelector('[data-col="'+key+'"]').textContent.trim();
      if (numeric){ return dir==='asc' ? (parseFloat(av)-parseFloat(bv)) : (parseFloat(bv)-parseFloat(av)); }
      return dir==='asc' ? av.localeCompare(bv) : bv.localeCompare(av);
    });
    rows.forEach(r => tbody.appendChild(r));
  }

  function initTable(){
    const table = document.getElementById('runsTable');
    if (!table) return;
    table.querySelectorAll('th.sort').forEach(th => {
      th.addEventListener('click', () => sortTable(table, th.dataset.key, th.dataset.type==='num'));
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    initToggles();
    initNav();
    initTable();
  });
})();