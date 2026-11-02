# 02 — Dicionário de dados e contratos

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## Inventário confirmado

**26 tabelas / 849,620 registros.** Tipos e nulidades obtidos por `PRAGMA table_info` e SQL. `NULL` não cobre strings vazias.

| Tabela | Linhas | PK declarada no SQLite |
|---|---:|---|
| `dCalendario` | 1,216 | `Data` |
| `dCampanha` | 72 | `CampanhaID` |
| `dCliente` | 35,000 | `ClienteID` |
| `dFilial` | 12 | `FilialID` |
| `dFornecedor` | 150 | `FornecedorID` |
| `dPosicaoArmazem` | 4,800 | `PosicaoID` |
| `dProduto` | 15,000 | `ProdutoID` |
| `dTransportadora` | 30 | `TransportadoraID` |
| `dVendedor` | 180 | `VendedorID` |
| `fCompra` | 8,640 | `CompraID` |
| `fContasPagar` | 8,640 | `PagamentoID` |
| `fContasReceber` | 88,979 | `TituloID` |
| `fDespesa` | 2,592 | `DespesaID` |
| `fDevolucao` | 3,159 | `DevolucaoID` |
| `fEntrega` | 88,979 | `EntregaID` |
| `fEstoqueMensal` | 86,400 | `EstoqueID` |
| `fFaturamento` | 88,979 | `FaturaID` |
| `fInteracaoCampanha` | 6,724 | `InteracaoID` |
| `fItemPedido` | 249,976 | `ItemPedidoID` |
| `fMeta` | 1,296 | `MetaID` |
| `fMovimentoEstoque` | 30,240 | `MovimentoID` |
| `fOcupacaoArmazem` | 15,120 | `OcupacaoID` |
| `fOrcamento` | 864 | `OrcamentoID` |
| `fPedido` | 100,000 | `PedidoID` |
| `fPrevisao` | 72 | `PrevisaoID` |
| `fVisitaComercial` | 12,500 | `VisitaID` |

## Contrato de importação
CSV: UTF-8 com BOM, vírgula, decimal ponto e datas `YYYY-MM-DD`, conforme README. SQLite é a fonte primária para validar o esquema; tipos TEXT de datas devem ser convertidos no Power Query. Verificar chaves, duplicatas e integridade referencial antes de ativar relacionamentos.

### `dCalendario` — 1,216 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `Data` | `TEXT` | 0 | Data ISO (verificar) |
| `Ano` | `INTEGER` | 0 | Atributo/medida |
| `Mes` | `INTEGER` | 0 | Atributo/medida |
| `NomeMes` | `TEXT` | 0 | Atributo/medida |
| `Trimestre` | `INTEGER` | 0 | Atributo/medida |
| `DiaSemana` | `INTEGER` | 0 | Atributo/medida |
| `DiaUtil` | `INTEGER` | 0 | Atributo/medida |
| `SemanaISO` | `INTEGER` | 0 | Atributo/medida |

### `dCampanha` — 72 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `CampanhaID` | `INTEGER` | 0 | Identificador/chave |
| `Campanha` | `TEXT` | 0 | Atributo/medida |
| `Inicio` | `TEXT` | 0 | Data ISO (verificar) |
| `Fim` | `TEXT` | 0 | Data ISO (verificar) |
| `Canal` | `TEXT` | 0 | Atributo/medida |
| `InvestimentoPrevisto` | `REAL` | 0 | Atributo/medida |

### `dCliente` — 35,000 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `ClienteID` | `INTEGER` | 0 | Identificador/chave |
| `RazaoSocial` | `TEXT` | 0 | Atributo/medida |
| `Segmento` | `TEXT` | 0 | Atributo/medida |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `ClassePotencial` | `TEXT` | 0 | Atributo/medida |
| `DataCadastro` | `TEXT` | 0 | Data ISO (verificar) |
| `LimiteCredito` | `REAL` | 0 | Atributo/medida |
| `CondicaoPagamento` | `TEXT` | 0 | Atributo/medida |
| `Inativo` | `INTEGER` | 0 | Atributo/medida |

