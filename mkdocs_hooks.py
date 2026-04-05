"""MkDocs hooks: sync figures and build snippet include from `article/krippendorff-alpha.md`."""

from __future__ import annotations

import shutil
from pathlib import Path


def _strip_yaml_front_matter(text: str) -> str:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---"):
        return text
    close = text.find("\n---\n", 3)
    if close == -1:
        return text
    return text[close + 5 :].lstrip("\n")


def _write_article_include(root: Path) -> None:
    src = root / "article" / "krippendorff-alpha.md"
    dst = root / "mkdocs_docs" / "_article_include.md"
    if not src.is_file():
        return
    body = _strip_yaml_front_matter(src.read_text(encoding="utf-8"))
    body = body.replace("](../figures/", "](figures/")
    dst.write_text(body, encoding="utf-8")


def on_pre_build(**_kwargs) -> None:
    root = Path(__file__).resolve().parent
    src = root / "figures"
    dst = root / "mkdocs_docs" / "figures"
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for path in sorted(src.glob("*.png")):
            shutil.copy2(path, dst / path.name)
    _write_article_include(root)
