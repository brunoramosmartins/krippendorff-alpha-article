# TIL backlog — Krippendorff's Alpha article

**These are seeds, not finished TILs.** Each entry gives the angle to
write from later: a Hook, the Insight to land, a candidate Example, and a
Takeaway direction — plus why it earns a slot. Write the actual TIL
yourself (Hook / Insight / Example / Takeaway, <1000 words). Ranked by how
well it stands alone and fits the DS/ML-practitioner audience.

Legend: ⭐ = strongest picks (most differentiated / portfolio-relevant).

---

## ⭐ 1. `til-random-raters-agree-half-the-time.md`
*Source: Introduction + The chance agreement problem (Exp A)*

- **Hook:** two people who label a yes/no task by coin flip — zero shared
  understanding — still agree 50% of the time.
- **Insight:** i.i.d. random labelers agree at exactly $\sum_k \pi_k^2$;
  for $K=2$ uniform that is $1/K = 0.50$. "Random" does not mean "zero
  agreement," it means agreement at the chance level set by the marginals.
- **Example:** Exp A — $A_o$ tracks $1/K$ while $\kappa_F$ and $\alpha$ sit
  at 0.
- **Takeaway:** a raw agreement number is meaningless without its chance
  baseline; report both or report neither.
- **Why:** it is the whole thesis in one sentence — the ideal entry TIL.

## ⭐ 2. `til-reliable-is-not-correct.md`
*Source: Reliability is not validity / the LLM hook*

- **Hook:** an LLM that agrees with your annotators perfectly can still be
  perfectly wrong.
- **Insight:** high $\alpha$ means the process is *reproducible*, not that
  it is *right*. A model that mimics human labelers inherits their
  systematic bias; consistency is cheap (a constant function is perfectly
  consistent).
- **Example:** content moderation — annotators trained on the same guide
  reliably agree on labels an external audit would reject.
- **Takeaway:** agreement with humans is necessary but not sufficient for
  quality; you still need disagreement audits and external validation.
- **Why:** most portfolio/LLM-relevant of the set; it is *your* workplace
  scenario generalized. Ties the series back to the opening.

## ⭐ 3. `til-alpha-counts-pairs-not-rows.md`
*Source: Experiment D (matches the figure we just rebuilt)*

- **Hook:** delete a single cell from your annotation grid and Fleiss'
  kappa returns `NaN`. Krippendorff's alpha does not blink.
- **Insight:** Fleiss needs a complete matrix; $\alpha$ is defined on
  *pairable* judgments, so it uses whatever pairs survive. The naive fix
  (drop incomplete rows) throws data away fast.
- **Example:** Exp D — at 50% MCAR missingness only ~3% of rows stay
  complete, yet $\alpha$ holds near its full-data value.
- **Takeaway:** in real pipelines (raters quit, calls time out) prefer the
  coefficient that degrades gracefully instead of the one that vanishes.
- **Why:** concrete, practical, and directly reusable from today's figure
  work.

## 4. `til-high-agreement-low-kappa-is-algebra.md`
*Source: Limitations of Kappa (the paradox)*

- **Hook:** 84% raw agreement, $\alpha = 0.35$ — not a contradiction, just
  arithmetic.
- **Insight:** as one class dominates, the chance baseline
  $\bar P_e = \sum_k p_k^2 \to 1$, so the corrected coefficient shrinks
  even when raw overlap looks excellent.
- **Example:** $\pi=(0.85,0.10,0.05)$, $\varepsilon=0.05$ ⇒ $A_o\approx0.84$
  while $\alpha\approx0.35$ (Exp B).
- **Takeaway:** you cannot compare raw agreement across tasks with
  different class balance — the baseline moved under you.
- **Why:** counterintuitive and memorable; a classic "aha" for
  practitioners ranking models by accuracy-like numbers.

## 5. `til-count-disagreement-not-agreement.md`
*Source: From agreement to disagreement*

- **Hook:** flip the question from "how often do we match?" to "how much
  farther apart are we than random pairing?" and one formula suddenly
  spans nominal, ordinal, interval, and ratio scales.
- **Insight:** weighting mismatches by a distance $\delta$ generalizes
  agreement; nominal agreement is just the special case $\delta\in\{0,1\}$.
- **Example:** interval $\delta=(c-c')^2$ punishes a 1-vs-5 Likert clash
  far more than 3-vs-4 — something raw agreement cannot express.
- **Takeaway:** the disagreement framing is why $\alpha$ unifies scales
  that Kappa handles only with bolt-ons.
- **Why:** the most "elegant idea" TIL; slightly more abstract, so ranked
  below the concrete ones.

---

### Deferred / mergeable ideas
- **"Consistent" is the trap word** — overlaps heavily with #2; fold in as
  the hook there rather than a separate TIL.
- **Always put $A_o$ and a chance-corrected number in the same table** —
  true but thin as a standalone; better as the takeaway of #1.
