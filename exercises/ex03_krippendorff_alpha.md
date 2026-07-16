# Exercises — Krippendorff's Alpha

Paper exercises for *From agreement to disagreement* and *Krippendorff's
Alpha*. Build the coincidence matrix by hand, then check against
`src/metrics.py`. Mirrors Phase 3 of `docs/math-derivations-checklist.md`.

## Proofs (paper)

1. **Alpha as a fractional reduction.** Starting from
   $\alpha = 1 - D_o^*/D_e^*$ with $D_o^* = \sum_{c,c'} O_{cc'} D_{cc'}$
   and $D_e^*$ the same sum against $\mathbf{E}$, rearrange to
   $\alpha = (D_e^* - D_o^*)/D_e^*$ and interpret it as the fractional
   reduction of observed disagreement relative to the random-pairing null.

2. **Expected coincidence.** With marginals $n_c$ derived from
   $\mathbf{O}$ and $N=\sum_c n_c$, derive
   $$E_{cc'} = \frac{n_c n_{c'} - n_c\,\delta_{cc'}}{N-1}$$
   and explain the "$-\,n_c\delta_{cc'}$" and "$N-1$" as
   sampling-without-replacement on pair slots.

3. **Boundary behaviour.** Assuming $D_e^*>0$, show that $\alpha=1$ when
   $D_o^*=0$ (nominal $\delta$, all pairable judgments coincide), $\alpha=0$
   when $D_o^*=D_e^*$, and $\alpha<0$ when $D_o^*>D_e^*$. What real-world
   situation makes $\alpha<0$?

4. **Why $\alpha \neq \kappa_C$ for $K>2$.** Both correct for chance on two
   raters with nominal data, yet need not agree numerically. Argue that
   the chance models differ: Cohen uses **per-rater** marginals, $\alpha$
   uses **pooled** coincidence marginals.

5. **Distance functions.** Write $\delta(c,c')$ for **nominal** (0/1),
   **interval** $(c-c')^2$, and **ratio** $((c-c')/(c+c'))^2$, and state in
   one line why **ordinal** weights must use the category masses $n_v$
   rather than plain rank gaps.

## Computations (paper)

Use the worked example from the article — three units, three raters, binary
domain $\{A,B\}$:

| Unit | R1 | R2 | R3 |
|------|----|----|----|
| 1 | A | A | B |
| 2 | B | B | — |
| 3 | A | A | A |

6. **Build $\mathbf{O}$.** For each unit form the count vector and add the
   local contributions $n_{ic}n_{ic'}/(m_i-1)$ (off-diagonal) and
   $n_{ic}(n_{ic}-1)/(m_i-1)$ (diagonal). *Target:*
   $$\mathbf{O}=\begin{bmatrix} 4 & 1 \\ 1 & 2 \end{bmatrix},\quad
     n_A=5,\; n_B=3,\; N=8.$$

7. **Build $\mathbf{E}$.** With $N-1=7$, compute $E_{AA}$, $E_{BB}$,
   $E_{AB}$. *Targets:* $E_{AA}=20/7\approx2.857$, $E_{BB}=6/7\approx0.857$,
   $E_{AB}=E_{BA}=15/7\approx2.143$.

8. **Nominal $\alpha$.** With $\delta$ nominal, $D_o^* = O_{AB}+O_{BA}=2$
   and $D_e^* = E_{AB}+E_{BA}=30/7$. Compute
   $\alpha = 1 - D_o^*/D_e^*$. *Target:* $\alpha = 1 - 14/30 \approx 0.533$.

## Self-check

```python
import numpy as np, pandas as pd
from src.metrics import krippendorff_alpha
data = pd.DataFrame([[0, 0, 1], [1, 1, np.nan], [0, 0, 0]])  # A=0, B=1
krippendorff_alpha(data, level_of_measurement="nominal")      # -> 0.5333
```
