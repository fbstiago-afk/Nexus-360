---
name: nexus360-powerbi-enterprise
version: 1.0.0
description: Skill mestra para construir, revisar e documentar o NEXUS 360 no Power BI PBIP, com identidade visual, modelo semântico, DAX, Deneb, HTML/SVG, mapas, simulações e módulos externos opcionais.
---

# SKILL MESTRA — NEXUS 360 | Enterprise Decision Intelligence

## 1. Missão
Criar uma plataforma de BI para uma distribuidora B2B fictícia, com análises acionáveis de comercial, clientes, logística, WMS, finanças, previsões e simulação. O objetivo NÃO é maximizar o número de gráficos por tela; é demonstrar o máximo de **técnicas úteis** da biblioteca Insights Visuais sem comprometer legibilidade, precisão ou desempenho.

**Entregável principal:** projeto Power BI em formato **PBIP** editável, modelo semântico TMDL, relatórios e documentação; exportar PBIX quando o ambiente permitir. Não alegar exportação bem-sucedida sem verificar o arquivo.

## 2. Fontes de verdade e arquivos
- `NEXUS360.db`: banco SQLite, 26 tabelas, histórico sintético.
- `csv/`: CSVs equivalentes por tabela (UTF-8 BOM, vírgula, ponto decimal, datas ISO).
- `DICIONARIO_DADOS.json`: consultar nomes e tipos exatos das colunas ANTES de criar consultas ou DAX.
- `RELACIONAMENTOS.csv`: proposta de relações, sujeita à revisão de cardinalidade e caminhos ambíguos.
- `README.md`: grãos, regras e limitações dos dados.
- `NEXUS360_Manual_Identidade_Visual.pdf`: identidade visual aprovada para referência.
- Logo NEXUS 360 fornecido como imagem; não reconstruir tipografia por aproximação.
- Não assumir que o manual, logo e banco estejam na mesma pasta: localizar caminhos e documentar os utilizados.

## 3. Identidade visual e design tokens
```css
:root {
  --nx-navy: #071528;
  --nx-deep-blue: #0A1C33;
  --nx-teal: #10D4C4;
  --nx-blue: #0878C9;
  --nx-white: #FFFFFF;
  --nx-muted: #A9B9CA;
  --nx-success: #22B89A;
  --nx-warning: #F2B84B;
  --nx-danger: #E76F75;
  --nx-radius: 14px;
}
```
- Interface dark premium; fundo predominantemente navy; teal para destaque e azul para séries secundárias. Evitar gradientes pesados, sombras excessivas e brilho neon.
- Cards HTML com fundo transparente quando sobrepostos ao template, borda lateral de destaque e animações CSS discretas; sempre apresentar valores e unidades claros.
- Cabeçalhos HTML consistentes, título dos gráficos centralizado, navegação elegante e botões de filtros ocultos com indicação visível dos filtros aplicados.
- Tabelas: primeira coluna com valores à esquerda, cabeçalho centralizado; números à direita; barras in-cell e minigráficos somente quando agregarem leitura.
- Acessibilidade: contraste suficiente, não usar apenas cor para status, texto legível, tooltips úteis, movimento reduzido quando necessário.
- Layout wide 16:9; preservar margens, alinhamentos, densidade controlada e responsividade quando suportada.
- Usar no máximo ~4–6 áreas analíticas principais por página, com exceção justificada para tabelas e detalhamento.

## 4. Modelagem semântica — regras obrigatórias
1. Inspecionar esquema SQLite/CSV e `DICIONARIO_DADOS.json`, medir unicidade, nulos, cobertura temporal e integridade referencial.
2. Definir grão de cada fato e documentar em tabela de mapeamento.
3. Preferir esquema estrela, dimensões `d*` filtrando fatos `f*` em direção única.
4. `fPedido` tem 1 linha por pedido; `fItemPedido` tem 1 linha por item; `fFaturamento` tem 1 fatura por pedido faturado; `fEntrega` tem 1 entrega por pedido faturado. Evitar duplicar receita ao combinar pedido, item e faturamento.
5. Criar `dPedido` com `PedidoID` único se necessário para compartilhar filtros entre fatos. Não usar fato como ponte sem examinar caminhos ambíguos.
6. Enriquecer `fItemPedido` com chaves de cliente/filial/vendedor/data, quando apropriado, via Power Query e junção 1:N validada.
7. Usar `dCalendario` para inteligência temporal; manter data principal ativa e alternativas por `USERELATIONSHIP` ou dimensões role-playing. Data histórica máxima: **31/10/2026**; previsão até **30/04/2027**. Nunca misturar previsto com realizado sem sinalização.
8. Organizar medidas por pastas: `00 Base`, `01 Comercial`, `02 Clientes`, `03 Logistica`, `04 Estoque`, `05 Financeiro`, `06 Previsao`, `07 Simulacao`, `08 UX`, `09 Qualidade`.
9. Medidas base únicas; derivadas por composição; `DIVIDE` para divisões; evitar ALL indiscriminado e bidirecionalidade por conveniência.
10. Não afirmar DRE auditável: despesas e movimentos financeiros são sintéticos e não reconciliam integralmente. Estoque mensal é amostra de 200 SKUs por filial/mês; ocupação WMS também é amostral.

