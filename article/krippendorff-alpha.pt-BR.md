---
title: "Quando o acordo é uma ilusão"
subtitle: "Fundamentos estatísticos do acordo entre anotadores — do acordo observado ao alpha de Krippendorff"
description: >
  Por que o acordo observado mistura sinal e acaso; como os kappas de Cohen e Fleiss
  corrigem o acaso mas falham com desbalanceamento e dados faltantes; como o alpha
  de Krippendorff reformula a confiabilidade via desacordo.
slug: krippendorff-alpha-pt
language: pt-BR
mathjax: true
source_repository: https://github.com/brunoramosmartins/krippendorff-alpha-article
canonical_article_en: krippendorff-alpha.md
keywords:
  - acordo entre anotadores
  - alpha de Krippendorff
  - kappa de Cohen
  - kappa de Fleiss
  - anotação
  - avaliação NLP
article_format:
  version: 1
  note: "Rascunho de revisão em PT-BR; o texto canónico em inglês é krippendorff-alpha.md."
---

# Quando o acordo é uma ilusão

*Fundamentos estatísticos do acordo entre anotadores — do acordo observado ao alpha de Krippendorff.*

> **Tese.** Um índice de acordo de 0,80 entre anotadores é com mais frequência evidência de ruído estruturado e prevalência do que de consenso verdadeiro quando o acordo por acaso não é contabilizado. Métricas como acordo bruto tratam sobreposição como sinal; o alpha de Krippendorff modela **desacordo** face a um referencial de aleatoriedade e generaliza-se a vários anotadores, dados faltantes e escalas de medição.

**Figuras.** Caminhos `../figures/<nome>.png` relativos a este ficheiro. Para exportar com `figures/` ao lado do Markdown, use `scripts/export_article_for_portfolio.py` (hoje exporta o `.md` em inglês por defeito; pode copiar este ficheiro manualmente ou estender o script).

**Anotações.** Use comentários HTML `<!-- ... -->` ou um ramo à parte para marcar ajustes desejados.

---

## 1. Introdução

Os seus anotadores concordaram em 80% dos itens. O painel fica verde; o modelo segue para produção. Esse número é **quase certamente enganador** como resumo de confiabilidade.

O **acordo observado** responde a uma pergunta estreita: que fração de **pares** de anotadores comparáveis recebeu a mesma etiqueta? **Não** responde: anotadores independentes com o mesmo comportamento marginal já concordariam com essa frequência? Quando a segunda resposta é sim, um valor alto na primeira diz pouco sobre leitura estável da tarefa. Pode refletir sobretudo **prevalência** (uma categoria domina) e **amostragem**, não consenso substantivo.

Isso pesa em **avaliação de LLMs**. Imagine um fluxo em que humanos e um modelo fine-tuned classificam projetos por marca. Negócio e jurídico querem um único número: “Concordamos?” Se só reportar a proporção de pares (humano, LLM) em acordo, um modelo que copia a classe majoritária pode parecer excelente sem julgamento cuidadoso. O mesmo armadilha aparece em codificação clínica, moderação de conteúdo e qualquer domínio com etiquetas enviesadas.

A linguística computacional usa coeficientes de acordo há décadas (Artstein e Poesio, 2008). A maturidade em torno de \(\kappa\) é desigual: leaderboards ainda misturam métricas **estilo acurácia** com tarefas **carregadas de prevalência**. Com **modelos foundation** como anotadores por defeito, a pergunta deixa de ser “batemos 80%?” e passa a ser se a automação **acompanha** a permutabilidade humana sob as mesmas instruções — o que empurra para coeficientes que toleram observação **parcial** e respeitam a **escala**.

Este artigo segue um arco:

1. Formalizar o acordo como **estimador** e separar **sinal** de **acaso** (Secções 2–3).
2. Apresentar \(\kappa\) de **Cohen** e **Fleiss** como correção padrão, e onde **falham** (4–5).
3. Reformular confiabilidade via **desacordo** e **matriz de coincidências**, até ao **alpha** de Krippendorff (6–7).
4. **Validar** com quatro simulações controladas (8).
5. Fechar com **guia prático** e limites honestos (9–10).

**Notação:** \(K\) categorias, \(n\) itens, \(m\) anotadores salvo indicação contrária. Matriz \((X_{ij})\), \(X_{ij}\in\{1,\ldots,K\}\) (o código pode usar \(0,\ldots,K-1\)). Julgamentos faltantes quando indicado.

---

## 2. O acordo como estimador

