# 05 — Biblioteca de componentes visuais

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## Tokens (propostos com base no manual)
```css
:root { --nx-bg:#071528; --nx-surface:#0A1C33; --nx-teal:#10D4C4; --nx-blue:#0878C9; --nx-text:#FFFFFF; --nx-muted:#A9B9CA; --nx-radius:14px; --nx-gap:16px; }
```
Aplicar tokens centralizados em cada componente HTML, sem introduzir cores aleatórias. Definir cores semânticas de sucesso/risco somente após teste de contraste.

## Catálogo de componentes
| ID | Componente | Implementação | Uso | Restrições |
|---|---|---|---|---|
| C01 | Cabeçalho com contexto | HTML Content + DAX | Todas as telas | Mostrar filtros realmente aplicados |
| C02 | Card KPI + sparkline | HTML/CSS + SVG DAX | Executivo, comercial, financeiro | HTML sanitizado; linha usa dados reais |
| C03 | Card variação temporal | DAX + HTML | Metas e comparações | Base temporal compatível |
| C04 | Gráfico horizontal inteligente | Deneb/Vega-Lite ou nativo | Ranking de vendedor/produto | Rótulos completos, sem excesso de categorias |
| C05 | Bullet chart | Deneb | Realizado vs meta | Indicador filtrado |
| C06 | Matriz com data bars | Matriz nativa + formatação | Mix e rentabilidade | Alinhamento: primeira coluna à esquerda |
| C07 | Tooltip enriquecido | Tooltip page / HTML Content | Diagnóstico | Sem depender exclusivamente de hover |
| C08 | Quadrantes RFQ/RFM | Scatter/Deneb | Clientes | Definir faixas no modelo |
| C09 | Calendário de eventos | Matriz nativa + CONCATENATEX | Campanhas/visitas | Segunda a domingo; cruzamento de meses |
| C10 | Waterfall de margem | Nativo/Deneb | Financeiro | DRE gerencial, não auditada |
| C11 | Mapa filiais | Azure Maps | Logística | Coordenadas de `dFilial` |
| C12 | WMS 3D | Fabric App/Three.js | Armazém | Não prometer execução 3D dentro do HTML Content |
| C13 | Indicador de previsão | Linha + faixa/Deneb | Forecast | `MargemErroEstimada` requer definição |
| C14 | Simulador What-if | Parâmetros desconectados + DAX | Cenários | Não gravar transações reais |
| C15 | Navegação / filtros ocultos | Bookmarks + botões | Global | Não sobrescrever seleção do usuário |
| C16 | Agente de BI | App com ferramentas DAX tipadas | Assistente | Autenticação, auditoria e allowlist |

## Padrão HTML/CSS
- Fundo transparente, sem scroll horizontal, tipografia consistente e CSS com prefixo `.nx-`.
- SVG inline pequeno e sanitizado; evitar scripts e dependências de rede em HTML Content.
- Transições discretas e condicionais; respeitar `prefers-reduced-motion` quando suportado.
- KPI deve conter rótulo, valor, unidade, comparação válida e informação acessível.
- Tooltip deve mostrar denominador, período e regra da medida quando relevante.

## Deneb
Criar specs Vega-Lite versionadas em arquivos independentes; usar datasets do visual, não fontes externas. Priorizar escalas consistentes, tooltips, legendas e barras horizontais para categorias longas. Não criar gráficos 3D falsos no Deneb.

## Matriz calendário
`dCalendario` tem `Data`, `DiaSemana`, `SemanaISO`, `Mes`, `Ano`. Para matriz por mês, criar **PROPOSTA** coluna de semana no mês/ano e ordenação por dia da semana após validar valores reais. `CONCATENATEX` deve limitar texto por célula e lidar com múltiplos eventos. Campanhas têm `Inicio`/`Fim`, visitas têm `DataVisita`, interações `DataInteracao`; não tratar uma campanha como visita diária sem regra.

## Critérios de aceitação
Visual usa dados existentes; sem valores estáticos apresentados como reais; sem sobreposição; não quebra em filtro vazio; respeita contexto; carga aceitável; alternativa acessível; código reutilizável.
