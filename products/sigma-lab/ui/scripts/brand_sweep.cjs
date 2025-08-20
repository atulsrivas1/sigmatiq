const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src');
// Flag legacy brand/product names in UI source files
// - Sigmatix → Sigmatiq
// - ZeroEdge → ZeroSigma (except literal "ZeroEdge Workspace" if present)
const banned = [
  /\bSigmatix\b/i,
  /sigmatix[_-]/i,
  /ZeroEdge(?!\sWorkspace)/i,
];
let bad = [];

function walk(p){
  const st = fs.statSync(p);
  if (st.isDirectory()){
    for (const f of fs.readdirSync(p)){
      if (f === 'brand' || f === 'styles' || f === 'routes' || f.endsWith('.tsx') || f.endsWith('.ts') || f.endsWith('.css')){
        walk(path.join(p,f));
      }
    }
  } else if (st.isFile()){
    const rel = path.relative(SRC, p);
    if (!rel.startsWith('..')){
      const txt = fs.readFileSync(p, 'utf8');
      for (const re of banned){
        if (re.test(txt)) bad.push(rel);
      }
    }
  }
}

if (fs.existsSync(SRC)){
  walk(SRC);
}
if (bad.length){
  console.error('Brand sweep failed. Found legacy names in:');
  for (const f of bad) console.error(' -', f);
  process.exit(1);
} else {
  console.log('Brand sweep OK');
}

