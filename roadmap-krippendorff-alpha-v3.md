# Roadmap: When Agreement Is an Illusion

## Statistical Foundations of Inter-Annotator Agreement — from Observed Agreement to Krippendorff's Alpha

---

## Project Context

Build a **portfolio-grade technical article** that derives inter-annotator agreement metrics from first principles, demonstrates their limitations, and introduces Krippendorff's Alpha as a general solution. The article connects theory to a real-world LLM evaluation scenario — assessing whether a prompt-tuned LLM agrees with human annotators on multi-class classification (e.g., brand-based project labelling). The project includes reproducible experiments and is designed to showcase mathematical rigour and applied ML evaluation skills.

### Tech Stack

- Python 3.x
- numpy / pandas
- scikit-learn
- matplotlib / seaborn
- scipy
- krippendorff (reference implementation)
- MkDocs + GitHub Pages (publication)

### Author Background

Analytics Engineer transitioning to Data Science / Machine Learning. Background in Mathematics. Portfolio oriented toward statistical thinking, ML evaluation, and applied NLP. Publication targets: GitHub Pages and Medium.

---

## Thesis (v0.1)

> "An agreement score of 0.80 among annotators is more likely evidence of structured noise than of true consensus when chance agreement is not properly accounted for. Metrics like raw agreement fail because they treat observed agreement as signal, rather than as an estimator composed of signal and chance. Krippendorff's Alpha resolves this by explicitly modelling disagreement under randomness."

### Central Axis

Every agreement metric is an estimator under uncertainty.

```
Observed agreement = signal + chance
```

---

## GitHub Semantic Guide

This section defines how Git tags, releases, milestones, and issues map to this specific project. Every example uses real names from this roadmap.

### Tags

Tags are immutable snapshots of the repository at a specific point. In this project, tags mark the end of each phase.

**Convention:** `v0.x-phase-name` for internal milestones, `v1.0.0` for the public portfolio release.

```bash
# After completing Phase 0 (Foundation)
git tag -a v0.1-foundation -m "Phase 0: thesis, dataset design, project outline"
git push origin v0.1-foundation

# After completing Phase 3 (Krippendorff's Alpha derivation)
git tag -a v0.4-alpha-derivation -m "Phase 3: full Alpha derivation and validation"
git push origin v0.4-alpha-derivation

# Public portfolio release
git tag -a v1.0.0 -m "v1.0.0: full article, experiments, and GitHub Pages site"
git push origin v1.0.0
```

**When to create a tag:** At the end of every phase, after the phase's PR is merged into `main`.

### Releases

Releases are GitHub-specific artifacts built on top of tags. They include changelogs, downloadable assets, and human-readable descriptions. **Not every tag gets a release.**

**Rule:** Create a release only when there is external value — something a reader, recruiter, or peer could consume.

| Tag | Release? | Reasoning |
|-----|----------|-----------|
| `v0.1-foundation` | No | Internal scaffolding, nothing to consume externally |
| `v0.2-statistical-foundation` | No | Theory notes only, no public-facing artefact |
| `v0.3-kappa-family` | No | Intermediate derivations |
| `v0.4-alpha-derivation` | No | Core theory complete but not published |
| `v0.5-experiments` | Yes (pre-release) | Reproducible notebooks; useful for peer review |
| `v0.6-article-draft` | Yes (pre-release) | Full draft article; ready for feedback |
| `v1.0.0` | **Yes (stable)** | Published article on GitHub Pages + Medium |

```bash
# Create a pre-release for experiments
gh release create v0.5-experiments \
  --title "v0.5 — Reproducible Experiments" \
  --notes "All four experiments (A–D) complete with notebooks and figures." \
  --prerelease

# Create the stable public release
gh release create v1.0.0 \
  --title "v1.0.0 — When Agreement Is an Illusion" \
  --notes "Full technical article published. Includes derivations, experiments, and GitHub Pages site."
```

### Milestones

Milestones group related issues and track progress toward a phase's completion. Each phase maps to exactly one milestone.

```
Milestone: "Phase 0 — Foundation"
  ├── Issue #1: Write thesis document
  ├── Issue #2: Design synthetic dataset
  ├── Issue #3: Define LLM evaluation scenario
  └── Issue #4: Create project outline and structure
```

**When to close a milestone:** When all its issues are closed and the phase PR is merged.

### Issues

Issues are atomic units of work. Every task in this roadmap becomes an issue with a full body (see issue templates below). Issues are always linked to a milestone.

**Numbering convention:** Issues are created in phase order. Each issue title follows the pattern:

```
[Phase X] Short description of the task
```

**Example:**

```
[Phase 1] Derive expected agreement for k classes
[Phase 3] Implement coincidence matrix builder
[Phase 4] Experiment B — high agreement trap simulation
```

### How They Relate

