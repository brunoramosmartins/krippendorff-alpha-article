# Dataset design

This document specifies the **synthetic** annotation generator (primary) and the optional **real** data path, plus the **LLM evaluation** scenario that motivates the article.

---

## 1. Formal setting

- **Items** \(i = 1,\ldots,n\): units to label (e.g. project descriptions).
- **Annotators** \(j = 1,\ldots,m\): human coders and/or an LLM treated as another rater.
- **Categories** \(k \in \{1,\ldots,K\}\): mutually exclusive labels (e.g. brand buckets).

**Annotation matrix** \(X \in \mathbb{R}^{n \times m}\): entry \(X_{ij}\) is the category assigned by annotator \(j\) to item \(i\), or **missing** (encoded as `NaN`).

---

## 2. Synthetic generator parameters

| Parameter | Default | Range | Role |
|-----------|---------|-------|------|
| `n_items` | 10,000 | 100–50,000 | Number of items |
| `n_annotators` | 5 | 3–10 | Panel size |
| `n_classes` | 3 | 2–10 | Number of categories \(K\) |
| `noise_level` \(\varepsilon\) | 0.2 | 0.0–1.0 | Probability of deviating from the latent “true” class |
| `class_distribution` | uniform | uniform / imbalanced / extreme | Prior over true classes per item |
| `missing_rate` | 0.0 | 0.0–0.5 | MCAR missingness for entries \(X_{ij}\) |
| `seed` | — | any int | Reproducibility |

### 2.1 Latent truth and noise model

For each item \(i\), draw a **true** class \(Y_i \sim \mathrm{Categorical}(\pi)\) where \(\pi\) is determined by `class_distribution`.

Given \(Y_i = c\), annotator \(j\) observes a **noisy** draw:

- With probability \(1 - \varepsilon\): \(X_{ij} = c\).
- With probability \(\varepsilon\): \(X_{ij}\) is uniform over the **other** \(K-1\) classes:

\[
P(X_{ij} = c' \mid Y_i = c) = \begin{cases}
1 - \varepsilon & c' = c \\
\varepsilon / (K - 1) & c' \neq c
\end{cases}
\]

**Edge cases:**

- \(\varepsilon = 0\): perfect agreement with truth (all annotators copy \(Y_i\)).
- \(\varepsilon = 1\): labels are **uniform random** on the \(K-1\) wrong classes only if we still anchor on \(Y_i\); for **pure chance** agreement benchmarks, the roadmap uses **uniform draws over all \(K\) classes** independent of truth (implemented explicitly in simulation code in Phase 1 — see `src/simulate.py` when available).

*Clarification for Phase 1 implementation:* the codebase will expose a flag or parameter for **“pure random raters”** (ignore \(Y_i\), i.i.d. uniform labels) versus **“noisy copy of truth”** as above.

For **Phase 1 / issue #7** (convergence of empirical \(A_o\) to the independence baseline), set **`pure_random=True`**. That makes every cell i.i.d. \(\mathrm{Categorical}(\pi)\), so the theoretical benchmark is \(A_e=\sum_k\pi_k^2\) (e.g. \(1/K\) under uniform \(\pi\)); this matches the experiment “random annotators” in the roadmap. With **`pure_random=False`** and \(\varepsilon=1\), labels are still tied to latent \(Y_i\) and restricted to wrong categories only, so the marginal over \(K\) is **not** uniform and \(A_o\) need not approach \(1/K\).

### 2.2 Class distribution scenarios

Let \(K=3\) for examples; generalise by normalising a length-\(K\) probability vector.

| Scenario | Probability vector \(\pi\) | Rationale |
|----------|----------------------------|-----------|
| **Uniform** | \([1/3,\,1/3,\,1/3]\) | Baseline; \(A_e\) for independence matches classic textbook examples. |
| **Imbalanced** | \([0.70,\,0.20,\,0.10]\) | Common skew; inflates naive agreement. |
| **Extreme** | \([0.90,\,0.05,\,0.05]\) | Stress-test for Kappa paradox / high \(A_o\) with low reliability. |

For general \(K\), **uniform** is \(1/K\) each; imbalanced/extreme patterns extend by fixing a dominant mass on class 1 and splitting the remainder.

### 2.3 Missing data (MCAR)

After all labels are drawn, each cell \(X_{ij}\) is set to **missing** independently with probability `missing_rate`. This is **missing completely at random (MCAR)**: missingness does not depend on the label or item.

---

## 3. Real dataset (optional)

- **Source:** Hugging Face `datasets` (e.g. sentiment or NLI tasks with multiple annotators).
- **Usage:** compare **human** distributions to **LLM** outputs mapped into the same category set; optional extension after synthetic validation.

Implementation target: `src/loader.py` (Phase 1+).

---

## 4. LLM evaluation scenario (workplace-inspired)

**Story:** A company classifies initiatives into **three brand-related categories** to steer investment. A **prompt-tuned LLM** proposes labels; humans audit a sample. The question is whether the LLM **agrees** with the human panel in a way that survives chance correction.

### 4.1 Mapping LLM outputs into the annotation matrix

- Humans \(j = 1,\ldots,m-1\) label items as usual.
- The **LLM** is annotator \(j = m\): each item receives one predicted category (or missing if the call fails — treated as MCAR / optional separate model in code).

### 4.2 Models and prompting (real API path)

Candidate models (examples): GPT-4.x, Claude 3.x — final choice documented when experiments run. Prompting: fixed system + user template with **closed set** of labels and **JSON** or single-token output for parsing.

### 4.3 Fallback (no API)

**Simulated LLM:** same generator as humans but with a **slightly higher** `noise_level` (e.g. humans 0.10, LLM 0.15) to emulate a weaker rater. This supports reproducible figures without external keys.

### 4.4 Minimal matrix example (\(n=3\), 3 humans + LLM)

| Item | Human 1 | Human 2 | Human 3 | LLM |
|------|---------|---------|---------|-----|
| 1 | A | A | B | A |
| 2 | B | B | B | C |
| 3 | C | C | C | C |

Metrics: pairwise Cohen's \(\kappa\) (each human vs LLM), Fleiss \(\kappa\) on the full table, Krippendorff's \(\alpha\) with nominal distance — implemented in later phases.

---

## 5. Pseudocode (generator)

```text
INPUT: n_items, n_annotators, n_classes, noise_level, class_dist, missing_rate, seed
RNG <- seeded generator
pi <- vector from class_dist scenario
FOR i IN 1..n_items:
    Y[i] ~ Categorical(pi)
    FOR j IN 1..n_annotators:
        draw X[i,j] from noise model around Y[i] (or pure-random mode if configured)
FOR each cell (i,j):
    with probability missing_rate: X[i,j] <- NA
OUTPUT: DataFrame X (n_items x n_annotators)
```

---

## 6. Formal problem statement (LaTeX-friendly)

Given a matrix \(X \in \{1,\ldots,K\}^{n \times m}\) with missing entries, **reliability** is assessed by comparing **observed** patterns of agreement / disagreement to a **baseline** induced by a chance model (independence, preserving marginals, etc.). The article studies estimators \( \hat{A}_o, \hat{\kappa}, \hat{\alpha} \) as answers to subtly different **estimands**; the synthetic generator supplies known latent structure to stress-test each estimator.
