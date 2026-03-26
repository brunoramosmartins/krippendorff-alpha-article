# Article outline

Target length: **6,000–8,000 words** total. Section word counts are indicative.

| § | Section | Approx. words | Primary phase | Dependencies |
|---|---------|----------------|---------------|--------------|
| 1 | Introduction | 600 | 5 | Thesis, scenario hook |
| 2 | Agreement as an estimator | 500 | 5 | Phase 1 notes |
| 3 | The chance agreement problem | 600 | 5 | Phase 1 + Fig. convergence |
| 4 | The Kappa family | 700 | 5 | Phase 2 notes |
| 5 | Limitations of Kappa | 500 | 5 | Phase 2 + Kappa paradox figure |
| 6 | From agreement to disagreement | 400 | 5 | Phase 3 intro |
| 7 | Krippendorff's Alpha | 800 | 5 | Phase 3 derivation |
| 8 | Experiments | 1,000 | 5 | Phase 4 figures A–D |
| 9 | A practical framework | 400 | 5 | Cross-cutting |
| 10 | Conclusion | 300 | 5 | Full arc |

**Total (indicative):** ~5,800 words before editing passes.

## Section → artefact map

1. **Introduction** — `docs/thesis.md`, LLM scenario from `docs/dataset-design.md`.
2. **Agreement as an estimator** — `notes/phase1-theory.md` (observed agreement).
3. **Chance agreement** — Phase 1 derivation + `figures/random_agreement_convergence.png` (once built).
4. **Kappa family** — `notes/phase2-kappa.md`.
5. **Limitations** — `notes/phase2-kappa.md` + `figures/kappa_paradox.png`.
6. **Disagreement framing** — `notes/phase3-alpha.md` (conceptual pivot).
7. **Alpha** — `notes/phase3-alpha.md`, `src/coincidence.py`, `src/distances.py`, `src/metrics.py`.
8. **Experiments** — `scripts/experiment_*.py`, `figures/exp_*.png`, `notebooks/04_experiments.ipynb`.
9. **Practical framework** — consolidated table / flowchart (new figure or ASCII in repo).
10. **Conclusion** — thesis restatement + ML evaluation takeaway.

## Narrative dependencies (DAG)

```text
§1 hook → §2 formal problem → §3 A_e and random baseline
    → §4–5 Kappa and paradox
    → §6–7 disagreement and Alpha
    → §8 empirical validation
    → §9–10 guidance and close
```

No section depends on material that will not exist by the end of the mapped phase; §8 waits until Phase 4 figures exist.
