# NEXUS 360 — Modelo semântico (F2/F3)

**Estado:** implementado e testado no Power BI Desktop 2.159.883.0 (out/2026), em 01/11/2026.
**Projeto:** `pbip/NEXUS360.pbip`, com modelo em TMDL (`NEXUS360.SemanticModel/definition`) e relatório em PBIR (ainda vazio).
**Escala:** 33 tabelas (26 de dados + 5 desconectadas + `_Parametros` + `_Medidas`), 147 medidas e 68 relacionamentos (63 ativos, 0 bidirecionais).
**Detalhe:** `RELACIONAMENTOS_MODELO.md`, `DICIONARIO_MEDIDAS.md`, `../testes/resultados/QA_MODELO_SEMANTICO.md`.

## 1. Arquitetura

```text
dados/NEXUS360/csv/*.csv  (26 arquivos, intocados)
  └─ fxLerCsv(nome)            UTF-8, vírgula, remove BOM, "" → null
     ├─ staging (não carregado): stgPedido, stgFaturaData, stgCompra, stgPosicao, stgClienteFilial, stgPrevisaoDatas
     └─ 9 dimensões + 17 fatos (tipagem explícita, cultura en-US) + _Parametros + _Medidas
```

| Parâmetro M | Valor | Uso |
|---|---|---|
| `pPastaDados` | `E:\Projetos BI\18 - Nexus 360\dados\NEXUS360\csv\` | Caminho único das fontes. Em outra máquina, basta alterar este valor |
| `pDataCorte` | 2026-10-31 | Elegibilidade histórica (`ElegivelHistorico`, `FlagRealizado`) e medida `[Data Corte]` |
O DAX lê a data de corte na tabela oculta `_Parametros`. Os limites de churn estão em tabelas DAX desconectadas (§6).

## 2. Desenho: estrelas independentes com chaves materializadas
Atende à decisão A2 do plano. `fItemPedido`, `fFaturamento`, `fEntrega`, `fDevolucao` e `fContasReceber` recebem as chaves de `fPedido` (`ClienteID`, `FilialID`, `VendedorID`, `CampanhaID`, `DataPedido`) por um merge 1:1 em `PedidoID`. O merge é seguro porque `PedidoID` é único (auditoria §2) e nenhum registro ficou sem par (QA). Resultado do desenho:

- Não há relação fato→fato nem tabela-ponte `dPedido`.
- Não há caminho ambíguo: as dimensões nunca se relacionam entre si.
- A filial analítica é sempre a filial transacional do pedido (M2). `dCliente[FilialID]`, `dVendedor[FilialID]` e `dPosicaoArmazem[FilialID]` ficam ocultas e sem relação.
- Em `fVisitaComercial` e `fInteracaoCampanha`, a filial vem do cadastro do cliente. Ela coincide com a filial transacional em 100% dos pedidos.
- Em `fOcupacaoArmazem`, a filial é materializada a partir de `dPosicaoArmazem`. Em `fContasPagar`, filial, fornecedor, produto e data da compra vêm de `fCompra`.

## 3. Datas

| Fato | Data ativa | Inativas (USERELATIONSHIP) |
|---|---|---|
| fPedido, fItemPedido | DataPedido | — |
| fFaturamento | DataFaturamento | DataPedido |
| fEntrega | DataEntrega | DataPrometida |
| fContasReceber | Vencimento | DataPagamento, DataFaturamento |
| fContasPagar | Vencimento | DataPagamento |
| Demais | a data única da tabela | — |

`dCalendario` (marcada como tabela de datas) reúne as 1.216 linhas da fonte e mais 61 linhas de extensão (mai–jun/2027), criadas no Power Query para cobrir `fPrevisao` (C3). A coluna `OrigemLinha` identifica cada caso. Nomes em PT-BR, `SemanaDoMes`, `FlagRealizado`. A data/hora automática está desligada.

A "linha em branco" de `dCalendario` vem das datas de pagamento nulas nas relações inativas (8.166 em CR e 713 em CP). É esperada e não afeta as relações ativas, todas com 0 órfãos.

## 4. Regras implementadas

### D1 — Recebimento (`fContasReceber[StatusRecebimento]`)
| Status | Regra | Títulos | Valor título |
|---|---|---:|---:|
| Recebido | `ValorPago > 0` **e** `DataPagamento` preenchida **e** `DataPagamento >= DataFaturamento` | 73.496 | R$ 425.826.672,87 |
| Em aberto | `ValorPago = 0` **e** sem `DataPagamento` | 715 | R$ 4.155.054,32 |
| Inconsistente | qualquer outra combinação | 14.768 | R$ 85.302.231,77 |

`MotivoInconsistencia`: data de pagamento sem valor pago (7.283), valor pago sem data de pagamento (7.451) e pagamento anterior ao faturamento (34). Os inconsistentes continuam na base e ficam fora de recebimento confirmado, saldo e inadimplência. O acompanhamento é feito em `09 Qualidade\Recebimento`.

As medidas as-of (`Saldo … (Data Ref.)`, `Inadimplência %`) reconstroem a posição em qualquer data: um título conta como aberto naquela data se estiver "Em aberto", ou se estiver "Recebido" com pagamento posterior à data.

### D2 — Elegibilidade histórica (sem exclusão física)
`ElegivelHistorico` (1/0) existe em `fDespesa`, `fCompra`, `fContasPagar` (pela data da compra), `fEstoqueMensal`, `fMovimentoEstoque` e `fOcupacaoArmazem`. As medidas de realizado filtram `= 1`. `fMeta`, `fOrcamento` e `fPrevisao` não recebem o filtro, porque são planejamento. A auditoria fica em `09 Qualidade\Corte temporal`:

| Medida | Valor |
|---|---:|
| Registros pós-corte (total) | 8.424 |
| Despesas pós-corte | 144 / R$ 3.763.520,62 |
| Compras pós-corte | 480 / R$ 22.212.197,33 |
| Contas a pagar pós-corte | 480 / R$ 22.212.197,33 (mesmas compras, não somar) |
| Estoque / movimentos / ocupação pós-corte | 4.800 / 1.680 / 840 |
| Valor financeiro pós-corte (despesas + compras) | R$ 25.975.717,95 |
| Data máxima encontrada | 31/12/2026 |
| Data de corte | 31/10/2026 |

### Outras regras
- **Receita** vem só de `fFaturamento`. Os itens faturados (`[Valor Itens Faturados]`) somam exatamente a receita, porém datados pelo pedido.
- **Metas de razão** (C8): `Meta Margem Bruta % (ponderada)` usa a meta de faturamento de cada filial-mês como peso. `Meta OTIF %` é uma média simples, com rótulo explícito.
- **Comparações temporais** (`LY`, `YTD LY`, `YoY`) são limitadas a datas ≤ corte. Por isso jan–out/2026 é comparado com jan–out/2025, e não com 2025 inteiro.
- **Snapshots** (estoque e WMS) usam o último mês elegível do contexto e nunca somam meses.
- **Clientes**: ver §6. `DataCadastro` não é usada (C6).

## 5. Limitações conhecidas
1. **Receita por produto (resolvida em 01/11/2026).** Receita Líquida, CMV, Faturas, Desconto Médio Ponderado, Clientes Positivados e Vendedores com Venda agora vêm de `fItemPedido` (itens com `StatusPedido = "Faturado"`), pela relação inativa `fItemPedido[DataFaturamento] → dCalendario` ativada com `USERELATIONSHIP`. Não houve rateio: a soma dos itens faturados é igual à receita das faturas em todos os grãos testados (408 células mês × filial, 1.035 dias, 32.225 clientes; diferença 0). Agora reagem a produto, categoria, subcategoria e marca.
   - **Continuam sem produto**, porque a fonte não tem esse grão: impostos (≈7,5% mesmo em faturas isentas, sem regra de alocação), frete, devoluções, despesas e metas. As medidas que dependem deles ficam em branco quando há filtro de produto (guarda `[Filtro de Produto Ativo]`) e a barra de filtros mostra um aviso.
   - **Fornecedor:** não há atribuição válida (8.473 produtos vendidos nunca comprados; 1.727 com mais de um fornecedor). A receita por fornecedor não foi implementada.
2. As medidas de campanha só servem como atributo: 97% dos pedidos com campanha estão fora da vigência (C7).
3. Estoque e WMS são amostrais. A ocupação % é a distribuição de status na amostra, não a capacidade da filial (C9).
4. Out/2026 tem datas truncadas em 31/10 (C5): OTIF, vencimentos e pagamentos do mês ficam distorcidos.
5. `Margem Erro Estimada` não tem semântica validada e não deve ser usada como intervalo de confiança.
6. `pPastaDados` é um caminho absoluto, porque o Power Query não aceita caminho relativo para arquivos locais. Em outra máquina, ajuste o parâmetro.

## 6. Clientes: status, eventos e recompra (aprovado em 01/11/2026)
Motivo da revisão: o intervalo mediano entre faturas é de 173 dias (média 225; 56.754 intervalos). A janela anterior de 90 dias classificava 78% da base como churn.

**Parâmetros desconectados** (sem relação, lidos por `SELECTEDVALUE`):
| Tabela | Valores | Padrão | Medida |
|---|---|---:|---|
| `Param Limite Ativo` | 60–300 (passo 30) | 180 | `[Limite Ativo (dias)]`, limitada a Limite Churn − 1 |
| `Param Limite Churn` | 180, 270, 365, 450, 540, 730 | 365 | `[Limite Churn (dias)]` |
| `Param Janela Comparativa` | 90, 180, 270, 365, 540, 730 | — | eixo de `[Taxa de Churn (Janela Comparativa) %]` |
| `dStatusCliente` | Novo, Ativo, Reativado, Em risco, Churn (+ Ordem, Grupo) | — | eixo de `[Clientes por Status]` |
| `dCohortOffset` | 0–33 meses | — | eixo da retenção por cohort |

O parâmetro M `pJanelaChurnDias` foi removido. A regra existe agora num único lugar.

**Status atual na Data Referência** (mutuamente exclusivos, avaliados nesta ordem; compra = fatura):
1. **Churn**: dias desde a última compra ≥ Limite Churn.
2. **Em risco**: dias desde a última compra ≥ Limite Ativo.
3. **Novo**: primeira compra há menos de Limite Ativo dias. *Interpretação de "primeiro ciclo de compra" = primeira compra dentro da janela de atividade.*
4. **Reativado**: houve compra de retorno (fatura com `DiasDesdeCompraAnterior` ≥ Limite Churn) há menos de Limite Ativo dias.
5. **Ativo**: os demais com compra recente.

Clientes sem fatura até a Data Referência não são classificados. Um cliente novo nunca vira churn por falta de histórico: churn exige ≥ 365 dias sem compra, o que só ocorre se a primeira compra tiver mais de 365 dias.

**Base técnica:** `fFaturamento[DataCompraAnterior]` e `[DiasDesdeCompraAnterior]`, calculadas no Power Query (ordem ClienteID, DataFaturamento, FaturaID; 0 = mesma data). Também `dCliente[CohortInicio]` e `[Cohort]` (calculadas).

**Eventos no período** (análise temporal): `Reativações no Período` (clientes com compra de retorno no período), `Receita Recuperada` (receita do período desses clientes a partir da primeira compra de retorno) e `Clientes Novos (no período)`.
**Recompra:** intervalo médio/mediano entre compras, `Compras por Cliente` (faturas por cliente positivado) e `Taxa de Recompra %` (clientes com mais de uma fatura no período).
**Cohort:** `Tamanho Cohort`, `Clientes Retidos (Cohort)`, `Retenção Cohort %` (linhas `dCliente[Cohort]` × colunas `dCohortOffset`).

| Data Ref. (180/365) | Novo | Ativo | Reativado | Em risco | Churn | Taxa de churn |
|---|---:|---:|---:|---:|---:|---:|
| 31/10/2026 | 1.543 | 6.287 | 4.759 | 8.187 | 11.449 | 35,5% |
| 31/12/2025 | 3.288 | 6.320 | 2.970 | 8.199 | 8.368 | 28,7% |

## 6a. Decisões de apresentação registradas (fase visual)
- **Canvas:** 1920×1080. Os fundos de 1672×941 serão ampliados 1,148× com proporção preservada. A nitidez será conferida na F4, e se houver perda relevante será registrada a necessidade de reexportação.
- **Mapa da Home:** o mapa desenhado no fundo é artístico, sem projeção conhecida, e seus pontos estão no Norte e Nordeste, onde não há filiais. Decisão: mapa SVG independente, com projeção a partir de `dFilial[Latitude/Longitude]` (12 filiais reais). O fundo fica como elemento decorativo, e os pontos ilustrativos não são associados a dados. Conexões só serão desenhadas se houver fluxo nos dados entre filiais. Hoje não há tabela de transferência origem→destino; `fMovimentoEstoque` tem "Transferência" sem destino. Portanto, não haverá rotas entre filiais.
- **Fabric / Service:** não verificado. A conta está desconectada do Desktop e não são inseridas credenciais pela automação. O Desktop segue como ambiente principal.

## 7. Reprodutibilidade
`pbip/_gerador/gerar_tmdl.py` e `gerar_medidas.py` criaram a primeira versão do TMDL. A partir de agora, a fonte de verdade é o TMDL salvo pelo Desktop. Rodar os geradores de novo cria novas lineageTags e substitui as edições feitas depois; use-os só para recriar o projeto do zero. `gerar_docs_modelo.py` refaz o dicionário de medidas e a tabela de relações a partir do TMDL atual.
