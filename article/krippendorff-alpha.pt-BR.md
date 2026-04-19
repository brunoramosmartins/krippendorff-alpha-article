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
  note: "Versão em PT-BR; o texto canónico em inglês é krippendorff-alpha.md."
---

# Quando o acordo é uma ilusão

*Fundamentos estatísticos do acordo entre anotadores — do acordo observado ao alpha de Krippendorff.*

> **Tese.** Um índice de acordo de 0,80 pode ser enganador quando o acordo por acaso não é explicitamente modelado. Sob desbalanceamento de classes e marginais independentes, sobreposição observada alta emerge sem compreensão partilhada. O alpha de Krippendorff aborda isso ao modelar **desacordo** face a um referencial de aleatoriedade e generalizar-se a vários anotadores, dados faltantes e escalas de medição.

---

## 1. Introdução

Você conduz um exercício de anotação com um pequeno painel de analistas. A tarefa é simples: classificar cada item de trabalho numa de algumas categorias predefinidas com base na descrição. Em paralelo, você solicita a um LLM que faça a mesma classificação. A expectativa é direta — humanos fornecem a referência, o modelo os aproxima.

O que acontece é menos confortável. Os anotadores não concordam consistentemente entre si. O mesmo item é mapeado para categorias diferentes dependendo de quem o lê. Enquanto isso, o LLM — dado um prompt fixo — produz saídas estáveis e repetíveis. Nesse ponto surge uma pergunta natural: se humanos não concordam entre si, o que exatamente estamos pedindo ao modelo que replique?

Encontrei esse cenário pela primeira vez num projeto de trabalho onde a conclusão pragmática foi que o LLM pode ser preferível justamente por ser consistente, mesmo que humanos não o sejam. Essa conclusão é operacionalmente atraente — mas estatisticamente frágil.

Um acordo observado alto, seja entre humanos ou entre humanos e um modelo, não indica necessariamente compreensão partilhada. Pode refletir **prevalência** (uma categoria domina), viés nas distribuições marginais, ou aleatoriedade estruturada. Sob distribuições de classes enviesadas, anotadores independentes que não partilham sinal latente podem ainda concordar em mais de metade dos itens — e um modelo que sombra a classe majoritária pode parecer excelente sem julgamento cuidadoso.

A linguística computacional usa coeficientes de acordo desde a era da anotação de corpora (Artstein e Poesio, 2008), mas a maturidade em torno de $\kappa$ permanece desigual: leaderboards ainda misturam resumos **estilo acurácia** com tarefas **carregadas de prevalência**. Com **modelos foundation** como anotadores por defeito — anotadores determinísticos condicionados a prompts — a pergunta deixa de ser “batemos 80%?” e passa a ser se a automação **acompanha** a permutabilidade humana sob as mesmas instruções. Isso empurra para coeficientes que toleram observação **parcial** e respeitam a **escala**.

Este artigo segue um arco:

1. Formalizar o acordo como **estimador** e separar **sinal** de **acaso** (Secções 2–3).
2. Apresentar $\kappa$ de **Cohen** e **Fleiss** como correção padrão, e onde **falham** (Secções 4–5).
3. Reformular confiabilidade via **desacordo** e **matriz de coincidências**, até ao $\alpha$ de **Krippendorff** (Secções 6–7).
4. **Validar** com quatro simulações controladas (Secção 8).
5. Fechar com **guia prático** e limites honestos (Secções 9–10).

**Notação.** $K$ categorias, $n$ itens (unidades), $m$ anotadores salvo indicação contrária. A matriz de anotação é $(X_{ij})$ com $X_{ij} \in \{1,\ldots,K\}$. Julgamentos faltantes quando indicado.

---

## 2. O acordo como estimador

### 2.1 O problema da anotação

Consideramos um estudo de confiabilidade em que múltiplos anotadores atribuem uma de $K$ categorias nominais a cada um de $n$ itens. Este setup parece enganosamente simples. Na prática, corresponde frequentemente a tarefas como categorizar itens de trabalho por descrições textuais, atribuir etiquetas em pipelines de NLP, ou avaliar saídas de modelos face ao julgamento humano.

Crucialmente, **nenhuma verdade de referência é diretamente observada**. O que observamos é uma coleção de julgamentos humanos, cada um moldado por interpretação, ambiguidade e viés individual. Não estamos a medir acurácia — estamos a medir a **consistência** de um processo de medição sob aplicação repetida.

