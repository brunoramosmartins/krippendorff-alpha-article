# Thesis and scope

## Central claim (v0.1)

> An agreement score of 0.80 among annotators is more likely evidence of **structured noise** than of true consensus when **chance agreement** is not properly accounted for. Metrics like raw agreement fail because they treat observed agreement as pure signal, rather than as an **estimator** composed of signal and chance. **Krippendorff's Alpha** addresses this by explicitly modelling **disagreement under randomness** while accommodating multiple raters, missing data, and (via distance functions) several measurement scales.

## Formal axis

Every agreement metric is an estimator under uncertainty:

\[
\text{Observed agreement} = \text{signal} + \text{chance}
\]

The article argues that transparently separating these components — and correcting for chance — is necessary before interpreting any single scalar as “reliability.”

## Scope (what the article covers)

- The annotation setup as a **multi-class labelling** problem: items, multiple annotators, nominal categories (extensions to other scales via Alpha).
- **Observed agreement** \(A_o\) and **expected agreement under independence** \(A_e\): derivations, intuition, and simulation.
- **Chance-corrected** metrics: **Cohen's Kappa**, **Fleiss' Kappa**, strengths and limitations (imbalance “paradox,” fixed design, missing data).
- **Krippendorff's Alpha**: coincidence matrix, distances (nominal, ordinal, interval, ratio), observed vs expected disagreement, boundary behaviour, validation against reference implementations.
- **Empirical experiments** tying claims to figures: random raters, high-\(A_o\) / low-reliability traps, LLM-as-rater vs humans (synthetic analogue), missing-data robustness.
- A short **practical guide**: when to use which metric, with caveats.

## Anti-scope (what the article does *not* cover)

- Exhaustive treatment of **weighted Kappa** variants and all historical disputes around weighting schemes.
- **Bayesian** or hierarchical annotation models; **crowd consensus** algorithms as a full alternative framework.
- **Deep learning** models that jointly learn annotator behaviour; **IRT**-style rater models beyond a passing pointer.
- Legal, contractual, or workflow tooling for annotation operations.

## Audience and prerequisites

- **Primary:** ML practitioners, data scientists, and NLP engineers who run or evaluate annotation for datasets or LLM outputs.
- **Assumed background:** comfort with probability at an introductory graduate level, basic linear algebra, and Python data tooling (NumPy / pandas). No prior exposure to Krippendorff's Alpha is required.

## Abstract (draft)

Inter-annotator agreement is often summarised by a single proportion: “they agreed 80% of the time.” That number can be **misleadingly high** when categories are imbalanced or when independent random labellers would already agree often by chance. This article rebuilds agreement metrics from first principles — observed and expected agreement, the Kappa family, and finally **Krippendorff's Alpha** — and supports the narrative with reproducible simulations inspired by evaluating an LLM against a human panel. The goal is not to advocate one statistic in all settings, but to show **what each number estimates** and why Alpha provides a flexible, principled default when data are messy.

## Falsifiability

The thesis is falsifiable: one can construct (and the project will implement) scenarios where **raw agreement is high** while **chance-corrected reliability is low**, and conversely where corrections align with known ground-truth simulation parameters. If, under broad conditions, raw agreement were sufficient to rank model or rater quality, the central warning of the article would weaken.

## References (anchor texts)

- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology*. Sage.
- Artstein, R. & Poesio, M. (2008). Inter-Coder Agreement for Computational Linguistics. *Computational Linguistics*.
