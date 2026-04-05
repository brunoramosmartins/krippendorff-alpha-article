# When Agreement Is an Illusion

[![CI](https://github.com/brunoramosmartins/krippendorff-alpha-article/actions/workflows/ci.yml/badge.svg)](https://github.com/brunoramosmartins/krippendorff-alpha-article/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Technical article (and reproducible code) on **inter-annotator agreement**: why raw **observed agreement** mixes signal and chance, how **Kappa**-style metrics correct for chance yet break under imbalance and missing data, and how **Krippendorff's Alpha** models **disagreement** in a way that generalises across raters and scales.

If your GitHub username or repository name differs, update the CI badge URL above.

## Thesis (v0.1)

> An agreement score of 0.80 among annotators is more likely evidence of structured noise than of true consensus when chance agreement is not properly accounted for. Metrics like raw agreement treat observed agreement as signal, rather than as an estimator composed of signal and chance. Krippendorff's Alpha resolves this by explicitly modelling disagreement under randomness.

## Roadmap

The full phased plan (phases 0–6, repo layout, Git workflow, issues, and deliverables) lives in:

**[`roadmap-krippendorff-alpha-v3.md`](roadmap-krippendorff-alpha-v3.md)**

**Status (code):** Phase 0 (foundation) and Phase 1 (statistical foundation: `simulate`, `observed_agreement`, convergence figure) are implemented; Phase 2 adds **Cohen's** and **Fleiss'** kappa in `src/metrics.py`, theory in `notes/phase2-kappa.md`, and `figures/kappa_paradox.png`.

## Repository layout (short)

| Path | Purpose |
|------|---------|
| `article/` | Long-form article source (`krippendorff-alpha.md`) |
| `docs/` | Thesis, dataset design, outline |
| `notes/` | Phase theory notes (Phase 1–3) |
| `src/` | Simulations, loaders, metrics (implemented phase by phase) |
| `scripts/` | Phase plots + experiments A–D (Phase 4) |
| `notebooks/` | Exploratory / presentation notebooks |
| `figures/` | Generated plots (tracked when produced) |
| `mkdocs_docs/` | Site pages; canonical article included from `article/` |
| `tests/` | Unit tests |

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

pip install -r requirements.txt
pip install -e .

pytest tests/ -q
python -m ruff check src tests scripts
```

### Regenerate key figures

```bash
python scripts/phase1_convergence_plot.py
python scripts/kappa_paradox_plot.py
```

### Documentation site (local)

```bash
python -m mkdocs serve
```

Open the URL shown (typically [http://127.0.0.1:8000](http://127.0.0.1:8000)).

Before `mkdocs gh-deploy`, set `repo_url` / `site_url` in `mkdocs.yml` to your GitHub Pages location.

### Makefile (optional)

On Unix-like shells, `make install`, `make test`, `make docs`, and `make experiments` are available. On Windows, run the underlying `pip` / `pytest` / `mkdocs` commands directly.

## Tech stack

Python 3.10+, NumPy, pandas, SciPy, scikit-learn, matplotlib, seaborn, [krippendorff](https://pypi.org/project/krippendorff/), Jupyter, pytest, Ruff, MkDocs Material.

## Licence

MIT — see [`LICENSE`](LICENSE).

## Author

Bruno Ramos Martins
