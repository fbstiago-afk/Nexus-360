# NEXUS 360 — QA da página-modelo Executive Command Center

**Data:** 01/11/2026, 21:00–21:18. **Ambiente:** Power BI Desktop 2.159.883.0, PBIP (TMDL + PBIR), canvas 1920×1080. Visuais custom: HTML Content Secure e Deneb (AppSource).
**Evidências:** `testes/screenshots/` (capturas da tela do Desktop, zoom 74%).

## 1. Resultado por teste pedido

| # | Teste | Resultado | Status |
|---|---|---|---|
| 1 | Abrir o PBIP | 1ª tentativa: 4 erros de esquema nos favoritos (`preserveNewVisualVisibility` não é aceito junto com `suppressData`). Propriedade removida; a abertura seguinte não teve erros | PASS (após correção) |
| 2 | Carregamento dos visuais | 16 visuais renderizam: cabeçalho, barra de filtros, 5 cards, combo, bullet Deneb, cascata, matriz, 4 botões | PASS |
| 3a | Painel de filtros (favorito) | Abre e fecha. Ano sem "(Em branco)" e sem 2027 (filtro de visual `FlagRealizado = 1`) | PASS |
| 3b | Seleção preservada ao fechar | Região = Sudeste continua aplicada depois de fechar o painel (favoritos só de exibição, `suppressData`) | PASS |
| 3c | Barra de filtros ativos | Mostra `REGIÃO SUDESTE · FILIAL 6 DE 12` (filtro cruzado) e volta a `TODAS` ao limpar | PASS |
| 3d | Painéis de informações e navegação | Abrem e fecham por favorito; cada um oculta os outros | PASS |
| 3e | Botão Home | Sem destino, porque a Home não foi construída. Tem dica de ferramenta explicando | PENDENTE (por escopo) |
| 3f | Botão "Limpar filtros" | Configurado como `ClearAllSlicers`. Não clicado, porque limpa também o ano padrão 2026 | NÃO EXECUTADO |
| 4 | Indicadores | Receita 2026 = R$ 151,1 mi (QA: 151.079.018,69). Receita Sudeste 2026 no card = R$ 75,5 mi; DAX = 75.510.685,47. Margem 26,9%, OTIF 64,3%, churn 35,5% e 8.187 em risco iguais ao QA do modelo | PASS |
| 5 | Nitidez do fundo | Sem serrilhado nem borrão no zoom de 74%; caminhão do fundo não aparece sob os visuais (transparência 8%) | PASS |
| 6a | HTML Content | Cabeçalho, barra, cards com sparkline/progresso e painel de informações renderizam com CSS | PASS |
| 6b | Deneb | Bullet por filial renderiza, ordenado por atingimento, com cores semânticas; reage ao filtro de região | PASS |
| 6c | Tooltip de página (TT Filial) | Página, medida (2.032 caracteres de HTML válido para Campinas) e configuração na matriz conferidas no painel de formato. **Ao passar o mouse aparece o tooltip padrão**, não a página | FALHA (pendência P1) |
| 7 | Performance (Performance Analyzer, filtro Sudeste, sessão já aberta) | Matriz 404 ms; cards HTML 338–388 ms; cabeçalho e barra 201–202 ms; combo e cascata 226 ms; Deneb 164 ms; botões 81–83 ms. Nenhum visual acima de 410 ms | PASS |
| 8 | Sobreposições | Sem sobreposição no estado padrão. Os painéis ficam por cima dos visuais, como previsto. Há um traço de 4 px à direita dos títulos "Filtros" e "Páginas" (caixa de texto) | PASS com ressalva (P3) |
| 9 | Comparação com o wireframe (doc 04, Tela 01) | Atendidos: título + período + filtros ativos + botão de filtros, tendência receita/margem, ranking de filiais (bullet), desvio de metas (matriz). Desvios: **5 KPIs em vez de 4** (taxa de churn como 5º card); **menu lateral fixo virou painel recolhível**, para dar a largura toda à análise; a DRE em cascata é um visual a mais que o wireframe não lista | PASS com desvios documentados (decisão do usuário) |
| 10 | Registro de problemas | Esta tabela e a seção 2 | — |

## 2. Problemas encontrados e correções