### `dFilial` — 12 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `Filial` | `TEXT` | 0 | Atributo/medida |
| `Cidade` | `TEXT` | 0 | Atributo/medida |
| `UF` | `TEXT` | 0 | Atributo/medida |
| `Regiao` | `TEXT` | 0 | Atributo/medida |
| `Latitude` | `REAL` | 0 | Atributo/medida |
| `Longitude` | `REAL` | 0 | Atributo/medida |
| `CapacidadePaletes` | `INTEGER` | 0 | Atributo/medida |

### `dFornecedor` — 150 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `FornecedorID` | `INTEGER` | 0 | Identificador/chave |
| `Fornecedor` | `TEXT` | 0 | Atributo/medida |
| `UF` | `TEXT` | 0 | Atributo/medida |
| `LeadTimeMedio` | `INTEGER` | 0 | Atributo/medida |
| `Confiabilidade` | `REAL` | 0 | Atributo/medida |

### `dPosicaoArmazem` — 4,800 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `PosicaoID` | `INTEGER` | 0 | Identificador/chave |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `EnderecoWMS` | `TEXT` | 0 | Atributo/medida |
| `EixoX` | `INTEGER` | 0 | Atributo/medida |
| `EixoY` | `INTEGER` | 0 | Atributo/medida |
| `EixoZ` | `INTEGER` | 0 | Atributo/medida |
| `Zona` | `TEXT` | 0 | Atributo/medida |

### `dProduto` — 15,000 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `ProdutoID` | `INTEGER` | 0 | Identificador/chave |
| `Produto` | `TEXT` | 0 | Atributo/medida |
| `Categoria` | `TEXT` | 0 | Atributo/medida |
| `Subcategoria` | `TEXT` | 0 | Atributo/medida |
| `Marca` | `TEXT` | 0 | Atributo/medida |
| `Unidade` | `TEXT` | 0 | Atributo/medida |
| `CustoReferencia` | `REAL` | 0 | Valor numérico |
| `PrecoTabela` | `REAL` | 0 | Valor numérico |
| `LeadTimeDias` | `INTEGER` | 0 | Atributo/medida |
| `Descontinuado` | `INTEGER` | 0 | Atributo/medida |

### `dTransportadora` — 30 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `TransportadoraID` | `INTEGER` | 0 | Identificador/chave |
| `Transportadora` | `TEXT` | 0 | Atributo/medida |
| `Modal` | `TEXT` | 0 | Atributo/medida |
| `IndiceServico` | `REAL` | 0 | Atributo/medida |

### `dVendedor` — 180 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `VendedorID` | `INTEGER` | 0 | Identificador/chave |
| `Vendedor` | `TEXT` | 0 | Atributo/medida |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `Equipe` | `TEXT` | 0 | Atributo/medida |
| `DataAdmissao` | `TEXT` | 0 | Data ISO (verificar) |
| `Ativo` | `INTEGER` | 0 | Atributo/medida |

### `fCompra` — 8,640 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `CompraID` | `INTEGER` | 0 | Identificador/chave |
| `FornecedorID` | `INTEGER` | 0 | Identificador/chave |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `ProdutoID` | `INTEGER` | 0 | Identificador/chave |
| `DataCompra` | `TEXT` | 0 | Data ISO (verificar) |
| `Quantidade` | `INTEGER` | 0 | Atributo/medida |
| `ValorCompra` | `REAL` | 0 | Valor numérico |
| `StatusCompra` | `TEXT` | 0 | Atributo/medida |

### `fContasPagar` — 8,640 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `PagamentoID` | `INTEGER` | 0 | Identificador/chave |
| `CompraID` | `INTEGER` | 0 | Identificador/chave |
| `ValorTitulo` | `REAL` | 0 | Valor numérico |
| `Vencimento` | `TEXT` | 0 | Data ISO (verificar) |
| `DataPagamento` | `TEXT` | 713 | Data ISO (verificar) |

### `fContasReceber` — 88,979 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `TituloID` | `INTEGER` | 0 | Identificador/chave |
| `PedidoID` | `INTEGER` | 0 | Identificador/chave |
| `ClienteID` | `INTEGER` | 0 | Identificador/chave |
| `ValorTitulo` | `REAL` | 0 | Valor numérico |
| `Vencimento` | `TEXT` | 0 | Data ISO (verificar) |
| `DataPagamento` | `TEXT` | 8166 | Data ISO (verificar) |
| `ValorPago` | `REAL` | 0 | Valor numérico |
| `FormaPagamento` | `TEXT` | 0 | Atributo/medida |

