# 00 — Plano de implementação NEXUS 360

**Base:** auditoria `00_AUDITORIA_DADOS.md` (IDs C*/M* referenciados abaixo) + docs 01–08 + SKILL + Design System. Nada aqui está implementado ainda.

## 1. Decisões de arquitetura (propostas com justificativa)

| # | Decisão | Por quê |
|---|---|---|
| A1 | Fonte = CSV via parâmetro `pPastaDados` (relativo à raiz) | SQLite ausente (C1); CSV não exige driver ODBC |
| A2 | **Estrelas independentes com chaves materializadas no PQ** (não `dPedido` como ponte): `fItemPedido`, `fFaturamento`, `fEntrega`, `fContasReceber`, `fDevolucao` recebem `ClienteID`, `FilialID`, `VendedorID`, `CampanhaID`, `DataPedido` por merge 1:1 com `fPedido` | Evita fato→fato e caminhos ambíguos (doc 03 §1 pede escolher um desenho); join validado 1:1 |
| A3 | `PedidoID` mantido como coluna de drillthrough; sem `dPedido` | Cardinalidade 100k sem atributos próprios |
| A4 | `dCalendario` gerada no PQ 2024-01-01→2027-06-30, com colunas da fonte + PT-BR + `FlagRealizado` (≤ `pDataCorte`) + semana do mês | Cobre fPrevisao (C3); M6 |
| A5 | Datas: ativa por evento principal; inativas para alternativas (`fEntrega[DataPrometida]`, `fContasReceber[DataPagamento]`, `DataPedido` nos fatos enriquecidos) com `USERELATIONSHIP` | Doc 03 |
| A6 | Parâmetro `pDataCorte = 2026-10-31`; fatos realizados filtrados no PQ; contagem de excluídos exposta em `99_QA` | C2, sem correção silenciosa |
| A7 | Filial analítica = `fPedido[FilialID]` → `dFilial`; `dVendedor[FilialID]` e `dCliente[FilialID]` só atributos | M2 |
| A8 | fMeta pivotada por indicador em medidas separadas; metas de razão ponderadas | C8 |
| A9 | Canvas 1920×1080; fundos de `assets/img`; zonas do fundo analítico (px em 1920×1080): título 586–1596 × 23–99; filtros ativos 149–1889 × 126–195; botões Filtro 1636–1711, Info 1729–1804, Home 1823–1898 (y 23–99); área útil y ≥ 212 | Conflito canvas (Inventário §5); coordenadas a ajustar ao pixel no Desktop |
| A10 | Navegação entre páginas por painel recolhível acionado pelo ícone de ajustes da barra de filtros (x≈60–150) | Fundo não tem sidebar |

### Relacionamentos previstos (todos 1:N, direção única dimensão→fato)
`dCalendario` → todos os fatos (data principal) · `dFilial` → fPedido, fItemPedido*, fFaturamento*, fEntrega*, fContasReceber*, fDevolucao*, fCompra, fDespesa, fMeta, fOrcamento, fPrevisao, fEstoqueMensal, fMovimentoEstoque, dPosicaoArmazem→fOcupacaoArmazem (filial via posição, materializada) · `dCliente` → fPedido, fatos*, fVisitaComercial, fInteracaoCampanha · `dVendedor` → fPedido, fatos*, fVisitaComercial · `dProduto` → fItemPedido, fCompra, fEstoqueMensal, fMovimentoEstoque, fOcupacaoArmazem · `dCampanha` → fPedido, fatos*, fInteracaoCampanha · `dTransportadora` → fEntrega · `dFornecedor` → fCompra · `dPosicaoArmazem` → fOcupacaoArmazem. `fContasPagar` recebe `FilialID`/`FornecedorID` por merge com fCompra. (*) = chave materializada (A2). Nenhuma relação fato-fato, nenhuma bidirecional.

## 2. Sequência de fases