### 2.1 O problema da anotação

Temos um **estudo de confiabilidade**: vários anotadores atribuem uma de \(K\) categorias **nominais** a cada um de \(n\) itens. Sem padrão-ouro; o objetivo é quantificar com que consistência os anotadores **reproduzem** os mesmos juízos sobre o mesmo conteúdo — **confiabilidade** (replicabilidade do processo), não **validade** (se as categorias correspondem ao mundo).

Pode haver alta confiabilidade e baixa validade (todos aplicam o mesmo guia errado) e o inverso. Este texto trata **só** da primeira questão: se o **procedimento** de anotação é estável entre pessoas e, por extensão, se um sistema automatizado que as imita está alinhado num sentido **replicável**.

### 2.2 Acordo observado por pares

Fixe um item \(i\). Seja \(S_i\) o conjunto de pares não ordenados \((j,\ell)\), \(j<\ell\), em que **ambos** \(X_{ij}\) e \(X_{i\ell}\) estão observados. Indicador \(I_{ij\ell}=1\) se \(X_{ij}=X_{i\ell}\), senão \(0\).

O **acordo observado** é a fração de pares comparáveis em acordo:

\[
A_o
=
\frac{\displaystyle\sum_{i=1}^n \sum_{(j,\ell)\in S_i} I_{ij\ell}}
     {\displaystyle\sum_{i=1}^n |S_i|}.
\]

Assim \(A_o\) é uma **proporção amostral** de pares concordantes, agregada pelos itens.

**Exemplo (3 itens, 2 anotadores).** Itens 1 e 3 concordam; o 2 discorda. Então \(A_o=2/3\).

### 2.3 Acordo global com reposição

Alguns relatórios usam um resumo **global**: agregam todos os julgamentos, \(N\) o tamanho do pool, \(n_k\) a contagem da categoria \(k\), e imaginam **dois sorteios uniformes com reposição** do pool. A probabilidade de ambos serem \(k\) é \((n_k/N)^2\), logo

\[
P(\text{acordo}) = \sum_{k=1}^K \Bigl(\frac{n_k}{N}\Bigr)^2.
\]

Coincide com o \(A_o\) por pares dentro do item em desenhos simples e balanceados, mas **diverge** com \(m\) variável ou faltantes desiguais. O código do repositório implementa ambas as variantes.

### 2.4 O que \(A_o\) estima — e o que não estima

\(A_o\) é uma estatística **descritiva** clara. **Não** mede “quanto melhor que o acaso” age o painel. Dois anotadores independentes com distribuição \(\pi\) concordam com probabilidade \(\sum_k\pi_k^2\), muitas vezes bem acima de zero. Se o seu \(A_o\) reportado está perto disso, os dados são compatíveis com **independência**, não com verdade latente partilhada.

Como qualquer proporção, \(A_o\) tem **variabilidade amostral**; nos experimentos usa-se \(n=10{,}000\) em parte para curvas estáveis. Na prática, use intervalos de confiança e vistas desagregadas.

---

## 3. O problema do acordo por acaso

### 3.1 Acordo esperado sob independência

**Modelo.** Dois anotadores etiquetam **independentemente**, cada um com a mesma distribuição \(\pi=(\pi_1,\ldots,\pi_K)\). Então

\[
A_e
=
P(\text{ambos na mesma categoria})
=
\sum_{k=1}^K \pi_k^2.
\]

Se \(\pi_k=1/K\), \(A_e=1/K\). Para \(K=2\), “moedas” independentes concordam metade do tempo **sem** verdade partilhada.

**Exemplo desbalanceado.** \(\pi=(0{,}7,0{,}2,0{,}1)\):

\[
A_e = 0{,}7^2+0{,}2^2+0{,}1^2 = 0{,}54.
\]

| Cenário | \(A_e=\sum_k\pi_k^2\) |
|---------|------------------------|
| \(K=2\), uniforme | \(0{,}50\) |
| \(K=3\), uniforme | \(\approx 0{,}333\) |
| \(K=3\), \(\pi=(0{,}7,0{,}2,0{,}1)\) | \(0{,}54\) |

### 3.2 Anotadores aleatórios: por que \(A_o\not\to 0\)

Se cada célula da matriz é **independente** \(\sim\pi\) (sem verdade latente por item), dois julgamentos no mesmo item concordam com probabilidade **exatamente** \(\sum_k\pi_k^2>0\).

**“Aleatório” não é “acordo zero”**; é acordo ao nível de **acaso** das marginais.

