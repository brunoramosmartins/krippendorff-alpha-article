#!/usr/bin/env python3
"""Export article + figures for a portfolio repo (MD → HTML pipeline).

The canonical articles use paths `../figures/*.png` (correct inside this monorepo).
This script writes a self-contained folder:

  <out>/
    krippendorff-alpha.md   # image links rewritten to figures/...
    figures/
      *.png

Usage:
  python scripts/export_article_for_portfolio.py
  python scripts/export_article_for_portfolio.py --lang pt-BR
  python scripts/export_article_for_portfolio.py --out TARGET_DIR
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTICLES = {
    "en": ROOT / "article" / "krippendorff-alpha.md",
    "pt-BR": ROOT / "article" / "krippendorff-alpha.pt-BR.md",
}

FIG_REF = re.compile(r"\]\(\.\./figures/([^)]+)\)")


def strip_yaml_frontmatter(text: str) -> str:
    """Remove YAML frontmatter delimited by --- at the start of the file."""
    if text.startswith("---"):
        end = text.index("---", 3)
        text = text[end + 3 :].lstrip("\n")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Export article + figures for portfolio site.")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "dist" / "portfolio-article",
        help="Output directory (default: dist/portfolio-article)",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "pt-BR"],
        default="en",
        help="Article language to export (default: en)",
    )
    args = parser.parse_args()
    out: Path = args.out.resolve()
    article_path = ARTICLES[args.lang]

    if not article_path.is_file():
        print(f"Missing {article_path}", file=sys.stderr)
        sys.exit(1)

    text = article_path.read_text(encoding="utf-8")
    text = strip_yaml_frontmatter(text)

    needed = sorted(set(FIG_REF.findall(text)))
    if not needed:
        print("No ../figures/ references found in article.", file=sys.stderr)
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)
    fig_out = out / "figures"
    fig_out.mkdir(parents=True, exist_ok=True)

    missing: list[str] = []
    for name in needed:
        src = ROOT / "figures" / name
        if not src.is_file():
            missing.append(name)
            continue
        shutil.copy2(src, fig_out / name)

    portable = text.replace("](../figures/", "](figures/")
    out_filename = article_path.name
    (out / out_filename).write_text(portable, encoding="utf-8")

    print(f"Wrote {out / out_filename}")
    print(f"Copied {len(needed) - len(missing)} PNG(s) to {fig_out}/")
    if missing:
        msg = "Missing source PNGs (run figure scripts first): " + ", ".join(missing)
        print(msg, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