| Fase | Entrega | Depende de | Validação de saída |
|---|---|---|---|
| F2 Modelo | PBIP vazio + PQ (staging desabilitado) + 9 dims + 17 fatos + calendário + relações | Decisões §5; Power BI Desktop confirmado | Abre no Desktop; refresh sem erro; contagens = Auditoria §1 (após corte) |
| F3 Medidas | `00 Base` a `09 Qualidade` + `99_QA` | F2 | DAX = SQL da Auditoria §3 (diferença 0) via `powerbi-modeling-mcp` |
| F4 Design system | Tema JSON, biblioteca HTML/SVG (`componentes_html/`), medidas `08 UX`, página-modelo com header, barra de filtros ativos, painel de filtros, info e navegação | F3 | Barra reflete filtros reais em 6 cenários (vazio, 1, múltiplo, cruzado, página, sincronizado) |
| F5 Home | Fundo + KPIs HTML + mapa SVG + botão INICIAR | F4 | KPIs = medidas; navegação funciona |
| F6 Páginas | Ordem abaixo, uma por vez | F4 | Checklist §4 por página |
| F7 Avançados | Tooltips, drillthrough, Deneb, calendário, simulador, WMS 3D externo, agente | F6 | QA11 |
| F8 QA/entrega | Performance Analyzer/DAX Studio, screenshots, docs finais, PBIX via Desktop | F7 | QA01–QA14 com evidência |

**Ordem das páginas** (por dependência de medidas e risco): 01 Executive → 02 Commercial → 03 Customer (churn) → 04 Logistics → 06 Financial (bloqueio C4) → 05 WMS 2D → 09 Calendar → 07 Predictive → 08 Simulator → 10 AI Assistant. A Home é feita em F5 mas os KPIs reutilizam medidas da 01.

## 3. Mapa página × técnica × dependências

| Página | Medidas-chave (pasta) | Técnica | Bloqueios/ressalvas |
|---|---|---|---|
| Home | Receita, Clientes ativos, Entregas, Margem %, Filiais | HTML Content (KPIs + mapa SVG com lat/long reais projetadas) | Mapa da imagem tem pontos ilustrativos no N/NE (§6) |
| 01 Executive | Receita, Margem, Resultado gerencial, Meta fat., atingimento | Cards HTML+sparkline, linha nativa, barras filial, bullet (Deneb) | Meta de margem ponderada (C8); despesa ≤ corte |
| 02 Commercial | Valor itens faturados, mix, desconto médio, ranking vendedor | Deneb barras horizontais, matriz nativa c/ data bars, dispersão desconto×margem | M3 |
| 03 Customer | Ativos, Novos (1ª compra), Em risco, Churn 90d, Reativados | Cohort (matriz), scatter quadrantes, tooltip cliente | C6 (cadastro inválido), M5 |
| 04 Logistics | OTIF %, No prazo %, In full %, frete/entrega, atraso médio | Mapa filiais (Azure Maps ou SVG), ranking transportadoras, dispersão custo×OTIF | M1, C5 |
| 05 WMS | Distribuição de status, paletes, posições amostradas | Heatmap SVG X×Y por nível Z (2D nativo/HTML) + app 3D externo | C9 |
| 06 Financial | DRE gerencial simplificada, despesa por conta, aging | Waterfall, matriz, aging | **C4 bloqueia aging/inadimplência** |
| 07 Predictive | Histórico vs previsão, banda ± MargemErro, sazonalidade | Deneb linha + faixa | C3 (lacuna nov–dez/26); semântica de `MargemErroEstimada` |
| 08 Simulator | Receita/margem cenário | Parâmetros What-if desconectados, tornado (Deneb) | Premissas explícitas |
| 09 Calendar | Visitas, interações, campanhas ativas por dia | Matriz semana×dia + CONCATENATEX | C7 |
| 10 AI | — | Página de especificação + demo rotulada | Sem backend (§6) |