| Problema | Causa | Correção | Estado |
|---|---|---|---|
| Erro de esquema ao abrir | `preserveNewVisualVisibility` em favorito com `suppressData` | Propriedade removida dos 4 favoritos e do script | Corrigido |
| Texto "Fechar" invisível (aparecia como traço) | No PBIR o botão precisa de uma entrada `text.show` **sem seletor**, além da entrada do estado `default` | Entrada adicionada aos 4 botões; descoberto salvando pelo Desktop e comparando o JSON | Corrigido |
| Ano com "(Em branco)" e 2027 | Calendário estendido até jun/2027 | Filtro de visual `dCalendario[FlagRealizado] = 1` nos slicers Ano e Mês | Corrigido |
| Região cortada | Altura do slicer | 140 px; Filial reposicionada | Corrigido |
| Navegador com estilo padrão | Sem formatação | Fundo, contorno, estado selecionado e páginas de tooltip ocultas | Corrigido |
| Página ativa salva como tooltip | `activePageName` | Agora `pgExecutive` | Corrigido |
| Tooltip de página não aciona | Não identificada. Já testado: `type: Tooltip`, `pageBinding`, `HiddenInViewMode`, configuração visível no painel de formato | — | **P1 aberto** |
| Matriz com barra de rolagem (12 filiais, 11 visíveis) | Altura da área inferior | — | P2 aberto |
| Rótulos da cascata inclinados | 10 categorias em 900 px | — | P2 aberto |
| Linhas do combo suavizadas | Padrão do visual | — | P3 aberto |
| Traço de 4 px no título dos painéis | Caixa de texto | — | P3 aberto |

## 3. Não executado
- Teste no Power BI Service (modo leitura real, sem Ctrl+clique) e em outro monitor.
- Teste com o filtro de categoria (aviso de medidas sem produto) pela interface. A lógica foi validada só por DAX.
- Performance com cache frio (DAX Studio com Clear Cache).

## 4. Rodada 2 — correções (02/11/2026, 09:20–09:35)

| Item | Causa encontrada | Correção | Teste | Status |
|---|---|---|---|---|
| 2.1 Tooltip por filial | O Desktop grava "Página de relatório" como `type: 'Canvas'`. O valor `'ReportPage'` (usado a partir de referência pública) aparece no painel de formato como "Página de relatório", mas não aciona a página. Experimento: página criada pela interface (só `type: Tooltip`, sem `pageBinding`) falhou igual na matriz e na tabela e funcionou na cascata, que a interface gravou como `'Canvas'` | `visualTooltip.type = 'Canvas'` na matriz; `pageBinding` removido da página de tooltip; páginas e cartão de teste movidos para `_to_delete/exp_tooltip_20261102` | Passar o mouse sobre Brasília abre o tooltip HTML (receita 12 meses com barras, receita, atingimento, margem e OTIF com desvios). **HTML Content funciona dentro de tooltip** | PASS |
| 2.2 Matriz | 332 px para 14 linhas | Faixa inferior 706–1056 (350 px), gráficos 378–690 (312 px), `rowPadding` 1, preenchimento do visual 8/4 | 12 filiais + total sem rolagem; 1ª coluna à esquerda, números à direita, cores semânticas mantidas | PASS |
| 2.3 Cascata | 10 categorias + eixo de valores em 900 px | Eixo de valores removido (os rótulos já trazem os valores), categorias em 9pt | Rótulos horizontais; aumento verde, redução vermelha, total ciano | PASS |
| 2.4 Combo | O tema base Fluent2 do Desktop define `lineChartType: smooth` para todos os visuais | `lineChartType: linear` no tema NEXUS 360 (`*` e combo) e no visual | Segmentos retos | PASS |
| 2.5 Traço de 4 px | Barra de rolagem da caixa de texto do título (15pt + preenchimento > 40 px) | 14pt, preenchimento 0, altura 36 | Traço ausente | PASS |
| 2.6a Limpar filtros | `ClearAllSlicers` também limpa o ano padrão | Favorito "Redefinir filtros": só dados, só os 5 slicers, restaura Ano = 2026 | Sudeste + Alimentos → Limpar → Região/Categoria "Todas", Ano 2026, painel continua aberto | PASS |
| 2.6b Filtro de categoria (interface) | Bullet mostrava 28–31% (receita de Alimentos ÷ meta total); combo mostrava a meta de margem | Guarda `[Filtro de Produto Ativo]` em `Meta Faturamento` e `Meta Margem Bruta % (ponderada)`; título dinâmico da cascata (`UX Título DRE`) | Com Alimentos: aviso na barra, cards sem meta, bullet vazio, combo sem meta, cascata "DRE gerencial indisponível com filtro de produto", matriz com devolução e Δ margem em branco | PASS |
| 2.6c Botão Home | — | Depende da Home (Etapa A) | — | PENDENTE |

**Regressão DAX após a guarda nas metas:** Meta Faturamento 494.870.779,94; até o corte 470.000.292,87; Meta Margem ponderada até o corte 28,2983% (iguais ao QA do modelo). Atingimento 2026 98,99%. Com filtro de Alimentos: em branco.

**Performance (Performance Analyzer, sem filtro, 02/11 09:34):** maior visual 418 ms (card HTML); matriz 241 ms; cascata 192 ms; combo 174 ms; Deneb 113 ms; botões 55–56 ms.

**Resíduo aceito:** com filtro de produto, a cascata desenha "R$ 0,0 Mi Total". O total é calculado pelo próprio visual, sem medida a controlar; o título avisa a indisponibilidade.