### Medidas DAX de referência (validar nomes e contexto)
```dax
Receita Líquida = SUM ( fFaturamento[ReceitaLiquida] )
CMV = SUM ( fFaturamento[CMV] )
Margem Bruta = [Receita Líquida] - [CMV]
Margem Bruta % = DIVIDE ( [Margem Bruta], [Receita Líquida] )
Entregas OTIF = CALCULATE ( COUNTROWS ( fEntrega ), fEntrega[NoPrazo] = 1, fEntrega[InFull] = 1 )
Entregas Total = COUNTROWS ( fEntrega )
OTIF % = DIVIDE ( [Entregas OTIF], [Entregas Total] )
```
**Nota:** medidas de exemplo não dispensam auditoria de esquema, status, cancelamentos, devoluções e datas. Devolução não deve ser subtraída duas vezes; desconto já está no valor líquido dos itens.

## 5. Biblioteca de skills visuais — quando e como aplicar

### 5.1 `MODERN_VISUAL_DEFAULTS`
Tokens de cor, espaçamento, bordas, tipografia, hierarquia, acessibilidade e consistência. Aplicar a todas as páginas e templates.

### 5.2 `HTML_CONTENT_CSS_CARDS`
Cards com KPI, comparação, sparklines SVG, barras de progresso, badges semânticos, flip cards opcionais e tooltips ricos. Priorizar medidas DAX que devolvem HTML/SVG sanitizado. Evitar CSS/JS que o visual não suporta; não presumir JavaScript executável.

### 5.3 `SVG_DAX_ADVANCED`
Minigráficos, bullet charts, lollipop, progress rings, heatmaps, linhas e ícones SVG em tabelas, tooltips e cards. Testar `data:image/svg+xml;utf8,` e codificação conforme o tipo de visual e categoria de dados. Usar fallback textual.

### 5.4 `DENEB_VEGA_LITE`
Dumbbell, slope, waterfall customizado, bullet, dot plot, variance, distribuição e gráficos com anotação contextual. Usar Deneb somente quando o gráfico nativo não atender com a mesma clareza. Garantir cross-filter e tooltip quando disponíveis.

### 5.5 `MOTION_ANALYTICS`
Animações suaves e intencionais para transição temporal e foco; evitar looping que distraia e excesso de atualização. Se o recurso depender de visual externo, documentar dependência e fallback estático.

### 5.6 `INTERACTIVE_CALENDAR_MATRIX_DAX`
Matriz de calendário com linhas por semana e colunas segunda–domingo, mostrar itens sem dados, sem subtotais, `CONCATENATEX` para eventos/campanhas/gastos, segmentador desconectado e formatação condicional para destacar datas. Validar virada de mês, semana e calendário sem eventos.

### 5.7 `SPATIAL_LOGISTICS_3D`
Armazém com posições X/Y/Z, ocupação, corredores, endereçamento, picking e giro. Construir visualização 3D externa em Three.js/Fabric App ou componente suportado, vinculada a dados do Power BI com segurança; não afirmar que HTML Content renderiza Three.js arbitrariamente. WMS é amostral, portanto mostrar escopo.

### 5.8 `GEOSPATIAL_POWERBI`
Mapas por filial, cliente e entrega, heatmaps, cobertura comercial, rotas e desempenho territorial. Usar latitude/longitude válidas quando existirem; não inventar coordenadas. Verificar licenciamento, privacidade, geocodificação e limites do Azure Maps.

### 5.9 `ADAPTIVE_BUDGETING`
Orçamento vs realizado, rolling 12M, sazonalidade, run-rate e cenários. Diferenciar orçamento, meta, projeção e realizado em cores/legendas e grãos.