## 4. Critérios de validação por página (Definition of Done)
1. Toda medida exibida reconciliada com SQL (arquivo em `testes/sql/`).
2. Filtros: vazio, seleção única, múltipla, cruzada — barra de filtros coerente.
3. Painel de filtros abre/fecha sem perder seleção (bookmark sem "Dados").
4. Tooltips e drillthrough no contexto certo.
5. Sem sobreposição a 1920×1080 e legível a 1366×768.
6. Estados BLANK/zero/indisponível distintos.
7. Performance Analyzer: tempos registrados (sem metas inventadas).
8. Screenshot em `testes/screenshots/`.

## 5. Decisões que dependem do usuário (antes da F2/F3)
| # | Pergunta | Recomendação |
|---|---|---|
| D1 | Regra de pagamento em `fContasReceber` (C4): pago = `ValorPago > 0`, = `DataPagamento` preenchida, ou exigir ambos? | Exigir ambos para "liquidado"; os 14.734 incoerentes em categoria própria "inconsistente", visível no QA |
| D2 | Excluir no PQ os registros pós-corte dos fatos realizados (C2)? | Sim, com contagem em `99_QA` |
| D3 | Canvas 1920×1080 (fundo upscalado) ou 1600×900? | 1920×1080; idealmente fundos reexportados em 1920×1080 |
| D4 | Mapa da Home: os 8 pontos desenhados no N/NE não correspondem a nenhuma filial real | Pedir versão do fundo sem pontos/rotas; até lá, camada SVG própria com as 12 filiais reais |
| D5 | Power BI Desktop: versão instalada e preview PBIR/TMDL habilitados? HTML Content e Deneb instalados? | Necessário para F2 |
| D6 | Fabric/Power BI Service disponível (para Fabric Apps, Azure Maps, agente via XMLA/REST)? | Define o caminho do 3D e da IA |

## 6. Limitações técnicas antecipadas
- **HTML Content** não executa JavaScript; CSS `@keyframes` e SVG inline funcionam. Tooltip nativo do Power BI não lê `title` do SVG → tooltips do mapa via página de tooltip, não por ponto do HTML.
- **Visuais custom em PBIR** exigem GUID/versão do pacote; inserir uma instância de HTML Content e Deneb pelo Desktop antes de gerar o restante por arquivo.
- **3D (Warehouse):** Three.js não roda dentro de HTML Content. Caminhos: (a) app HTML/Three.js standalone em `apps/wms3d` lendo snapshot JSON exportado do modelo — funcional, mas não filtrado ao vivo pelo relatório; (b) visual custom `.pbiviz` com Three.js — exige Node/pbiviz (ausentes no Windows); (c) Fabric App — depende de licença. Recomendado: (a) + fallback 2D nativo no relatório.
- **AI Decision Assistant:** sem serviço de IA embutível no relatório. `powerbi-modeling-mcp` é ferramenta de desenvolvimento local, não backend de produção. Entrega desta fase: manifesto de ferramentas tipadas, allowlist de medidas, página demonstrativa rotulada "não conectada". Integração real exige Service (executeQueries/XMLA) + backend autenticado.
- **PBIX:** só por "Salvar como" no Desktop; não será declarado sem arquivo verificado.
- **Validação visual:** requer Desktop aberto; screenshots via controle do computador quando autorizado.


