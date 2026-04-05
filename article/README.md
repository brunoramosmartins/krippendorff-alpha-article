# Article source (`krippendorff-alpha.md`)

## Structure

- **YAML front matter** (between `---` lines): metadata for static-site generators — `title`, `slug`, `description`, `keywords`, `mathjax`, `source_repository`, etc. Your portfolio pipeline can read this with PyYAML and strip it before MD→HTML, or ignore it if your converter passes unknown YAML through safely.
- **Body**: numbered sections `## 1.` … `## 10.`, display math `\( … \)` / `\[ … \]` (MathJax-compatible), figure captions, ASCII flowchart (` ```text `), and references.

## Images in this repository

Paths are **`../figures/<file>.png`**: from `article/krippendorff-alpha.md`, the `figures/` directory is the repo root folder next to `article/`.

Generate PNGs from the project root:

```bash
python scripts/phase1_convergence_plot.py
python scripts/kappa_paradox_plot.py
python scripts/experiment_a_random.py
python scripts/experiment_b_trap.py
python scripts/experiment_c_llm.py
python scripts/experiment_d_missing.py
```

## Export for another repo (e.g. GitHub.io portfolio)

Produces a **self-contained** directory: one Markdown file + `figures/*.png` with links rewritten to `figures/...` (same folder level as in many blog engines).

```bash
python scripts/export_article_for_portfolio.py --out path/to/your-portfolio/content/krippendorff-alpha
```

Default output: `dist/portfolio-article/`. Copy that folder into your portfolio repository. If any PNG is missing, run the figure scripts first (exit code 2 lists missing files).

## MkDocs in *this* repo

`mkdocs build` runs a hook that strips front matter from the article for the docs page, rewrites image paths for `mkdocs_docs/figures/`, and writes `mkdocs_docs/_article_include.md` (gitignored). You do not need to maintain that file by hand.

**Math rendering:** the Material theme uses `content.math` and pymdownx **Arithmatex** (`generic: true`). Snippets must resolve includes from `mkdocs_docs/`, so `mkdocs.yml` sets `pymdownx.snippets.base_path` to `["mkdocs_docs", "."]` — otherwise `_article_include.md` is not found and the Article page renders **without** body or equations.

## Portuguese review draft

`krippendorff-alpha.pt-BR.md` is a **parallel draft** for review and annotations (not wired into MkDocs by default). Keep `krippendorff-alpha.md` as the canonical English source for export and the docs site.

## Pen-and-paper derivations (roadmap)

See `docs/math-derivations-checklist.md` for a checklist of formulas and proofs aligned with Phases 1–3 of the roadmap.
