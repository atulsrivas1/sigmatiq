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

# Copy docs to build dir, excluding archives and junk
rsync -a --delete \
  --exclude '_archive/' \
  --exclude '.git/' \
  --exclude '.DS_Store' \
  "$DOCS_DIR"/ "$BUILD_DIR"/

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

# Sync build files into wiki root
rsync -a --delete "$BUILD_DIR"/ "$WIKI_DIR"/

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