No exemplo motivador da introdução, anotadores diferentes discordavam frequentemente sobre o mesmo item — não por descuido, mas porque a tarefa permitia múltiplas interpretações plausíveis. O LLM, por contraste, impunha uma única interpretação via prompt fixo. Isso destaca o objeto central de estudo: **confiabilidade não diz respeito a correção, mas a se o processo é reproduzível entre agentes**.

A distinção entre **confiabilidade** (replicabilidade do procedimento) e **validade** (se as categorias correspondem ao mundo) é fundamental. Pode haver alta confiabilidade e baixa validade — todos aplicam o mesmo guia errado — e o inverso. Este texto trata **apenas** de confiabilidade. Afirmações sobre verdade de referência ou utilidade a jusante requerem evidência adicional.

Se anotadores discordam, o problema pode não ser que o acordo é baixo — pode ser que a tarefa não define uma única verdade latente.

Formalmente, representamos os dados como uma matriz de anotação $(X_{ij})$, onde $X_{ij} \in \{1,\ldots,K\}$ é a etiqueta atribuída pelo anotador $j$ ao item $i$. Entradas faltantes são permitidas, refletindo cenários reais de anotação onde nem todo anotador etiqueta todo item.

### 2.2 Acordo observado por pares

Fixe um item $i$. Seja $S_i$ o conjunto de pares não ordenados $(j,\ell)$, $j<\ell$, em que **ambos** $X_{ij}$ e $X_{i\ell}$ estão observados. Indicador $I_{ij\ell}=1$ se $X_{ij}=X_{i\ell}$, senão $0$.

O **acordo observado** é a fração de pares comparáveis em acordo:

$$
A_o = \frac{\displaystyle\sum_{i=1}^n \sum_{(j,\ell)\in S_i} I_{ij\ell}}{\displaystyle\sum_{i=1}^n |S_i|}.
$$

Assim $A_o$ é uma **proporção amostral** de pares concordantes, agregada pelos itens.

**Exemplo (3 itens, 2 anotadores).** Itens 1 e 3 concordam; o 2 discorda. Então $A_o=2/3$.

### 2.3 Acordo global com reposição

Alguns relatórios usam um resumo **global**: agregam todos os julgamentos, $N$ o tamanho do pool, $n_k$ a contagem da categoria $k$, e imaginam **dois sorteios uniformes com reposição** do pool. A probabilidade de ambos serem $k$ é $(n_k/N)^2$, logo

$$
P(\text{acordo}) = \sum_{k=1}^K \Bigl(\frac{n_k}{N}\Bigr)^2.
$$

Coincide com o $A_o$ por pares dentro do item em desenhos simples e balanceados, mas **diverge** com $m$ variável ou faltantes desiguais. O código do repositório implementa ambas as variantes.

### 2.4 O que $A_o$ estima — e o que não estima

$A_o$ é uma estatística **descritiva** clara. **Não** mede “quanto melhor que o acaso” age o painel. Dois anotadores independentes com distribuição $\pi$ concordam com probabilidade $\sum_k\pi_k^2$, muitas vezes bem acima de zero. Se o seu $A_o$ reportado está perto disso, os dados são compatíveis com **independência**, não com verdade latente partilhada.

Como qualquer proporção, $A_o$ tem **variabilidade amostral**; nos experimentos usa-se $n = 10\,000$ em parte para curvas estáveis. Na prática, complemente estimativas pontuais com **intervalos de confiança** (bootstrap sobre itens é comum) e com vistas **desagregadas** (acordo por estrato, matrizes de confusão).

Logo, o enquadramento: trate $A_o$ como um **estimador** de sobreposição sob o seu esquema amostral, e pergunte sempre contra que **referencial** ele deveria ser comparado.

### 2.5 Dois processos geradores de dados

Os experimentos deste artigo apoiam-se em dois modelos generativos distintos. Confundi-los leva a interpretações erradas, por isso enunciamo-los explicitamente.

**Modelo 1 — Etiquetagem puramente aleatória (sem sinal).** Cada anotador sorteia $X_{ij} \sim \pi$ independentemente. Não há verdade latente por item; o acordo surge **apenas** de marginais partilhadas. Este modelo é a hipótese nula para as Secções 3 e 8.1.

**Modelo 2 — Anotação ruidosa em torno de verdade latente.** Cada item $i$ tem uma etiqueta verdadeira latente $Y_i \sim \pi$. Cada anotador observa $Y_i$ com ruído:

$$P(X_{ij} = k \mid Y_i) = \begin{cases} 1 - \varepsilon & \text{se } k = Y_i, \\ \varepsilon / (K-1) & \text{caso contrário.} \end{cases}$$

