# Phase 1 — Observed vs expected agreement

This note formalises **pairwise observed agreement** \(A_o\) and **expected agreement under independence** \(A_e\), and records the core warning for the article: **high \(A_o\) is not evidence of reliability** when chance alone would already produce substantial agreement.

Notation: \(K\) categories (indexed \(k=1,\ldots,K\)), \(n\) items, \(m\) annotators. The annotation matrix is \((X_{ij})\) with \(X_{ij}\in\{1,\ldots,K\}\) (code uses \(0,\ldots,K-1\)).

---

## 1. Pairwise observed agreement

Fix an item \(i\). Let \(S_i\) be the set of annotator pairs \((j,\ell)\) with \(j<\ell\) such that **both** \(X_{ij}\) and \(X_{i\ell}\) are observed. For each such pair, define an **agreement indicator** \(I_{ij\ell}=1\) if \(X_{ij}=X_{i\ell}\), else \(0\).

The **observed agreement** is the fraction of comparable pairs that agree:

\[
A_o
=
\frac{\displaystyle\sum_{i=1}^n \sum_{(j,\ell)\in S_i} I_{ij\ell}}
     {\displaystyle\sum_{i=1}^n |S_i|}.
\]

**Interpretation:** \(A_o\) is a **sample proportion** of agreeing rater-pairs, pooled over items. It estimates the probability that two randomly chosen ratings on the **same** item agree, under the sampling scheme implied by which pairs are observed (here: uniform over unordered pairs of observed labels on that item).

**Worked example (3 items, 2 annotators).** Suppose

| item | \(X_{i1}\) | \(X_{i2}\) |
|------|------------|------------|
| 1 | A | A |
| 2 | B | A |
| 3 | C | C |

There are three items and one pair per item. Agreements on items 1 and 3; disagreement on item 2. Hence \(A_o = 2/3\).

---

## 2. Alternative form: random pair of judgments **with replacement**

Pool all observed judgments across the study and let \(N\) be their total count. Let \(n_k\) be how many judgments equal category \(k\). Draw two judgments **uniformly at random from the pool, with replacement**. Then

\[
P(\text{both draws are category } k) = \Bigl(\frac{n_k}{N}\Bigr)^2,
\qquad
P(\text{agree}) = \sum_{k=1}^K \Bigl(\frac{n_k}{N}\Bigr)^2.
\]

This quantity is **not** identical to the pairwise-within-item \(A_o\) above when \(m>2\) or when missingness varies, but it is a useful **global** summary and matches the roadmap’s \(\sum_k (n_k/N)^2\) expression for that sampling scheme.

Implementation: `src.metrics.observed_agreement` (within-item pairs) vs `observed_agreement_global_with_replacement` (pool).

---

## 3. Expected agreement under independence (“chance”)

**Model.** Two annotators assign labels **independently**, each following the same category distribution \(\pi=(\pi_1,\ldots,\pi_K)\), \(\pi_k\ge 0\), \(\sum_k\pi_k=1\).

Then

\[
A_e
=
P(\text{both pick the same category})
=
\sum_{k=1}^K P(\text{first}=k)P(\text{second}=k)
=
\sum_{k=1}^K \pi_k^2.
\]

### 3.1 Uniform categories

If \(\pi_k = 1/K\) for all \(k\),

\[
A_e = K\cdot (1/K)^2 = 1/K.
\]

So for **two** classes and uniform marginals, \(A_e = 1/2\): independent “coin-flip” labellers agree half the time **even with no shared truth**.

### 3.2 Imbalanced example (\(K=3\))

Let \(\pi=(0.7,0.2,0.1)\). Then

\[
A_e = 0.7^2 + 0.2^2 + 0.1^2 = 0.49 + 0.04 + 0.01 = 0.54.
\]

**Numerical check (three examples from roadmap):**

| Setting | \(A_e\) |
|---------|--------|
| \(K=2\), uniform | \(0.50\) |
| \(K=3\), uniform | \(1/3 \approx 0.333\) |
| \(K=3\), \(\pi=(0.7,0.2,0.1)\) | \(0.54\) |

---

## 4. Random annotators: why \(A_o \not\to 0\)

If each cell of the matrix is drawn **independently** from \(\pi\) (no latent shared truth — `pure_random=True` in `src.simulate`), then two ratings on the same item are **independent** draws from \(\pi\). The probability they agree is **exactly** \(A_e=\sum_k\pi_k^2>0\) for any non-degenerate \(\pi\).

Therefore **“random” does not mean “zero agreement”**; it means agreement at the **chance** level induced by the marginals. Any interpretation of raw \(A_o\) must compare to that baseline.

---

## 5. Connection to later phases

- **Kappa** uses the same **chance correction** idea: compare \(A_o\) to an \(A_e\) (sometimes estimated from data).
- **Krippendorff’s \(\alpha\)** reframes agreement in terms of **disagreement** and generalises distances; for nominal data it links back to related counting of matches.

---

## 6. Core insight (article line)

> **High \(A_o\) \(\neq\) high agreement in a substantive sense.**  
> Large \(A_o\) can be driven by **marginal prevalence** and **independence**, not by shared correct understanding of items. Always ask: **what would \(A_o\) be if annotators were independent but kept the same marginal behaviour?**

---

## References

- Artstein, R. & Poesio, M. (2008). *Inter-Coder Agreement for Computational Linguistics.*
- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology*, Chapter 11.
