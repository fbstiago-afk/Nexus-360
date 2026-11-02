# 08 — Plano de testes, qualidade e performance

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## Auditoria preliminar executada sobre SQLite
Foram inspecionadas 26 tabelas e 45 relações candidatas. As verificações abaixo são resultados reais do banco atual, não garantia de qualidade do PBIP futuro.

| Verificação | Falhas/órfãos | Status |
|---|---:|---|
| `Unicidade dCalendario.Data` | 0 | PASS |
| `Unicidade dCampanha.CampanhaID` | 0 | PASS |
| `Unicidade dCliente.ClienteID` | 0 | PASS |
| `Unicidade dFilial.FilialID` | 0 | PASS |
| `Unicidade dFornecedor.FornecedorID` | 0 | PASS |
| `Unicidade dPosicaoArmazem.PosicaoID` | 0 | PASS |
| `Unicidade dProduto.ProdutoID` | 0 | PASS |
| `Unicidade dTransportadora.TransportadoraID` | 0 | PASS |
| `Unicidade dVendedor.VendedorID` | 0 | PASS |
| `Unicidade fCompra.CompraID` | 0 | PASS |
| `Unicidade fContasPagar.PagamentoID` | 0 | PASS |
| `Unicidade fContasReceber.TituloID` | 0 | PASS |
| `Unicidade fDespesa.DespesaID` | 0 | PASS |
| `Unicidade fDevolucao.DevolucaoID` | 0 | PASS |
| `Unicidade fEntrega.EntregaID` | 0 | PASS |
| `Unicidade fEstoqueMensal.EstoqueID` | 0 | PASS |
| `Unicidade fFaturamento.FaturaID` | 0 | PASS |
| `Unicidade fInteracaoCampanha.InteracaoID` | 0 | PASS |
| `Unicidade fItemPedido.ItemPedidoID` | 0 | PASS |
| `Unicidade fMeta.MetaID` | 0 | PASS |
| `Unicidade fMovimentoEstoque.MovimentoID` | 0 | PASS |
| `Unicidade fOcupacaoArmazem.OcupacaoID` | 0 | PASS |
| `Unicidade fOrcamento.OrcamentoID` | 0 | PASS |
| `Unicidade fPedido.PedidoID` | 0 | PASS |
| `Unicidade fPrevisao.PrevisaoID` | 0 | PASS |
| `Unicidade fVisitaComercial.VisitaID` | 0 | PASS |
| `FK fPedido.ClienteID -> dCliente.ClienteID` | 0 | PASS |
| `FK fPedido.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fPedido.VendedorID -> dVendedor.VendedorID` | 0 | PASS |
| `FK fPedido.CampanhaID -> dCampanha.CampanhaID` | 0 | PASS |
| `FK fItemPedido.PedidoID -> fPedido.PedidoID` | 0 | PASS |
| `FK fItemPedido.ProdutoID -> dProduto.ProdutoID` | 0 | PASS |
| `FK fFaturamento.PedidoID -> fPedido.PedidoID` | 0 | PASS |
| `FK fEntrega.PedidoID -> fPedido.PedidoID` | 0 | PASS |
| `FK fEntrega.TransportadoraID -> dTransportadora.TransportadoraID` | 0 | PASS |
| `FK fContasReceber.PedidoID -> fPedido.PedidoID` | 0 | PASS |
| `FK fContasReceber.ClienteID -> dCliente.ClienteID` | 0 | PASS |
| `FK fDevolucao.PedidoID -> fPedido.PedidoID` | 0 | PASS |
| `FK fCompra.FornecedorID -> dFornecedor.FornecedorID` | 0 | PASS |
| `FK fCompra.ProdutoID -> dProduto.ProdutoID` | 0 | PASS |
| `FK fContasPagar.CompraID -> fCompra.CompraID` | 0 | PASS |
| `FK fEstoqueMensal.ProdutoID -> dProduto.ProdutoID` | 0 | PASS |
| `FK fOcupacaoArmazem.PosicaoID -> dPosicaoArmazem.PosicaoID` | 0 | PASS |
| `FK fOcupacaoArmazem.ProdutoID -> dProduto.ProdutoID` | 0 | PASS |
| `FK fVisitaComercial.ClienteID -> dCliente.ClienteID` | 0 | PASS |
| `FK fVisitaComercial.VendedorID -> dVendedor.VendedorID` | 0 | PASS |
| `FK fInteracaoCampanha.CampanhaID -> dCampanha.CampanhaID` | 0 | PASS |
| `FK fInteracaoCampanha.ClienteID -> dCliente.ClienteID` | 0 | PASS |
| `FK fEstoqueMensal.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fCompra.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fMovimentoEstoque.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fOrcamento.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fMeta.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fDespesa.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fPrevisao.FilialID -> dFilial.FilialID` | 0 | PASS |
| `FK fMovimentoEstoque.ProdutoID -> dProduto.ProdutoID` | 0 | PASS |
| `FK fOrcamento.DataReferencia -> dCalendario.Data` | 0 | PASS |
| `FK fMeta.DataReferencia -> dCalendario.Data` | 0 | PASS |
| `FK fDespesa.DataReferencia -> dCalendario.Data` | 0 | PASS |
| `FK fPrevisao.DataReferencia -> dCalendario.Data` | 24 | REVIEW |
| `FK fEstoqueMensal.DataReferencia -> dCalendario.Data` | 0 | PASS |
| `FK fPedido.DataPedido -> dCalendario.Data` | 0 | PASS |
| `FK fFaturamento.DataFaturamento -> dCalendario.Data` | 0 | PASS |
| `FK fEntrega.DataEntrega -> dCalendario.Data` | 0 | PASS |
| `FK fEntrega.DataPrometida -> dCalendario.Data` | 0 | PASS |
| `FK fContasReceber.Vencimento -> dCalendario.Data` | 0 | PASS |
| `FK fDevolucao.DataDevolucao -> dCalendario.Data` | 0 | PASS |
| `FK fCompra.DataCompra -> dCalendario.Data` | 0 | PASS |
| `FK fMovimentoEstoque.DataMovimento -> dCalendario.Data` | 0 | PASS |
| `FK fVisitaComercial.DataVisita -> dCalendario.Data` | 0 | PASS |
| `FK fInteracaoCampanha.DataInteracao -> dCalendario.Data` | 0 | PASS |

