# Phase 2 — Cohen's and Fleiss' Kappa

This note records the **chance-corrected agreement** family used throughout NLP and medicine, and why it still falls short of a fully general reliability coefficient — motivating Krippendorff's \(\alpha\) in Phase 3.

---

## 1. Chance correction pattern

Given an **observed** agreement \(A_o\) and an **expected** agreement \(A_e\) under a stated chance model,

\[
\kappa \;=\; \frac{A_o - A_e}{1 - A_e}.
\]

**Interpretation (when \(A_e<1\)):**

- \(\kappa = 1\): perfect observed agreement (\(A_o=1\)).
- \(\kappa = 0\): observed agreement equals chance (\(A_o = A_e\)).
- \(\kappa < 0\): observed agreement is **below** chance under the model.

Different metrics differ in **how** \(A_o\) and \(A_e\) are defined (which pairs count, which marginals define chance).

---

## 2. Cohen's \(\kappa\) — two fixed raters

Two annotators rate the **same** \(n\) items. Let \(X_{i1}, X_{i2}\in\{1,\ldots,K\}\).

### 2.1 Observed agreement

\[
A_o \;=\; \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{X_{i1}=X_{i2}\}.
\]

### 2.2 Expected agreement (independence of raters, fixed marginals)

Let \(p_{k\cdot} = \frac{1}{n}\sum_i \mathbf{1}\{X_{i1}=k\}\) and \(p_{\cdot k} = \frac{1}{n}\sum_i \mathbf{1}\{X_{i2}=k\}\).

Under **independence** with those marginals,

\[
A_e \;=\; \sum_{k=1}^K p_{k\cdot}\,p_{\cdot k}.
\]

### 2.3 Cohen's kappa

\[
\kappa_C \;=\; \frac{A_o - A_e}{1-A_e}.
\]

### 2.4 Worked \(2\times 2\) example (3 items)

| item | Rater 1 | Rater 2 | agree? |
|------|---------|---------|--------|
| 1 | A | A | yes |
| 2 | A | B | no |
| 3 | B | B | yes |

Encode \(A\to 0\), \(B\to 1\). Then \(A_o = 2/3\).

Marginals: rater 1 \((2/3, 1/3)\), rater 2 \((1/3, 2/3)\).

\[
A_e = (2/3)(1/3) + (1/3)(2/3) = 2/9 + 2/9 = 4/9.
\]

\[
\kappa_C = \frac{2/3 - 4/9}{1 - 4/9} = \frac{2/9}{5/9} = \frac{2}{5} = 0.4.
\]

Cross-check: `sklearn.metrics.cohen_kappa_score` on the same vectors.

---

## 3. Fleiss' \(\kappa\) — many raters, one item at a time

There are \(n\) items and \(m\) raters **per item** (balanced design). Each rater assigns exactly one of \(K\) nominal categories.

For item \(i\), let \(n_{ik}\) be the number of raters who chose category \(k\) (\(\sum_k n_{ik}=m\)).

### 3.1 Extent of agreement on item \(i\)

\[
P_i \;=\; \frac{1}{m(m-1)}\sum_{k=1}^K n_{ik}(n_{ik}-1),
\]

the fraction of **unordered rater pairs** on item \(i\) that agree.

### 3.2 Mean observed agreement

\[
\bar P \;=\; \frac{1}{n}\sum_{i=1}^n P_i.
\]

### 3.3 Category proportions (pooling all \(nm\) judgments)

\[
p_k \;=\; \frac{1}{nm}\sum_{i=1}^n n_{ik}.
\]

### 3.4 Expected agreement under random assignment with fixed \(p_k\)

\[
\bar P_e \;=\; \sum_{k=1}^K p_k^2.
\]

(This mirrors the \(A_e=\sum_k\pi_k^2\) form from Phase 1 when all judgments share the same marginal \(\pi_k\).)

### 3.5 Fleiss' kappa

\[
\kappa_F \;=\; \frac{\bar P - \bar P_e}{1-\bar P_e}.
\]

### 3.6 Tiny numerical check (\(n=2\), \(m=3\), \(K=2\))

- Item 1: labels \((0,0,1)\) → \(n_{10}=2,n_{11}=1\) → \(P_1 = (2\cdot1 + 1\cdot0)/(3\cdot2)=1/3\).
- Item 2: \((1,1,1)\) → \(P_2=1\).

\(\bar P = (1/3+1)/2 = 2/3\).

Total counts: class 0 appears twice, class 1 four times → \(p_0=1/3\), \(p_1=2/3\), \(\bar P_e = 5/9\).

\[
\kappa_F = \frac{2/3 - 5/9}{1-5/9} = \frac{1/9}{4/9} = 0.25.
\]

Implementation: `src.metrics.fleiss_kappa`.

---

## 4. The Kappa paradox (imbalance + high \(A_o\))

When one category is **very prevalent**, **independent** raters would still agree often (\(\bar P_e\) is large because \(p_k^2\) is dominated by the majority class). A high **raw** proportion of agreeing pairs can then yield a **small or even negative** \(\kappa\) after subtraction of that large baseline.

**Roadmap-style scenario:** latent distribution near \((0.9,0.05,0.05)\) with small noise — observed agreement \(A_o\) can sit around **0.85** while \(\kappa_F\) may fall near **0.2**. The figure `figures/kappa_paradox.png` sweeps the strength of the dominant class for fixed noise levels.

---

## 5. Structural limitations (why \(\alpha\) next)

| Limitation | Cohen | Fleiss |
|------------|-------|--------|
| Number of raters | Exactly **two** (fixed pair) | **\(m\ge 2\)** but same \(m\) for every item |
| Missing data | Not built in (pairs dropped ad hoc) | **Complete** matrix required |
| Scale | **Nominal** (unordered categories) | **Nominal** |
| Ordinal / interval / ratio | Needs **weighted** \(\kappa\) variants | Same |

Neither metric supplies a single framework that natively combines **missing data**, **variable numbers of raters**, and **metric distances** between categories — gaps Krippendorff's \(\alpha\) is designed to address.

---

## References

- Cohen, J. (1960). A Coefficient of Agreement for Nominal Scales. *Educational and Psychological Measurement*.
- Fleiss, J. L. (1971). Measuring Nominal Scale Agreement Among Many Raters. *Psychological Bulletin*.
- Feinstein, A. R. & Cicchetti, D. V. (1990). High Agreement but Low Kappa. *Journal of Clinical Epidemiology*.
- scikit-learn: `sklearn.metrics.cohen_kappa_score`.
