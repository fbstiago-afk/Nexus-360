# QA — Customer Intelligence

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Quem deixou de comprar, quem está em risco e quem vale recuperar?

## Componentes
- Painel de 5 status (Novo, Ativo, Reativado, Em risco, Churn)
- Deneb: heatmap de cohort (offset ≤ 12)
- Tabela Top 12 clientes em risco por receita 12M, tooltip ttCliente
- Grade frequência × valor
- Status mensal empilhado
- Comparação de janelas de churn

## Medidas criadas/usadas
- `UX Clientes Status`
- `UX Clientes Freq Valor`
- `Dias sem Compra (Data Ref.)`
- `Receita 12M (Data Ref.)`
- `Prioridade Risco (Receita 12M)`
- `UX Tooltip Cliente`

## Interações e validações
- Cohort sem interação de Ano/Mês (usa histórico completo)
- Tooltip de cliente: OK
- Status batem com os valores validados em QA_MODELO_SEMANTICO

## Performance (Performance Analyzer)
Status mensal 1.135 ms; painel HTML 950 ms; cohort 737 ms (acima da meta de 500 ms).

## Problemas e correções
- Eixo contínuo nas janelas → axisType Categorical
- Tabela com rolagem → Top 12

## Pendências
- Otimizar status mensal (34 meses × 5 status)
- RFM/RFQ não definido na documentação: usada grade frequência × valor
