# Checklist: derivações no papel (roadmap)

Lista consolidada das **fórmulas, derivações e provas** que o `roadmap-krippendorff-alpha-v3.md` associa às fases teóricas (Phases 1–3) e às issues de derivação. Use para estudar com papel e caneta antes de confiar só no código.

**Legenda:** Fase / issue do roadmap quando aplicável.

---

## Phase 1 — Fundamento estatístico (acordo observado vs acaso)

| # | O que fazer no papel | Roadmap / notas |
|---|----------------------|-----------------|
| 1.1 | Definir formalmente o problema de anotação (itens, raters, categorias). | Phase 1 intro; `docs/outline` |
| 1.2 | **Derivar** a fórmula de **acordo observado** \(A_o\) como fração de pares comparáveis que concordam (somatório de indicadores / número de pares). | Issue #5; `notes/phase1-theory.md` |
| 1.3 | **Derivar** o **acordo esperado sob independência** \(A_e = \sum_k \pi_k^2\) para duas etiquetas i.i.d. \(\sim \pi\). | Issue #5 |
| 1.4 | **Provar** \(A_e = 1/K\) quando \(\pi\) é uniforme em \(K\) classes. | Issue #5; roadmap Phase 1 |
| 1.5 | Calcular \(A_e\) para \(K=2\) uniforme \(\Rightarrow 0{,}50\) e \(K=3\) uniforme \(\Rightarrow 1/3\). | Issue #5 |
| 1.6 | Calcular \(A_e\) para \(\pi=(0{,}7,0{,}2,0{,}1)\). | Issue #5 |
| 1.7 | **Argumentar** por que anotadores “aleatórios” i.i.d. **não** levam \(A_o\to 0\): probabilidade de concordância num item = \(\sum_k \pi_k^2\). | Phase 1; `notes/phase1-theory.md` §4 |
| 1.8 | (Opcional) Forma alternativa com **reposição** no pool global: \(P(\text{agree})=\sum_k (n_k/N)^2\). | `notes/phase1-theory.md` §2 |

---

## Phase 2 — Família Kappa

| # | O que fazer no papel | Roadmap / notas |
|---|----------------------|-----------------|
| 2.1 | Escrever o **padrão geral** de correção por acaso: \(\kappa = (A_o - A_e)/(1-A_e)\) e interpretar \(\kappa\in\{1,0,<0\}\). | Issue #8; `notes/phase2-kappa.md` §1 |
| 2.2 | **Cohen:** definir \(A_o = \frac{1}{n}\sum_i \mathbf{1}\{X_{i1}=X_{i2}\}\). | Issue #8 |
| 2.3 | **Cohen:** definir \(p_{k\cdot}\), \(p_{\cdot k}\) e \(A_e = \sum_k p_{k\cdot} p_{\cdot k}\). | Issue #8 |
| 2.4 | **Cohen:** obter \(\kappa_C\) e refazer o exemplo \(2\times 2\) com \(A_o=2/3\), \(A_e=4/9\), \(\kappa=0{,}4\). | Issue #8; `notes/phase2-kappa.md` §2.4 |
| 2.5 | **Fleiss:** para contagens \(n_{ik}\) no item \(i\), derivar \(P_i = \frac{1}{m(m-1)}\sum_k n_{ik}(n_{ik}-1)\). | Issue #9; `notes/phase2-kappa.md` §3 |
| 2.6 | **Fleiss:** \(\bar P = \frac{1}{n}\sum_i P_i\), \(p_k = \frac{1}{nm}\sum_i n_{ik}\), \(\bar P_e=\sum_k p_k^2\), \(\kappa_F = (\bar P-\bar P_e)/(1-\bar P_e)\). | Issue #9 |
| 2.7 | Refazer o **exemplo mínimo** \(n=2\), \(m=3\), \(K=2\) com \(\kappa_F=0{,}25\). | `notes/phase2-kappa.md` §3.6 |
| 2.8 | **Paradoxo:** explicar por que prevalência extrema **infla** \(\bar P_e\) e pode **deflar** \(\kappa\) com \(A_o\) alto. | Issue #9; roadmap Phase 2 |

---

## Phase 3 — Alpha de Krippendorff

| # | O que fazer no papel | Roadmap / notas |
|---|----------------------|-----------------|
| 3.1 | Definir \(\alpha = 1 - D_o^*/D_e^*\) (discrepâncias observada vs esperada, pesadas por \(\mathbf{D}\)). | Issue #12; `notes/phase3-alpha.md` |
| 3.2 | Esboçar a construção da **matriz de coincidência** \(\mathbf{O}\) a partir de contagens por unidade (sem pares do mesmo rater; fator \(1/(m_i-1)\)). | Issue #12; Phase 3 tasks |
| 3.3 | **Dados incompletos:** como unidades com \(m_i<2\) não contribuem; como `NaN` exclui pares. | Phase 3 intro |
| 3.4 | Marginais \(n_c\), massa total \(N\), e **coincidência esperada** \(E_{cc'} = \frac{n_c n_{c'} - n_c\delta_{cc'}}{N-1}\). | `notes/phase3-alpha.md` §4 |
| 3.5 | Definir \(D_o^* = \sum_{c,c'} O_{cc'} D_{cc'}\) e \(D_e^* = \sum_{c,c'} E_{cc'} D_{cc'}\). | Issue #12 |
| 3.6 | **Provar / argumentar limites:** \(\alpha=1\) quando \(D_o^*=0\) (acordo perfeito no sentido nominal); \(\alpha=0\) quando \(D_o^*=D_e^*\); \(\alpha<0\) quando \(D_o^*>D_e^*\). | Issue #12; roadmap Phase 3 |
| 3.7 | Escrever \(\delta\) para **nominal** (0/1), **intervalo** \((c-c')^2\), **ratio** \(\bigl(\frac{c-c'}{c+c'}\bigr)^2\), e nota sobre **ordinal** (pesos com \(n_v\)). | `notes/phase3-alpha.md` §5 |
| 3.8 | Micro-exemplo: uma unidade, 3 raters, contagens \((2,1,0)\) — matriz local após ajuste diagonal (cf. `notes/phase3-alpha.md` §9). | `notes/phase3-alpha.md` §9 |
| 3.9 | **Equivalência discutível:** Cohen vs \(\alpha\) com 2 raters, nominal, dados completos — **modelos de acaso diferentes** se \(K>2\) (não exigir igualdade numérica; exigir argumento). | Issue #12; `notes/phase3-alpha.md` §8 |

---

## Artigo (Phase 5) — alinhamento

O ficheiro `article/krippendorff-alpha.md` deve **cobrir em prosa** os itens acima; use este checklist para marcar o que já consegue reconstituir **sem olhar para as notas**.

---

## Referência rápida

- Roadmap: `roadmap-krippendorff-alpha-v3.md` (secções Phase 1, 2, 3 e issues #5, #8, #9, #12).
- Notas: `notes/phase1-theory.md`, `notes/phase2-kappa.md`, `notes/phase3-alpha.md`.