### `fDespesa` — 2,592 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `DespesaID` | `INTEGER` | 0 | Identificador/chave |
| `DataReferencia` | `TEXT` | 0 | Data ISO (verificar) |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `Conta` | `TEXT` | 0 | Atributo/medida |
| `Tipo` | `TEXT` | 0 | Atributo/medida |
| `Valor` | `REAL` | 0 | Valor numérico |

### `fDevolucao` — 3,159 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `DevolucaoID` | `INTEGER` | 0 | Identificador/chave |
| `PedidoID` | `INTEGER` | 0 | Identificador/chave |
| `DataDevolucao` | `TEXT` | 0 | Data ISO (verificar) |
| `ValorDevolvido` | `REAL` | 0 | Valor numérico |
| `Motivo` | `TEXT` | 0 | Atributo/medida |

### `fEntrega` — 88,979 registros

**Grão operacional:** uma entrega por pedido faturado; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `EntregaID` | `INTEGER` | 0 | Identificador/chave |
| `PedidoID` | `INTEGER` | 0 | Identificador/chave |
| `TransportadoraID` | `INTEGER` | 0 | Identificador/chave |
| `DataPrometida` | `TEXT` | 0 | Data ISO (verificar) |
| `DataEntrega` | `TEXT` | 0 | Data ISO (verificar) |
| `PesoKg` | `REAL` | 0 | Atributo/medida |
| `CustoFrete` | `REAL` | 0 | Valor numérico |
| `NoPrazo` | `INTEGER` | 0 | Atributo/medida |
| `InFull` | `INTEGER` | 0 | Atributo/medida |
| `StatusEntrega` | `TEXT` | 0 | Atributo/medida |

### `fEstoqueMensal` — 86,400 registros

**Grão operacional:** amostra de SKU-filial-mês; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `EstoqueID` | `INTEGER` | 0 | Identificador/chave |
| `DataReferencia` | `TEXT` | 0 | Data ISO (verificar) |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `ProdutoID` | `INTEGER` | 0 | Identificador/chave |
| `SaldoUnidades` | `INTEGER` | 0 | Atributo/medida |
| `EstoqueMinimo` | `INTEGER` | 0 | Atributo/medida |
| `ValorEstoque` | `REAL` | 0 | Valor numérico |
| `Ruptura` | `INTEGER` | 0 | Atributo/medida |
| `DiasSemMovimento` | `INTEGER` | 0 | Atributo/medida |

### `fFaturamento` — 88,979 registros

**Grão operacional:** uma fatura por pedido faturado; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `FaturaID` | `INTEGER` | 0 | Identificador/chave |
| `PedidoID` | `INTEGER` | 0 | Identificador/chave |
| `DataFaturamento` | `TEXT` | 0 | Data ISO (verificar) |
| `ReceitaLiquida` | `REAL` | 0 | Valor numérico |
| `Impostos` | `REAL` | 0 | Valor numérico |
| `CMV` | `REAL` | 0 | Valor numérico |

### `fInteracaoCampanha` — 6,724 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `InteracaoID` | `INTEGER` | 0 | Identificador/chave |
| `CampanhaID` | `INTEGER` | 0 | Identificador/chave |
| `ClienteID` | `INTEGER` | 0 | Identificador/chave |
| `DataInteracao` | `TEXT` | 0 | Data ISO (verificar) |
| `TipoInteracao` | `TEXT` | 0 | Atributo/medida |

### `fItemPedido` — 249,976 registros

**Grão operacional:** um item de pedido; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `ItemPedidoID` | `INTEGER` | 0 | Identificador/chave |
| `PedidoID` | `INTEGER` | 0 | Identificador/chave |
| `ProdutoID` | `INTEGER` | 0 | Identificador/chave |
| `Quantidade` | `INTEGER` | 0 | Atributo/medida |
| `PrecoUnitario` | `REAL` | 0 | Valor numérico |
| `ValorLiquido` | `REAL` | 0 | Valor numérico |
| `CustoMercadoria` | `REAL` | 0 | Valor numérico |
| `Tributacao` | `TEXT` | 0 | Atributo/medida |

