# NEXUS 360 — QA do modelo semântico (F2/F3)

**Data:** 01/11/2026. **Ambiente:** Power BI Desktop 2.159.883.0 (Microsoft Store, out/2026), engine 17.0.93.23. Consultas DAX feitas pelo powerbi-modeling-mcp em localhost:57091 (porta obtida pelo DAX Studio 3.4.0 aberto via Ferramentas externas).
**Referência independente:** SQLite reconstruído a partir dos CSV, script `testes/scripts/a03_esperados_modelo.py`, saída `a03_esperados_modelo.json`.

## 1. Carga e estrutura
| Teste | Resultado | Status |
|---|---|---|
| Abertura do PBIP com TMDL gerado | Abriu sem erro de sintaxe; 28 tabelas | PASS |
| Refresh completo (esquema + dados) | Sem erros. Refresh Full pelo MCP: ≈21 s de relógio, medido entre chamadas e incluindo overhead da ferramenta | PASS |
| Linhas por tabela (25 tabelas de origem) | Iguais aos CSV (soma 849.620, com os registros pós-corte preservados) | PASS |
| dCalendario | 1.277 = 1.216 da fonte + 61 da extensão (mai–jun/2027) | PASS |
| Órfãos nas 63 relações ativas | 0 em todas as datas e dimensões | PASS |
| Linha em branco em dCampanha | 84.903 pedidos sem campanha (FK nula na fonte) | PASS (esperado) |
| Linha em branco em dCalendario | DataPagamento nula nas relações inativas de CR/CP | PASS (esperado) |
| Merges de chaves (fatura, CR, ocupação, CP) | 0 linhas sem chave materializada | PASS |
| Relações bidirecionais / M:N / fato-fato | 0 / 0 / 0 | PASS |
| Data/hora automática | Desligada (`__PBI_TimeIntelligenceEnabled = 0`) | PASS |