```
Issue → belongs to → Milestone (1 milestone per phase)
Milestone completion → triggers → Tag (1 tag per phase)
Tag (when externally valuable) → triggers → Release
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     ARTICLE PIPELINE                        │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Theory   │───▶│  Code    │───▶│ Figures  │              │
│  │  Notes    │    │  (src/)  │    │ (figs/)  │              │
│  │ (notes/) │    │          │    │          │              │
│  └──────────┘    └────┬─────┘    └────┬─────┘              │
│                       │               │                     │
│                       ▼               ▼                     │
│              ┌────────────────────────────┐                 │
│              │     Article (article/)     │                 │
│              │  krippendorff-alpha.md     │                 │
│              └────────────┬──────────────┘                 │
│                           │                                 │
│                           ▼                                 │
│              ┌────────────────────────────┐                 │
│              │   MkDocs / GitHub Pages    │                 │
│              │   + Medium cross-post      │                 │
│              └────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     DATA FLOW                               │
│                                                             │
│  ┌────────────────┐     ┌────────────────┐                  │
│  │   Synthetic     │     │  Real Dataset   │                 │
│  │   Generator     │     │  (HuggingFace)  │                 │
│  │  src/simulate.py│     │  src/loader.py  │                 │
│  └───────┬────────┘     └───────┬────────┘                  │
│          │                      │                            │
│          ▼                      ▼                            │
│  ┌──────────────────────────────────────┐                   │
│  │        Annotation Matrix (n × m)     │                   │
│  │        n = items, m = annotators     │                   │
│  └──────────────────┬───────────────────┘                   │
│                     │                                        │
│          ┌──────────┼──────────┐                             │
│          ▼          ▼          ▼                              │
│   ┌──────────┐ ┌────────┐ ┌───────────┐                     │
│   │Raw Agree.│ │ Kappa  │ │Kripp. α   │                     │
│   │  A_o     │ │ κ / κ_f│ │           │                     │
│   └──────────┘ └────────┘ └───────────┘                     │
│          │          │          │                              │
│          ▼          ▼          ▼                              │
│   ┌──────────────────────────────────────┐                   │
│   │    Comparison & Visualization        │                   │
│   │    scripts/experiment_*.py           │                   │
│   └──────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
krippendorff-alpha-article/
│
├── article/                          # Final article source
│   └── krippendorff-alpha.md         # Main article in Markdown
│
├── docs/                             # Project planning documents
│   ├── thesis.md                     # Thesis statement and scope
│   ├── dataset-design.md             # Synthetic + real dataset specs
│   └── outline.md                    # Article section outline
│
├── src/                              # Reusable source code
│   ├── __init__.py
│   ├── simulate.py                   # Synthetic annotation generator
│   ├── loader.py                     # Real dataset loader (HuggingFace)
│   ├── metrics.py                    # Agreement metrics (A_o, κ, κ_f, α)
│   ├── coincidence.py                # Coincidence matrix builder
│   └── distances.py                  # Distance functions (nominal, ordinal, interval, ratio)
│
├── scripts/                          # Standalone experiment scripts
│   ├── experiment_a_random.py        # Exp A: random annotators → α ≈ 0
│   ├── experiment_b_trap.py          # Exp B: high A_o, low α
│   ├── experiment_c_llm.py           # Exp C: LLM vs humans
│   └── experiment_d_missing.py       # Exp D: missing data robustness
│
├── notebooks/                        # Jupyter notebooks (exploratory + presentation)
│   ├── 01_statistical_foundation.ipynb
│   ├── 02_kappa_family.ipynb
│   ├── 03_alpha_derivation.ipynb
│   └── 04_experiments.ipynb
│
├── figures/                          # Generated plots and diagrams
│   └── .gitkeep
│
├── notes/                            # Phase-by-phase theory notes
│   ├── phase1-theory.md              # Observed vs expected agreement
│   ├── phase2-kappa.md               # Cohen's and Fleiss' Kappa
│   └── phase3-alpha.md               # Krippendorff's Alpha derivation
│
├── site/                             # MkDocs generated site (gitignored)
│
├── tests/                            # Unit tests for src/
│   ├── test_metrics.py
│   ├── test_coincidence.py
│   └── test_distances.py
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── task.md                   # Task issue template
│   │   └── bug.md                    # Bug issue template
│   └── PULL_REQUEST_TEMPLATE.md      # PR template
│
├── mkdocs.yml                        # MkDocs configuration
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Project metadata
├── Makefile                          # Common commands (test, lint, build)
├── LICENSE                           # MIT
└── README.md                         # Project overview + quick start
```

---

## Dataset Strategy

### Synthetic Dataset

Controlled annotation simulation with configurable parameters:

| Parameter | Default | Range |
|-----------|---------|-------|
| `n_items` | 10,000 | 100–50,000 |
| `n_annotators` | 5 | 3–10 |
| `n_classes` | 3 | 2–10 |
| `noise_level` | 0.2 | 0.0–1.0 |
| `class_distribution` | uniform | uniform / imbalanced / extreme |
| `missing_rate` | 0.0 | 0.0–0.5 |

### Real Dataset (Optional)

- Source: HuggingFace datasets (e.g., sentiment or NLI with multiple annotators)
- Use case: human labels vs LLM outputs to mirror the workplace scenario

---

## Phase 0 — Foundation

### Objective

Establish the project's intellectual scope, define the thesis, design the synthetic dataset, and create the repository skeleton. This phase produces no code — only planning documents and project infrastructure. The goal is to ensure every subsequent phase has a clear target and no ambiguous tasks.

### Tasks

- [ ] **Write thesis document**
  - Draft the central claim (v0.1 above)
  - Define scope boundaries: what the article covers and what it explicitly excludes
  - Identify the target audience (ML practitioners, data scientists, NLP engineers)
- [ ] **Define the annotation problem formally**
  - Specify the multi-class classification setting
  - Define notation: items (i), annotators (j), categories (k)
  - Write the formal problem statement in LaTeX-compatible Markdown
- [ ] **Design synthetic dataset**
  - Specify all configurable parameters (see Dataset Strategy)
  - Document three class distribution scenarios: uniform, imbalanced (70/20/10), extreme (90/5/5)
  - Define noise model: P(correct) = 1 − noise_level, P(other class) = noise_level / (k − 1)
  - Document missing data injection strategy
- [ ] **Define LLM evaluation scenario**
  - Describe the workplace-inspired setup: LLM classifies projects into brand categories
  - Define how LLM outputs map to the annotation matrix
  - Specify which models to use (e.g., GPT-4, Claude) and prompting strategy
- [ ] **Create project outline**
  - Map article sections to phases
  - Define dependencies between sections
  - Estimate word count per section

### Deliverables

- [ ] `docs/thesis.md`
- [ ] `docs/dataset-design.md`
- [ ] `docs/outline.md`
- [ ] `README.md` (initial version)
- [ ] `requirements.txt`
- [ ] `.github/ISSUE_TEMPLATE/task.md`
- [ ] `.github/ISSUE_TEMPLATE/bug.md`
- [ ] `.github/PULL_REQUEST_TEMPLATE.md`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-0/foundation` |
| Merge strategy | Squash merge |
| PR title | `feat(docs): Phase 0 — foundation documents and project scaffold` |
| Milestone | `Phase 0 — Foundation` |
| Tag | `v0.1-foundation` |
| Release | **No** — internal scaffolding only, no external value |

### Issues

#### Issue #1 — Write thesis document

```markdown
## Context
The thesis is the intellectual anchor for the entire article. Without a clear,
falsifiable claim, the article risks becoming a tutorial rather than an argument.
The thesis must be strong enough to sustain 6,000+ words of derivation and evidence.