Aqui $\varepsilon \in [0, 1]$ controla o ruído de anotação. Com $\varepsilon = 0$, todos os anotadores concordam perfeitamente; com $\varepsilon = (K-1)/K$, o Modelo 2 reduz-se ao Modelo 1. Os Experimentos B, C e D usam este modelo com $\varepsilon$ e $\pi$ variáveis.

A distinção importa: sob o Modelo 1, **qualquer** acordo observado é puro acaso. Sob o Modelo 2, o acordo decompõe-se numa componente de **sinal** (verdade latente partilhada) e numa componente de **acaso** (sobreposição marginal). Os coeficientes deste artigo destinam-se a remover a componente de acaso — mas pressupõem que o ruído é **simétrico e independente por item**. Erros estruturados (e.g. um LLM que sistematicamente sobreprevê a classe majoritária) violam este pressuposto e requerem ferramentas diagnósticas adicionais além do que $\alpha$ sozinho fornece (ver Secção 9.5).

---

## 3. O problema do acordo por acaso

### 3.1 Acordo esperado sob independência

**Modelo.** Dois anotadores etiquetam **independentemente**, cada um com a mesma distribuição $\pi=(\pi_1,\ldots,\pi_K)$, $\pi_k \ge 0$, $\sum_k \pi_k = 1$ (Modelo 1 da Secção 2.5). Então

$$
A_e = P(\text{ambos na mesma categoria}) = \sum_{k=1}^K \pi_k^2.
$$

Se $\pi_k=1/K$, $A_e=1/K$. Para $K=2$, “moedas” independentes concordam metade do tempo **sem** verdade partilhada.

**Exemplo desbalanceado.** $\pi=(0{,}7,0{,}2,0{,}1)$:

$$
A_e = 0{,}7^2+0{,}2^2+0{,}1^2 = 0{,}54.
$$

| Cenário | $A_e=\sum_k\pi_k^2$ |
|---------|------------------------|
| $K=2$, uniforme | $0{,}50$ |
| $K=3$, uniforme | $\approx 0{,}333$ |
| $K=3$, $\pi=(0{,}7,0{,}2,0{,}1)$ | $0{,}54$ |

### 3.2 Anotadores aleatórios: por que $A_o\not\to 0$

Se cada célula da matriz é **independente** $\sim\pi$ (sem verdade latente por item), dois julgamentos no mesmo item concordam com probabilidade **exatamente** $\sum_k\pi_k^2>0$.

**“Aleatório” não é “acordo zero”**; é acordo ao nível de **acaso** das marginais.

### 3.3 Verificação empírica: convergência para $\sum_k\pi_k^2$

O código do repositório simula anotadores do Modelo 1 e acompanha $A_o$ à medida que o número de itens cresce. A simulação confirma a teoria: o acordo empírico concentra-se em $\sum_k\pi_k^2$. Se dados reais se comportassem assim, o processo de anotação não carregaria nenhum sinal específico por item. Estudos reais normalmente violam essa premissa — razão pela qual precisamos de coeficientes que separem acordo estruturado de sobreposição movida pela prevalência.

![Convergência simulada do acordo observado ao referencial de independência sob etiquetagem aleatória i.i.d.](../figures/random_agreement_convergence.png)

**Figura 1.** Anotadores aleatórios i.i.d.: o acordo observado empírico aproxima o acordo esperado teórico $A_e=\sum_k\pi_k^2$ à medida que o tamanho amostral cresce.

A implicação é clara: $A_o$ sozinho não consegue distinguir entre consenso genuíno e sobreposição movida pela prevalência. Precisamos de uma correção que **subtraia** o referencial de acaso antes de interpretar o que resta. É exatamente isso que a família Kappa oferece.

---

## 4. A família Kappa

### 4.1 Padrão de correção

$$
\kappa = \frac{A_o-A_e}{1-A_e}.
$$

Se $A_e<1$: $\kappa=1$ se $A_o=1$; $\kappa=0$ se $A_o=A_e$; $\kappa<0$ se abaixo do referencial.

### 4.2 Kappa de Cohen (dois anotadores fixos)

$$
A_o = \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{X_{i1}=X_{i2}\}.
$$

Com marginais empíricas $p_{k\cdot}$, $p_{\cdot k}$:

$$
A_e = \sum_{k=1}^K p_{k\cdot}\,p_{\cdot k},
\qquad
\kappa_C=\frac{A_o-A_e}{1-A_e}.
$$

### 4.3 Kappa de Fleiss

