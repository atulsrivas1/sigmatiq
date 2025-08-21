#!/usr/bin/env bash
set -euo pipefail

# Sync docs/ into the GitHub Wiki repo for this project.
# - Copies docs/ content to a temp build folder
# - Drops the leading docs/ (so content sits at wiki root)
# - Excludes _archive/
# - Ensures Home.md exists (from INDEX.md)
# - Clones or updates the <repo>.wiki.git repo and pushes changes

ROOT_DIR="$(git rev-parse --show-toplevel)"
DOCS_DIR="$ROOT_DIR/docs"
BUILD_DIR="$ROOT_DIR/.wiki_build"
FLAT_DIR="$ROOT_DIR/.wiki_flat"
WIKI_DIR="$ROOT_DIR/.wiki_repo"

if [[ ! -d "$DOCS_DIR" ]]; then
  echo "docs/ directory not found at $DOCS_DIR" >&2
  exit 1
fi

rm -rf "$BUILD_DIR" "$FLAT_DIR"
mkdir -p "$BUILD_DIR"

# Copy docs to build dir, excluding archives and junk (rsync if available, else Python)
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '_archive/' \
    --exclude 'v1-archive/' \
    --exclude '.git/' \
    --exclude '.DS_Store' \
    "$DOCS_DIR"/ "$BUILD_DIR"/
else
  python - "$DOCS_DIR" "$BUILD_DIR" << 'PY'
import os, shutil, sys
src, dst = sys.argv[1:3]
def ignore(dir, files):
    ig = set()
    if os.path.basename(dir) in {'_archive','v1-archive'}:
        return set(files)
    for f in files:
        if f in {'.git', '.DS_Store'}:
            ig.add(f)
    return ig
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=ignore)
PY
fi

# Ensure Home.md exists (copy from INDEX.md if present)
if [[ -f "$BUILD_DIR/INDEX.md" ]]; then
  cp -f "$BUILD_DIR/INDEX.md" "$BUILD_DIR/Home.md"
fi

# Flatten directory structure into FLAT_DIR and rewrite links to flattened filenames
python - "$BUILD_DIR" "$FLAT_DIR" << 'PY'
import os, shutil, sys, re
src, dst = sys.argv[1:3]

def flatten_name(rel):
    rel = rel.replace('\\', '/').lstrip('./')
    if rel.startswith('_archive/') or rel.startswith('v1-archive/'):
        return None
    base = os.path.basename(rel)
    # Preserve Home and _Sidebar at root
    if rel in ('Home.md', '_Sidebar.md'):
        return base
    # Skip INDEX.md since Home.md is created from it
    if base.lower() == 'index.md':
        return None
    # Root-level files keep their original filename to avoid breaking links
    if '/' not in rel:
        return base
    parts = rel.split('/')
    # Drop leading 'Sigma' or 'sigma' directory if present
    if parts[0].lower() == 'sigma':
        parts = parts[1:]
    # If README.md, drop it and use the directory path
    if parts[-1].lower() == 'readme.md':
        parts = parts[:-1]
    else:
        # remove extension from last part
        root, ext = os.path.splitext(parts[-1])
        parts[-1] = root
    # Normalize segments: lowercase, spaces/underscores to hyphens
    norm = []
    for p in parts:
        p = p.replace(' ', '-').replace('_', '-').strip('-')
        p = p.lower()
        if p:
            norm.append(p)
    title = '-'.join(norm)
    if not title:
        title = 'readme'
    return f"{title}.md"

# Build mapping relpath -> flattened filename, avoid collisions
mappings = {}
os.makedirs(dst, exist_ok=True)
for root, dirs, files in os.walk(src):
    dirs[:] = [d for d in dirs if d not in {'.git', '_archive'}]
    for name in files:
        rel = os.path.relpath(os.path.join(root, name), src)
        rel = rel.replace('\\', '/')
        base = os.path.basename(rel)
        ext = os.path.splitext(base)[1].lower()
        # Only sync markdown files (keep Home.md and _Sidebar.md regardless)
        if base not in ('Home.md', '_Sidebar.md') and ext not in ('.md', '.markdown'):
            continue
        out = flatten_name(rel)
        if not out:
            continue
        candidate = out
        i = 2
        while os.path.exists(os.path.join(dst, candidate)):
            b, e = os.path.splitext(out)
            candidate = f"{b} ({i}){e}"
            i += 1
        mappings[rel] = candidate

