from __future__ import annotations
import argparse
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Generate a simple docs index")
    ap.add_argument("--root", default="docs", help="Docs root directory (default: docs)")
    ap.add_argument("--out", default="docs/INDEX.md", help="Output Markdown file (default: docs/INDEX.md)")
    args = ap.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    if not root.exists():
        raise SystemExit(f"Docs root not found: {root}")

    sections = {}
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        # Skip the generated file itself
        if rel.as_posix().upper() == "INDEX.MD":
            continue
        top = rel.parts[0] if len(rel.parts) > 1 else "root"
        sections.setdefault(top, []).append(rel)

    lines = []
    lines.append("# Docs Index\n")
    for sec in sorted(sections):
        lines.append(f"## {sec}\n")
        for rel in sections[sec]:
            lines.append(f"- [{rel.as_posix()}]({rel.as_posix()})")
        lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

