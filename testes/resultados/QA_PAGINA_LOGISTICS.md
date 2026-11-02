# QA — Logistics Control Tower

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Onde e por que a entrega falha, e quanto custa?

## Componentes
- KPIs com bullet de OTIF vs meta
- Mapa SVG de OTIF por filial (origem; sem rotas)
- Combo OTIF mensal
- Deneb: distribuição de dias de atraso
- Deneb: dispersão transportadoras OTIF × frete
- Tabela das 12 piores transportadoras, tooltip ttTransportadora

## Medidas criadas/usadas
- `UX Logística Mapa`
- `UX Cor OTIF Relativo`
- `UX Cor Desvio OTIF`

## Interações e validações
- Tooltip de transportadora: OK

## Performance (Performance Analyzer)
Máximo 207 ms.

## Problemas e correções
- Tabela com rolagem → rowPadding 2

## Pendências
- Sem destino geográfico na fonte; out/2026 com datas truncadas (C5)