### `fMeta` — 1,296 registros

**Grão operacional:** filial-mês-indicador; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `MetaID` | `INTEGER` | 0 | Identificador/chave |
| `DataReferencia` | `TEXT` | 0 | Data ISO (verificar) |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `Indicador` | `TEXT` | 0 | Atributo/medida |
| `ValorMeta` | `REAL` | 0 | Valor numérico |

### `fMovimentoEstoque` — 30,240 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `MovimentoID` | `INTEGER` | 0 | Identificador/chave |
| `DataMovimento` | `TEXT` | 0 | Data ISO (verificar) |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `ProdutoID` | `INTEGER` | 0 | Identificador/chave |
| `TipoMovimento` | `TEXT` | 0 | Atributo/medida |
| `QuantidadeAssinada` | `INTEGER` | 0 | Atributo/medida |
| `Origem` | `TEXT` | 0 | Atributo/medida |

### `fOcupacaoArmazem` — 15,120 registros

**Grão operacional:** posição amostrada no tempo; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `OcupacaoID` | `INTEGER` | 0 | Identificador/chave |
| `DataReferencia` | `TEXT` | 0 | Data ISO (verificar) |
| `PosicaoID` | `INTEGER` | 0 | Identificador/chave |
| `ProdutoID` | `INTEGER` | 0 | Identificador/chave |
| `Paletes` | `INTEGER` | 0 | Atributo/medida |
| `StatusPosicao` | `TEXT` | 0 | Atributo/medida |

### `fOrcamento` — 864 registros

**Grão operacional:** filial-mês-conta; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `OrcamentoID` | `INTEGER` | 0 | Identificador/chave |
| `DataReferencia` | `TEXT` | 0 | Data ISO (verificar) |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `Conta` | `TEXT` | 0 | Atributo/medida |
| `ValorOrcado` | `REAL` | 0 | Valor numérico |

### `fPedido` — 100,000 registros

**Grão operacional:** um pedido; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `PedidoID` | `INTEGER` | 0 | Identificador/chave |
| `ClienteID` | `INTEGER` | 0 | Identificador/chave |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `VendedorID` | `INTEGER` | 0 | Identificador/chave |
| `DataPedido` | `TEXT` | 0 | Data ISO (verificar) |
| `StatusPedido` | `TEXT` | 0 | Atributo/medida |
| `DescontoPercentual` | `REAL` | 0 | Atributo/medida |
| `CampanhaID` | `INTEGER` | 84903 | Identificador/chave |
| `Canal` | `TEXT` | 0 | Atributo/medida |

### `fPrevisao` — 72 registros

**Grão operacional:** filial-mês futuro; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `PrevisaoID` | `INTEGER` | 0 | Identificador/chave |
| `DataReferencia` | `TEXT` | 0 | Data ISO (verificar) |
| `FilialID` | `INTEGER` | 0 | Identificador/chave |
| `ReceitaPrevista` | `REAL` | 0 | Valor numérico |
| `MargemErroEstimada` | `REAL` | 0 | Valor numérico |

### `fVisitaComercial` — 12,500 registros

**Grão operacional:** confirmar pelo identificador e unicidade da chave; grão inferido de README quando explicitado, demais sujeitos a QA.

| Coluna real | Tipo SQLite | Nulos | Papel / observação |
|---|---|---:|---|
| `VisitaID` | `INTEGER` | 0 | Identificador/chave |
| `VendedorID` | `INTEGER` | 0 | Identificador/chave |
| `ClienteID` | `INTEGER` | 0 | Identificador/chave |
| `DataVisita` | `TEXT` | 0 | Data ISO (verificar) |
| `TipoContato` | `TEXT` | 0 | Atributo/medida |
| `Resultado` | `TEXT` | 0 | Atributo/medida |

## Relações CANDIDATAS fornecidas (não ativar cegamente)

