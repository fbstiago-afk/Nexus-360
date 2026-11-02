# QA — Financial & Profitability

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Onde a margem se perde e como o caixa acompanha o resultado?

## Componentes
- DRE gerencial HTML com LY e orçamento
- Deneb: ponte do resultado vs LY
- Combo de caixa (recebimentos/pagamentos pela data de pagamento, saldo), tooltip ttMesFinanceiro
- Recebíveis HTML
- Deneb: desvio de despesa vs orçamento
- Deneb: Pareto de margem por subcategoria

## Medidas criadas/usadas
- `UX Financeiro DRE`
- `Recebimentos (Data Pagamento)`
- `Pagamentos (Data Pagamento)`
- `Saldo Recebimentos - Pagamentos`
- `Orçamento Despesa Operacional (até corte)`
- `Valor DRE Gerencial LY`

## Interações e validações
- Caixa = SQL por ano: recebimentos 130.949.566,63 / 153.290.732,67 / 141.586.373,57; pagamentos 112.248.032,09 / 122.478.616,26 / 115.526.500,37

## Performance (Performance Analyzer)
Máximo 218 ms.

## Problemas e correções
- Nenhum

## Pendências
- Caixa parcial: despesas operacionais sem registro de pagamento
