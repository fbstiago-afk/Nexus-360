# NEXUS 360 — Relacionamentos do modelo

**Fonte:** `relationships.tmdl` salvo pelo Power BI Desktop. **Total:** 69 (63 ativos, 6 inativos). Cardinalidade N:1 em todos (fato → dimensão); 0 com filtro bidirecional.

| Fato | Coluna | Dimensão | Coluna | Ativo | Filtro |
|---|---|---|---|:---:|:---:|
| fCompra | DataCompra | dCalendario | Data | Sim | Única |
| fCompra | FilialID | dFilial | FilialID | Sim | Única |
| fCompra | FornecedorID | dFornecedor | FornecedorID | Sim | Única |
| fCompra | ProdutoID | dProduto | ProdutoID | Sim | Única |
| fContasPagar | Vencimento | dCalendario | Data | Sim | Única |
| fContasPagar | FilialID | dFilial | FilialID | Sim | Única |
| fContasPagar | FornecedorID | dFornecedor | FornecedorID | Sim | Única |
| fContasPagar | ProdutoID | dProduto | ProdutoID | Sim | Única |
| fContasPagar | DataPagamento | dCalendario | Data | Não (USERELATIONSHIP) | Única |
| fContasReceber | Vencimento | dCalendario | Data | Sim | Única |
| fContasReceber | ClienteID | dCliente | ClienteID | Sim | Única |
| fContasReceber | FilialID | dFilial | FilialID | Sim | Única |
| fContasReceber | VendedorID | dVendedor | VendedorID | Sim | Única |
| fContasReceber | DataPagamento | dCalendario | Data | Não (USERELATIONSHIP) | Única |
| fContasReceber | DataFaturamento | dCalendario | Data | Não (USERELATIONSHIP) | Única |
| fDespesa | DataReferencia | dCalendario | Data | Sim | Única |
| fDespesa | FilialID | dFilial | FilialID | Sim | Única |
| fDevolucao | DataDevolucao | dCalendario | Data | Sim | Única |
| fDevolucao | ClienteID | dCliente | ClienteID | Sim | Única |
| fDevolucao | FilialID | dFilial | FilialID | Sim | Única |
| fDevolucao | VendedorID | dVendedor | VendedorID | Sim | Única |
| fEntrega | DataEntrega | dCalendario | Data | Sim | Única |
| fEntrega | ClienteID | dCliente | ClienteID | Sim | Única |
| fEntrega | FilialID | dFilial | FilialID | Sim | Única |
| fEntrega | TransportadoraID | dTransportadora | TransportadoraID | Sim | Única |
| fEntrega | VendedorID | dVendedor | VendedorID | Sim | Única |
| fEntrega | DataPrometida | dCalendario | Data | Não (USERELATIONSHIP) | Única |
| fEstoqueMensal | DataReferencia | dCalendario | Data | Sim | Única |
| fEstoqueMensal | FilialID | dFilial | FilialID | Sim | Única |
| fEstoqueMensal | ProdutoID | dProduto | ProdutoID | Sim | Única |
| fFaturamento | DataFaturamento | dCalendario | Data | Sim | Única |
| fFaturamento | CampanhaID | dCampanha | CampanhaID | Sim | Única |
| fFaturamento | ClienteID | dCliente | ClienteID | Sim | Única |
| fFaturamento | FilialID | dFilial | FilialID | Sim | Única |
| fFaturamento | VendedorID | dVendedor | VendedorID | Sim | Única |
| fFaturamento | DataPedido | dCalendario | Data | Não (USERELATIONSHIP) | Única |
| fInteracaoCampanha | DataInteracao | dCalendario | Data | Sim | Única |
| fInteracaoCampanha | CampanhaID | dCampanha | CampanhaID | Sim | Única |
| fInteracaoCampanha | ClienteID | dCliente | ClienteID | Sim | Única |
| fInteracaoCampanha | FilialID | dFilial | FilialID | Sim | Única |
| fItemPedido | DataPedido | dCalendario | Data | Sim | Única |
| fItemPedido | CampanhaID | dCampanha | CampanhaID | Sim | Única |
| fItemPedido | ClienteID | dCliente | ClienteID | Sim | Única |
| fItemPedido | FilialID | dFilial | FilialID | Sim | Única |
| fItemPedido | ProdutoID | dProduto | ProdutoID | Sim | Única |
| fItemPedido | VendedorID | dVendedor | VendedorID | Sim | Única |
| fItemPedido | DataFaturamento | dCalendario | Data | Não (USERELATIONSHIP) | Única |
| fMeta | DataReferencia | dCalendario | Data | Sim | Única |
| fMeta | FilialID | dFilial | FilialID | Sim | Única |
| fMovimentoEstoque | DataMovimento | dCalendario | Data | Sim | Única |
| fMovimentoEstoque | FilialID | dFilial | FilialID | Sim | Única |
| fMovimentoEstoque | ProdutoID | dProduto | ProdutoID | Sim | Única |
| fOcupacaoArmazem | DataReferencia | dCalendario | Data | Sim | Única |
| fOcupacaoArmazem | FilialID | dFilial | FilialID | Sim | Única |
| fOcupacaoArmazem | PosicaoID | dPosicaoArmazem | PosicaoID | Sim | Única |
| fOcupacaoArmazem | ProdutoID | dProduto | ProdutoID | Sim | Única |
| fOrcamento | DataReferencia | dCalendario | Data | Sim | Única |
| fOrcamento | FilialID | dFilial | FilialID | Sim | Única |
| fPedido | DataPedido | dCalendario | Data | Sim | Única |
| fPedido | CampanhaID | dCampanha | CampanhaID | Sim | Única |
| fPedido | ClienteID | dCliente | ClienteID | Sim | Única |
| fPedido | FilialID | dFilial | FilialID | Sim | Única |
| fPedido | VendedorID | dVendedor | VendedorID | Sim | Única |
| fPrevisao | DataReferencia | dCalendario | Data | Sim | Única |
| fPrevisao | FilialID | dFilial | FilialID | Sim | Única |
| fVisitaComercial | DataVisita | dCalendario | Data | Sim | Única |
| fVisitaComercial | ClienteID | dCliente | ClienteID | Sim | Única |
| fVisitaComercial | FilialID | dFilial | FilialID | Sim | Única |
| fVisitaComercial | VendedorID | dVendedor | VendedorID | Sim | Única |