### 5.10 `PREDICTIVE_ANALYTICS`
Forecast por filial/categoria, sazonalidade, faixas de incerteza e backtesting temporal. Com dados sintéticos, avaliar erro apenas como teste de pipeline, não como evidência de precisão no mundo real. Projeções futuras devem ser rotuladas.

### 5.11 `CONVERSATIONAL_BI`
Perguntas orientadas ao modelo semântico, respostas com fonte/medida/período/filtros, drill-through e evidências. Restringir perguntas às tabelas e métricas autorizadas.

### 5.12 `AGENTIC_BI_TYPED_TOOLS_MCP_DAX`
Agente embutido com manifesto pequeno de funções tipadas, queries DAX direcionadas ao modelo Tabular e, opcionalmente, SQL/REST/arquivos. Não presumir número exato de funções sem manifesto real. Exigir controle de acesso, validação de parâmetros, consultas somente leitura, timeout, auditoria e revisão humana para recomendações.

### 5.13 `AI_AGENT_FABRIC_APPS`
Protótipos de agentes e interface em Fabric Apps quando disponíveis. Implementação externa é opcional; não bloquear PBIP caso a licença ou integração não esteja disponível.

### 5.14 `SUPPLY_CHAIN_PERIODIC_TABLE`
Taxonomia de conceitos operacionais (demanda, cobertura, lead time, OTIF, giro, ruptura, picking etc.). Usar como glossário navegável e página educativa opcional, sem transformar a área operacional em painel decorativo.

### 5.15 `POWERBI_PBIVIZ_LIBRARY`
Avaliar visuais customizados existentes por função, custo, manutenção, certificação, exportação, acessibilidade e compatibilidade. Evitar instalar dezenas de pbiviz sem justificativa.

### 5.16 `DAX_PERFORMANCE_GOVERNANCE`
DAX Studio, Performance Analyzer, Tabular Editor quando disponível, revisão de medidas não usadas, dependências, cardinalidade, compressão, query folding, storage mode e medidas base. Não remover medidas ou colunas sem análise de dependência e backup.

## 6. Dez páginas — especificação funcional

| Página | Pergunta principal | Fontes principais | Técnicas prioritárias |
|---|---|---|---|
| 00 Home | Onde começar? | metadados/medidas | capa, navegação HTML, estado dos filtros |
| 01 Executive Command Center | Onde a empresa ganha/perde resultado? | fFaturamento, fDespesa, fMeta | cards HTML/SVG, waterfall, bullet, tendência |
| 02 Commercial Intelligence | Quem, onde e o que vende melhor? | fPedido, fItemPedido, dProduto, dVendedor | Deneb, RFQ, ranking, matriz com barras |
| 03 Customer Intelligence | Quem pode abandonar ou reativar? | fPedido, dCliente, fVisitaComercial | churn 90d, cohorts, quadrantes, tooltip SVG |
| 04 Logistics Control Tower | Onde falham prazo e entrega completa? | fEntrega, dTransportadora, dFilial | OTIF, mapas, Gantt, dispersão |
| 05 Warehouse Digital Twin | Onde estão os gargalos de ocupação? | dPosicaoArmazem, fOcupacaoArmazem | heatmap WMS, 3D externo opcional |
| 06 Financial & Profitability | Onde se deteriora a margem e o caixa? | fFaturamento, fDespesa, fContasReceber, fContasPagar | waterfall, DRE gerencial, aging, Pareto |
| 07 Predictive Intelligence | O que pode acontecer nos próximos meses? | fPrevisao, fFaturamento, fEstoqueMensal | forecast, bandas, sazonalidade |
| 08 Decision Simulator | Qual o impacto das alternativas? | medidas base e parâmetros desconectados | What-if, tornado, sensibilidade |
| 09 Operations Calendar | Quais eventos impactam o dia a dia? | dCampanha, fInteracaoCampanha, fVisitaComercial | calendar matrix DAX |
| 10 AI Decision Assistant | Por que o indicador mudou? | modelo semântico governado | typed tools, DAX read-only, explicabilidade |

**Contagem:** Home + 10 páginas analíticas. Caso o escopo de publicação exija exatamente 10 páginas, integrar o calendário à página Comercial ou a Home ao centro executivo; documentar a escolha.