## 2. Reconciliação DAX × SQL (diferença exigida: 0)
| Medida | DAX | SQL | Status |
|---|---:|---:|---|
| Receita Líquida | 515.283.958,96 | 515.283.958,96 | PASS |
| CMV | 376.561.791,51 | 376.561.791,51 | PASS |
| Impostos | 38.646.291,11 | 38.646.291,11 | PASS |
| Margem Bruta % | 26,9215% | 26,9215% | PASS |
| Faturas / Pedidos / Faturados / Cancelados / Pendentes | 88.979 / 100.000 / 88.979 / 3.457 / 7.564 | idem | PASS |
| Valor Itens (todos) / Itens Faturados | 579.865.662,52 / 515.283.958,96 | idem | PASS |
| Quantidade Itens Faturados | 2.109.893 | 2.109.893 | PASS |
| Valor Devolvido / Devoluções | 4.984.803,21 / 3.159 | idem | PASS |
| Despesas Operacionais (elegíveis) | 71.028.404,16 | 71.028.404,16 | PASS |
| Desconto Médio Ponderado % | 8,21402% | 8,21402% | PASS |
| Clientes Positivados | 32.225 | 32.225 | PASS |
| Entregas / OTIF / No Prazo / In Full / Ocorrência | 88.979 / 56.768 / 60.703 / 83.221 / 22.391 | idem | PASS |
| OTIF % | 63,7993% | 63,7993% | PASS |
| Custo Frete | 23.043.925,05 | 23.043.925,05 | PASS |
| Atraso Médio / Lead Time Médio (dias) | 1,9733 / 5,3229 | idem | PASS |
| Recebidos (qtd / valor) | 73.496 / 425.826.672,87 | idem | PASS |
| Em aberto (qtd / valor) | 715 / 4.155.054,32 | idem | PASS |
| Inconsistentes (qtd / valor / pago declarado) | 14.768 / 85.302.231,77 / 43.487.646,77 | idem | PASS |
| Motivos (sem valor / sem data / antes do faturamento) | 7.283 / 7.451 / 34 | idem | PASS |
| Saldo vencido em aberto em 31/10/2026 | 4.009.005,05 | 4.009.005,05 | PASS |
| Saldo a vencer em aberto em 31/10/2026 | 146.049,27 | 146.049,27 | PASS |
| Base vencida (denominador) | 414.768.613,21 | 414.768.613,21 | PASS |
| Saldo vencido em aberto em 31/12/2025 (as-of histórico) | 5.496.038,68 | 5.496.038,68 | PASS |
| Pós-corte: despesas, compras, CP (qtd/R$) | 144/3.763.520,62 · 480/22.212.197,33 · 480/22.212.197,33 | idem | PASS |
| Pós-corte: estoque / movimentos / ocupação | 4.800 / 1.680 / 840 | idem | PASS |
| Data Máxima Encontrada / Data Corte | 31/12/2026 / 31/10/2026 | idem | PASS |
| Clientes com histórico / ativos 90d em 31/10/2026 (regra antiga, substituída em 3a) | 32.225 / 6.992 | idem | PASS |
| Clientes novos 2025 / 2026 | 8.514 / 3.080 | idem | PASS |
| Snapshot estoque out/26 (un, R$, linhas, ruptura, abaixo do mín.) | 544.128 / 95.274.368,97 / 2.400 / 6 / 333 | idem | PASS |
| Snapshot WMS out/26 (registros, posições, paletes) | 420 / 398 / 1.049 | idem | PASS |
| Compras elegíveis (qtd / R$) | 8.160 / 381.878.644,53 | idem | PASS |
| Contas a pagar elegíveis (total / pago / aberto) | 381.878.644,53 / 350.253.148,72 / 31.625.495,81 | idem | PASS |
| Meta faturamento (total / até corte) | 494.870.779,94 / 470.000.292,87 | idem | PASS |
| Meta margem ponderada até corte | 28,2983% | 28,2983% | PASS |
| Meta OTIF média simples | 93,8187% | 93,8187% | PASS |
| Receita 2026 / LY (jan–out/2025) | 151.079.018,69 / 154.406.313,04 | idem | PASS |
| Receita YTD LY 2026 | 154.406.313,04 | 154.406.313,04 | PASS |
| Receita out/26 / mês anterior | 15.649.875,62 / 14.856.924,90 | idem | PASS |
| Receita filial 1 | 42.647.109,09 | 42.647.109,09 | PASS |
| Itens faturados, categoria Alimentos | 155.769.780,80 | 155.769.780,80 | PASS |
| Receita Prevista total | 82.242.367,18 | 82.242.367,18 | PASS |

## 3. Comportamento de contexto
| Teste | Resultado | Status |
|---|---|---|
| 41 medidas derivadas por ano (2024–2027 + total) | Sem erro de avaliação; 180 ms | PASS |
| Medidas as-of em período sem realizado (2027) | Inicialmente mostravam o valor do corte. **Corrigido** em `[Data Referência]` (BLANK quando o contexto inteiro é posterior ao corte) e testado de novo | PASS (após correção) |
| Receita filtrada por `dProduto` | Substituído em 01/11: receita passou a vir dos itens faturados e reage a produto (ver seção 5) | PASS |
| Clientes Novos/Reativados/Ativos/Churn por mês × filial (22 meses × 12) | 616 ms (SE 219 ms, FE 344 ms) | PASS |

## 3a. Revisão de clientes/churn (01/11/2026, 20:20)
Referência independente: `testes/scripts/a04_esperados_churn.py` → `a04_esperados_churn.json` (Python sobre o SQLite de auditoria).