| Origem (FK) | Destino (PK candidata) |
|---|---|
| `fPedido[ClienteID]` | `dCliente[ClienteID]` |
| `fPedido[FilialID]` | `dFilial[FilialID]` |
| `fPedido[VendedorID]` | `dVendedor[VendedorID]` |
| `fPedido[CampanhaID]` | `dCampanha[CampanhaID]` |
| `fItemPedido[PedidoID]` | `fPedido[PedidoID]` |
| `fItemPedido[ProdutoID]` | `dProduto[ProdutoID]` |
| `fFaturamento[PedidoID]` | `fPedido[PedidoID]` |
| `fEntrega[PedidoID]` | `fPedido[PedidoID]` |
| `fEntrega[TransportadoraID]` | `dTransportadora[TransportadoraID]` |
| `fContasReceber[PedidoID]` | `fPedido[PedidoID]` |
| `fContasReceber[ClienteID]` | `dCliente[ClienteID]` |
| `fDevolucao[PedidoID]` | `fPedido[PedidoID]` |
| `fCompra[FornecedorID]` | `dFornecedor[FornecedorID]` |
| `fCompra[ProdutoID]` | `dProduto[ProdutoID]` |
| `fContasPagar[CompraID]` | `fCompra[CompraID]` |
| `fEstoqueMensal[ProdutoID]` | `dProduto[ProdutoID]` |
| `fOcupacaoArmazem[PosicaoID]` | `dPosicaoArmazem[PosicaoID]` |
| `fOcupacaoArmazem[ProdutoID]` | `dProduto[ProdutoID]` |
| `fVisitaComercial[ClienteID]` | `dCliente[ClienteID]` |
| `fVisitaComercial[VendedorID]` | `dVendedor[VendedorID]` |
| `fInteracaoCampanha[CampanhaID]` | `dCampanha[CampanhaID]` |
| `fInteracaoCampanha[ClienteID]` | `dCliente[ClienteID]` |
| `fEstoqueMensal[FilialID]` | `dFilial[FilialID]` |
| `fCompra[FilialID]` | `dFilial[FilialID]` |
| `fMovimentoEstoque[FilialID]` | `dFilial[FilialID]` |
| `fOrcamento[FilialID]` | `dFilial[FilialID]` |
| `fMeta[FilialID]` | `dFilial[FilialID]` |
| `fDespesa[FilialID]` | `dFilial[FilialID]` |
| `fPrevisao[FilialID]` | `dFilial[FilialID]` |
| `fMovimentoEstoque[ProdutoID]` | `dProduto[ProdutoID]` |
| `fOrcamento[DataReferencia]` | `dCalendario[Data]` |
| `fMeta[DataReferencia]` | `dCalendario[Data]` |
| `fDespesa[DataReferencia]` | `dCalendario[Data]` |
| `fPrevisao[DataReferencia]` | `dCalendario[Data]` |
| `fEstoqueMensal[DataReferencia]` | `dCalendario[Data]` |
| `fPedido[DataPedido]` | `dCalendario[Data]` |
| `fFaturamento[DataFaturamento]` | `dCalendario[Data]` |
| `fEntrega[DataEntrega]` | `dCalendario[Data]` |
| `fEntrega[DataPrometida]` | `dCalendario[Data]` |
| `fContasReceber[Vencimento]` | `dCalendario[Data]` |
| `fDevolucao[DataDevolucao]` | `dCalendario[Data]` |
| `fCompra[DataCompra]` | `dCalendario[Data]` |
| `fMovimentoEstoque[DataMovimento]` | `dCalendario[Data]` |
| `fVisitaComercial[DataVisita]` | `dCalendario[Data]` |
| `fInteracaoCampanha[DataInteracao]` | `dCalendario[Data]` |

## Contratos de integridade
1. Dimensões precisam ter chaves únicas, não nulas; medir duplicatas antes de criar relação 1:N.
2. Todas as FK candidatas devem ser verificadas quanto a órfãos, incluindo datas fora do calendário.
3. A presença de `PedidoID` em múltiplas fatos não autoriza ligação fato-fato bidirecional.
4. `dCliente[FilialID]` e `dVendedor[FilialID]` são atributos cadastrais, não substituem filial transacional do pedido.
5. `fEstoqueMensal` contém apenas 200 SKUs amostrados por filial/mês, e `fOcupacaoArmazem` apenas posições amostradas.
6. Registros futuros de previsão não são realizados; estoque e despesas não reconciliam com razão contábil.
7. Para colunas sem definição de unidade, semântica ou domínio na fonte, documentar como **pendente de validação**, sem atribuir significado inventado.
