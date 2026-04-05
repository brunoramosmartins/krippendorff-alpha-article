# Phase 3 — Krippendorff's Alpha

This note matches the **coincidence-matrix** construction and \(\alpha\) formula implemented in `src/coincidence.py`, `src/distances.py`, and `src.metrics.krippendorff_alpha`, aligned with Krippendorff (2004, Ch. 11) and the reference `krippendorff` Python package.

---

## 1. From agreement to disagreement

Instead of correcting raw agreement with a single scalar \(A_e\) (Kappa family), Krippendorff works with **pairwise metric disagreement** \(\delta(c,c')\) between category values. Reliability is

\[
\alpha = 1 - \frac{D_o}{D_e},
\]

where \(D_o\) aggregates **observed** weighted disagreements from the data and \(D_e\) is the corresponding expectation under a **random pairing** model that preserves overall category exposure.

---

## 2. Reliability matrix and missing data

**Convention in this repo:** rows = **units** (items), columns = **raters**; missing entries are `NaN`.

For each unit \(i\), let \(m_i\) be the number of **non-missing** judgments. Only pairs of distinct raters on the same unit contribute. If \(m_i<2\), the unit contributes nothing to coincidence totals.

---

## 3. Category counts and coincidence matrix \(\mathbf{O}\)

Fix an ordered **value domain** \((v_1,\ldots,v_V)\). For unit \(i\), let \(n_{iv}\) be how many raters assigned \(v_v\) (so \(\sum_v n_{iv}=m_i\)).

Stack \(\mathbf{n}_i=(n_{i1},\ldots,n_{iV})\). The **unnormalised** co-occurrence for that unit (excluding same-rater self-pairs) is \(\mathbf{n}_i\mathbf{n}_i^\top\) with diagonal entries reduced from \(n_{iv}^2\) to \(n_{iv}(n_{iv}-1)\). Equivalently, subtract the diagonal matrix with \(n_{iv}\) on the diagonal.

Let \(\tilde m_i=\max(m_i,2)\). Scale that matrix by \(1/(\tilde m_i-1)\) and **sum over units** to obtain the **observed coincidence matrix** \(\mathbf{O}\in\mathbb{R}^{V\times V}\). Entry \(O_{cc'}\) counts (weighted) how often category \(v_c\) and \(v_{c'}\) co-occur on **distinct raters** of the same unit.

Properties:

- \(\mathbf{O}\) is **symmetric**.
- On the diagonal, \(O_{cc}\) relates to **within-category pairing** (agreement mass for nominal \(\delta\)).

**Missing data:** a rater with `NaN` is dropped before forming \(\mathbf{n}_i\); no pair is formed with a missing cell.

---

## 4. Marginals and expected coincidence \(\mathbf{E}\)

Let \(n_v = \sum_c O_{cv}\) (column sums of \(\mathbf{O}\); implementation uses `marginal_totals`). Let \(N=\sum_v n_v\), the total **pairable** coincidence mass.

Under random assignment of pair slots preserving these totals,

\[
E_{cc'} = \frac{n_c n_{c'} - n_c\,\delta_{cc'}}{N-1}.
\]

So \(\mathbf{E}\) is symmetric with zero contribution from “impossible” self-pairs in the numerator adjustment.

---

## 5. Metric \(\delta\) and distance matrix \(\mathbf{D}\)

- **Nominal:** \(\delta(c,c')=0\) if \(c=c'\), else \(1\).
- **Interval:** \((c-c')^2\).
- **Ratio:** \(\bigl((c-c')/(c+c')\bigr)^2\) with \(0\) if \(c+c'=0\).
- **Ordinal:** uses **ordered** domain and the empirical totals \(n_v\) (Krippendorff §11.4); not merely \((\mathrm{rank}(c)-\mathrm{rank}(c'))^2\) without those weights.

Assemble \(\mathbf{D}\) with \(D_{cc'}=\delta(v_c,v_{c'})\) on the domain grid.

---

## 6. Observed and expected disagreement scalars

Define

\[
D_o^\* = \sum_{c,c'} O_{cc'}\,D_{cc'},
\qquad
D_e^\* = \sum_{c,c'} E_{cc'}\,D_{cc'}.
\]

Then

\[
\alpha = 1 - \frac{D_o^\*}{D_e^\*}.
\]

**Nominal link to agreement:** when \(\delta\) is 0–1 off-diagonal, \(D_o^\*\) measures weighted **disagreement**; for binary data and simple designs, this relates to observed agreement, but the **matrix \(\mathbf{O}\)** already encodes the multi-rater structure differently from raw pairwise \(A_o\) in Phase 1.

---

## 7. Boundary behaviour

Assume \(D_e^\*>0\) (otherwise \(\alpha\) is undefined / not reported as a finite number).

- If **perfect reliability** in the sense that all pairable judgments on every unit coincide nominally, then off-diagonal \(\mathbf{O}\) mass vanishes for nominal \(\delta\), \(D_o^\*=0\), hence \(\alpha=1\).
- If **observed** disagreement equals **expected** (\(D_o^\*=D_e^\*\)), then \(\alpha=0\) (chance-level under the model).
- If \(D_o^\*>D_e^\*\), then \(\alpha<0\) (**systematic** disagreement beyond the random baseline).

Implementation returns `nan` when \(D_e^\*\) is numerically zero.

---

## 8. Relationship to Cohen's \(\kappa\) (two raters)

Cohen's \(\kappa\) uses **per-rater** marginals on the same \(n\) items to form \(A_e=\sum_k p_{k\cdot}p_{\cdot k}\). Krippendorff's \(\alpha\) uses the **pooled** coincidence marginals \(n_v\) derived from \(\mathbf{O}\). For **two raters** and **nominal** data, both correct for chance, but the **numerical value** need not equal Cohen's \(\kappa\) when \(K>2\): the chance models differ. The implementation is validated against the `krippendorff` package (which follows Krippendorff's coincidence definition), not against `sklearn`'s Cohen kappa on the same table.

---

## 9. Worked micro-example (one unit, three raters)

Domain \((0,1,2)\), counts \(\mathbf{n}=(2,1,0)\) (\(m=3\)). After scaling by \(1/(3-1)\), the contribution to \(\mathbf{O}\) is

\[
\frac{1}{2}\left(
\begin{bmatrix}4&2&0\\2&1&0\\0&0&0\end{bmatrix}
-
\begin{bmatrix}2&0&0\\0&1&0\\0&0&0\end{bmatrix}
\right)
=
\begin{bmatrix}1&1&0\\1&0&0\\0&0&0\end{bmatrix}.
\]

See `tests/test_coincidence.py`.

---

## References

- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology*. Sage. Chapter 11.
- `krippendorff` package: https://pypi.org/project/krippendorff/