### 3.3 Verificação empírica

A Fase 1 do código simula anotadores i.i.d. puramente aleatórios; o \(A_o\) empírico concentra-se em \(\sum_k\pi_k^2\).

![Convergência simulada do acordo observado ao referencial de independência.](../figures/random_agreement_convergence.png)

**Figura 1.** \(A_o\) empírico aproxima \(A_e=\sum_k\pi_k^2\) quando \(n\) cresce.

---

## 4. A família Kappa

### 4.1 Padrão de correção

\[
\kappa = \frac{A_o-A_e}{1-A_e}.
\]

Se \(A_e<1\): \(\kappa=1\) se \(A_o=1\); \(\kappa=0\) se \(A_o=A_e\); \(\kappa<0\) se abaixo do referencial.

### 4.2 Kappa de Cohen (dois anotadores fixos)

\[
A_o = \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{X_{i1}=X_{i2}\}.
\]

Com marginais empíricas \(p_{k\cdot}\), \(p_{\cdot k}\):

\[
A_e = \sum_{k=1}^K p_{k\cdot}\,p_{\cdot k},
\qquad
\kappa_C=\frac{A_o-A_e}{1-A_e}.
\]

### 4.3 Kappa de Fleiss

\(P_i = \frac{1}{m(m-1)}\sum_k n_{ik}(n_{ik}-1)\), \(\bar P=\frac1n\sum_i P_i\), \(p_k=\frac{1}{nm}\sum_i n_{ik}\), \(\bar P_e=\sum_k p_k^2\), \(\kappa_F=(\bar P-\bar P_e)/(1-\bar P_e)\).

### 4.4 Por que Kappa ajuda

Reexprime sobreposição face a um referencial de acaso **estimado dos dados**. Quando \(A_o\) é alto só porque \(\bar P_e\) é alto, \(\kappa_F\) aproxima-se de zero.

---

## 5. Limitações do Kappa

### 5.1 Paradoxo do Kappa

Prevalência extrema infla \(\sum_k p_k^2\); \(A_o\) bruto pode ser alto com \(\kappa\) baixo — o coeficiente está a fazer o trabalho dele.

![Kappa de Fleiss vs desbalanceamento (paradoxo).](../figures/kappa_paradox.png)

**Figura 2.** \(\kappa_F\) pode cair com \(A_o\) ainda “alto” em escalas ingénuas.

### 5.2 Restrições estruturais

Cohen: exatamente **dois** anotadores; Fleiss: grelha **completa** tipicamente; ambos **nominais** na forma básica.

### 5.3 Por que \(\alpha\)

Precisamos de desacordo comparável ao acaso, **dados faltantes** e **distâncias** entre valores — o alpha de Krippendorff cobre isso num único esqueleto.

---

## 6. Do acordo ao desacordo

Contagens de **acertos** vs **distâncias** entre etiquetas. Matriz de confiabilidade (unidades \(\times\) anotadores); **matriz de coincidências** \(\mathbf{O}\); esperada \(\mathbf{E}\) sob reemparelhamento aleatório que preserva marginais; **discrepância** ponderada por \(\mathbf{D}\).

---

## 7. Alpha de Krippendorff