def rewrite_links(text):
    # Markdown links: [text](path)
    def repl_md(m):
        label, path = m.group(1), m.group(2)
        # Split off anchors/query to reattach later
        tail = ''
        for sep in ['#', '?']:
            if sep in path:
                path, tail = path.split(sep, 1)
                tail = sep + tail
                break
        key = path.replace('\\', '/').lstrip('./')
        # Try direct and with .md suffix
        for k in (key, key + ('' if key.lower().endswith('.md') else '.md')):
            if k in mappings:
                target = mappings[k]
                # Drop .md extension for wiki-style target
                if target.lower().endswith('.md'):
                    target = target[:-3]
                return f"[[{label}|{target}]]"
        return m.group(0)

    # Wiki links: [[path|text]] or [[path]]
    def repl_wiki(m):
        first = m.group(1)
        second = m.group(2)
        # Support both orders: [[path|label]] and [[label|path]]
        # Try treating first as path
        def as_target(p, label):
            key = p.replace('\\', '/').lstrip('./')
            for k in (key, key + ('' if key.lower().endswith('.md') else '.md')):
                if k in mappings:
                    target = mappings[k]
                    if target.lower().endswith('.md'):
                        target = target[:-3]
                    return f"[[{label}|{target}]]"
            return None
        # Case 1: [[path|label]]
        if second is not None:
            out = as_target(first, second)
            if out:
                return out
            # Case 2: [[label|path]]
            out = as_target(second, first)
            if out:
                return out
            return m.group(0)
        else:
            # [[path]] -> use same text as label
            out = as_target(first, first)
            return out or m.group(0)

    text = re.sub(r"(\[[^\]]*\])\(([^)]+)\)", repl_md, text)
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", repl_wiki, text)
    return text

for rel, out in mappings.items():
    sp = os.path.join(src, rel)
    dp = os.path.join(dst, out)
    os.makedirs(os.path.dirname(dp), exist_ok=True)
    with open(sp, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    txt = rewrite_links(txt)
    with open(dp, 'w', encoding='utf-8') as f:
        f.write(txt)

print(f"Flattened {len(mappings)} files into {dst}")
PY

# Determine wiki remote URL from origin
ORIGIN_URL="$(git -C "$ROOT_DIR" remote get-url origin)"
if [[ "$ORIGIN_URL" == *.git ]]; then
  WIKI_URL="${ORIGIN_URL%.git}.wiki.git"
else
  WIKI_URL="${ORIGIN_URL}.wiki.git"
fi

echo "Using wiki URL: $WIKI_URL"

# Clone or update wiki repo
if [[ -d "$WIKI_DIR/.git" ]]; then
  git -C "$WIKI_DIR" fetch --all --prune
  git -C "$WIKI_DIR" checkout -B master origin/master || git -C "$WIKI_DIR" checkout master || true
else
  rm -rf "$WIKI_DIR"
  git clone "$WIKI_URL" "$WIKI_DIR"
fi

# Archive existing wiki contents into archive/v1-archive-<timestamp>/ before syncing
ts="$(date -u +%Y%m%d_%H%M%S)"
ARCHIVE_DIR="$WIKI_DIR/archive/v1-archive-$ts"
mkdir -p "$WIKI_DIR/archive"
# If there are files (other than .git and archive) at root, move them
shopt -s nullglob dotglob
to_move=("$WIKI_DIR"/*)
shopt -u dotglob
if (( ${#to_move[@]} > 0 )); then
  mkdir -p "$ARCHIVE_DIR"
  for p in "${to_move[@]}"; do
    name="$(basename "$p")"
    if [[ "$name" == ".git" || "$name" == "archive" ]]; then
      continue
    fi
    mv "$p" "$ARCHIVE_DIR"/
  done
  echo "Archived existing wiki pages to archive/$(basename "$ARCHIVE_DIR")"
fi

# Sync FLAT_DIR files into wiki root (rsync or Python fallback)
if command -v rsync >/dev/null 2>&1; then
  # Preserve the archive/ folder created above
  rsync -a --delete --exclude 'archive/' "$FLAT_DIR"/ "$WIKI_DIR"/
else
  python - "$FLAT_DIR" "$WIKI_DIR" << 'PY'
import os, shutil, sys
src, dst = sys.argv[1:3]
for root, dirs, files in os.walk(dst):
    pass
# Clear destination except .git and archive
for name in os.listdir(dst):
    if name in ('.git', 'archive'):
        continue
    p = os.path.join(dst, name)
    if os.path.isfile(p) or os.path.islink(p):
        os.remove(p)
    else:
        shutil.rmtree(p)
# Copy from src to dst
for root, dirs, files in os.walk(src):
    rel = os.path.relpath(root, src)
    troot = dst if rel == '.' else os.path.join(dst, rel)
    os.makedirs(troot, exist_ok=True)
    for d in dirs:
        os.makedirs(os.path.join(troot, d), exist_ok=True)
    for f in files:
        sp = os.path.join(root, f)
        dp = os.path.join(troot, f)
        if os.path.islink(sp):
            continue
        shutil.copy2(sp, dp)
PY
fi

pushd "$WIKI_DIR" >/dev/null
# Write a simple Legacy_Archive page linking to the latest archived Home
if [[ -d "$ARCHIVE_DIR" ]]; then
  LATEST_BASENAME="$(basename "$ARCHIVE_DIR")"
  WEB_WIKI_URL="${WIKI_URL%.git}"
  cat > Legacy_Archive.md <<EOF
# Legacy Documentation Archive

Looking for the previous wiki? Start here:
- [[archive/$LATEST_BASENAME/Home|Browse Archived Home]]

Or browse the folder on GitHub:
- $WEB_WIKI_URL/tree/master/archive/$LATEST_BASENAME
EOF
fi

git add -A
if git diff --cached --quiet; then
  echo "No changes to publish to wiki."
else
  git commit -m "Sync wiki from docs/"
  git push origin HEAD:master
fi
popd >/dev/null

echo "Wiki sync complete."

