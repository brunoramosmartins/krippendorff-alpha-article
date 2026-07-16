# Exercises — The Kappa Family

Paper exercises for *The Kappa family* and *Limitations of Kappa*. Do them
by hand first; check the numeric targets against `src/metrics.py`. Mirrors
Phase 2 of `docs/math-derivations-checklist.md`.

## Proofs (paper)

1. **The chance-correction pattern.** Given observed agreement $A_o$ and
   expected agreement $A_e$ under a stated chance model, define
   $\kappa = (A_o - A_e)/(1 - A_e)$. Show that $\kappa=1$ when $A_o=1$,
   $\kappa=0$ when $A_o=A_e$, and $\kappa<0$ when $A_o<A_e$. Explain in
   one sentence why dividing by $1-A_e$ makes $\kappa$ comparable across
   tasks with different baselines — and why it also makes $\kappa$ swing
   when a rare-class count nudges $A_e$.

2. **Cohen's observed and expected agreement.** For two fixed raters,
   write $A_o = \frac{1}{n}\sum_i \mathbf{1}\{X_{i1}=X_{i2}\}$ and derive
   $A_e = \sum_k p_{k\cdot}\,p_{\cdot k}$ from the **empirical per-rater
   marginals**. State clearly which independence assumption $A_e$ encodes.

3. **Fleiss' per-item agreement.** With $m$ raters on item $i$ and counts
   $n_{ik}$ ($\sum_k n_{ik}=m$), derive
   $$P_i = \frac{1}{m(m-1)}\sum_{k=1}^{K} n_{ik}(n_{ik}-1)$$
   as the fraction of **unordered** rater pairs on item $i$ that agree.

4. **Fleiss' coefficient.** From $\bar P = \frac{1}{n}\sum_i P_i$,
   $p_k = \frac{1}{nm}\sum_i n_{ik}$, and $\bar P_e = \sum_k p_k^2$,
   assemble $\kappa_F = (\bar P - \bar P_e)/(1-\bar P_e)$.

5. **The paradox is algebra.** Let one class have proportion
   $p_\text{major}\to 1$. Show that $\bar P_e = \sum_k p_k^2 \to 1$, and
   argue why $\kappa_F$ can be driven toward $0$ (or negative) even while
   raw agreement $A_o$ stays in the "excellent" band. Why is this a
   feature, not a bug?

## Computations (paper)

6. **Cohen $2\times 2$.** Three items, encodings A/B giving $A_o=2/3$ with
   marginals $(2/3,1/3)$ for rater 1 and $(1/3,2/3)$ for rater 2. Compute
   $A_e$ and $\kappa_C$. *Targets:* $A_e = 4/9$, $\kappa_C = 0.4$.

7. **Fleiss tiny case.** $n=2$ items, $m=3$ raters, $K=2$. Item 1 has
   counts $(2,1)$, item 2 has counts $(0,3)$. Compute $P_1$, $P_2$,
   $\bar P$, the pooled $p_k$, $\bar P_e$, and $\kappa_F$.
   *Targets:* $P_1=1/3$, $P_2=1$, $\bar P=2/3$, $p=(1/3,2/3)$,
   $\bar P_e=5/9$, $\kappa_F=0.25$.

## Self-check

```python
import numpy as np
from src.metrics import cohens_kappa, fleiss_kappa
cohens_kappa([0, 0, 1], [0, 1, 1])                 # -> 0.4
fleiss_kappa(np.array([[0, 0, 1], [1, 1, 1]]))     # -> 0.25
```
