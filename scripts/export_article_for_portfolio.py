#!/usr/bin/env python3
"""Export `article/krippendorff-alpha.md` + figures for a portfolio repo (MD → HTML pipeline).

The canonical article uses paths `../figures/*.png` (correct inside this monorepo).
This script writes a self-contained folder:

  <out>/
    krippendorff-alpha.md   # image links rewritten to figures/...
    figures/
      *.png

Usage:
  python scripts/export_article_for_portfolio.py
  python scripts/export_article_for_portfolio.py --out TARGET_DIR
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "article" / "krippendorff-alpha.md"
FIG_REF = re.compile(r"\]\(\.\./figures/([^)]+)\)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export article + figures for portfolio site.")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "dist" / "portfolio-article",
        help="Output directory (default: dist/portfolio-article)",
    )
    args = parser.parse_args()
    out: Path = args.out.resolve()

    if not ARTICLE.is_file():
        print(f"Missing {ARTICLE}", file=sys.stderr)
        sys.exit(1)

    text = ARTICLE.read_text(encoding="utf-8")
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
    (out / "krippendorff-alpha.md").write_text(portable, encoding="utf-8")

    print(f"Wrote {out / 'krippendorff-alpha.md'}")
    print(f"Copied {len(needed) - len(missing)} PNG(s) to {fig_out}/")
    if missing:
        msg = "Missing source PNGs (run figure scripts first): " + ", ".join(missing)
        print(msg, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
