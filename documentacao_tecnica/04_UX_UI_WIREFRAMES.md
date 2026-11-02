# 04 — UX/UI | Wireframes funcionais das 11 telas

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## Sistema visual
Canvas 16:9, recomendação 1600x900 (PROPOSTA). Fundo `#071528`, superfícies `#0A1C33`, destaque `#10D4C4`, azul `#0878C9`, branco `#FFFFFF`, texto secundário `#A9B9CA`. Valores do manual visual do projeto; conferir versão final antes de exportar tema. Grid 12 colunas, margens 24 px, gap 16 px (PROPOSTA). Cabeçalhos em HTML, fundos transparentes nos visuais, no máximo 4 a 6 visuais analíticos principais por página.

**Layout global:** topo 72 px com título e contexto dos filtros; barra lateral de navegação 76 px; botão de filtros abre painel sobreposto; indicadores de seleção no topo; rodapé discreto com última data de dados. Todos os tamanhos são PROPOSTAS de UI.

**Interações:** filtros por data, filial e atributos aplicáveis; sincronização apenas onde a relação funciona; botões para limpar filtros, tooltip contextual, drillthrough, estados vazios e avisos de amostra.

## Tela 00 — Home
**Fontes confirmadas:** `dCalendario`, `dFilial`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** Marca, período histórico, botão iniciar e 4 atalhos; sem KPIs inventados.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 01 — Executive Command Center
**Fontes confirmadas:** `fFaturamento`, `fDespesa`, `fMeta`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** 4 KPIs superiores, tendência receita/margem, ranking filiais, desvio de metas.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 02 — Commercial Intelligence
**Fontes confirmadas:** `fPedido`, `fItemPedido`, `dVendedor`, `dProduto`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** 4 KPIs, gráfico horizontal por vendedor, matriz de mix, dispersão de descontos.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 03 — Customer Intelligence
**Fontes confirmadas:** `fPedido`, `dCliente`, `fVisitaComercial`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** 4 KPIs, coortes de compra, quadrantes frequência/valor, reativação.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 04 — Logistics Control Tower
**Fontes confirmadas:** `fEntrega`, `dTransportadora`, `dFilial`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** OTIF, atrasos, mapa de filiais, ranking transportadoras e detalhe.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 05 — Warehouse Digital Twin
**Fontes confirmadas:** `dPosicaoArmazem`, `fOcupacaoArmazem`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** KPI ocupação amostral, planta 2D e 3D opcional, zona, evolução.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 06 — Financial & Profitability
**Fontes confirmadas:** `fFaturamento`, `fDespesa`, `fContasReceber`, `fContasPagar`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** Receita/CMV/margem, waterfall gerencial, vencimentos, despesa por conta.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 07 — Predictive Intelligence
**Fontes confirmadas:** `fPrevisao`, `fFaturamento`, `dCalendario`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** Série histórica vs projeção, sazonalidade, erro estimado, ranking filiais.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 08 — Decision Simulator
**Fontes confirmadas:** `fFaturamento`, `fDespesa`, `parâmetros PROPOSTOS`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** Parâmetros What-if, KPIs de cenário, tornado, comparativo.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 09 — Operations Calendar
**Fontes confirmadas:** `fVisitaComercial`, `fInteracaoCampanha`, `dCampanha`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** Matriz semana x dia, visitas e interações, seletor campanha.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Tela 10 — AI Decision Assistant
**Fontes confirmadas:** `modelo semântico; agente externo opcional`.

**Wireframe lógico:**
```text
┌──────────────────────────────────────────────────────────────────┐
│ NAVEGAÇÃO │ TÍTULO + PERÍODO + FILTROS ATIVOS       [FILTROS]  │
├───────────┬──────────────────────────────────────────────────────┤
│           │ KPI 1      KPI 2      KPI 3      KPI 4             │
│ MENU      ├──────────────────────────────┬───────────────────────┤
│           │ VISUAL PRINCIPAL             │ VISUAL SECUNDÁRIO     │
│           ├──────────────────────────────┴───────────────────────┤
│           │ DETALHE / INSIGHT / EXCEÇÕES (quando aplicável)     │
└───────────┴──────────────────────────────────────────────────────┘
```
**Composição específica:** Perguntas sugeridas, respostas verificáveis, gráfico vinculado, avisos.

**Critérios:** título centralizado por visual, legenda acessível, unidade explícita, tooltip com período, estado vazio, filtro funcional e nenhum texto narrativo longo. Para Home e Assistente, substituir KPIs por conteúdo específico.

## Responsividade e validação
Verificar Desktop em 1600x900 e 1366x768, com zoom padrão; evitar clipping. Painel de filtros não deve sobrepor elementos críticos sem fechamento. Tooltips não podem depender de hover para transmitir informações essenciais. Respeitar contraste WCAG e preferência de redução de movimento em camadas HTML.