## 7. Registro de decisões (atualizado em 01/11/2026)
| # | Decisão | Estado |
|---|---|---|
| D1 | Recebido somente com valor pago > 0 **e** data de pagamento válida (>= faturamento); demais combinações = `Inconsistente`, mantidas na base e monitoradas | Aprovada e implementada |
| D2 | Sem exclusão física; `ElegivelHistorico` em fatos realizados; metas, orçamento e previsão sem filtro; medidas de auditoria do corte | Aprovada e implementada |
| D5 | Desktop 2.159.883.0, DAX Studio, Tabular Editor 2, Measure Killer e Power BI Helper verificados; HTML Content/Deneb não verificados | Resolvida (parcial) |
| A2 | Estrelas independentes com chaves materializadas (sem `dPedido`) | Implementada |
| — | Churn: Ativo < 180 d, Em risco 180–364 d, Churn ≥ 365 d, Reativado e Novo como status exclusivos; reativação também como evento; limites em parâmetros desconectados | Aprovada e implementada |
| D3 | Canvas 1920×1080; fundos ampliados 1,148× sem distorção; checar nitidez na F4 | Aprovada (aplicar na F4) |
| D4 | Mapa SVG independente com as 12 filiais reais; pontos do fundo só decorativos; sem rotas entre filiais (não há dado origem→destino) | Aprovada (aplicar na F5) |
| D6 | Desktop como ambiente principal; Fabric/Service não verificado (conta desconectada). 3D: 2D nativo + app Three.js complementar; IA: catálogo, ferramentas tipadas e arquitetura documentados, sem integração simulada | Aprovada |

### Decisões de 02/11/2026 (aprovadas pelo usuário)
| # | Decisão | Prevalece sobre |
|---|---|---|
| D7 | Executive Command Center com **5 KPIs** (inclui taxa de churn 365 dias) | doc 04, Tela 01 (4 KPIs) |
| D8 | Navegação por **painel recolhível** acionado por botão, em todas as páginas | doc 04 (menu lateral fixo) |
| D9 | **DRE em cascata** na página executiva | doc 04, Tela 01 |
| D10 | Metas (faturamento e margem) ficam em branco com filtro de produto, como as demais medidas sem grão de produto | — (estende a regra já documentada) |
| D11 | Tooltips de página: gravar `visualTooltip.type = 'Canvas'` no PBIR | referência pública que usa `'ReportPage'` |

### Decisões de 02/11/2026 (tomadas na execução autônoma)
| # | Decisão | Motivo |
|---|---|---|
| D12 | Simulador sem elasticidade: preço e volume independentes; resultado do simulador = receita − CMV − frete − despesas (difere da DRE gerencial) | Não há elasticidade documentada; frete é alavanca pedida |
| D13 | Simulação indisponível com filtro de produto | Frete e despesas não têm grão de produto (D10) |
| D14 | Projeção sazonal × tendência 12M com faixa de 90% por t de Student sobre backtest de 10 meses; previsão da fonte exibida separada | Distinguir histórico, projeção e previsão |
| D15 | Calendário: matriz nativa + célula SVG; mês único visível; borda vermelha = OTIF 5 p.p. abaixo da média do mês (OTIF está abaixo da meta em quase todos os dias) | Destaque precisa discriminar |
| D16 | Assistente: ferramentas tipadas + DAX fixo; página mostra resultados reais e marca integração como pendente | Não simular IA |
| D17 | Customer: grade frequência × valor no lugar de RFM | RFM/RFQ sem regra na documentação |
| D18 | Fontes +20% em todos os visuais, HTML e Deneb; +30% em tabelas e matrizes; colunas centralizadas (inclusive a primeira); valores sem casas decimais (formatos de medidas, colunas, FORMAT em HTML e Deneb). Implementado em `pbip/_gerador/nx_estilo.py`, aplicado na escrita pelos geradores; aplicação única aos arquivos existentes em `aplicar_estilo_existente.py` | Pedido do usuário em 02/11/2026 17:04; substitui a regra "primeira coluna à esquerda". Rótulos que ficariam iguais ao arredondar passaram a R$ mil (vendedores, marcas, ponte financeira, ponte do simulador, gap por filial); índice de sazonalidade em base 100 |
| D19 | Parâmetros do simulador com `extendedProperty ParameterMetadata` (What-if) e desconto em passos inteiros de 1 p.p. | Sem o metadado o slider gerava valores fora da série (ex.: 0,0347) e o SELECTEDVALUE voltava a 0 |