## 7. Padrões de experiência
- Barra superior: logo discreto, título, período, data de atualização e chips de filtros ativos.
- Painel de filtros oculto por botão; bookmarks sincronizados; estado de filtro sempre legível.
- Tooltips HTML padronizados: KPI, contexto, período, comparativo e micrográfico.
- Drill-through: Cliente, Produto, Filial, Pedido, Transportadora; manter contexto de origem.
- Navegação consistente; reset de filtros e botão Home.
- Nunca usar valores inventados como se fossem medidas calculadas; distinguir mockup de dado real.
- Evitar textos narrativos longos nas telas; insights objetivos e acionáveis quando derivados de dados.

## 8. Regras de negócio para validação
- Receita: partir de `fFaturamento[ReceitaLiquida]`; não somar receita de itens com receita de fatura na mesma medida.
- CMV e margem: partir da mesma granularidade de faturamento.
- OTIF: `NoPrazo = 1` E `InFull = 1`; informar denominador e recortes.
- Churn: estabelecer 90 dias sem compra como hipótese, separar novos, recorrentes, perdidos e reativados; não classificar clientes recém-adquiridos como churn.
- Contas a receber: aging em uma data de corte, considerando pagamentos posteriores à data de corte.
- Estoque: usar apenas cobertura amostral, sem afirmar ruptura global do catálogo.
- WMS: posições e ocupação amostrais; não calcular capacidade total não fornecida.
- Metas/orçamento: conferir grão e distribuição; evitar multiplicar metas ao cruzar dimensões.
- Previsões: evitar vazamento temporal e não extrapolar para fatos realizados.

## 9. Etapas de implementação obrigatórias
**Fase A — Diagnóstico:** inventariar arquivos, conferir schema, contagens, datas, chaves, nulos e reconciliações; registrar anomalias.

**Fase B — Modelo:** criar PBIP, Power Query, dimensões, relacionamentos sem ambiguidade, calendário e medidas base; gerar mapa de relações.

**Fase C — Design system:** tema JSON, componentes HTML/CSS/SVG reutilizáveis, tipografia, fundos, navegação, tooltips e estados vazios.

**Fase D — Páginas:** desenvolver uma página por vez, testar filtros, medidas, desempenho e legibilidade; capturar evidências visuais.

**Fase E — Avançados:** Deneb, calendário, mapa, simulador, WMS 3D externo e agente opcional; documentar pré-requisitos/licenças.

**Fase F — QA e entrega:** comparar totais com SQL, revisar relações e contexto de filtro, medir tempo de renderização, remover recursos não usados com cautela, gerar documentação e checklist de publicação.

## 10. Critérios de aceite
- PBIP abre sem erros; caminhos de dados parametrizados, sem dependência de diretórios absolutos de outra máquina.
- Todas as 26 tabelas de origem inventariadas; carregar no modelo somente o necessário e documentar exclusões.
- Medidas base reconciliadas com consultas SQL e totalizações por período/filial.
- Sem multiplicação indevida de faturamento por join entre fatos.
- Filtros, tooltips, bookmarks e drill-through testados.
- Layouts consistentes com identidade visual e legíveis em 16:9.
- Limitações de amostragem e dados sintéticos explicitadas.
- Recursos 3D e IA com fallback caso não sejam implementáveis no ambiente.
- Entregar `README.md`, `MODELO_SEMANTICO.md`, `DICIONARIO_MEDIDAS.md`, `REGRAS_NEGOCIO.md`, `GUIA_VISUAL.md`, `QA_CHECKLIST.md`, tema JSON, código PBIP e screenshots.

## 11. Prompt de ativação para Claude/Codex
> Atue como arquiteto sênior de Power BI, modelador dimensional, especialista em DAX e designer de visualização de dados. Leia integralmente `SKILL_NEXUS360_POWERBI.md`, `README.md`, `DICIONARIO_DADOS.json`, `RELACIONAMENTOS.csv` e o manual de identidade visual. Antes de alterar qualquer arquivo, inspecione o banco real e apresente o plano de modelagem, riscos de cardinalidade, medidas base e mapa das páginas. Construa um PBIP incremental, com validação SQL x DAX e evidências visuais. Priorize exatidão, desempenho e poucos visuais bem escolhidos por tela. Não invente colunas, números, APIs, capacidades de visuais ou resultados de testes. Solicite apenas informações indispensáveis que não estejam nos arquivos.

## 12. Fontes e cautelas
As técnicas listadas refletem a biblioteca de Insights Visuais fornecida no projeto, não são garantias de compatibilidade automática entre ferramentas. Antes de instalar ou integrar visuais de terceiros, conferir a documentação atual do fabricante e o ambiente/licença Power BI/Fabric disponível.
