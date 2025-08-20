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
WIKI_DIR="$ROOT_DIR/.wiki_repo"

if [[ ! -d "$DOCS_DIR" ]]; then
  echo "docs/ directory not found at $DOCS_DIR" >&2
  exit 1
fi

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy docs to build dir, excluding archives and junk (rsync if available, else Python)
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '_archive/' \
    --exclude '.git/' \
    --exclude '.DS_Store' \
    "$DOCS_DIR"/ "$BUILD_DIR"/
else
  python - "$DOCS_DIR" "$BUILD_DIR" << 'PY'
import os, shutil, sys
src, dst = sys.argv[1:3]
def ignore(dir, files):
    ig = set()
    if os.path.basename(dir) == '_archive':
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

# Sync build files into wiki root (rsync or Python fallback)
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$BUILD_DIR"/ "$WIKI_DIR"/
else
  python - "$BUILD_DIR" "$WIKI_DIR" << 'PY'
import os, shutil, sys
src, dst = sys.argv[1:3]
for root, dirs, files in os.walk(dst):
    pass
# Clear destination except .git
for name in os.listdir(dst):
    if name == '.git':
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
git add -A
if git diff --cached --quiet; then
  echo "No changes to publish to wiki."
else
  git commit -m "Sync wiki from docs/"
  git push origin HEAD:master
fi
popd >/dev/null

echo "Wiki sync complete."