## Tasks
- [ ] Draft central claim (v0.1: "An agreement score of 0.80...")
- [ ] Define scope: what the article covers (observed agreement, chance correction,
      Kappa family, Krippendorff's Alpha, LLM evaluation)
- [ ] Define anti-scope: what it does NOT cover (weighted Kappa variants, Bayesian
      approaches, deep-learning-based annotation models)
- [ ] Identify target audience and prerequisite knowledge
- [ ] Write 1-paragraph abstract

## Definition of Done
- [ ] `docs/thesis.md` exists with thesis, scope, anti-scope, audience, and abstract
- [ ] Thesis is a single falsifiable sentence
- [ ] At least one peer has reviewed the thesis statement (self-review acceptable)

## References
- Krippendorff, K. (2004). Content Analysis: An Introduction to Its Methodology
- Artstein, R. & Poesio, M. (2008). Inter-Coder Agreement for Computational Linguistics
```

**Labels:** `phase:0`, `type:documentation`, `priority:high`

---

#### Issue #2 — Design synthetic dataset

```markdown
## Context
The experiments require a controllable data source where ground truth is known.
A synthetic annotation generator lets us isolate each variable (noise, imbalance,
missing data) and verify metric behaviour under known conditions.

## Tasks
- [ ] Define the noise model: P(correct) = 1 − ε, P(other) = ε / (k − 1)
- [ ] Define three class distribution scenarios:
      - Uniform: [1/3, 1/3, 1/3]
      - Imbalanced: [0.70, 0.20, 0.10]
      - Extreme: [0.90, 0.05, 0.05]
- [ ] Define missing data injection: MCAR (Missing Completely At Random) with configurable rate
- [ ] Document all parameters in `docs/dataset-design.md`
- [ ] Write example usage pseudocode

## Definition of Done
- [ ] `docs/dataset-design.md` exists with full parameter table
- [ ] Noise model is mathematically specified
- [ ] All three distribution scenarios are documented with rationale
- [ ] Missing data model is defined

## References
- Phase 4 experiment specs depend on this design
```

**Labels:** `phase:0`, `type:documentation`, `priority:high`

---

#### Issue #3 — Define LLM evaluation scenario

```markdown
## Context
The article's applied relevance comes from connecting inter-annotator agreement
to LLM evaluation — a real scenario from the author's workplace. Defining this
scenario early ensures the experiments are grounded in a practical use case.

## Tasks
- [ ] Describe the scenario: a company uses 3 brand categories to direct investment;
      a prompt-tuned LLM classifies projects; the question is whether the LLM
      "agrees" with human annotators
- [ ] Define how LLM outputs become entries in the annotation matrix
- [ ] Specify evaluation: LLM as one additional annotator vs human panel
- [ ] List candidate models and prompting strategies (if using real LLM calls)
- [ ] Define fallback: simulated LLM outputs with controlled agreement levels

## Definition of Done
- [ ] Scenario documented in `docs/dataset-design.md` (LLM section)
- [ ] Annotation matrix construction from LLM outputs is specified
- [ ] At least one concrete example (3 items × 4 annotators including LLM)

## References
- Workplace scenario described in project motivation
- Phase 4, Experiment C depends on this
```

**Labels:** `phase:0`, `type:documentation`, `priority:medium`

---

#### Issue #4 — Create project outline and repository structure

```markdown
## Context
A clear outline maps each article section to the phase that produces it,
ensuring no orphaned content and no missing derivations. The repository
structure ensures code, theory, and article live in well-defined locations.

## Tasks
- [ ] Create `docs/outline.md` with all 10 article sections
- [ ] Map each section to its source phase
- [ ] Estimate word count per section (total target: 6,000–8,000 words)
- [ ] Initialize repository structure (all directories + .gitkeep files)
- [ ] Write initial `README.md` with project description and roadmap link
- [ ] Create `requirements.txt` with pinned versions
- [ ] Create GitHub issue templates and PR template

## Definition of Done
- [ ] `docs/outline.md` exists with section → phase mapping
- [ ] All directories from repository structure exist
- [ ] `README.md` has project description, thesis, and "how to run" placeholder
- [ ] `requirements.txt` is pip-installable
- [ ] Issue and PR templates are in `.github/`

## References
- Repository structure defined in this roadmap
```

**Labels:** `phase:0`, `type:infrastructure`, `priority:high`

---

## Phase 1 — Statistical Foundation

### Objective

Formalize agreement as a probabilistic estimator. Derive observed agreement from first principles. Prove mathematically that random annotators produce non-zero agreement and quantify this expected agreement for k classes. Implement the synthetic annotation generator and run the first simulation to validate theory against empirical results. This phase builds the mathematical foundation that every subsequent metric builds on.

### Tasks

- [ ] **Derive observed agreement formula**
  - Define A_o = (number of agreeing pairs) / (total pairs)
  - Show equivalence to: A_o = Σ_k (n_k / n)² for pairwise formulation
  - Work through a 3-item, 2-annotator example by hand
- [ ] **Derive expected agreement under chance**
  - Assume annotators assign categories independently from marginal distributions
  - Derive A_e = Σ_k p_k² for k categories
  - Prove: for k classes with uniform distribution, A_e = 1/k
  - Show: for k = 2 with uniform, A_e = 0.50 (coin flip annotators agree half the time)
- [ ] **Implement synthetic annotation generator**
  - Implement `src/simulate.py` with all configurable parameters
  - Include noise model, class distributions, and missing data injection
  - Write unit tests in `tests/test_simulate.py`
- [ ] **Simulate random annotators**
  - Generate 10,000 items × 5 random annotators
  - Compute A_o empirically
  - Compare to theoretical A_e
  - Visualize convergence as n_items increases
- [ ] **Write Phase 1 theory notes**
  - Document all derivations step by step
  - Include worked examples
  - State the core insight: A_o alone is unreliable

### Deliverables

- [ ] `notes/phase1-theory.md`
- [ ] `src/simulate.py`
- [ ] `src/metrics.py` (initial: `observed_agreement()`)
- [ ] `tests/test_simulate.py`
- [ ] `notebooks/01_statistical_foundation.ipynb`
- [ ] `figures/random_agreement_convergence.png`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-1/statistical-foundation` |
| Merge strategy | Squash merge |
| PR title | `feat(core): Phase 1 — statistical foundation and synthetic generator` |
| Milestone | `Phase 1 — Statistical Foundation` |
| Tag | `v0.2-statistical-foundation` |
| Release | **No** — theory notes and internal tooling only |

### Issues

#### Issue #5 — Derive observed and expected agreement

```markdown
## Context
The entire article rests on the decomposition: observed = signal + chance.
This issue formalizes both components mathematically and proves that chance
agreement is non-trivial (A_e > 0 for any finite k).

## Tasks
- [ ] Derive A_o from counting agreeing pairs
- [ ] Derive A_e under independence assumption
- [ ] Prove A_e = 1/k for uniform distribution over k classes
- [ ] Work through 3 concrete examples:
      - k=2, uniform → A_e = 0.50
      - k=3, uniform → A_e = 0.33
      - k=3, imbalanced [0.7, 0.2, 0.1] → A_e = 0.54
- [ ] Document in `notes/phase1-theory.md`

## Definition of Done
- [ ] All derivations are step-by-step with no skipped algebra
- [ ] Three worked examples with numerical verification
- [ ] Core insight explicitly stated: "high A_o ≠ high agreement"

## References
- Artstein & Poesio (2008), Section 2
- Krippendorff (2004), Chapter 11
```

**Labels:** `phase:1`, `type:theory`, `priority:high`

---

#### Issue #6 — Implement synthetic annotation generator

```markdown
## Context
Every experiment in Phase 4 depends on a flexible, well-tested annotation
generator. This is the project's core data infrastructure.

## Tasks
- [ ] Implement `SimulatedAnnotation` class in `src/simulate.py`
- [ ] Parameters: n_items, n_annotators, n_classes, noise_level, class_dist, missing_rate, seed
- [ ] Output: pandas DataFrame (items × annotators), NaN for missing
- [ ] Implement noise model: P(correct) = 1 − ε, P(error) = ε / (k − 1)
- [ ] Implement missing data: MCAR with configurable rate
- [ ] Write unit tests:
      - Noise level 0.0 → perfect agreement
      - Noise level 1.0 → random assignment
      - Missing rate 0.3 → ~30% NaN values
      - Class distribution matches target within tolerance

## Definition of Done
- [ ] `src/simulate.py` passes all unit tests
- [ ] Generator is reproducible with seed parameter
- [ ] Docstrings with usage examples

## References
- `docs/dataset-design.md` (from Phase 0)
```

**Labels:** `phase:1`, `type:code`, `priority:high`

---

#### Issue #7 — Simulate random annotators and validate theory

```markdown
## Context
The first empirical validation: do random annotators produce the expected
agreement predicted by theory? This simulation grounds the mathematical
derivation in observable data.

## Tasks
- [ ] Generate 10,000 items × 5 annotators with noise_level=1.0 (pure random)
- [ ] Compute A_o empirically using `src/metrics.py`
- [ ] Compare to theoretical A_e for k=3, uniform
- [ ] Plot convergence: A_o vs n_items (100, 500, 1K, 5K, 10K)
- [ ] Repeat for imbalanced distribution
- [ ] Save figure to `figures/random_agreement_convergence.png`
- [ ] Create notebook `notebooks/01_statistical_foundation.ipynb`

## Definition of Done
- [ ] Empirical A_o matches theoretical A_e within 0.01 for n=10,000
- [ ] Convergence plot shows clear approach to theoretical value
- [ ] Notebook is self-contained and executable

## References
- Theory from Issue #5
- Generator from Issue #6
```

**Labels:** `phase:1`, `type:experiment`, `priority:medium`

---

## Phase 2 — Kappa Family

### Objective

Derive Cohen's Kappa and Fleiss' Kappa from first principles as chance-corrected agreement metrics. Demonstrate their construction, show they improve on raw agreement, and then expose their structural limitations: sensitivity to class imbalance (the Kappa paradox), requirement of fixed annotators (Cohen) or complete data (Fleiss), and inability to handle different measurement scales. This phase builds the case for why a more general metric is needed.

### Tasks

- [ ] **Derive Cohen's Kappa**
  - Start from the chance-correction formula: κ = (A_o − A_e) / (1 − A_e)
  - Define A_e using marginal distributions from the confusion matrix
  - Work through a 2×2 example step by step
  - Interpret the scale: κ = 0 (chance), κ = 1 (perfect), κ < 0 (worse than chance)
- [ ] **Extend to Fleiss' Kappa**
  - Generalise from 2 annotators to m annotators
  - Define A_e using overall category proportions
  - Derive the per-item agreement formula
  - Work through a 3-annotator, 3-class example
- [ ] **Demonstrate the Kappa paradox**
  - Construct a scenario: high A_o (e.g., 0.85) but low κ (e.g., 0.20)
  - Show that extreme class imbalance inflates A_e, deflating κ
  - Visualise: κ as a function of class imbalance for fixed A_o
- [ ] **Catalogue limitations**
  - Cohen: requires exactly 2 fixed annotators
  - Fleiss: requires all annotators to rate all items (no missing data)
  - Both: assume nominal categories only (no ordinal, interval, or ratio scales)
  - Both: no principled handling of missing data
- [ ] **Implement metrics**
  - Add `cohens_kappa()` and `fleiss_kappa()` to `src/metrics.py`
  - Write unit tests with known-answer examples
- [ ] **Write Phase 2 theory notes**

### Deliverables

- [ ] `notes/phase2-kappa.md`
- [ ] `src/metrics.py` (updated: `cohens_kappa()`, `fleiss_kappa()`)
- [ ] `tests/test_metrics.py` (updated)
- [ ] `notebooks/02_kappa_family.ipynb`
- [ ] `figures/kappa_paradox.png`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-2/kappa-family` |
| Merge strategy | Squash merge |
| PR title | `feat(core): Phase 2 — Kappa family derivation and limitations` |
| Milestone | `Phase 2 — Kappa Family` |
| Tag | `v0.3-kappa-family` |
| Release | **No** — intermediate derivations, not externally consumable |

### Issues

#### Issue #8 — Derive Cohen's Kappa from first principles

```markdown
## Context
Cohen's Kappa is the first chance-corrected metric most practitioners encounter.
Deriving it step-by-step from A_o and A_e establishes the chance-correction
pattern that Krippendorff's Alpha will later generalise.

## Tasks
- [ ] State the chance-correction formula: κ = (A_o − A_e) / (1 − A_e)
- [ ] Define A_e from marginal distributions of a 2-annotator confusion matrix
- [ ] Derive A_e = Σ_k (p_k1 · p_k2) where p_kj is annotator j's proportion for class k
- [ ] Work through a 2×2 example (3 items, 2 annotators, 2 classes)
- [ ] Verify with scikit-learn's `cohen_kappa_score`
- [ ] Document interpretation scale with references

## Definition of Done
- [ ] Derivation has no skipped steps
- [ ] Worked example matches scikit-learn output
- [ ] `notes/phase2-kappa.md` contains full derivation

## References
- Cohen, J. (1960). A Coefficient of Agreement for Nominal Scales
- scikit-learn documentation: `sklearn.metrics.cohen_kappa_score`
```

**Labels:** `phase:2`, `type:theory`, `priority:high`

---

#### Issue #9 — Derive Fleiss' Kappa and demonstrate the Kappa paradox

```markdown
## Context
Fleiss' Kappa extends Cohen's to multiple annotators but inherits and amplifies
the imbalance sensitivity problem. The Kappa paradox — where high raw agreement
yields low Kappa — is the key motivating example for Krippendorff's Alpha.

## Tasks
- [ ] Derive Fleiss' Kappa for m annotators and k categories
- [ ] Define per-item agreement: P_i = (1 / (m(m−1))) Σ_k n_ik(n_ik − 1)
- [ ] Define A_o = (1/n) Σ_i P_i and A_e = Σ_k p_k²
- [ ] Work through a 3-annotator, 3-class, 5-item example
- [ ] Construct Kappa paradox scenario:
      - 3 classes with distribution [0.90, 0.05, 0.05]
      - Noise level 0.05 → A_o ≈ 0.85, but κ_f ≈ 0.20
- [ ] Create visualisation: κ vs class imbalance for fixed noise levels
- [ ] Implement `fleiss_kappa()` in `src/metrics.py`

## Definition of Done
- [ ] Fleiss derivation is complete with worked example
- [ ] Kappa paradox is demonstrated with a concrete numerical example
- [ ] Visualisation saved to `figures/kappa_paradox.png`
- [ ] `fleiss_kappa()` passes unit tests

## References
- Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters
- Feinstein, A. R. & Cicchetti, D. V. (1990). High agreement but low Kappa
```

**Labels:** `phase:2`, `type:theory`, `type:code`, `priority:high`

---

## Phase 3 — Krippendorff's Alpha

### Objective

Derive Krippendorff's Alpha from first principles as a disagreement-based metric that resolves all limitations identified in Phase 2. Build the coincidence matrix, define distance functions for multiple measurement scales, derive observed and expected disagreement, and assemble the full formula. Validate the implementation against known examples and the `krippendorff` reference library.

### Tasks

- [ ] **Build the coincidence matrix**
  - Define: a symmetric matrix where entry (c, c') counts how often categories c and c' co-occur across annotator pairs for the same item
  - Derive the construction algorithm for incomplete data (missing values)
  - Work through a 5-item, 3-annotator example by hand
  - Implement `src/coincidence.py`
- [ ] **Define distance functions**
  - Nominal: δ(c, c') = 0 if c = c', 1 otherwise
  - Ordinal: δ based on rank differences
  - Interval: δ(c, c') = (c − c')²
  - Ratio: δ(c, c') = ((c − c') / (c + c'))²
  - Implement in `src/distances.py`
- [ ] **Derive observed disagreement**
  - D_o = (1 / n) Σ_{c,c'} o_{cc'} · δ(c, c')
  - where o_{cc'} are entries of the coincidence matrix
  - Show relationship to A_o: D_o = 1 − A_o for nominal distance
- [ ] **Derive expected disagreement**
  - D_e = (1 / (n(n−1))) Σ_{c,c'} n_c · n_{c'} · δ(c, c')
  - where n_c are marginal totals
  - Show this represents disagreement under random assignment preserving marginals
- [ ] **Assemble the full formula**
  - α = 1 − (D_o / D_e)
  - Prove: α = 1 when D_o = 0 (perfect agreement)
  - Prove: α = 0 when D_o = D_e (chance-level)
  - Prove: α < 0 when D_o > D_e (systematic disagreement)
  - Show equivalence to Cohen's Kappa under special conditions (2 annotators, nominal, complete data)
- [ ] **Validate implementation**
  - Compare against `krippendorff` Python library
  - Reproduce examples from Krippendorff (2004)
  - Test edge cases: all agree, all disagree, single annotator, all missing
- [ ] **Write Phase 3 theory notes**

### Deliverables

- [ ] `notes/phase3-alpha.md`
- [ ] `src/coincidence.py`
- [ ] `src/distances.py`
- [ ] `src/metrics.py` (updated: `krippendorff_alpha()`)
- [ ] `tests/test_coincidence.py`
- [ ] `tests/test_distances.py`
- [ ] `tests/test_metrics.py` (updated)
- [ ] `notebooks/03_alpha_derivation.ipynb`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-3/krippendorff-alpha` |
| Merge strategy | Squash merge |
| PR title | `feat(core): Phase 3 — Krippendorff's Alpha derivation and implementation` |
| Milestone | `Phase 3 — Krippendorff's Alpha` |
| Tag | `v0.4-alpha-derivation` |
| Release | **No** — core theory complete but not yet validated through experiments |

### Issues

#### Issue #10 — Build coincidence matrix with missing data support

```markdown
## Context
The coincidence matrix is the data structure at the heart of Krippendorff's Alpha.
Unlike confusion matrices (which require fixed annotator pairs), the coincidence
matrix works with any number of annotators and handles missing data natively.

## Tasks
- [ ] Define coincidence matrix construction algorithm
- [ ] Handle missing values: only count pairs where both annotators provided a label
- [ ] Implement `build_coincidence_matrix()` in `src/coincidence.py`
- [ ] Work through a 5-item, 3-annotator example by hand and verify programmatically
- [ ] Write unit tests:
      - Complete data matches manual calculation
      - Missing data is handled correctly
      - Matrix is symmetric
      - Diagonal = agreement counts, off-diagonal = disagreement counts

## Definition of Done
- [ ] Implementation matches hand-computed examples
- [ ] Missing data test passes
- [ ] Docstring includes the mathematical definition

## References
- Krippendorff (2004), Chapter 11, Section 11.3
```

**Labels:** `phase:3`, `type:code`, `type:theory`, `priority:high`

---

#### Issue #11 — Implement distance functions for multiple scales

```markdown
## Context
Krippendorff's Alpha is unique among agreement metrics in its ability to handle
different measurement scales through interchangeable distance functions. This
generality is a key advantage over the Kappa family.

## Tasks
- [ ] Implement four distance functions in `src/distances.py`:
      - `nominal_distance(c, c')` → 0 or 1
      - `ordinal_distance(c, c')` → rank-based
      - `interval_distance(c, c')` → (c − c')²
      - `ratio_distance(c, c')` → ((c − c') / (c + c'))²
- [ ] Write unit tests for each function
- [ ] Document when to use each scale with examples:
      - Nominal: brand categories, sentiment labels
      - Ordinal: Likert scales, severity ratings
      - Interval: temperature, year
      - Ratio: length, weight, duration

## Definition of Done
- [ ] All four functions implemented and tested
- [ ] Each function has a docstring with use-case example
- [ ] Functions handle edge cases (identical values, zeros for ratio)

## References
- Krippendorff (2004), Section 11.4
```

**Labels:** `phase:3`, `type:code`, `priority:high`

---

#### Issue #12 — Derive and implement full Alpha formula

```markdown
## Context
This is the culminating derivation of the article. Alpha must be derived
step-by-step from D_o and D_e, with proofs of its boundary behaviour and
its relationship to Kappa under special conditions.

## Tasks
- [ ] Derive D_o from coincidence matrix and distance function
- [ ] Derive D_e from marginal totals and distance function
- [ ] Assemble α = 1 − (D_o / D_e)
- [ ] Prove boundary conditions: α = 1 (perfect), α = 0 (chance), α < 0 (systematic)
- [ ] Prove equivalence to Cohen's κ: 2 annotators, nominal, complete data
- [ ] Implement `krippendorff_alpha()` in `src/metrics.py`
- [ ] Validate against `krippendorff` library on 5+ test cases
- [ ] Reproduce at least 2 examples from Krippendorff (2004)

## Definition of Done
- [ ] Full derivation in `notes/phase3-alpha.md` with no skipped steps
- [ ] Equivalence to κ is proved, not just asserted
- [ ] Implementation matches reference library within floating-point tolerance
- [ ] Notebook `03_alpha_derivation.ipynb` walks through the derivation interactively

## References
- Krippendorff (2004), Chapter 11
- `krippendorff` Python library: https://github.com/peterp/krippendorff
```

**Labels:** `phase:3`, `type:theory`, `type:code`, `priority:critical`

---

## Phase 4 — Experiments

### Objective

Empirically validate all theoretical claims from Phases 1–3 through four controlled experiments. Each experiment isolates one property of the metrics and produces a figure for the article. The experiments must be fully reproducible from a single command.

### Tasks

- [ ] **Experiment A — Random annotators**
  - Generate data with noise_level = 1.0 (pure random)
  - Compute A_o, κ_f, and α
  - Verify: A_o ≈ 1/k, κ_f ≈ 0, α ≈ 0
  - Vary k from 2 to 10 and plot all three metrics
- [ ] **Experiment B — High agreement trap**
  - Construct scenario: extreme class imbalance + low noise
  - Show: A_o is high (e.g., 0.90), κ is low (e.g., 0.30), α reveals the truth
  - Create a 2×2 summary table for the article
  - Visualise: heatmap of A_o vs α across (imbalance, noise) grid
- [ ] **Experiment C — LLM vs humans**
  - Use synthetic data simulating the workplace scenario:
    - 3 human annotators with noise_level = 0.10
    - 1 LLM annotator with noise_level = 0.15 (slightly noisier)
  - Compute all metrics: A_o, κ (pairwise human-LLM), κ_f (all), α (all)
  - Compare: does α flag the LLM as less reliable?
  - Sensitivity analysis: vary LLM noise from 0.0 to 0.5
- [ ] **Experiment D — Missing data robustness**
  - Take a fixed dataset (noise = 0.15, k = 3, balanced)
  - Inject missing data at rates: 0%, 10%, 20%, 30%, 40%, 50%
  - Compute κ_f and α at each rate
  - Show: κ_f becomes undefined or unstable; α degrades gracefully
  - Plot both metrics vs missing rate
- [ ] **Create reproducibility infrastructure**
  - `Makefile` target: `make experiments` runs all four
  - All scripts use fixed seeds for reproducibility
  - All figures saved to `figures/`

### Deliverables

- [ ] `scripts/experiment_a_random.py`
- [ ] `scripts/experiment_b_trap.py`
- [ ] `scripts/experiment_c_llm.py`
- [ ] `scripts/experiment_d_missing.py`
- [ ] `notebooks/04_experiments.ipynb`
- [ ] `figures/exp_a_random_metrics.png`
- [ ] `figures/exp_b_agreement_trap_heatmap.png`
- [ ] `figures/exp_c_llm_vs_humans.png`
- [ ] `figures/exp_d_missing_robustness.png`
- [ ] `Makefile` (updated with `experiments` target)

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-4/experiments` |
| Merge strategy | Squash merge |
| PR title | `feat(experiments): Phase 4 — four reproducible validation experiments` |
| Milestone | `Phase 4 — Experiments` |
| Tag | `v0.5-experiments` |
| Release | **Yes (pre-release)** — reproducible notebooks and figures ready for peer review |

### Issues

#### Issue #13 — Experiment A: random annotators validation

```markdown
## Context
This is the most basic sanity check: if annotators are purely random,
all chance-corrected metrics should be approximately zero. This validates
the theoretical derivation from Phase 1.

## Tasks
- [ ] Generate 10,000 items × 5 annotators, noise_level = 1.0, k = 3
- [ ] Compute A_o, κ_f, α
- [ ] Assert: A_o ≈ 0.33, κ_f ≈ 0.00, α ≈ 0.00 (within tolerance)
- [ ] Sweep k from 2 to 10, plot all three metrics
- [ ] Save figure to `figures/exp_a_random_metrics.png`
- [ ] Use seed = 42 for reproducibility

## Definition of Done
- [ ] Script runs end-to-end with `python scripts/experiment_a_random.py`
- [ ] Figure is publication-quality (labelled axes, legend, title)
- [ ] Results match theoretical predictions within ±0.02

## References
- Theory: `notes/phase1-theory.md`
```

**Labels:** `phase:4`, `type:experiment`, `priority:high`

---

#### Issue #14 — Experiment B: high agreement trap

```markdown
## Context
This is the article's "hero" experiment — the one that most directly supports
the thesis. It shows a concrete scenario where raw agreement looks excellent
but chance-corrected metrics reveal the agreement is illusory.

## Tasks
- [ ] Construct scenario: k=3, distribution=[0.90, 0.05, 0.05], noise=0.05
- [ ] Compute A_o, κ_f, α
- [ ] Create summary table: metric name, value, interpretation
- [ ] Create heatmap: (imbalance ratio, noise level) → α value
      - imbalance: [uniform, 60/20/20, 80/10/10, 90/5/5, 95/2.5/2.5]
      - noise: [0.01, 0.05, 0.10, 0.20, 0.30]
- [ ] Save figure to `figures/exp_b_agreement_trap_heatmap.png`
- [ ] Write paragraph interpreting results for the article

## Definition of Done
- [ ] Heatmap clearly shows regions where A_o > 0.80 but α < 0.40
- [ ] Summary table is ready for direct inclusion in the article
- [ ] Script runs end-to-end with `python scripts/experiment_b_trap.py`

## References
- Kappa paradox from Issue #9
- Thesis statement
```

**Labels:** `phase:4`, `type:experiment`, `priority:critical`

---

#### Issue #15 — Experiment C: LLM vs humans

```markdown
## Context
This experiment connects the mathematical framework to the applied motivation:
evaluating whether an LLM "agrees" with human annotators on project classification.

## Tasks
- [ ] Simulate 3 human annotators (noise=0.10) + 1 LLM (noise=0.15), k=3, n=10,000
- [ ] Compute pairwise κ between each human and the LLM
- [ ] Compute κ_f and α for the full panel (humans + LLM)
- [ ] Compute α for humans only, then with LLM included → does α drop?
- [ ] Sensitivity: vary LLM noise from 0.0 to 0.5, plot α trajectory
- [ ] Save figure to `figures/exp_c_llm_vs_humans.png`

## Definition of Done
- [ ] Results show whether α can distinguish LLM quality levels
- [ ] Sensitivity plot has clear inflection points annotated
- [ ] Script runs with `python scripts/experiment_c_llm.py`

## References
- LLM scenario from Issue #3
```

**Labels:** `phase:4`, `type:experiment`, `priority:high`

---

#### Issue #16 — Experiment D: missing data robustness

```markdown
## Context
Missing data is the norm in real annotation tasks. This experiment shows
that Krippendorff's Alpha handles it gracefully while Fleiss' Kappa degrades
or fails entirely.

## Tasks
- [ ] Generate baseline: n=10,000, k=3, balanced, noise=0.15, 5 annotators
- [ ] Inject missing data at rates: [0%, 10%, 20%, 30%, 40%, 50%]
- [ ] At each rate, compute κ_f and α
- [ ] Plot both metrics vs missing rate on the same axes
- [ ] Note the point where κ_f becomes undefined or erratic
- [ ] Save figure to `figures/exp_d_missing_robustness.png`

## Definition of Done
- [ ] Plot clearly shows α stability vs κ_f instability
- [ ] Script handles edge cases (κ_f undefined → NaN, plotted as gap)
- [ ] Script runs with `python scripts/experiment_d_missing.py`

## References
- Missing data design from `docs/dataset-design.md`
```

**Labels:** `phase:4`, `type:experiment`, `priority:high`

---

## Phase 5 — Article Writing

### Objective

Assemble all theory notes, experiment results, and figures into a cohesive, publication-ready technical article. The article follows a narrative arc: motivate the problem, build the theory, expose the trap, introduce the solution, validate empirically, and connect to practice.

### Tasks

- [ ] **Section 1: Introduction** (~600 words)
  - Hook: "Your annotators agreed 80% of the time. That number is almost certainly misleading."
  - Motivate with the LLM evaluation scenario
  - Preview the article's argument
- [ ] **Section 2: Agreement as an estimator** (~500 words)
  - Define the annotation problem formally
  - Introduce observed agreement
  - Frame it as an estimator: what it estimates and what it misses
- [ ] **Section 3: The chance agreement problem** (~600 words)
  - Derive expected agreement
  - Worked example: random annotators on 3 classes
  - Include convergence figure from Phase 1
- [ ] **Section 4: The Kappa family** (~700 words)
  - Derive Cohen's Kappa
  - Extend to Fleiss' Kappa
  - Show they improve on raw agreement
- [ ] **Section 5: Limitations of Kappa** (~500 words)
  - The Kappa paradox (with figure)
  - Fixed annotators, no missing data, nominal only
  - Build the case for a better metric
- [ ] **Section 6: From agreement to disagreement** (~400 words)
  - Conceptual shift: measuring what went wrong instead of what went right
  - Introduce the coincidence matrix
- [ ] **Section 7: Krippendorff's Alpha** (~800 words)
  - Full derivation with all steps
  - Distance functions
  - Boundary proofs
  - Equivalence to Kappa under constraints
- [ ] **Section 8: Experiments** (~1,000 words)
  - Present all four experiments with figures
  - Interpret results in context of the thesis
- [ ] **Section 9: A practical framework** (~400 words)
  - When to use which metric
  - Decision flowchart
  - Recommended thresholds with caveats
- [ ] **Section 10: Conclusion** (~300 words)
  - Restate thesis with evidence
  - Connect to broader ML evaluation practices
  - Call to action for practitioners
- [ ] **Review and polish**
  - Ensure notation is consistent throughout
  - Verify all cross-references between sections
  - Check that every figure is referenced in text
  - Proofread for mathematical errors

### Deliverables

- [ ] `article/krippendorff-alpha.md` (full article, ~5,800 words)
- [ ] All figures referenced and embedded
- [ ] `mkdocs.yml` configured for GitHub Pages

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-5/article` |
| Merge strategy | Squash merge |
| PR title | `feat(article): Phase 5 — full article draft` |
| Milestone | `Phase 5 — Article Writing` |
| Tag | `v0.6-article-draft` |
| Release | **Yes (pre-release)** — full draft ready for feedback |

### Issues

#### Issue #17 — Write article sections 1–5 (foundation through limitations)

```markdown
## Context
The first half of the article builds the problem: from naive agreement through
Kappa to its breaking points. This establishes the need for a better metric.

## Tasks
- [ ] Write sections 1–5 following the outline above
- [ ] Include all derivations from `notes/phase1-theory.md` and `notes/phase2-kappa.md`
- [ ] Embed figures: convergence plot, Kappa paradox
- [ ] Ensure consistent notation (define all symbols on first use)
- [ ] Target: ~2,900 words

## Definition of Done
- [ ] Sections 1–5 are complete in `article/krippendorff-alpha.md`
- [ ] All mathematical notation is consistent
- [ ] Figures are referenced with captions
- [ ] A reader with linear algebra background can follow every derivation

## References
- `notes/phase1-theory.md`, `notes/phase2-kappa.md`
```

**Labels:** `phase:5`, `type:writing`, `priority:high`

---

#### Issue #18 — Write article sections 6–10 (Alpha through conclusion)

```markdown
## Context
The second half presents the solution (Alpha), validates it experimentally,
and provides practical guidance. This is where the article delivers on its thesis.

## Tasks
- [ ] Write sections 6–10 following the outline above
- [ ] Include full Alpha derivation from `notes/phase3-alpha.md`
- [ ] Embed all four experiment figures
- [ ] Create decision flowchart for Section 9 (can be ASCII or generated)
- [ ] Write conclusion that ties back to the opening hook
- [ ] Target: ~2,900 words

## Definition of Done
- [ ] Sections 6–10 are complete
- [ ] Alpha derivation is self-contained (reader doesn't need to check notes)
- [ ] All four experiments are presented with interpretation
- [ ] Decision flowchart is clear and actionable
- [ ] Article reads as a cohesive narrative from start to finish

## References
- `notes/phase3-alpha.md`
- All experiment scripts and figures from Phase 4
```

**Labels:** `phase:5`, `type:writing`, `priority:high`

---

## Phase 6 — Review, Polish & Publish

### Objective

Validate the article mathematically, ensure code reproducibility, set up the publication infrastructure, and publish to GitHub Pages and Medium. This phase transforms a draft into a portfolio piece.

### Tasks

- [ ] **Mathematical validation**
  - Review every derivation for correctness
  - Verify numerical examples match code output
  - Check boundary cases in proofs
- [ ] **Code reproducibility**
  - Clone the repo fresh and run `make experiments`
  - Verify all figures are regenerated identically (fixed seeds)
  - Test on Python 3.10+ with `requirements.txt`
- [ ] **Article polish**
  - Proofread for grammar and clarity
  - Ensure all references are properly cited
  - Add author bio and date
  - Add "How to cite this article" section
- [ ] **GitHub Pages setup**
  - Configure `mkdocs.yml` with material theme
  - Add navigation, code highlighting, LaTeX rendering (MathJax)
  - Deploy with `mkdocs gh-deploy`
  - Verify rendering on desktop and mobile
- [ ] **Medium cross-post**
  - Adapt article for Medium (no LaTeX → use images for equations if needed)
  - Add canonical link pointing to GitHub Pages version
  - Schedule publication
- [ ] **LinkedIn post**
  - Write a summary post (3–5 paragraphs) linking to the article
  - Include one key figure (agreement trap heatmap)
- [ ] **Final README update**
  - Add badges (Python version, license, article link)
  - Add "Quick Start" with installation and experiment commands
  - Add "About" section with article abstract

### Deliverables

- [ ] Published GitHub Pages site
- [ ] Medium article (cross-posted)
- [ ] LinkedIn post draft
- [ ] Final `README.md`
- [ ] All tests passing in CI

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-6/publish` |
| Merge strategy | Squash merge |
| PR title | `chore(publish): Phase 6 — final review and publication` |
| Milestone | `Phase 6 — Review & Publish` |
| Tag | `v1.0.0` |
| Release | **Yes (stable)** — public portfolio release with article link and downloadable assets |

### Issues

#### Issue #19 — Mathematical validation and code reproducibility

```markdown
## Context
A portfolio article with mathematical errors or non-reproducible code undermines
credibility. This issue ensures everything checks out before publication.

## Tasks
- [ ] Review all derivations in `article/krippendorff-alpha.md`
- [ ] Cross-check numerical examples against code output
- [ ] Fresh clone → `pip install -r requirements.txt` → `make experiments`
- [ ] Verify all figures match those in the article
- [ ] Run `pytest tests/` and ensure 100% pass rate
- [ ] Fix any discrepancies found

## Definition of Done
- [ ] Zero mathematical errors in derivations
- [ ] `make experiments` reproduces all figures from a fresh clone
- [ ] All tests pass on Python 3.10+

## References
- Full article in `article/krippendorff-alpha.md`
```

**Labels:** `phase:6`, `type:review`, `priority:critical`

---

#### Issue #20 — Publish to GitHub Pages and Medium

```markdown
## Context
The article needs to be published in two formats: a richly formatted GitHub Pages
site (primary, with LaTeX rendering) and a Medium cross-post (for discoverability).

## Tasks
- [ ] Configure `mkdocs.yml`:
      - Theme: material
      - Plugins: search, MathJax for LaTeX
      - Navigation: Home → Article → Experiments → About
- [ ] Run `mkdocs gh-deploy` and verify live site
- [ ] Test on desktop (Chrome, Firefox) and mobile
- [ ] Adapt article for Medium:
      - Replace LaTeX with equation images where needed
      - Add canonical link to GitHub Pages
      - Ensure figures are embedded properly
- [ ] Write LinkedIn summary post
- [ ] Update `README.md` with live links and badges

## Definition of Done
- [ ] GitHub Pages site is live and renders correctly
- [ ] Medium article is published with canonical link
- [ ] LinkedIn post is drafted and ready to publish
- [ ] README has live links

## References
- MkDocs Material docs: https://squidfunk.github.io/mkdocs-material/
```

**Labels:** `phase:6`, `type:infrastructure`, `type:writing`, `priority:high`

---

## GitHub Workflow Standards

### Branch Naming Convention

```
<type>/<phase-number>-<short-description>

Examples:
  phase-0/foundation
  phase-1/statistical-foundation
  phase-2/kappa-family
  phase-3/krippendorff-alpha
  phase-4/experiments
  phase-5/article
  phase-6/publish
  fix/kappa-edge-case
  docs/update-readme
```

### Conventional Commits

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature or capability | `feat(core): implement coincidence matrix builder` |
| `fix` | Bug fix | `fix(metrics): handle division by zero in Fleiss Kappa` |
| `docs` | Documentation only | `docs(thesis): refine scope boundaries` |
| `test` | Adding or updating tests | `test(metrics): add edge case for perfect agreement` |
| `refactor` | Code change that neither fixes nor adds | `refactor(simulate): extract noise model to separate method` |
| `chore` | Maintenance, CI, configs | `chore(ci): add GitHub Actions workflow for tests` |
| `style` | Formatting, no logic change | `style(article): fix LaTeX spacing in Alpha derivation` |

**Commit message format:**

```
<type>(<scope>): <short description>

<optional body — what and why, not how>

<optional footer — references issues>
Closes #12
```

### Pull Request Template

```markdown
## Summary

<!-- What does this PR do? Link to the relevant issue. -->

Closes #

## Type of Change

- [ ] New feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Documentation (`docs`)
- [ ] Refactor (`refactor`)
- [ ] Test (`test`)

## Checklist

- [ ] Code runs without errors
- [ ] Tests pass (`pytest tests/`)
- [ ] Documentation updated (if applicable)
- [ ] Figures regenerated (if applicable)
- [ ] No hardcoded paths or secrets

## Mathematical Validation (if applicable)

- [ ] Derivations reviewed for correctness
- [ ] Numerical examples match code output
```

### Issue Templates

#### Task Template (`.github/ISSUE_TEMPLATE/task.md`)

```markdown
---
name: Task
about: A specific piece of work to be done
labels: ''
---

## Context
<!-- Why does this issue exist? What problem does it solve? -->

## Tasks
<!-- Specific, actionable checklist -->
- [ ] Task 1
- [ ] Task 2

## Definition of Done
<!-- Verifiable completion criteria -->
- [ ] Criterion 1
- [ ] Criterion 2

## References
<!-- Relevant links, docs, related code -->
```

#### Bug Template (`.github/ISSUE_TEMPLATE/bug.md`)

```markdown
---
name: Bug
about: Something is not working as expected
labels: 'type:bug'
---

## Description
<!-- What is broken? -->

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behaviour
<!-- What should happen? -->

## Actual Behaviour
<!-- What happens instead? -->

## Environment
- Python version:
- OS:
- Relevant packages:

## References
<!-- Related issues, error logs, etc. -->
```

### Labels

| Label | Color | Description |
|-------|-------|-------------|
| `phase:0` | `#0E8A16` | Phase 0 — Foundation |
| `phase:1` | `#1D76DB` | Phase 1 — Statistical Foundation |
| `phase:2` | `#5319E7` | Phase 2 — Kappa Family |
| `phase:3` | `#D93F0B` | Phase 3 — Krippendorff's Alpha |
| `phase:4` | `#FBCA04` | Phase 4 — Experiments |
| `phase:5` | `#B60205` | Phase 5 — Article Writing |
| `phase:6` | `#006B75` | Phase 6 — Review & Publish |
| `type:theory` | `#C5DEF5` | Mathematical derivation or proof |
| `type:code` | `#BFD4F2` | Implementation task |
| `type:experiment` | `#D4C5F9` | Experimental validation |
| `type:writing` | `#FEF2C0` | Article writing task |
| `type:documentation` | `#0075CA` | Planning or project docs |
| `type:infrastructure` | `#E4E669` | Repo setup, CI, tooling |
| `type:review` | `#F9D0C4` | Review or validation task |
| `type:bug` | `#D73A4A` | Something is broken |
| `priority:critical` | `#B60205` | Must be done, blocks other work |
| `priority:high` | `#D93F0B` | Important, do soon |
| `priority:medium` | `#FBCA04` | Can wait, but should be done |
| `priority:low` | `#0E8A16` | Nice to have |

---

## Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 0 — Foundation | 3–4 days | Week 1 |
| Phase 1 — Statistical Foundation | 4–5 days | Week 1–2 |
| Phase 2 — Kappa Family | 5–7 days | Week 2–3 |
| Phase 3 — Krippendorff's Alpha | 7–10 days | Week 3–4 |
| Phase 4 — Experiments | 5–7 days | Week 5 |
| Phase 5 — Article Writing | 7–10 days | Week 6–7 |
| Phase 6 — Review & Publish | 3–5 days | Week 7–8 |

**Total: 6–8 weeks**

---

## References

- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology*. Sage.
- Krippendorff, K. (2011). Computing Krippendorff's Alpha-Reliability.
- Cohen, J. (1960). A Coefficient of Agreement for Nominal Scales. *Educational and Psychological Measurement*.
- Fleiss, J. L. (1971). Measuring Nominal Scale Agreement Among Many Raters. *Psychological Bulletin*.
- Artstein, R. & Poesio, M. (2008). Inter-Coder Agreement for Computational Linguistics. *Computational Linguistics*.
- Feinstein, A. R. & Cicchetti, D. V. (1990). High Agreement but Low Kappa. *Journal of Clinical Epidemiology*.