| Teste | DAX | Python/SQL | Status |
|---|---:|---:|---|
| Faturas após nova etapa PQ / receita | 88.979 / 515.283.958,96 | idem | PASS |
| Intervalos entre compras / média / mediana | 56.754 / 225,12 / 173 | idem | PASS |
| Status 31/10/2026, 180/365 (Novo, Ativo, Reativado, Em risco, Churn) | 1.543 / 6.287 / 4.759 / 8.187 / 11.449 | idem | PASS |
| Soma dos status = clientes com histórico | 32.225 | 32.225 | PASS |
| Status 31/12/2025, 180/365 | 3.288 / 6.320 / 2.970 / 8.199 / 8.368 | idem | PASS |
| Status 31/10/2026 com parâmetros 90/180 (teste dos parâmetros) | 684 / 1.941 / 4.367 / 5.597 / 19.636 | idem | PASS |
| Taxa de churn 31/10/2026 (365) | 35,53% | 35,53% | PASS |
| Reativações no período 2025 / 2026 | 4.261 / 7.553 | idem | PASS |
| Receita recuperada 2025 / 2026 | 32.815.544,75 / 59.393.894,99 | idem | PASS |
| Compras por cliente 2026 / taxa de recompra 2026 | 1,4196 / 32,87% | idem | PASS |
| Churn por janela comparativa (90/180/270/365/540/730) | 78,30 / 60,93 / 47,19 / 35,53 / 19,99 / 9,50% | idem | PASS |
| Cohort 2025-01: tamanho / m0 / m3 / m12 | 1.072 / 1.072 / 61 / 78 | idem | PASS |
| Clientes Novos (no período) 2025 / 2026 | 8.514 / 3.080 | idem | PASS |

**Performance:** 3 cenários × 8 medidas de status em 1,5 s. Evolução mensal 34 meses × 5 status em **2,8 s** (FE 2,7 s, SE 31 ms). Fica dentro da meta proposta de 5 s por página, mas acima da meta de 2 s por interação se usada com segmentação. Candidato a otimização na fase visual: limitar o eixo a 12–24 meses ou materializar a última compra por cliente-mês.

**Mudanças estruturais:** parâmetro M `pJanelaChurnDias` e coluna `_Parametros[JanelaChurnDias]` removidos (nenhuma referência restante no TMDL). 6 medidas antigas de clientes substituídas por 23 novas (130 → 147).

## 5. Receita por item faturado (01/11/2026, 20:40)
Mudança: receita, CMV, faturas, desconto, clientes positivados e vendedores passaram de `fFaturamento` para `fItemPedido` (itens faturados, relação de data de faturamento por `USERELATIONSHIP`). Backup em `backups/20261101_2327_pre_receita_item`.

| Teste | DAX | SQL/Python | Status |
|---|---:|---:|---|
| Receita total | 515.283.958,96 | 515.283.958,96 | PASS |
| Receita mês × filial (408 células) | diferença máx. 0 | — | PASS |
| Receita por dia (1.035 dias) / por cliente (32.225) | diferença máx. 0 | — | PASS |
| Categoria Alimentos | 155.769.780,80 | 155.769.780,80 | PASS |
| Recortes de produto com período (2024 / LY de 2026) | 54.438.197,34 / 46.563.667,94 | idem | PASS |
| Marca Prime em 2026 | 15.574.157,68 | 15.574.157,68 | PASS |
| Status de churn em 31/10/2026 | 1.543 / 6.287 / 4.759 / 8.187 / 11.449 | inalterados | PASS |
| Receita Recuperada após a mudança | erro detectado (R$ 545 bi) e corrigido para `fFaturamento[ReceitaLiquida]` | 59.393.894,99 (2026) | PASS (após correção) |
| Medidas sem grão de produto com filtro de produto | BLANK (guarda `[Filtro de Produto Ativo]`) | — | PASS |

## 4. Não executado nesta etapa
- Performance Analyzer, que exige visuais (fase F4 em diante).
- VertiPaq Analyzer e análise de cardinalidade detalhada.
- Testes de bookmarks, filtros e tooltips (fase visual).