$P_i = \frac{1}{m(m-1)}\sum_k n_{ik}(n_{ik}-1)$, $\bar P=\frac1n\sum_i P_i$, $p_k=\frac{1}{nm}\sum_i n_{ik}$, $\bar P_e=\sum_k p_k^2$, $\kappa_F=(\bar P-\bar P_e)/(1-\bar P_e)$.

### 4.4 Por que Kappa ajuda

Reexprime sobreposição face a um referencial de acaso **estimado dos dados**. Quando $A_o$ é alto só porque $\bar P_e$ é alto, $\kappa_F$ aproxima-se de zero.

---

## 5. Limitações do Kappa

### 5.1 Paradoxo do Kappa

Prevalência extrema infla $\sum_k p_k^2$; $A_o$ bruto pode ser alto com $\kappa$ baixo — o coeficiente está a fazer o trabalho dele.

![Kappa de Fleiss vs desbalanceamento (paradoxo).](../figures/kappa_paradox.png)

**Figura 2.** $\kappa_F$ pode cair com $A_o$ ainda “alto” em escalas ingénuas. Note a escala Y mais estreita no painel direito.

### 5.2 Restrições estruturais

Cohen: exatamente **dois** anotadores; Fleiss: grelha **completa** tipicamente; ambos **nominais** na forma básica.

### 5.3 Por que $\alpha$

Precisamos de desacordo comparável ao acaso, **dados faltantes** e **distâncias** entre valores — o alpha de Krippendorff cobre isso num único esqueleto.

---

## 6. Do acordo ao desacordo

### 6.1 Por que mudar a perspetiva

Acordo bruto e os numeradores do Kappa contam **acertos**: quantos pares deram a mesma etiqueta? A visão dual conta **desacertos** ponderados pela distância entre as categorias atribuídas. Para dados nominais, a distância é binária — igual ou diferente. Para dados de intervalo, diferenças ao quadrado penalizam erros grandes mais que erros pequenos. Essa visão dual é mais geral: acomoda naturalmente **escalas de medição** além da nominal e conduz a uma fórmula única que unifica todos os casos.

### 6.2 A matriz de confiabilidade

A construção de Krippendorff parte de uma **matriz de confiabilidade**: linhas são **unidades** (itens), colunas são **anotadores**, entradas são valores (categorias ou pontuações numéricas). Entradas faltantes são **excluídas** de todos os cálculos; só pares de anotadores distintos na mesma unidade contribuem informação. Uma unidade com uma única etiqueta observada não forma par e é silenciosamente descartada — sem imputação, sem eliminação de linhas.

### 6.3 Construção da matriz de coincidências — exemplo trabalhado

Considere três itens avaliados por três anotadores num domínio binário $\{A, B\}$:

| Unidade | Anotador 1 | Anotador 2 | Anotador 3 |
|---------|------------|------------|------------|
| 1       | A          | A          | B          |
| 2       | B          | B          | —          |
| 3       | A          | A          | A          |

**Passo 1 — vetores de contagem.** Para cada unidade, contar quantas vezes cada valor aparece entre as avaliações **observadas**:

- Unidade 1: $\mathbf{n}_1 = (2, 1)$, com $m_1 = 3$ anotadores.
- Unidade 2: $\mathbf{n}_2 = (0, 2)$, com $m_2 = 2$ anotadores (Anotador 3 faltante).
- Unidade 3: $\mathbf{n}_3 = (3, 0)$, com $m_3 = 3$ anotadores.

**Passo 2 — contribuições locais de coincidência.** Para cada unidade, a contribuição à matriz de coincidências é proporcional à frequência com que pares de anotadores **distintos** atribuíram cada combinação de valores. Para uma unidade com vetor de contagem $\mathbf{n}_i$, a entrada fora da diagonal $(c, c')$ recebe $n_{ic} \cdot n_{ic'}/(m_i - 1)$, e a entrada diagonal $(c, c)$ recebe $n_{ic}(n_{ic} - 1)/(m_i - 1)$. O denominador $m_i - 1$ garante que cada unidade contribui **uma unidade de massa total** independentemente do número de anotadores.

Aplicando ao exemplo:

- **Unidade 1** ($m_1 = 3$): diagonal $(A,A) = 2 \cdot 1 / 2 = 1$; diagonal $(B,B) = 1 \cdot 0 / 2 = 0$; fora da diagonal $(A,B) = 2 \cdot 1 / 2 = 1$.
- **Unidade 2** ($m_2 = 2$): diagonal $(B,B) = 2 \cdot 1 / 1 = 2$; restante zero.
- **Unidade 3** ($m_3 = 3$): diagonal $(A,A) = 3 \cdot 2 / 2 = 3$; restante zero.

