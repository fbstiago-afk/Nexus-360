# QA — Warehouse Digital Twin

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Onde há gargalo de ocupação e estoque parado?

## Componentes
- KPIs (posições, lidas, ocupada, bloqueada, estoque, ruptura, abaixo do mínimo, parados 90+)
- Grade 2D de 4 níveis × 10×10 posições (último snapshot WMS)
- Seletor de filial de seleção única
- Matriz por zona
- Status mensal 100%
- Entradas × saídas com tooltip ttEstoqueMes

## Medidas criadas/usadas
- `UX Armazém KPIs`
- `UX Armazém Grade`
- `Produtos Parados 90+ (amostra)`
- `Posições Cadastradas`
- `UX Tooltip Estoque Mês`

## Interações e validações
- Contagens batem com SQL: 8/16/11 de 35 leituras, 94 paletes (Campinas, out/2026)
- Ruptura exibe 0,0% (COALESCE) e células sem leitura em #12304F: verificado 02/11

## Performance (Performance Analyzer)
Máximo 223 ms.

## Problemas e correções
- Ruptura em branco → COALESCE

## Pendências
- Aplicação 3D (Three.js) complementar ainda não construída