\[
D_o^\* = \sum_{c,c'} O_{cc'}D_{cc'},
\quad
D_e^\* = \sum_{c,c'} E_{cc'}D_{cc'},
\quad
\alpha = 1-\frac{D_o^\*}{D_e^\*}.
\]

\[
E_{cc'} = \frac{n_c n_{c'}-n_c\delta_{cc'}}{N-1}.
\]

**Limites:** \(\alpha=1\) se \(D_o^\*=0\) (caso nominal perfeito); \(\alpha=0\) se \(D_o^\*=D_e^\*\); \(\alpha<0\) se \(D_o^\*>D_e^\*\).

\[
\alpha = \frac{D_e^\*-D_o^\*}{D_e^\*}.
\]

Relação com Cohen: modelos de acaso diferentes se \(K>2\) — não espere igualdade numérica.

**Distâncias \(\delta\):** nominal — \(0\) se \(c=c'\), senão \(1\); intervalo — \((c-c')^2\); ratio — \(\bigl(\frac{c-c'}{c+c'}\bigr)^2\) (convenção se \(c+c'=0\)); ordinal — usa domínio ordenado e massas \(n_v\) (Krippendorff 2004, cap. 11).

---

## 8. Experimentos

Quatro simulações com **sementes fixas** (`make experiments` ou `scripts/experiment_*.py`).

### 8.1 A — Anotadores aleatórios

\(A_o\approx 1/K\); \(\kappa_F,\alpha\approx 0\).

![Experimento A.](../figures/exp_a_random_metrics.png)

### 8.2 B — Armadilha do alto acordo

\(A_o\) alto com \(\alpha\) baixo sob skew + baixo ruído.

![Experimento B.](../figures/exp_b_agreement_trap_heatmap.png)

### 8.3 C — LLM vs humanos (sintético)

Sensibilidade ao ruído do “LLM”.

![Experimento C.](../figures/exp_c_llm_vs_humans.png)

### 8.4 D — Dados faltantes

\(\alpha\) estável; Fleiss vira `NaN` com células faltantes.

![Experimento D.](../figures/exp_d_missing_robustness.png)

---

## 9. Quadro prático

### 9.1 Quando usar cada métrica

- Reporte \(A_o\) como resumo transparente sensível à prevalência, **sempre** com um coeficiente consciente do acaso.
- **Kappa de Cohen** com exatamente **dois** anotadores fixos, dados **completos**, categorias **nominais** (ou kappa ponderado).
- **Kappa de Fleiss** quando cada item tem o **mesmo** \(m\) e a matriz está **completa**.
- **Alpha de Krippendorff** com julgamentos **faltantes**, número **variável** de anotadores por unidade, ou distâncias **ordinal/intervalo/ratio** num só quadro.

### 9.2 Fluxograma (ASCII)

```text
                    Início: estudo de confiabilidade
                              |
              Há faltantes ou m_i varia entre unidades?
                     /                              \
                   Sim                             Não
                    |                                |
         Preferir alpha de Krippendorff      Exatamente 2 anotadores fixos?
         (nível: nominal / ordinal /              /            \
          intervalo / ratio)                      Sim            Não
            |                                    |              |
            |                               Kappa de Cohen   Mesmo m, grelha completa?
            |                                                      /        \
            |                                                    Sim        Não
            |                                            Kappa de Fleiss  -> alpha
            v
     Reportar alpha com domínio de valores e distância claros;
     opcionalmente também A_o e um Kappa quando válido.
```

### 9.3 Limiares (com ressalvas)

Não há corte universal que substitua julgamento de domínio. Regras tipo Landis–Koch não foram feitas para corpora NLP modernos enviesados. Trate qualquer limiar único como **heurística**: intervalos de confiança, sensibilidade à prevalência, análise de erros nos itens em desacordo. Se \(\alpha \ll 0\) com \(A_o\) alto, investigue **prevalência e acaso** antes de celebrar confiabilidade.

### 9.4 Checklist de relatório

1. Qual definição de acordo (pares dentro do item vs pool global).
2. \(A_o\) (ou equivalente) **e** pelo menos um coeficiente consciente do acaso adequado ao desenho.
3. Declarar \(K\), frequências de classe aproximadas, taxa de faltantes.
4. Para \(\alpha\): nível de medição e **domínio de valores**.
5. Arquivar **código e sementes** para refazer figuras e tabelas.

### 9.5 O que coeficientes não consertam

\(\alpha\) não substitui **regras de codificação**, **treino** ou **piloto**. Desacordo concentrado em poucos itens ambíguos pede **revisão do guia**, não só mais dados. Acordo enviesado (todos erram da mesma forma) não é detetado como problema de validade. **Anotadores não independentes** (chat, cópia, partilha de outputs de modelo) violam pressupostos; a solução é **protocolo**, não álgebra posterior.

---

## 10. Conclusão

Acordo alto é fácil de fabricar com marginais enviesadas. Kappa corrige parte do problema; alpha reformula via desacordo e lida melhor com incompletude. Para ML: nunca um único percentual sem referencial de acaso; prefira o coeficiente que corresponde ao desenho amostral e à escala.

---

## Nota de revisão

Figuras 1–6 na mesma ordem que a versão EN. Para o site MkDocs deste repositório: `mkdocs build` (o include `_article_include.md` usa só o `.md` em inglês). Para estudar derivações no papel, veja `docs/math-derivations-checklist.md`.

---

## Referências

(As mesmas da versão em inglês.)

1. Cohen (1960); 2. Fleiss (1971); 3. Feinstein & Cicchetti (1990); 4. Krippendorff (2004); 5. Artstein & Poesio (2008); 6. Landis & Koch (1977).

---

*Rascunho de revisão PT-BR — alinhar com `article/krippendorff-alpha.md` antes da publicação final.*