**Passo 3 — somar para obter $\mathbf{O}$.**

|       | A   | B   |
|-------|-----|-----|
| **A** | 4   | 1   |
| **B** | 1   | 2   |

As marginais são $n_A = 5$, $n_B = 3$, e a massa total emparelhável é $N = 8$.

**Passo 4 — coincidência esperada $\mathbf{E}$.** Sob a hipótese nula de reemparelhamento aleatório preservando marginais, $E_{cc'} = (n_c n_{c'} - n_c \delta_{cc'}) / (N - 1)$. Por exemplo, $E_{AB} = (5 \cdot 3) / 7 \approx 2{,}14$ e $E_{AA} = (5 \cdot 4) / 7 \approx 2{,}86$.

### 6.4 De coincidência a desacordo

O **desacordo observado** é a soma ponderada $D_o^* = \sum_{c,c'} O_{cc'} D_{cc'}$, onde $D_{cc'} = \delta(c, c')$ codifica a distância. O **desacordo esperado** $D_e^*$ usa $\mathbf{E}$ na mesma fórmula. A razão $D_o^* / D_e^*$ indica como o padrão real de desacordos do painel se compara ao que o emparelhamento aleatório produziria.

A mudança conceitual é simples: em vez de "com que frequência concordamos?", perguntar **"quão mais longe estamos do que o emparelhamento aleatório preveria?"** Acordo é o caso especial em que a distância é zero na diagonal e um fora dela ($\delta$ nominal). A Secção 7 monta essas peças na fórmula completa de $\alpha$.

---

## 7. Alpha de Krippendorff

$$
D_o^* = \sum_{c,c'} O_{cc'}D_{cc'},
\quad
D_e^* = \sum_{c,c'} E_{cc'}D_{cc'},
\quad
\alpha = 1-\frac{D_o^*}{D_e^*}.
$$

$$
E_{cc'} = \frac{n_c n_{c'}-n_c\delta_{cc'}}{N-1}.
$$

**Limites:** $\alpha=1$ se $D_o^*=0$ (caso nominal perfeito); $\alpha=0$ se $D_o^*=D_e^*$; $\alpha<0$ se $D_o^*>D_e^*$.

$$
\alpha = \frac{D_e^*-D_o^*}{D_e^*}.
$$

Relação com Cohen: modelos de acaso diferentes se $K>2$ — não espere igualdade numérica.

**Distâncias $\delta$:** nominal — $0$ se $c=c'$, senão $1$; intervalo — $(c-c')^2$; ratio — $\bigl(\frac{c-c'}{c+c'}\bigr)^2$ (convenção se $c+c'=0$); ordinal — usa domínio ordenado e massas $n_v$ (Krippendorff 2004, cap. 11).

---

## 8. Experimentos

Quatro simulações (Fase 4 do código) isolam propriedades de $A_o$, $\kappa_F$ e $\alpha$. Todas usam **sementes fixas** e são reproduzíveis via `make experiments` ou os scripts individuais `scripts/experiment_*.py`.

São **sintéticas** de propósito: alvos analíticos existem para etiquetagem aleatória, e varrimentos sobre ruído e desbalanceamento são baratos de repetir. Traduzir as lições qualitativas para uma API de LLM real requer camadas adicionais (calibração, prompts adversariais, fatores humanos) que ficam fora deste texto — mas as **armadilhas algébricas** do acordo bruto e os **limites estruturais** de Fleiss permanecem.

### 8.1 A — Anotadores aleatórios (teste de sanidade)

**Setup.** Modelo 1 (etiquetagem puramente aleatória), $\pi$ uniforme, varrimento de $K \in \{2,\ldots,10\}$ com $n = 10\,000$, $m=5$.

**Expectativa.** $A_o \approx 1/K$; $\kappa_F \approx 0$; $\alpha \approx 0$.

**Resultado.** As curvas empíricas correspondem à teoria dentro de tolerância apertada. Este é um **teste de sanidade**, não uma descoberta: coeficientes corrigidos pelo acaso anulam-se quando não há estrutura partilhada. A sobreposição quase perfeita entre a curva de $A_o$ e $1/K$ é uma propriedade do modelo, não um bug — simulamos exatamente o cenário analítico.

![Experimento A: $A_o$, $\kappa_F$ e $\alpha$ para anotadores aleatórios i.i.d. ao longo de $K$.](../figures/exp_a_random_metrics.png)

**Figura 3.** Anotadores aleatórios: acordo observado segue $1/K$; $\kappa_F$ e $\alpha$ seguem zero.

### 8.2 B — Armadilha do alto acordo

**Setup.** Modelo 2 (verdade ruidosa) com forte enviesamento de classe e baixo $\varepsilon$ num painel de cinco anotadores. Grelha sobre desbalanceamento e ruído.

**Definição formal.** A **armadilha do acordo** é a região do espaço de parâmetros onde o acordo bruto é confortavelmente alto mas a confiabilidade corrigida pelo acaso é baixa:

$$\mathcal{T} = \{(\pi, \varepsilon) : A_o(\pi, \varepsilon) > 0.80 \;\wedge\; \alpha(\pi, \varepsilon) < 0.40\}.$$

Esta região existe porque $A_e = \sum_k \pi_k^2$ cresce com o desbalanceamento de classes. Quando $\pi_{\text{major}}$ se aproxima de 1, mesmo anotadores ruidosos concordam na classe dominante a maior parte do tempo, inflacionando $A_o$ sem sinal genuíno ao nível do item.

**Resultado.** Heatmaps de $A_o$ e $\alpha$ mostram uma cunha visível que ocupa $\mathcal{T}$. Um exemplo concreto: com $\pi = (0{,}85,\; 0{,}10,\; 0{,}05)$ e $\varepsilon = 0{,}05$, obtém-se $A_o \approx 0{,}84$ enquanto $\alpha \approx 0{,}35$. Stakeholders veem uma percentagem bruta confortável; o coeficiente corrigido pelo acaso revela que o painel é apenas modestamente melhor que um referencial aleatório consciente da prevalência. A lição operacional: coloque **ambas** as vistas na mesma tabela por defeito.

![Experimento B: heatmaps de $\alpha$ e $A_o$ sobre desbalanceamento e ruído; caixas vermelhas marcam a região de armadilha.](../figures/exp_b_agreement_trap_heatmap.png)

**Figura 4.** Armadilha do acordo: sobreposição bruta alta coexiste com confiabilidade corrigida baixa sob enviesamento + baixo ruído.

### 8.3 C — LLM vs humanos (sintético)

**Setup.** Três anotadores “humanos” com ruído $\varepsilon = 0{,}10$ e um anotador “LLM” com $\varepsilon = 0{,}15$ numa tarefa de três classes; sensibilidade sobre ruído do LLM em $[0, 0{,}5]$.

**Resultado.** $\alpha$ acompanha a qualidade do painel; adicionar um anotador mais ruidoso reduz $\alpha$ relativamente ao sub-painel só de humanos. A curva de sensibilidade torna a relação dose-resposta visível.

**Ressalva importante.** Este experimento modela o erro do LLM como **ruído i.i.d. simétrico** (Modelo 2). Na prática, erros de LLMs são **estruturados**: um modelo pode sistematicamente sobreprevê a classe majoritária, exibir viés dependente do prompt, ou falhar em padrões semânticos específicos. Ruído simétrico é um referencial útil, mas a avaliação real de LLMs requer diagnósticos adicionais — matrizes de confusão estratificadas por classe, sondas adversariais, e análise de **onde** (não apenas com que frequência) ocorrem os desacordos. Um cenário com **viés direcional** (e.g. o LLM sempre prevê a classe majoritária quando incerto) provavelmente mostraria $\alpha$ a degradar mais rapidamente do que o caso simétrico prevê.

![Experimento C: sensibilidade de $\alpha$ ao ruído sintético do LLM; só humanos vs painel completo.](../figures/exp_c_llm_vs_humans.png)

**Figura 5.** LLM sintético vs humanos: $\alpha$ responde ao ruído injetado do LLM; comparar só humanos com o painel completo.

### 8.4 D — Dados faltantes

**Setup.** Painel balanceado fixo com ruído moderado; injetar faltantes MCAR de 0% a 50%.

**Expectativa.** A formulação de Fleiss (matriz completa) torna-se **indefinida** ou `NaN` com entradas faltantes; $\alpha$ **degrada graciosamente** porque é definido sobre unidades emparelháveis.

**Resultado.** $\alpha$ permanece estável perto do seu valor com dados completos enquanto Fleiss desaparece — uma razão prática para preferir $\alpha$ em regimes de anotação esparsa. A **vantagem de retenção por pares** é central: $\alpha$ usa toda a informação de pares disponível por unidade, enquanto Fleiss requer a grelha completa. Reduzir a casos completos introduz **viés de caso completo** quando a falta de dados correlaciona com dificuldade do item ou carga de trabalho do anotador.

Anotadores reais desistem a meio de lotes, merge requests dividem pools de revisores, e chamadas de LLM dão timeout. A lógica de coincidência de $\alpha$ não é mágica — se a falta de dados é **informativa** (itens mais difíceis são mais frequentemente ignorados), nenhum coeficiente é seguro — mas evita o modo de **falha estrutural** de requerer imputação ou eliminação de linhas apenas para retornar um número.

![Experimento D: $\alpha$ vs $\kappa_F$ à medida que a taxa de faltantes aumenta.](../figures/exp_d_missing_robustness.png)

**Figura 6.** Dados faltantes: $\alpha$ mantém-se informativo (média $\pm$ 1 DP sobre 10 seeds); Fleiss requer matriz completa.

### 8.5 Síntese

Em conjunto, os experimentos suportam a tese: **acordo bruto engana** sob independência e enviesamento; **Kappa** corrige parcialmente mas herda limites estruturais; **$\alpha$** lida com faltantes e unifica o pensamento baseado em desacordo — validado aqui sobre verdade sintética onde as expectativas são analíticas ou visualmente claras.

---

## 9. Quadro prático

### 9.1 Quando usar cada métrica

- Reporte $A_o$ como resumo transparente sensível à prevalência, **sempre** com um coeficiente consciente do acaso.
- **Kappa de Cohen** com exatamente **dois** anotadores fixos, dados **completos**, categorias **nominais** (ou kappa ponderado).
- **Kappa de Fleiss** quando cada item tem o **mesmo** $m$ e a matriz está **completa**.
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

Não há corte universal que substitua julgamento de domínio. Regras tipo Landis–Koch não foram feitas para corpora NLP modernos enviesados. Trate qualquer limiar único como **heurística**: intervalos de confiança, sensibilidade à prevalência, análise de erros nos itens em desacordo. Se $\alpha \ll 0$ com $A_o$ alto, investigue **prevalência e acaso** antes de celebrar confiabilidade.

### 9.4 Checklist de relatório

Ao escrever a secção de métodos de um artigo ou um model card interno:

1. Declarar **qual** definição de acordo é usada (pares dentro do item vs pool global).
2. Reportar $A_o$ (ou equivalente) **e** pelo menos um coeficiente **consciente do acaso** adequado ao desenho.
3. Divulgar $K$, **frequências de classe aproximadas** e taxas de **faltantes**.
4. Para $\alpha$: nomear o **nível de medição** (nominal vs ordinal, ...) e o **domínio de valores**.
5. Arquivar **código e sementes** para que figuras e tabelas sejam recalculáveis.

### 9.5 Confiabilidade não é validade (o problema do viés sistemático)

$\alpha$ alto significa que os anotadores **reproduzem** os julgamentos uns dos outros. **Não** significa que esses julgamentos estão corretos. Se todos os anotadores aplicam consistentemente a mesma interpretação errada — ou se um LLM e os seus treinadores humanos partilham o mesmo viés sistemático — a confiabilidade será alta enquanto a **validade** é pobre. Isto não é um caso limite teórico: em moderação de conteúdo, anotadores treinados com as mesmas diretrizes podem concordar de forma confiável em etiquetas que uma auditoria externa rejeitaria.

A implicação para avaliação de LLMs é direta: um modelo que imita perfeitamente anotadores humanos herda os seus vieses. Alto acordo entre modelo e humanos é necessário mas **não suficiente** para qualidade. Auditorias de desacordo, análise de erros estratificada e validação externa continuam essenciais.

### 9.6 O que coeficientes não consertam

$\alpha$ não é uma bala de prata. Não substitui **regras de codificação claras**, **treino** ou **estudos piloto**. Limitações específicas:

- **Itens ambíguos.** Se a confusão se concentra num punhado de itens, a resposta correta é **revisão iterativa do guia**, não mais dados.
- **Sensibilidade à prevalência.** $\alpha$ aborda parcialmente isso através do seu modelo de acaso, mas desbalanceamento extremo pode comprimir o alcance dinâmico do coeficiente. O **AC1 de Gwet** (Gwet, 2008) foi desenhado especificamente para ser mais estável sob o paradoxo do Kappa; vale a pena compará-lo quando a prevalência é extrema e $\kappa$ se comporta erraticamente.
- **Escolha da função de distância.** Para dados não nominais, o valor de $\alpha$ depende do $\delta$ escolhido. Pressupostos ordinais vs intervalo podem produzir resultados substancialmente diferentes — a escolha deve ser justificada pela teoria de medição, não pelo que produz um número mais alto.
- **Anotadores não independentes.** Anotadores que discutem etiquetas, copiam vizinhos ou partilham saídas de modelos violam os pressupostos de independência embutidos nos modelos de acaso. A solução é **desenho de protocolo** (isolamento, rotação, condições cegas), não álgebra posterior.
- **Erros estruturados.** Como notado no Experimento C, $\alpha$ não distingue desacordo **aleatório** de viés **direcional**. Dois anotadores que sistematicamente discordam em direções opostas podem produzir o mesmo $\alpha$ que dois anotadores que discordam aleatoriamente — mas as implicações a jusante são muito diferentes.

---

## 10. Conclusão

Abrimos com um cenário concreto: anotadores discordam, um LLM é consistente, e a tentação é confiar no número que parece melhor. O argumento do artigo é que **acordo alto pode ser enganador** sob desbalanceamento de classes e marginais independentes — não que é sempre enganador, mas que sem modelar explicitamente o acaso, não há como distinguir.

Os $\kappa$ de Cohen e Fleiss subtraem um referencial consciente da prevalência e melhoram a interpretação, mas cedem sob **paradoxos de desbalanceamento**, **dados faltantes** e scaffolding **nominal inflexível**. O $\alpha$ de Krippendorff reformula a questão em torno de **desacordo** ponderado por distâncias significativas, com uma construção de coincidência que absorve padrões de observação **parcial**. Os quatro experimentos mostram, em condições controladas sob dois processos geradores de dados explícitos, que $\alpha$ se comporta como a teoria exige: anula-se sob etiquetagem puramente aleatória, sinaliza a armadilha do acordo, responde à composição do painel, e sobrevive a faltantes onde Fleiss não consegue.

$\alpha$ não é uma bala de prata. Não deteta **viés sistemático**, não substitui diretrizes de anotação claras, e — como todo coeficiente corrigido pelo acaso — depende de pressupostos de modelação que dados reais podem violar. Alternativas como o AC1 de Gwet abordam modos de falha específicos de $\kappa$ sob prevalência extrema. A abordagem correta raramente é um coeficiente único; é um **kit de diagnóstico** que inclui $A_o$, uma medida corrigida pelo acaso, e análise qualitativa de erros.

Para **prática de ML**, a mensagem operacional é procedimental: **nunca** enviar um único percentual de acordo sem declarar o **referencial de acaso**; **preferir** coeficientes que correspondam ao **desenho amostral** e à **escala de medição**; e **investir** em auditorias de desacordo — especialmente quando o acordo de um LLM com humanos é usado como proxy para segurança ou qualidade.

O cenário inicial — humanos discordam, o modelo é consistente — não é um argumento contra a anotação humana. É um lembrete de que **consistência** e **correção** são propriedades diferentes, e que a distância entre o que se observa e o que o emparelhamento aleatório produziria é onde a confiabilidade vive.

---

## Referências

1. Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46. [doi:10.1177/001316446002000104](https://doi.org/10.1177/001316446002000104)
2. Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters. *Psychological Bulletin*, 76(5), 378–382. [doi:10.1037/h0031619](https://doi.org/10.1037/h0031619)
3. Feinstein, A. R., & Cicchetti, D. V. (1990). High agreement but low kappa: I. The problems of two paradoxes. *Journal of Clinical Epidemiology*, 43(6), 543–549. [doi:10.1016/0895-4356(90)90158-L](https://doi.org/10.1016/0895-4356(90)90158-L)
4. Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology* (2nd ed.). Sage. ISBN 978-0-7619-1544-7.
5. Artstein, R., & Poesio, M. (2008). Inter-coder agreement for computational linguistics. *Computational Linguistics*, 34(4), 555–596. [doi:10.1162/coli.07-034-R2](https://doi.org/10.1162/coli.07-034-R2)
6. Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174. [doi:10.2307/2529310](https://doi.org/10.2307/2529310)
7. Krippendorff, K. (2011). Computing Krippendorff's Alpha-Reliability. *Departmental Papers (ASC)*, University of Pennsylvania. [Available online](https://repository.upenn.edu/asc_papers/43/)
8. Gwet, K. L. (2008). Computing inter-rater reliability and its variance in the presence of high agreement. *British Journal of Mathematical and Statistical Psychology*, 61(1), 29–48. [doi:10.1348/000711006X126600](https://doi.org/10.1348/000711006X126600)
