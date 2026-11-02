# QA — Operations Calendar

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Quando acontecem campanhas, visitas e entregas, e em que dias a operação falha?

## Componentes
- Seletor visível de mês (seleção única, padrão out/2026)
- KPIs HTML do período ou do dia selecionado
- Matriz nativa semana × dia (segunda a domingo) com célula SVG: dia, campanha ativa, visitas/pedidos, entregas/OTIF
- Tooltip ttDia
- Deneb: cronograma das campanhas do mês com marcador do dia selecionado
- Tabela Top 10 vendedores por visitas

## Medidas criadas/usadas
- `Visitas`
- `Visitas com Pedido`
- `Conversão de Visitas %`
- `Interações de Campanha`
- `Conversões de Campanha`
- `Campanhas Ativas (período)`
- `Campanha no Período`
- `Período Início`
- `Período Fim`
- `Dia Selecionado`
- `UX Calendário Dia`
- `UX Calendário KPIs`
- `UX Tooltip Dia`

## Interações e validações
- Clique no dia 07/10 filtra KPIs, cronograma e tabela: 10 visitas, 81 entregas (= consulta DAX por dia)
- Tooltip 22/10: 12 visitas, 76 entregas (= consulta)
- Campanha como intervalo (05/10–31/10 e 24/09–13/10)
- Dias de outros meses vazios

## Performance (Performance Analyzer)
Máximo 265 ms (matriz).

## Problemas e correções
- % sem escape no data URI quebrava o SVG → %25
- Todos os dias abaixo da meta OTIF (64% vs 94%): borda passou a marcar dias 5 p.p. abaixo da média do mês
- Total da tabela Top 10 enganava → removido
- Date + número virava texto no Vega → time()

## Pendências
- Skill "Interactive Calendar Matrix DAX" não disponível nesta sessão: implementado com matriz nativa + SVG (doc 05 C09)
- Sem agenda futura de visitas na fonte