## SQL reproduzível
```sql
SELECT COUNT(*) AS registros, SUM(ReceitaLiquida) AS receita, SUM(CMV) AS cmv
FROM fFaturamento;
SELECT COUNT(*) AS pedidos, COUNT(DISTINCT PedidoID) AS pedidos_distintos FROM fPedido;
SELECT COUNT(*) AS otif FROM fEntrega WHERE NoPrazo = 1 AND InFull = 1;
SELECT COUNT(*) AS faturas_sem_pedido
FROM fFaturamento f LEFT JOIN fPedido p ON f.PedidoID = p.PedidoID
WHERE p.PedidoID IS NULL;
SELECT DataReferencia, FilialID, COUNT(*) AS linhas
FROM fEstoqueMensal GROUP BY DataReferencia, FilialID;
```

## Testes obrigatórios antes da implementação
| ID | Área | Teste | Critério |
|---|---|---|---|
| QA01 | Ingestão | Importar 26 tabelas sem erros de tipo | Zero erros silenciosos |
| QA02 | Chaves | PK e FK verificadas | Sem órfãos não explicados |
| QA03 | Grão | Não multiplicar faturas ao filtrar produtos | Totais reconciliados |
| QA04 | Datas | Realizado não inclui meses futuros | Corte 2026-10-31 |
| QA05 | DAX | Receita, CMV, margem, pedidos e OTIF vs SQL | Diferença 0 após mesma regra |
| QA06 | Metas | Comparar apenas indicador e mês compatíveis | Sem agregação cruzada |
| QA07 | Churn | Testar cliente novo, ativo, inativo e reativado | Casos reproduzíveis |
| QA08 | Estoque | Último snapshot, não soma mensal | Coerência temporal |
| QA09 | Financeiro | Inadimplência em data de corte | Sem look-ahead |
| QA10 | UI | 11 páginas, botões e filtros | Sem elementos cortados |
| QA11 | Visual | Deneb/HTML/tooltip/contraste | Fallback funcional |
| QA12 | Performance | Medir render e DAX em máquina referência | Metas documentadas |
| QA13 | Segurança | Testar acesso e RLS se usado | Nenhum dado fora do escopo |
| QA14 | Publicação | Abrir PBIP, atualizar e publicar | Sem credenciais expostas |

## Performance
Usar Performance Analyzer para identificar visuais caros, DAX Studio (Server Timings/Query Plan) para medidas complexas, VertiPaq Analyzer quando disponível para cardinalidade e compressão. Definir baseline com hardware, versão do Power BI, modo de armazenamento e filtros. Metas **propostas**: 5 s abertura / 2 s interação comum; nunca afirmar atingimento sem benchmark.

## Evidências de aceite
Guardar screenshots das 11 páginas, resultados SQL, lista de medidas, arquivo de relacionamentos finais, tempos de render, log de refresh, checklist de acessibilidade, issues conhecidas e versão de PBIP. Marcar como **BLOQUEADO** qualquer indicador que dependa de campo inexistente ou sem regra validada.
