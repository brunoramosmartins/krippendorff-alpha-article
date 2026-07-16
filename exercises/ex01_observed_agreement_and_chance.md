# Exercises — Observed Agreement and the Chance Baseline

Paper exercises for the *Agreement as an estimator* and *The chance
agreement problem* sections. Do them with pen and paper first; check the
numeric targets against `src/metrics.py` afterwards. Mirrors Phase 1 of
`docs/math-derivations-checklist.md`.

## Proofs (paper)

1. **Observed agreement from pairs.** Fix an item $i$ rated by several
   annotators. Let $S_i$ be the set of unordered rater pairs $(j,\ell)$,
   $j<\ell$, with **both** $X_{ij}$ and $X_{i\ell}$ observed, and let
   $I_{ij\ell}=\mathbf{1}\{X_{ij}=X_{i\ell}\}$. Write $A_o$ as a pooled
   fraction over all items and explain in one sentence what population
   quantity it estimates.

2. **Chance agreement under independence.** Two annotators label the same
   item **independently**, each drawing from $\pi=(\pi_1,\dots,\pi_K)$.
   Prove that
   $$A_e = P(\text{both pick the same category}) = \sum_{k=1}^{K}\pi_k^2.$$

3. **Uniform case.** Prove that if $\pi_k = 1/K$ for all $k$, then
   $A_e = 1/K$.

4. **Random does not mean zero.** Suppose every matrix entry is drawn
   i.i.d. from $\pi$ (no shared item-level truth). Argue that the
   probability two ratings on the same item agree is **exactly**
   $\sum_k \pi_k^2 > 0$ for any non-degenerate $\pi$, and hence that
   $A_o$ concentrates on $\sum_k \pi_k^2$ rather than on $0$ as the number
   of items grows. Why does this make a headline $A_o$ misleading on its
   own?

5. **(Optional) Global with-replacement form.** Pool all $N$ observed
   judgments with category counts $n_k$. Show that drawing two judgments
   uniformly **with replacement** gives $P(\text{agree})=\sum_k (n_k/N)^2$,
   and describe one design in which this diverges from the pairwise
   within-item $A_o$.

## Computations (paper)

6. **Imbalanced baseline.** For $\pi=(0.7,0.2,0.1)$ compute $A_e$.
   *Target:* $A_e = 0.54$. Comment on why "more than half by chance"
   is a warning shot for applied reports.

7. **Three items, two raters.** Items 1 and 3 agree; item 2 disagrees.
   Compute $A_o$. *Target:* $A_o = 2/3$.

8. **Baseline table.** Fill in $A_e = \sum_k \pi_k^2$ for: $K=2$ uniform;
   $K=3$ uniform; $K=3$ with $\pi=(0.7,0.2,0.1)$.
   *Targets:* $0.50$, $1/3\approx0.333$, $0.54$.

## Self-check

```python
from src.metrics import observed_agreement, expected_agreement_independence
expected_agreement_independence([0.7, 0.2, 0.1])  # -> 0.54
```
