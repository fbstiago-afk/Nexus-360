# NEXUS 360 — Dicionário de medidas

**Fonte:** `pbip/NEXUS360.SemanticModel/definition/tables/_Medidas.tmdl` (gerado automaticamente por `pbip/_gerador/gerar_docs_modelo.py`).

**Total:** 222 medidas em 38 pastas. Validação SQL × DAX em `testes/resultados/QA_MODELO_SEMANTICO.md`.

| Pasta | Medidas |
|---|---:|
| 00 Base | 24 |
| 01 Comercial | 7 |
| 02 Clientes\Cohort | 3 |
| 02 Clientes\Comparativo de janelas | 1 |
| 02 Clientes\Detalhe | 3 |
| 02 Clientes\Eventos no periodo | 3 |
| 02 Clientes\Parametros | 2 |
| 02 Clientes\Recompra | 4 |
| 02 Clientes\Status atual | 11 |
| 03 Logistica | 15 |
| 04 Estoque e WMS\Compras | 3 |
| 04 Estoque e WMS\Estoque | 9 |
| 04 Estoque e WMS\Movimentacao | 2 |
| 04 Estoque e WMS\WMS | 8 |
| 05 Financeiro\Caixa | 3 |
| 05 Financeiro\DRE | 1 |
| 05 Financeiro\Pagar | 3 |
| 05 Financeiro\Receber | 12 |
| 06 Planejamento | 15 |
| 07 Tempo | 10 |
| 08 UX\Armazém | 2 |
| 08 UX\Assistente | 4 |
| 08 UX\Calendário | 3 |
| 08 UX\Clientes | 2 |
| 08 UX\Comercial | 3 |
| 08 UX\Componentes | 11 |
| 08 UX\Cores | 7 |
| 08 UX\Financeiro | 2 |
| 08 UX\Home | 2 |
| 08 UX\Logística | 2 |
| 08 UX\Preditiva | 1 |
| 08 UX\Simulador | 2 |
| 09 Qualidade\Corte temporal | 13 |
| 09 Qualidade\Parametros | 4 |
| 09 Qualidade\Recebimento | 5 |
| 10 Previsão | 8 |
| 11 Simulador | 2 |
| 12 Operações | 10 |

## 00 Base

### Receita Líquida

Receita faturada calculada no grao do item (itens de pedidos faturados, datados pela DataFaturamento). Identica a SUM(fFaturamento[ReceitaLiquida]) em toda fatura (validado: diferenca 0 por fatura, dia, mes x filial e cliente) e responde a filtros de produto, categoria, subcategoria e marca.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE (
    SUM ( fItemPedido[ValorLiquido] ),
    KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ),
    USERELATIONSHIP ( fItemPedido[DataFaturamento], dCalendario[Data] )
)
```

### CMV

CMV no grao do item faturado; identico a SUM(fFaturamento[CMV]) por fatura. Responde a produto.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE (
    SUM ( fItemPedido[CustoMercadoria] ),
    KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ),
    USERELATIONSHIP ( fItemPedido[DataFaturamento], dCalendario[Data] )
)
```

### Impostos

Impostos da fatura (~7,5% da receita, independente da tributacao do item). Nao alocaveis por produto: BLANK quando ha filtro de produto.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
IF ( NOT [Filtro de Produto Ativo], SUM ( fFaturamento[Impostos] ) )
```

### Margem Bruta

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
[Receita Líquida] - [CMV]
```

### Margem Bruta %

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [Margem Bruta], [Receita Líquida] )
```

### Faturas

Faturas distintas. Com filtro de produto: faturas que contem o produto.

Formato: `#,0`

```dax
CALCULATE (
    DISTINCTCOUNTNOBLANK ( fItemPedido[FaturaID] ),
    KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ),
    USERELATIONSHIP ( fItemPedido[DataFaturamento], dCalendario[Data] )
)
```

### Ticket Médio Faturado

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
DIVIDE ( [Receita Líquida], [Faturas] )
```

### Pedidos

Todos os status. Data ativa: DataPedido.

Formato: `#,0`

```dax
COUNTROWS ( fPedido )
```

### Pedidos Faturados

Formato: `#,0`

```dax
CALCULATE ( [Pedidos], KEEPFILTERS ( fPedido[StatusPedido] = "Faturado" ) )
```

### Pedidos Cancelados

Formato: `#,0`

```dax
CALCULATE ( [Pedidos], KEEPFILTERS ( fPedido[StatusPedido] = "Cancelado" ) )
```

### Pedidos Pendentes

Formato: `#,0`

```dax
CALCULATE ( [Pedidos], KEEPFILTERS ( fPedido[StatusPedido] = "Pendente" ) )
```

### Taxa de Cancelamento %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Pedidos Cancelados], [Pedidos] )
```

### Valor Itens (todos os status)

Inclui pedidos cancelados e pendentes. Nao somar com Receita Liquida.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
SUM ( fItemPedido[ValorLiquido] )
```

### Valor Itens Faturados

Igual a Receita Liquida no total (validado), porem datado por DataPedido.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Valor Itens (todos os status)], KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )
```

### Custo Itens Faturados

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fItemPedido[CustoMercadoria] ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )
```

### Quantidade Itens Faturados

Formato: `#,0`

```dax
CALCULATE ( SUM ( fItemPedido[Quantidade] ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )
```

### Margem Itens Faturados %

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [Valor Itens Faturados] - [Custo Itens Faturados], [Valor Itens Faturados] )
```

### Valor Devolvido

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
SUM ( fDevolucao[ValorDevolvido] )
```

### Devoluções

Formato: `#,0`

```dax
COUNTROWS ( fDevolucao )
```

### Receita Ajustada por Devoluções

Devolucoes deduzidas uma unica vez. BLANK com filtro de produto (devolucao nao tem produto).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
IF ( NOT [Filtro de Produto Ativo], [Receita Líquida] - [Valor Devolvido] )
```

### Devolução % Receita

BLANK com filtro de produto (devolucao nao tem produto).

Formato: `0.00%;-0.00%;0.00%`

```dax
IF ( NOT [Filtro de Produto Ativo], DIVIDE ( [Valor Devolvido], [Receita Líquida] ) )
```

### Despesas Operacionais

Apenas registros elegiveis (<= Data Corte). Despesas sinteticas, nao auditaveis.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fDespesa[Valor] ), KEEPFILTERS ( fDespesa[ElegivelHistorico] = 1 ) )
```

### Resultado Gerencial Simplificado

DRE gerencial simplificada; nao contabil. BLANK com filtro de produto (despesa nao tem produto).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
IF ( NOT [Filtro de Produto Ativo], [Margem Bruta] - [Despesas Operacionais] )
```

### Resultado Gerencial %

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [Resultado Gerencial Simplificado], [Receita Líquida] )
```

## 01 Comercial

### Desconto Médio Ponderado %

Desconto do pedido ponderado pela receita faturada no grao do item. Responde a produto.

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE (
    CALCULATE (
        SUMX ( fItemPedido, fItemPedido[ValorLiquido] * fItemPedido[DescontoPercentual] ),
        KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ),
        USERELATIONSHIP ( fItemPedido[DataFaturamento], dCalendario[Data] )
    ),
    [Receita Líquida]
)
```

### Clientes Positivados

Clientes com fatura no periodo. Com filtro de produto: clientes que compraram o produto.

Formato: `#,0`

```dax
CALCULATE (
    DISTINCTCOUNT ( fItemPedido[ClienteID] ),
    KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ),
    USERELATIONSHIP ( fItemPedido[DataFaturamento], dCalendario[Data] )
)
```

### Vendedores com Venda

Formato: `#,0`

```dax
CALCULATE (
    DISTINCTCOUNT ( fItemPedido[VendedorID] ),
    KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ),
    USERELATIONSHIP ( fItemPedido[DataFaturamento], dCalendario[Data] )
)
```

### Receita por Vendedor

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
DIVIDE ( [Receita Líquida], [Vendedores com Venda] )
```

### SKUs Vendidos

Formato: `#,0`

```dax
CALCULATE ( DISTINCTCOUNT ( fItemPedido[ProdutoID] ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )
```

### Itens por Pedido Faturado

Datado por DataPedido. BLANK com filtro de produto.

Formato: `#,0.00`

```dax
IF (
    NOT [Filtro de Produto Ativo],
    DIVIDE ( CALCULATE ( COUNTROWS ( fItemPedido ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) ), [Pedidos Faturados] )
)
```

### Participação Receita %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Receita Líquida], CALCULATE ( [Receita Líquida], ALLSELECTED () ) )
```

## 02 Clientes\Cohort

### Tamanho Cohort

Clientes adquiridos no cohort (mes da primeira fatura).

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( dCliente ), KEEPFILTERS ( NOT ISBLANK ( dCliente[PrimeiraCompra] ) ) )
```

### Clientes Retidos (Cohort)

Clientes do cohort com fatura no mes N apos a aquisicao. Requer um unico cohort e um unico offset no contexto.

Formato: `#,0`

```dax
VAR _mes = SELECTEDVALUE ( dCohortOffset[Meses desde 1a Compra] )
VAR _cohort = SELECTEDVALUE ( dCliente[CohortInicio] )
VAR _corte = [Data Corte]
VAR _ini = EDATE ( _cohort, _mes )
VAR _fim = MIN ( EOMONTH ( _ini, 0 ), _corte )
RETURN
    IF (
        NOT ISBLANK ( _cohort ) && NOT ISBLANK ( _mes ) && _ini <= _corte,
        CALCULATE ( DISTINCTCOUNT ( fFaturamento[ClienteID] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= _ini, dCalendario[Data] <= _fim )
    )
```

### Retenção Cohort %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Clientes Retidos (Cohort)], [Tamanho Cohort] )
```

## 02 Clientes\Comparativo de janelas

### Taxa de Churn (Janela Comparativa) %

Taxa de churn se o limite fosse a janela do eixo (sem compra nos ultimos N dias / clientes com historico).

Formato: `0.0%;-0.0%;0.0%`

```dax
VAR _janela = SELECTEDVALUE ( 'Param Janela Comparativa'[Janela (dias)] )
VAR _ref = [Data Referência]
VAR _historico =
    CALCULATE ( DISTINCTCOUNT ( fFaturamento[ClienteID] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
VAR _compraram =
    CALCULATE ( DISTINCTCOUNT ( fFaturamento[ClienteID] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] > _ref - _janela, dCalendario[Data] <= _ref )
RETURN
    IF ( NOT ISBLANK ( _janela ) && NOT ISBLANK ( _ref ), DIVIDE ( _historico - _compraram, _historico ) )
```

## 02 Clientes\Detalhe

### Dias sem Compra (Data Ref.)

Dias entre a ultima fatura do cliente e a Data Referencia. So no grao de um cliente.

Formato: `#,0`

```dax
VAR _ref = [Data Referência]
VAR _ult = CALCULATE ( MAX ( fFaturamento[DataFaturamento] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
RETURN IF ( NOT ISBLANK ( _ult ) && HASONEVALUE ( dCliente[ClienteID] ), DATEDIFF ( _ult, _ref, DAY ) )
```

### Receita 12M (Data Ref.)

Receita liquida dos 12 meses encerrados na Data Referencia.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _ref = [Data Referência]
RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] > EDATE ( _ref, -12 ), dCalendario[Data] <= _ref )
```

### Prioridade Risco (Receita 12M)

Receita 12M apenas para clientes Em risco (mesma regra de dias do status); ordena a lista de prioridade de contato.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _d = [Dias sem Compra (Data Ref.)]
RETURN IF ( _d >= [Limite Ativo (dias)] && _d < [Limite Churn (dias)], [Receita 12M (Data Ref.)] )
```

## 02 Clientes\Eventos no periodo

### Clientes Novos (no período)

Evento: clientes cuja primeira fatura ocorre no periodo (DataCadastro nao e usada - C6). Difere de Clientes Novos (status), que e o status atual na Data Referencia.

Formato: `#,0`

```dax
VAR _corte = [Data Corte]
VAR _ini = MIN ( dCalendario[Data] )
VAR _fim = MIN ( MAX ( dCalendario[Data] ), _corte )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( fFaturamento[ClienteID] ),
        KEEPFILTERS ( dCalendario[Data] <= _corte ),
        KEEPFILTERS ( dCliente[PrimeiraCompra] >= _ini ),
        KEEPFILTERS ( dCliente[PrimeiraCompra] <= _fim )
    )
```

### Reativações no Período

Evento historico: clientes que voltaram a comprar no periodo apos um intervalo >= Limite Churn.

Formato: `#,0`

```dax
VAR _corte = [Data Corte]
VAR _churn = [Limite Churn (dias)]
RETURN
    CALCULATE (
        DISTINCTCOUNT ( fFaturamento[ClienteID] ),
        KEEPFILTERS ( dCalendario[Data] <= _corte ),
        KEEPFILTERS ( fFaturamento[DiasDesdeCompraAnterior] >= _churn )
    )
```

### Receita Recuperada

Receita faturada no periodo pelos clientes reativados no periodo, a partir da primeira compra de retorno. Indicador de cliente (base fFaturamento): nao responde a produto.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
VAR _fim = MIN ( MAX ( dCalendario[Data] ), _corte )
VAR _churn = [Limite Churn (dias)]
VAR _retornos =
    CALCULATETABLE (
        ADDCOLUMNS ( VALUES ( fFaturamento[ClienteID] ), "@Retorno", CALCULATE ( MIN ( fFaturamento[DataFaturamento] ) ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte ),
        KEEPFILTERS ( fFaturamento[DiasDesdeCompraAnterior] >= _churn )
    )
RETURN
    SUMX (
        _retornos,
        VAR _inicio = [@Retorno]
        RETURN
            CALCULATE ( SUM ( fFaturamento[ReceitaLiquida] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= _inicio, dCalendario[Data] <= _fim )
    )
```

## 02 Clientes\Parametros

### Limite Churn (dias)

Dias sem compra para classificar Churn. Padrao 365 (aprovado em 01/11/2026).

Formato: `0`

```dax
SELECTEDVALUE ( 'Param Limite Churn'[Dias], 365 )
```

### Limite Ativo (dias)

Dias desde a ultima compra para o cliente ser Ativo. Padrao 180. Limitado a Limite Churn - 1 para manter as faixas consistentes.

Formato: `0`

```dax
VAR _ativo = SELECTEDVALUE ( 'Param Limite Ativo'[Dias], 180 )
VAR _churn = [Limite Churn (dias)]
RETURN
    MIN ( _ativo, _churn - 1 )
```

## 02 Clientes\Recompra

### Intervalo Médio entre Compras (dias)

Media dos intervalos entre faturas consecutivas do mesmo cliente que terminam no periodo.

Formato: `#,0.0`

```dax
AVERAGE ( fFaturamento[DiasDesdeCompraAnterior] )
```

### Intervalo Mediano entre Compras (dias)

Formato: `#,0`

```dax
MEDIAN ( fFaturamento[DiasDesdeCompraAnterior] )
```

### Compras por Cliente

Frequencia de compra no periodo: faturas por cliente positivado.

Formato: `#,0.00`

```dax
DIVIDE ( [Faturas], [Clientes Positivados] )
```

### Taxa de Recompra %

% de clientes com fatura no periodo que tiveram mais de uma fatura no periodo. Indicador de cliente: nao responde a produto.

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE (
    COUNTROWS ( FILTER ( VALUES ( fFaturamento[ClienteID] ), CALCULATE ( COUNTROWS ( fFaturamento ) ) > 1 ) ),
    DISTINCTCOUNT ( fFaturamento[ClienteID] )
)
```

## 02 Clientes\Status atual

### Clientes por Status

Clientes por status atual na Data Referencia (mutuamente exclusivos): Churn (>= Limite Churn sem compra) > Em risco (>= Limite Ativo) > Novo (1a compra ha menos de Limite Ativo) > Reativado (retorno apos gap >= Limite Churn ha menos de Limite Ativo) > Ativo. Clientes sem fatura ate a Data Referencia nao sao classificados.

Formato: `#,0`

```dax
VAR _ref = [Data Referência]
VAR _churn = [Limite Churn (dias)]
VAR _ativo = [Limite Ativo (dias)]
VAR _selecao = VALUES ( dStatusCliente[Status] )
VAR _base =
    CALCULATETABLE (
        ADDCOLUMNS (
            VALUES ( fFaturamento[ClienteID] ),
            "@Ultima", CALCULATE ( MAX ( fFaturamento[DataFaturamento] ) ),
            "@Primeira", CALCULATE ( MIN ( fFaturamento[DataFaturamento] ) ),
            "@Retorno", CALCULATE ( MAX ( fFaturamento[DataFaturamento] ), fFaturamento[DiasDesdeCompraAnterior] >= _churn )
        ),
        REMOVEFILTERS ( dCalendario ),
        dCalendario[Data] <= _ref
    )
VAR _classificado =
    ADDCOLUMNS (
        _base,
        "@Status",
            VAR _dias = DATEDIFF ( [@Ultima], _ref, DAY )
            RETURN
                SWITCH (
                    TRUE (),
                    _dias >= _churn, "Churn",
                    _dias >= _ativo, "Em risco",
                    DATEDIFF ( [@Primeira], _ref, DAY ) < _ativo, "Novo",
                    NOT ISBLANK ( [@Retorno] ) && DATEDIFF ( [@Retorno], _ref, DAY ) < _ativo, "Reativado",
                    "Ativo"
                )
    )
RETURN
    IF ( NOT ISBLANK ( _ref ), COUNTROWS ( FILTER ( _classificado, [@Status] IN _selecao ) ) )
```

### Clientes com Histórico

Clientes com ao menos uma fatura ate a Data Referencia (soma dos cinco status).

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], REMOVEFILTERS ( dStatusCliente ) )
```

### Clientes Novos (status)

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], TREATAS ( { "Novo" }, dStatusCliente[Status] ) )
```

### Clientes Ativos Recorrentes

Status Ativo: compra recente, sem ser novo nem reativado.

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], TREATAS ( { "Ativo" }, dStatusCliente[Status] ) )
```

### Clientes Reativados (status)

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], TREATAS ( { "Reativado" }, dStatusCliente[Status] ) )
```

### Clientes Ativos (total)

Novos + Ativos + Reativados. Por mes, mostra a evolucao mensal de clientes ativos.

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], TREATAS ( { "Novo", "Ativo", "Reativado" }, dStatusCliente[Status] ) )
```

### Clientes em Risco

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], TREATAS ( { "Em risco" }, dStatusCliente[Status] ) )
```

### Clientes em Churn

Formato: `#,0`

```dax
CALCULATE ( [Clientes por Status], TREATAS ( { "Churn" }, dStatusCliente[Status] ) )
```

### Taxa de Churn %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Clientes em Churn], [Clientes com Histórico] )
```

### Clientes em Risco %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Clientes em Risco], [Clientes com Histórico] )
```

### Clientes Ativos %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Clientes Ativos (total)], [Clientes com Histórico] )
```

## 03 Logistica

### Entregas

Todas as entregas (DataEntrega sem nulos: todas elegiveis). Data ativa: DataEntrega.

Formato: `#,0`

```dax
COUNTROWS ( fEntrega )
```

### Entregas OTIF

Formato: `#,0`

```dax
CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[NoPrazo] = 1 ), KEEPFILTERS ( fEntrega[InFull] = 1 ) )
```

### OTIF %

NoPrazo = 1 e InFull = 1 / entregas.

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Entregas OTIF], [Entregas] )
```

### Entregas No Prazo

Formato: `#,0`

```dax
CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[NoPrazo] = 1 ) )
```

### No Prazo %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Entregas No Prazo], [Entregas] )
```

### Entregas In Full

Formato: `#,0`

```dax
CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[InFull] = 1 ) )
```

### In Full %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Entregas In Full], [Entregas] )
```

### Entregas com Ocorrência

StatusEntrega independe de OTIF (M1).

Formato: `#,0`

```dax
CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[StatusEntrega] = "Ocorrência" ) )
```

### Ocorrência %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Entregas com Ocorrência], [Entregas] )
```

### Custo Frete

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
SUM ( fEntrega[CustoFrete] )
```

### Frete por Entrega

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
DIVIDE ( [Custo Frete], [Entregas] )
```

### Frete % Receita

Frete datado por entrega e receita por faturamento. BLANK com filtro de produto (frete nao tem produto).

Formato: `0.00%;-0.00%;0.00%`

```dax
IF ( NOT [Filtro de Produto Ativo], DIVIDE ( [Custo Frete], [Receita Líquida] ) )
```

### Atraso Médio (dias)

Media de dias de atraso apenas das entregas fora do prazo.

Formato: `#,0.0`

```dax
CALCULATE ( AVERAGE ( fEntrega[DiasAtraso] ), KEEPFILTERS ( fEntrega[NoPrazo] = 0 ) )
```

### Lead Time Médio (dias)

Pedido ate entrega. Inclui 7 casos negativos da fonte (C6).

Formato: `#,0.0`

```dax
AVERAGE ( fEntrega[LeadTimePedidoDias] )
```

### Peso Entregue (kg)

Formato: `#,0.0`

```dax
SUM ( fEntrega[PesoKg] )
```

## 04 Estoque e WMS\Compras

### Compras

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fCompra ), KEEPFILTERS ( fCompra[ElegivelHistorico] = 1 ) )
```

### Valor Compras

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fCompra[ValorCompra] ), KEEPFILTERS ( fCompra[ElegivelHistorico] = 1 ) )
```

### Compras Atrasadas %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( CALCULATE ( [Compras], KEEPFILTERS ( fCompra[StatusCompra] = "Atrasado" ) ), [Compras] )
```

## 04 Estoque e WMS\Estoque

### Data Último Snapshot Estoque

Formato: `dd/MM/yyyy`

```dax
CALCULATE ( MAX ( fEstoqueMensal[DataReferencia] ), KEEPFILTERS ( fEstoqueMensal[ElegivelHistorico] = 1 ) )
```

### Saldo Estoque Amostra (un)

Snapshot do ultimo mes elegivel do contexto. Amostra de 200 SKUs por filial.

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot Estoque]
RETURN
    CALCULATE ( SUM ( fEstoqueMensal[SaldoUnidades] ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) )
```

### Valor Estoque Amostra

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _d = [Data Último Snapshot Estoque]
RETURN
    CALCULATE ( SUM ( fEstoqueMensal[ValorEstoque] ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) )
```

### SKU-Filial Amostrados

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot Estoque]
RETURN
    CALCULATE ( COUNTROWS ( fEstoqueMensal ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) )
```

### SKUs em Ruptura (amostra)

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot Estoque]
RETURN
    CALCULATE ( COUNTROWS ( fEstoqueMensal ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ), KEEPFILTERS ( fEstoqueMensal[Ruptura] = 1 ) )
```

### Ruptura % (amostra)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [SKUs em Ruptura (amostra)], [SKU-Filial Amostrados] )
```

### SKUs Abaixo do Mínimo (amostra)

Saldo abaixo do estoque minimo (inclui rupturas).

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot Estoque]
RETURN
    COUNTROWS (
        FILTER (
            CALCULATETABLE ( fEstoqueMensal, KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) ),
            fEstoqueMensal[SaldoUnidades] < fEstoqueMensal[EstoqueMinimo]
        )
    )
```

### Abaixo do Mínimo % (amostra)

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [SKUs Abaixo do Mínimo (amostra)], [SKU-Filial Amostrados] )
```

### Produtos Parados 90+ (amostra)

SKU-filial do ultimo snapshot de estoque do contexto com 90 ou mais dias sem movimento (DiasSemMovimento da fonte).

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot Estoque]
RETURN CALCULATE ( COUNTROWS ( fEstoqueMensal ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ), KEEPFILTERS ( fEstoqueMensal[DiasSemMovimento] >= 90 ) )
```

## 04 Estoque e WMS\Movimentacao

### Entradas Estoque (un)

Formato: `#,0`

```dax
CALCULATE ( SUM ( fMovimentoEstoque[QuantidadeAssinada] ), KEEPFILTERS ( fMovimentoEstoque[QuantidadeAssinada] > 0 ), KEEPFILTERS ( fMovimentoEstoque[ElegivelHistorico] = 1 ) )
```

### Saídas Estoque (un)

Saidas, ajustes e transferencias (quantidade assinada negativa), em valor absoluto.

Formato: `#,0`

```dax
- CALCULATE ( SUM ( fMovimentoEstoque[QuantidadeAssinada] ), KEEPFILTERS ( fMovimentoEstoque[QuantidadeAssinada] < 0 ), KEEPFILTERS ( fMovimentoEstoque[ElegivelHistorico] = 1 ) )
```

## 04 Estoque e WMS\WMS

### Data Último Snapshot WMS

Formato: `dd/MM/yyyy`

```dax
CALCULATE ( MAX ( fOcupacaoArmazem[DataReferencia] ), KEEPFILTERS ( fOcupacaoArmazem[ElegivelHistorico] = 1 ) )
```

### Registros WMS (amostra)

Registros posicao x produto do ultimo snapshot elegivel. Amostra; nao representa a filial (C9).

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot WMS]
RETURN
    CALCULATE ( COUNTROWS ( fOcupacaoArmazem ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )
```

### Posições Amostradas

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot WMS]
RETURN
    CALCULATE ( DISTINCTCOUNT ( fOcupacaoArmazem[PosicaoID] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )
```

### Paletes (amostra)

Formato: `#,0`

```dax
VAR _d = [Data Último Snapshot WMS]
RETURN
    CALCULATE ( SUM ( fOcupacaoArmazem[Paletes] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )
```

### Registros Ocupada %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( CALCULATE ( [Registros WMS (amostra)], KEEPFILTERS ( fOcupacaoArmazem[StatusPosicao] = "Ocupada" ) ), [Registros WMS (amostra)] )
```

### Registros Bloqueada %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( CALCULATE ( [Registros WMS (amostra)], KEEPFILTERS ( fOcupacaoArmazem[StatusPosicao] = "Bloqueada" ) ), [Registros WMS (amostra)] )
```

### Registros Disponível %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( CALCULATE ( [Registros WMS (amostra)], KEEPFILTERS ( fOcupacaoArmazem[StatusPosicao] = "Disponível" ) ), [Registros WMS (amostra)] )
```

### Posições Cadastradas

Posicoes de dPosicaoArmazem das filiais no contexto (dPosicaoArmazem nao se relaciona com dFilial; filtro por TREATAS).

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( dPosicaoArmazem ), TREATAS ( VALUES ( dFilial[FilialID] ), dPosicaoArmazem[FilialID] ) )
```

## 05 Financeiro\Caixa

### Recebimentos (Data Pagamento)

Recebido confirmado (regra D1) datado pelo pagamento (relacao inativa fContasReceber[DataPagamento]).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Valor Recebido Confirmado], USERELATIONSHIP ( fContasReceber[DataPagamento], dCalendario[Data] ) )
```

### Pagamentos (Data Pagamento)

Contas a pagar elegiveis pagas, datadas pelo pagamento (relacao inativa fContasPagar[DataPagamento]). Despesas operacionais nao tem registro de pagamento.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Valor Pago (CP)], USERELATIONSHIP ( fContasPagar[DataPagamento], dCalendario[Data] ) )
```

### Saldo Recebimentos - Pagamentos

Entradas de clientes menos pagamentos a fornecedores no periodo (nao e o fluxo de caixa completo).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
[Recebimentos (Data Pagamento)] - [Pagamentos (Data Pagamento)]
```

## 05 Financeiro\DRE

### Valor DRE Gerencial

DRE gerencial simplificada por linha de dLinhaDRE (receitas positivas, custos e despesas negativos). Total = Resultado Gerencial Simplificado. BLANK com filtro de produto.

Formato: `R$ #,0;-R$ #,0;R$ #,0`

```dax
VAR _linha = SELECTEDVALUE ( dLinhaDRE[Linha] )
RETURN
    IF (
        NOT [Filtro de Produto Ativo],
        SWITCH (
            TRUE (),
            ISBLANK ( _linha ), [Resultado Gerencial Simplificado],
            _linha = "Receita Líquida", [Receita Líquida],
            _linha = "CMV", - [CMV],
            - CALCULATE ( [Despesas Operacionais], TREATAS ( { _linha }, fDespesa[Conta] ) )
        )
    )
```

## 05 Financeiro\Pagar

### Valor Contas a Pagar

Data ativa: Vencimento. Exclui titulos de compras pos-corte.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), KEEPFILTERS ( fContasPagar[ElegivelHistorico] = 1 ) )
```

### Valor Pago (CP)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), KEEPFILTERS ( fContasPagar[ElegivelHistorico] = 1 ), KEEPFILTERS ( NOT ISBLANK ( fContasPagar[DataPagamento] ) ) )
```

### Valor em Aberto (CP)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), KEEPFILTERS ( fContasPagar[ElegivelHistorico] = 1 ), KEEPFILTERS ( ISBLANK ( fContasPagar[DataPagamento] ) ) )
```

## 05 Financeiro\Receber

### Títulos

Data ativa: Vencimento.

Formato: `#,0`

```dax
COUNTROWS ( fContasReceber )
```

### Valor Títulos

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
SUM ( fContasReceber[ValorTitulo] )
```

### Títulos Recebidos

Formato: `#,0`

```dax
CALCULATE ( [Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Recebido" ) )
```

### Valor Recebido Confirmado

Somente titulos com valor pago > 0 E data de pagamento valida (>= faturamento). Regra D1.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fContasReceber[ValorPago] ), KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Recebido" ) )
```

### Títulos em Aberto

Formato: `#,0`

```dax
CALCULATE ( [Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Em aberto" ) )
```

### Valor em Aberto (status atual)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Valor Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Em aberto" ) )
```

### Prazo Médio Recebimento (dias)

Formato: `#,0.0`

```dax
CALCULATE (
    AVERAGEX ( fContasReceber, DATEDIFF ( fContasReceber[DataFaturamento], fContasReceber[DataPagamento], DAY ) ),
    KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Recebido" )
)
```

### Saldo Vencido em Aberto (Data Ref.)

As-of: faturado ate a Data Referencia, vencido antes dela e nao pago ate ela. Exclui Inconsistentes.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _ref = [Data Referência]
RETURN
    CALCULATE (
        SUM ( fContasReceber[ValorTitulo] ),
        REMOVEFILTERS ( dCalendario ),
        fContasReceber[DataFaturamento] <= _ref,
        fContasReceber[Vencimento] < _ref,
        FILTER (
            ALL ( fContasReceber[StatusRecebimento], fContasReceber[DataPagamento] ),
            fContasReceber[StatusRecebimento] = "Em aberto"
                || ( fContasReceber[StatusRecebimento] = "Recebido" && fContasReceber[DataPagamento] > _ref )
        )
    )
```

### Saldo a Vencer em Aberto (Data Ref.)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _ref = [Data Referência]
RETURN
    CALCULATE (
        SUM ( fContasReceber[ValorTitulo] ),
        REMOVEFILTERS ( dCalendario ),
        fContasReceber[DataFaturamento] <= _ref,
        fContasReceber[Vencimento] >= _ref,
        FILTER (
            ALL ( fContasReceber[StatusRecebimento], fContasReceber[DataPagamento] ),
            fContasReceber[StatusRecebimento] = "Em aberto"
                || ( fContasReceber[StatusRecebimento] = "Recebido" && fContasReceber[DataPagamento] > _ref )
        )
    )
```

### Saldo em Aberto (Data Ref.)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
[Saldo Vencido em Aberto (Data Ref.)] + [Saldo a Vencer em Aberto (Data Ref.)]
```

### Valor Vencido até Data Ref. (base)

Denominador da inadimplencia: titulos validos vencidos ate a Data Referencia.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _ref = [Data Referência]
RETURN
    CALCULATE (
        SUM ( fContasReceber[ValorTitulo] ),
        REMOVEFILTERS ( dCalendario ),
        fContasReceber[DataFaturamento] <= _ref,
        fContasReceber[Vencimento] < _ref,
        fContasReceber[StatusRecebimento] <> "Inconsistente"
    )
```

### Inadimplência % (Data Ref.)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [Saldo Vencido em Aberto (Data Ref.)], [Valor Vencido até Data Ref. (base)] )
```

## 06 Planejamento

### Meta Faturamento

Meta por filial-mes; BLANK com filtro de produto (a meta nao tem grao de produto).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
IF ( NOT [Filtro de Produto Ativo], CALCULATE ( SUM ( fMeta[ValorMeta] ), KEEPFILTERS ( fMeta[Indicador] = "Faturamento" ) ) )
```

### Meta Faturamento (até corte)

Meta restrita a meses com realizado, para comparacao.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE ( [Meta Faturamento], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
```

### Atingimento Meta Faturamento %

Meta por filial-mes; BLANK com filtro de produto.

Formato: `0.0%;-0.0%;0.0%`

```dax
IF ( NOT [Filtro de Produto Ativo], DIVIDE ( [Receita Líquida], [Meta Faturamento (até corte)] ) )
```

### Gap Meta Faturamento

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
IF ( NOT [Filtro de Produto Ativo] && NOT ISBLANK ( [Meta Faturamento (até corte)] ), [Receita Líquida] - [Meta Faturamento (até corte)] )
```

### Meta Margem Bruta % (ponderada)

Meta de margem (razao) ponderada pela meta de faturamento de cada filial-mes (C8); BLANK com filtro de produto.

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR _grao = SUMMARIZE ( fMeta, fMeta[DataReferencia], fMeta[FilialID] )
VAR _num =
    SUMX (
        _grao,
        CALCULATE ( SUM ( fMeta[ValorMeta] ), fMeta[Indicador] = "Faturamento" )
            * CALCULATE ( SUM ( fMeta[ValorMeta] ), fMeta[Indicador] = "Margem Bruta" )
    )
VAR _den = SUMX ( _grao, CALCULATE ( SUM ( fMeta[ValorMeta] ), fMeta[Indicador] = "Faturamento" ) )
RETURN
    IF ( NOT [Filtro de Produto Ativo], DIVIDE ( _num, _den ) )
```

### Desvio Margem vs Meta (p.p.)

Formato: `+0.0;-0.0;0.0`

```dax
VAR _corte = [Data Corte]
VAR _meta = CALCULATE ( [Meta Margem Bruta % (ponderada)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
RETURN
    IF (
        NOT [Filtro de Produto Ativo] && NOT ISBLANK ( _meta ) && NOT ISBLANK ( [Margem Bruta %] ),
        ( [Margem Bruta %] - _meta ) * 100
    )
```

### Meta OTIF % (média simples)

Media simples das metas filial-mes; nao ponderada (sem base de ponderacao definida na fonte).

Formato: `0.0%;-0.0%;0.0%`

```dax
CALCULATE ( AVERAGE ( fMeta[ValorMeta] ), KEEPFILTERS ( fMeta[Indicador] = "OTIF" ) )
```

### Orçamento Receita

Identico a Meta Faturamento em 100% das linhas (M8).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fOrcamento[ValorOrcado] ), KEEPFILTERS ( fOrcamento[Conta] = "Receita" ) )
```

### Orçamento Despesa Operacional

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fOrcamento[ValorOrcado] ), KEEPFILTERS ( fOrcamento[Conta] = "Despesa Operacional" ) )
```

### Desvio Despesa vs Orçamento

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
VAR _orc = CALCULATE ( [Orçamento Despesa Operacional], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
RETURN
    IF ( NOT ISBLANK ( _orc ), [Despesas Operacionais] - _orc )
```

### Receita Prevista

Projecao sintetica (jan-jun/2027). Nunca somar ao realizado.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
SUM ( fPrevisao[ReceitaPrevista] )
```

### Margem Erro Estimada (média)

Semantica da fonte pendente de validacao; nao usar como intervalo de confianca.

Formato: `0.0%;-0.0%;0.0%`

```dax
AVERAGE ( fPrevisao[MargemErroEstimada] )
```

### Desvio OTIF vs Meta (p.p.)

OTIF realizado menos meta OTIF (media simples, meses ate o corte), em pontos percentuais.

Formato: `+0.0;-0.0;0.0`

```dax
VAR _corte = [Data Corte]
VAR _meta = CALCULATE ( [Meta OTIF % (média simples)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _otif = [OTIF %]
RETURN
    IF ( NOT ISBLANK ( _meta ) && NOT ISBLANK ( _otif ), ( _otif - _meta ) * 100 )
```

### Orçamento Despesa Operacional (até corte)

Orcamento de despesa operacional restrito aos meses com realizado (mesma base do desvio).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN CALCULATE ( [Orçamento Despesa Operacional], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
```

### Valor DRE Gerencial LY

Valor DRE Gerencial no mesmo periodo do ano anterior, limitado ao corte.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Valor DRE Gerencial], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )
```

## 07 Tempo

### Receita LY

Mesmo periodo do ano anterior, limitado as datas <= Data Corte (comparacao justa).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Receita Líquida], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )
```

### Receita (até corte)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE ( [Receita Líquida], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
```

### Receita YoY %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Receita (até corte)] - [Receita LY], [Receita LY] )
```

### Receita YoY Δ

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
IF ( NOT ISBLANK ( [Receita LY] ), [Receita (até corte)] - [Receita LY] )
```

### Receita Mês Anterior

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Receita Líquida], DATEADD ( dCalendario[Data], -1, MONTH ) )
```

### Receita MoM %

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Receita Líquida] - [Receita Mês Anterior], [Receita Mês Anterior] )
```

### Receita YTD

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Receita Líquida], DATESYTD ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )
```

### Receita YTD LY

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE (
            CALCULATE ( [Receita Líquida], DATESYTD ( dCalendario[Data] ) ),
            SAMEPERIODLASTYEAR ( dCalendario[Data] )
        ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )
```

### Margem Bruta % LY

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Margem Bruta %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )
```

### Margem Bruta % YoY (p.p.)

Formato: `+0.0;-0.0;0.0`

```dax
VAR _corte = [Data Corte]
VAR _atual = CALCULATE ( [Margem Bruta %], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _ly = [Margem Bruta % LY]
RETURN
    IF ( NOT ISBLANK ( _ly ) && NOT ISBLANK ( _atual ), ( _atual - _ly ) * 100 )
```

## 08 UX\Armazém

### UX Armazém KPIs

Faixa de KPIs de armazem e estoque (amostras C9).

Formato: ``

```dax
VAR _t = "<div class='nx-k'><div class='nx-kl'>@L</div><div class='nx-kv'>@V</div><div class='nx-ks'>@S</div></div>"
VAR _d = [Data Último Snapshot WMS]
VAR _css = "<style>.nx-w{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(8,1fr);gap:10px;height:100vh;box-sizing:border-box}.nx-k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:11px 14px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-kl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:22px;font-weight:600;color:#FFFFFF;margin-top:3px;line-height:1.1}.nx-ks{font-size:10px;color:#A9B9CA;margin-top:3px}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
RETURN
    _css & "<div class='nx-w'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Posições cadastradas" ), "@V", FORMAT ( [Posições Cadastradas], "#,0", "pt-BR" ) ), "@S", "corredor × coluna × nível" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Posições lidas" ), "@V", FORMAT ( [Posições Amostradas], "#,0", "pt-BR" ) ), "@S", "snapshot de " & FORMAT ( _d, "dd/mm/yyyy" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Ocupadas (amostra)" ), "@V", "<span style='color:#10D4C4'>" & FORMAT ( [Registros Ocupada %], "0%", "pt-BR" ) & "</span>" ), "@S", FORMAT ( [Paletes (amostra)], "#,0", "pt-BR" ) & " paletes lidos" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Bloqueadas (amostra)" ), "@V", "<span style='color:#FF7285'>" & FORMAT ( [Registros Bloqueada %], "0%", "pt-BR" ) & "</span>" ), "@S", "posições indisponíveis" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Estoque (amostra)" ), "@V", "R$ " & FORMAT ( [Valor Estoque Amostra] / 1e6, "#,0.0", "pt-BR" ) & " mi" ), "@S", FORMAT ( [SKU-Filial Amostrados], "#,0", "pt-BR" ) & " SKU-filial" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Ruptura" ), "@V", FORMAT ( COALESCE ( [Ruptura % (amostra)], 0 ), "0.0%", "pt-BR" ) ), "@S", FORMAT ( COALESCE ( [SKUs em Ruptura (amostra)], 0 ), "#,0", "pt-BR" ) & " SKU-filial sem saldo" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Abaixo do mínimo" ), "@V", FORMAT ( [Abaixo do Mínimo % (amostra)], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [SKUs Abaixo do Mínimo (amostra)], "#,0", "pt-BR" ) & " SKU-filial" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Parados 90+ dias" ), "@V", FORMAT ( [Produtos Parados 90+ (amostra)], "#,0", "pt-BR" ) ), "@S", "sem movimento (baixo giro)" )
        & "</div>"
```

### UX Armazém Grade

Gemeo digital 2D: grade 10x10 por nivel com o status de cada posicao no ultimo snapshot do contexto; posicoes sem leitura aparecem vazias.

Formato: ``

```dax
VAR _nf = COUNTROWS ( VALUES ( dFilial[FilialID] ) )
VAR _d = [Data Último Snapshot WMS]
VAR _pos =
    ADDCOLUMNS (
        CALCULATETABLE (
            SUMMARIZE ( dPosicaoArmazem, dPosicaoArmazem[PosicaoID], dPosicaoArmazem[EixoX], dPosicaoArmazem[EixoY], dPosicaoArmazem[EixoZ], dPosicaoArmazem[Zona] ),
            TREATAS ( VALUES ( dFilial[FilialID] ), dPosicaoArmazem[FilialID] )
        ),
        "@st", CALCULATE ( MAX ( fOcupacaoArmazem[StatusPosicao] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) ),
        "@pl", CALCULATE ( SUM ( fOcupacaoArmazem[Paletes] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )
    )
VAR _niv =
    CONCATENATEX (
        { 1, 2, 3, 4 },
        VAR _z = [Value]
        RETURN
            "<div class='nx-n'><div class='nx-nt'>Nível " & _z & IF ( _z = 1, " (térreo)", "" ) & "</div><div class='nx-gr'>"
                & CONCATENATEX (
                    FILTER ( _pos, dPosicaoArmazem[EixoZ] = _z ),
                    VAR _cls = SWITCH ( [@st], "Ocupada", "o", "Bloqueada", "b", "Disponível", "d", "s" )
                    VAR _zc = SWITCH ( dPosicaoArmazem[Zona], "Expedição", "ze", "Picking", "zp", "zu" )
                    RETURN "<i class='" & _cls & " " & _zc & "'>" & IF ( [@pl] > 0, [@pl], "" ) & "</i>",
                    "", dPosicaoArmazem[EixoY], DESC, dPosicaoArmazem[EixoX], ASC
                )
                & "</div></div>",
        "", [Value], ASC
    )
VAR _css = "<style>.nx-a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:12px 18px;display:flex;flex-direction:column}.nx-at{font-size:13px;font-weight:600;text-align:center}.nx-as{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 10px}.nx-ns{display:flex;gap:22px;justify-content:center;flex:1}.nx-n{display:flex;flex-direction:column;align-items:center}.nx-nt{font-size:11px;color:#C9D6E3;margin-bottom:6px}.nx-gr{display:grid;grid-template-columns:repeat(10,24px);grid-auto-rows:24px;gap:3px}.nx-gr i{font-style:normal;font-size:9px;font-weight:600;display:flex;align-items:center;justify-content:center;border-radius:4px;background:#12304F;color:#071528;border-bottom:3px solid transparent;animation:nxIn .5s ease-out both}.nx-gr i.o{background:#10D4C4}.nx-gr i.b{background:#FF7285}.nx-gr i.d{background:#5FA8E6}.nx-gr i.s{background:#12304F;opacity:.75}.nx-gr i.ze{border-bottom-color:#FFC66D}.nx-gr i.zp{border-bottom-color:#7FE6DD}.nx-gr i.zu{border-bottom-color:#6F86A0}.nx-ax{font-size:9.5px;color:#6F86A0;margin-top:4px}.nx-lg{display:flex;gap:16px;justify-content:center;font-size:10.5px;color:#A9B9CA;margin-top:10px;flex-wrap:wrap}.nx-lg span{display:flex;align-items:center;gap:5px}.nx-lg b{display:inline-block;width:12px;height:12px;border-radius:3px}.nx-lg u{display:inline-block;width:14px;height:3px;text-decoration:none}@keyframes nxIn{from{opacity:0}to{opacity:1}}@media (prefers-reduced-motion:reduce){.nx-gr i{animation:none}}</style>"
VAR _leg = "<div class='nx-lg'><span><b style='background:#10D4C4'></b>Ocupada</span><span><b style='background:#FF7285'></b>Bloqueada</span><span><b style='background:#5FA8E6'></b>Disponível</span><span><b style='background:#12304F;border:1px solid #3E5C7A'></b>Sem leitura no snapshot</span><span><u style='background:#FFC66D'></u>Expedição</span><span><u style='background:#7FE6DD'></u>Picking</span><span><u style='background:#6F86A0'></u>Pulmão</span><span>número = paletes lidos</span></div>"
RETURN
    IF (
        _nf <> 1,
        _css & "<div class='nx-a'><div class='nx-at'>Mapa de posições</div><div class='nx-as'>Selecione uma única filial para ver o armazém.</div></div>",
        _css & "<div class='nx-a'><div class='nx-at'>Mapa de posições · " & SELECTEDVALUE ( dFilial[Cidade] ) & "</div><div class='nx-as'>vista de cima por nível · linhas = coluna (Y 10→1) · colunas = corredor (X 1→10) · snapshot de " & FORMAT ( _d, "dd/mm/yyyy" ) & " · " & COUNTROWS ( FILTER ( _pos, NOT ISBLANK ( [@st] ) ) ) & " de " & COUNTROWS ( _pos ) & " posições com leitura</div>"
            & "<div class='nx-ns'>" & _niv & "</div>" & _leg & "</div>"
    )
```

## 08 UX\Assistente

### UX Assistente Status

Faixa de status da integracao (implementado/testado/pendente).

Formato: ``

```dax
VAR _chip = "<span class='ch' style='border-color:@C'><b style='color:@C'>@S</b> · @T</span>"
RETURN
    "<style>.a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;overflow:hidden}.h{font-size:13px;font-weight:600;text-align:center;margin-bottom:8px}.sub{font-size:10.5px;color:#A9B9CA;text-align:center;margin-bottom:10px}.mono{font-family:Consolas,monospace;font-size:11px;color:#7FE6DD}.lb{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin:10px 0 4px}.q{background:#12304F;border-radius:10px 10px 10px 2px;padding:9px 12px;font-size:13px;display:inline-block}.st{border-left:2px solid #173B5C;margin-left:6px;padding:4px 0 4px 12px}.tb{width:100%;border-collapse:collapse;font-size:11.5px}.tb td{padding:5px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.tb td.n{text-align:right;color:#FFFFFF}.pd{border:1px dashed #FFC66D;border-radius:8px;padding:8px 12px;font-size:11px;color:#FFC66D;margin-top:10px}.in{border:1px solid #173B5C;border-radius:8px;padding:8px 12px;font-size:11.5px;color:#6F86A0;margin-top:10px}.ok{color:#45D5A1}.ch{display:inline-block;border:1px solid #173B5C;border-radius:12px;padding:3px 10px;margin:0 6px 6px 0;font-size:10.5px;color:#C9D6E3}</style><div class='a' style='padding:10px 18px;display:flex;align-items:center;gap:18px'>"
        & "<div style='min-width:310px'><div style='font-size:15px;font-weight:600'>Interface demonstrativa</div><div style='font-size:10.5px;color:#FFC66D'>Nenhum modelo de linguagem está conectado. Os números vêm de consultas DAX governadas, não de IA.</div></div><div>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#45D5A1" ), "@S", "Implementado" ), "@T", "catálogo de 8 ferramentas tipadas (JSON Schema)" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#45D5A1" ), "@S", "Testado" ), "@T", "8 consultas DAX executadas no modelo em 02/11/2026" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#FFC66D" ), "@S", "Pendente" ), "@T", "orquestrador LLM e linguagem natural" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#FFC66D" ), "@S", "Pendente" ), "@T", "autenticação Entra ID, RLS e endpoint executeQueries" )
        & "</div></div>"
```

### UX Assistente Fluxo

Demonstracao do fluxo pergunta -> ferramentas -> resultados DAX; sem resposta gerada por IA.

Formato: ``

```dax
VAR _rank = TOPN ( 3, FILTER ( ADDCOLUMNS ( VALUES ( dFilial[Cidade] ), "@a", [Atingimento Meta Faturamento %], "@g", [Gap Meta Faturamento] ), NOT ISBLANK ( [@a] ) ), [@a], ASC )
VAR _linhas = CONCATENATEX ( _rank, "<tr><td>" & dFilial[Cidade] & "</td><td class='n'>" & FORMAT ( [@a], "0.0%", "pt-BR" ) & "</td><td class='n'>R$ " & FORMAT ( [@g] / 1e6, "#,0.00", "pt-BR" ) & " mi</td></tr>", "", [@a], ASC )
VAR _ini = MIN ( dCalendario[Data] )
VAR _fim = MIN ( MAX ( dCalendario[Data] ), [Data Corte] )
RETURN
    "<style>.a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;overflow:hidden}.h{font-size:13px;font-weight:600;text-align:center;margin-bottom:8px}.sub{font-size:10.5px;color:#A9B9CA;text-align:center;margin-bottom:10px}.mono{font-family:Consolas,monospace;font-size:11px;color:#7FE6DD}.lb{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin:10px 0 4px}.q{background:#12304F;border-radius:10px 10px 10px 2px;padding:9px 12px;font-size:13px;display:inline-block}.st{border-left:2px solid #173B5C;margin-left:6px;padding:4px 0 4px 12px}.tb{width:100%;border-collapse:collapse;font-size:11.5px}.tb td{padding:5px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.tb td.n{text-align:right;color:#FFFFFF}.pd{border:1px dashed #FFC66D;border-radius:8px;padding:8px 12px;font-size:11px;color:#FFC66D;margin-top:10px}.in{border:1px solid #173B5C;border-radius:8px;padding:8px 12px;font-size:11.5px;color:#6F86A0;margin-top:10px}.ok{color:#45D5A1}.ch{display:inline-block;border:1px solid #173B5C;border-radius:12px;padding:3px 10px;margin:0 6px 6px 0;font-size:10.5px;color:#C9D6E3}</style><div class='a'><div class='h'>Fluxo de uma pergunta (demonstração com dados reais, sem IA)</div>"
        & "<div class='lb'>1 · Pergunta do usuário (exemplo fixo)</div><div class='q'>Onde a meta de faturamento está mais em risco neste período?</div>"
        & "<div class='lb'>2 · Plano de ferramentas que o orquestrador chamaria</div><div class='st'><div class='mono'>resumo_executivo(periodo={" & FORMAT ( _ini, "yyyy-mm-dd" ) & ".." & FORMAT ( _fim, "yyyy-mm-dd" ) & "}, filiais=contexto)</div>"
        & "<div class='mono'>ranking_filiais(metrica=""Atingimento Meta Faturamento %"", ordem=""asc"", top_n=3)</div></div>"
        & "<div class='lb'>3 · Resultado das ferramentas (DAX ao vivo, filtros da página)</div>"
        & "<table class='tb'><tr><td>Receita líquida</td><td class='n'>R$ " & FORMAT ( [Receita (até corte)] / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td class='n'>meta R$ " & FORMAT ( [Meta Faturamento (até corte)] / 1e6, "#,0.0", "pt-BR" ) & " mi</td></tr>"
        & "<tr><td>Atingimento da meta</td><td class='n'>" & FORMAT ( [Atingimento Meta Faturamento %], "0.0%", "pt-BR" ) & "</td><td class='n'>margem bruta " & FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" ) & "</td></tr></table>"
        & "<div class='lb' style='margin-top:8px'>Filiais com menor atingimento (atingimento · gap)</div><table class='tb'>" & _linhas & "</table>"
        & "<div class='pd'>4 · Resposta em linguagem natural: <b>pendente</b>. Quando integrado, o LLM redigirá a resposta somente a partir das linhas acima e citará a ferramenta de origem de cada número.</div>"
        & "<div class='in'>Digite uma pergunta…  <span style='float:right'>entrada desativada: integração pendente</span></div></div>"
```

### UX Assistente Ferramentas

Catalogo de ferramentas tipadas com o resultado atual de cada uma.

Formato: ``

```dax
VAR _r = "<tr><td class='mono'>@N</td><td>@D</td><td class='n'>@V</td></tr>"
VAR _fw = TOPN ( 1, FILTER ( VALUES ( dFilial[Cidade] ), NOT ISBLANK ( [Atingimento Meta Faturamento %] ) ), [Atingimento Meta Faturamento %], ASC )
VAR _vd = TOPN ( 1, VALUES ( dVendedor[Vendedor] ), [Receita Líquida], DESC )
VAR _tr = TOPN ( 1, FILTER ( VALUES ( dTransportadora[Transportadora] ), [Entregas] >= 50 ), [OTIF %], ASC )
VAR _proj = CALCULATE ( SUMX ( VALUES ( dCalendario[AnoMes] ), [Projeção Sazonal Receita] ), REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] IN { 202611, 202612 } )
VAR _sim = CALCULATE ( [Sim Valor Etapa], 'Sim Etapa'[Ordem] = 1 )
RETURN
    "<style>.a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;overflow:hidden}.h{font-size:13px;font-weight:600;text-align:center;margin-bottom:8px}.sub{font-size:10.5px;color:#A9B9CA;text-align:center;margin-bottom:10px}.mono{font-family:Consolas,monospace;font-size:11px;color:#7FE6DD}.lb{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin:10px 0 4px}.q{background:#12304F;border-radius:10px 10px 10px 2px;padding:9px 12px;font-size:13px;display:inline-block}.st{border-left:2px solid #173B5C;margin-left:6px;padding:4px 0 4px 12px}.tb{width:100%;border-collapse:collapse;font-size:11.5px}.tb td{padding:5px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.tb td.n{text-align:right;color:#FFFFFF}.pd{border:1px dashed #FFC66D;border-radius:8px;padding:8px 12px;font-size:11px;color:#FFC66D;margin-top:10px}.in{border:1px solid #173B5C;border-radius:8px;padding:8px 12px;font-size:11.5px;color:#6F86A0;margin-top:10px}.ok{color:#45D5A1}.ch{display:inline-block;border:1px solid #173B5C;border-radius:12px;padding:3px 10px;margin:0 6px 6px 0;font-size:10.5px;color:#C9D6E3}</style><div class='a'><div class='h'>Ferramentas tipadas e o que retornam agora</div><div class='sub'>Somente leitura · parâmetros validados por JSON Schema · consultas em apps/ai_assistant/CONSULTAS_DAX.dax</div><table class='tb'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "resumo_executivo" ), "@D", "receita, margem, meta, churn, OTIF" ), "@V", "R$ " & FORMAT ( [Receita (até corte)] / 1e6, "#,0.0", "pt-BR" ) & " mi · " & FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "ranking_filiais" ), "@D", "ranking por métrica permitida" ), "@V", "menor atingimento: " & MAXX ( _fw, dFilial[Cidade] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "clientes_em_risco" ), "@D", "180–364 dias sem compra, por receita 12M" ), "@V", FORMAT ( [Clientes em Risco], "#,0", "pt-BR" ) & " clientes" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "desempenho_vendedores" ), "@D", "receita, margem e desconto" ), "@V", "maior receita: " & MAXX ( _vd, dVendedor[Vendedor] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "otif_transportadoras" ), "@D", "OTIF, atraso e frete (mín. 50 entregas)" ), "@V", "menor OTIF: " & MAXX ( _tr, dTransportadora[Transportadora] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "dre_gerencial" ), "@D", "DRE por linha vs ano anterior" ), "@V", "resultado R$ " & FORMAT ( [Resultado Gerencial Simplificado] / 1e6, "#,0.0", "pt-BR" ) & " mi" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "projecao_receita" ), "@D", "projeção sazonal com faixa de 90%" ), "@V", "nov–dez/26 R$ " & FORMAT ( _proj / 1e6, "#,0.0", "pt-BR" ) & " mi" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "simular_cenario" ), "@D", "resultado sob premissas (não é previsão)" ), "@V", "base R$ " & FORMAT ( _sim / 1e6, "#,0.0", "pt-BR" ) & " mi" )
        & "</table></div>"
```

### UX Assistente Arquitetura

Diagrama da arquitetura proposta e controles de seguranca.

Formato: ``

```dax
"<style>.a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;overflow:hidden}.h{font-size:13px;font-weight:600;text-align:center;margin-bottom:8px}.sub{font-size:10.5px;color:#A9B9CA;text-align:center;margin-bottom:10px}.mono{font-family:Consolas,monospace;font-size:11px;color:#7FE6DD}.lb{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin:10px 0 4px}.q{background:#12304F;border-radius:10px 10px 10px 2px;padding:9px 12px;font-size:13px;display:inline-block}.st{border-left:2px solid #173B5C;margin-left:6px;padding:4px 0 4px 12px}.tb{width:100%;border-collapse:collapse;font-size:11.5px}.tb td{padding:5px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.tb td.n{text-align:right;color:#FFFFFF}.pd{border:1px dashed #FFC66D;border-radius:8px;padding:8px 12px;font-size:11px;color:#FFC66D;margin-top:10px}.in{border:1px solid #173B5C;border-radius:8px;padding:8px 12px;font-size:11.5px;color:#6F86A0;margin-top:10px}.ok{color:#45D5A1}.ch{display:inline-block;border:1px solid #173B5C;border-radius:12px;padding:3px 10px;margin:0 6px 6px 0;font-size:10.5px;color:#C9D6E3}</style><div class='a'><div class='h'>Arquitetura proposta e controles de segurança</div>"
    & "<svg viewBox='0 0 880 120' width='100%' height='118' font-family='Segoe UI' font-size='11'>"
    & "<defs><marker id='m' viewBox='0 0 8 8' refX='7' refY='4' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0 L8,4 L0,8 z' fill='#5FA8E6'/></marker></defs>"
    & "<g fill='#0C223D' stroke='#173B5C'><rect x='2' y='30' width='130' height='56' rx='8'/><rect x='178' y='30' width='160' height='56' rx='8' stroke='#FFC66D' stroke-dasharray='4 3'/><rect x='384' y='30' width='150' height='56' rx='8'/><rect x='580' y='30' width='140' height='56' rx='8' stroke='#FFC66D' stroke-dasharray='4 3'/><rect x='766' y='30' width='110' height='56' rx='8'/></g>"
    & "<g fill='#FFFFFF' text-anchor='middle' font-weight='600'><text x='67' y='54'>Usuário</text><text x='258' y='54'>Orquestrador LLM</text><text x='459' y='54'>Ferramentas tipadas</text><text x='650' y='54'>API executeQueries</text><text x='821' y='54'>Modelo NEXUS360</text></g>"
    & "<g fill='#A9B9CA' text-anchor='middle' font-size='9.5'><text x='67' y='72'>pergunta</text><text x='258' y='72'>pendente</text><text x='459' y='72'>8 · validadas</text><text x='650' y='72'>pendente</text><text x='821' y='72'>RLS · leitura</text></g>"
    & "<g stroke='#5FA8E6' stroke-width='1.5' marker-end='url(#m)'><line x1='134' y1='58' x2='174' y2='58'/><line x1='340' y1='58' x2='380' y2='58'/><line x1='536' y1='58' x2='576' y2='58'/><line x1='722' y1='58' x2='762' y2='58'/></g>"
    & "<text x='440' y='110' fill='#6F86A0' font-size='9.5' text-anchor='middle'>tracejado = componente não implementado</text></svg>"
    & "<table class='tb' style='margin-top:6px'>"
    & "<tr><td>Sem DAX livre: o LLM escolhe ferramenta e parâmetros; o servidor valida o schema e monta a consulta a partir de modelo fixo.</td></tr>"
    & "<tr><td>Allowlist de medidas e colunas; limites de top_n (≤ 20), de período (até o corte) e de tempo de consulta.</td></tr>"
    & "<tr><td>Identidade do usuário propagada (Entra ID) para aplicar RLS; credencial só de leitura; trilha de auditoria por chamada.</td></tr>"
    & "<tr><td>Resposta obrigatoriamente citada: cada número traz a ferramenta e os filtros de origem; sem dado, sem resposta.</td></tr>"
    & "</table></div>"
```

## 08 UX\Calendário

### UX Calendário Dia

Celula SVG do calendario: dia, campanha ativa, visitas/pedidos e entregas/OTIF. Ponto: verde >= meta, ambar < meta, vermelho = OTIF 5 p.p. abaixo da media do mes (tambem borda). Tracejado apos o corte.

Formato: ``

```dax
VAR _n = COUNTROWS ( VALUES ( dCalendario[Data] ) )
VAR _d = MAX ( dCalendario[Data] )
VAR _corte = [Data Corte]
VAR _fds = WEEKDAY ( _d, 2 ) >= 6
VAR _vis = [Visitas]
VAR _ped = [Visitas com Pedido]
VAR _ent = [Entregas]
VAR _otif = [OTIF %]
VAR _am = MAX ( dCalendario[AnoMes] )
VAR _meta = CALCULATE ( [Meta OTIF % (média simples)], REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] = _am )
VAR _camp = CALCULATE ( COUNTROWS ( FILTER ( dCampanha, dCampanha[Inicio] <= _d && dCampanha[Fim] >= _d ) ) )
VAR _nome = IF ( _camp = 1, CALCULATE ( MAXX ( FILTER ( dCampanha, dCampanha[Inicio] <= _d && dCampanha[Fim] >= _d ), dCampanha[Campanha] ) ) )
VAR _nomeC = IF ( LEN ( _nome ) > 22, LEFT ( _nome, 21 ) & "...", _nome )
VAR _futuro = _d > _corte
VAR _media = CALCULATE ( [OTIF %], REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] = _am, dCalendario[Data] <= _corte )
VAR _abaixo = NOT ISBLANK ( _otif ) && NOT ISBLANK ( _meta ) && _otif < _meta
VAR _pior = NOT ISBLANK ( _otif ) && _otif < _media - 0.05
VAR _stroke = IF ( _pior, "%23FF7285", "%23173B5C" )
VAR _bg = IF ( _fds, "%23081A2E", "%230C223D" )
VAR _txt = IF ( _fds, "%23A9B9CA", "%23FFFFFF" )
VAR _svgCamp =
    IF (
        _camp > 0,
        "<rect x='8' y='30' width='164' height='16' rx='3' fill='%2310D4C4' fill-opacity='0.22'/><text x='14' y='42' font-size='11' fill='%237FE6DD'>"
            & IF ( _camp = 1, SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _nomeC, "&", "e" ), "<", "" ), "'", "" ), "%", "%25" ), "#", "%23" ), _camp & " campanhas ativas" ) & "</text>"
    )
VAR _svgVis =
    IF ( NOT ISBLANK ( _vis ),
        "<circle cx='13' cy='64' r='3.5' fill='%235FA8E6'/><text x='22' y='68' font-size='12' fill='%23C9D6E3'>" & _vis & " visitas %C2%B7 " & ( _ped + 0 ) & " pedidos</text>" )
VAR _svgEnt =
    IF ( NOT ISBLANK ( _ent ),
        "<circle cx='13' cy='86' r='3.5' fill='" & IF ( _pior, "%23FF7285", IF ( _abaixo, "%23FFC66D", "%2345D5A1" ) ) & "'/><text x='22' y='90' font-size='12' fill='%23C9D6E3'>" & _ent & " entregas %C2%B7 OTIF "
            & FORMAT ( _otif * 100, "0" ) & "%25</text>" )
RETURN
    IF (
        _n = 1,
        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='100' viewBox='0 0 180 100' font-family='Segoe UI'>"
            & "<rect x='1' y='1' width='178' height='98' rx='7' fill='" & _bg & "' stroke='" & _stroke & "' stroke-width='" & IF ( _pior, "1.8", "1" ) & "'"
            & IF ( _futuro, " stroke-dasharray='3 3' fill-opacity='0.4'", "" ) & "/>"
            & "<text x='10' y='22' font-size='17' font-weight='600' fill='" & _txt & "'>" & DAY ( _d ) & "</text>"
            & IF ( _futuro, "<text x='170' y='20' font-size='10' text-anchor='end' fill='%236F86A0'>sem dados</text>", "" )
            & _svgCamp & _svgVis & _svgEnt & "</svg>"
    )
```

### UX Calendário KPIs

Faixa de indicadores do periodo ou do dia selecionado.

Formato: ``

```dax
VAR _i = MIN ( dCalendario[Data] )
VAR _f = MIN ( MAX ( dCalendario[Data] ), [Data Corte] )
VAR _um = _i = MAX ( dCalendario[Data] )
VAR _rotulo = IF ( _um, FORMAT ( _i, "dd/mm/yyyy (dddd)", "pt-BR" ), FORMAT ( _i, "dd/mm" ) & " a " & FORMAT ( _f, "dd/mm/yyyy" ) )
VAR _vis = [Visitas]
VAR _conv = [Conversão de Visitas %]
VAR _int = [Interações de Campanha]
VAR _cvc = [Conversões de Campanha]
VAR _camp = [Campanhas Ativas (período)]
VAR _ent = [Entregas]
VAR _otif = [OTIF %]
VAR _am = MAX ( dCalendario[AnoMes] )
VAR _metaOtif = CALCULATE ( [Meta OTIF % (média simples)], REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] = _am )
VAR _rec = [Receita (até corte)]
VAR _meta = IF ( NOT _um && HASONEVALUE ( dCalendario[AnoMes] ), [Meta Faturamento (até corte)] )
VAR _ating = DIVIDE ( _rec, _meta )
VAR _card = "<div class='k' style='border-color:@C'><div class='l'>@L</div><div class='v'>@V</div><div class='s'>@S</div></div>"
VAR _css = "<style>.w{font-family:'Segoe UI',sans-serif;color:#FFFFFF;display:grid;grid-template-columns:1.25fr repeat(5,1fr);gap:12px;height:100vh;box-sizing:border-box;padding:4px 0}.k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-left:3px solid;border-radius:10px;padding:10px 14px;animation:a .5s ease-out both}.l{font-size:10px;letter-spacing:.08em;color:#A9B9CA;text-transform:uppercase}.v{font-size:22px;font-weight:600;margin-top:2px}.s{font-size:10.5px;color:#A9B9CA;margin-top:2px}.p{font-size:15px;font-weight:600;line-height:1.25}@keyframes a{from{opacity:0;transform:translateY(4px)}to{opacity:1}}@media (prefers-reduced-motion:reduce){.k{animation:none}}</style>"
RETURN
    IF (
        ISBLANK ( _vis ) && ISBLANK ( _ent ),
        _css & "<div class='w'><div class='k' style='border-color:#6F86A0;grid-column:1 / span 6'><div class='l'>Sem atividade registrada</div><div class='v' style='font-size:15px'>" & _rotulo & "</div><div class='s'>Datas após o corte (31/10/2026) não têm dados.</div></div></div>",
        _css & "<div class='w'>"
            & "<div class='k' style='border-color:#10D4C4'><div class='l'>" & IF ( _um, "Dia selecionado", "Período" ) & "</div><div class='p'>" & _rotulo & "</div><div class='s'>clique em um dia para detalhar; clique de novo para voltar ao mês</div></div>"
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", "#5FA8E6" ), "@L", "Visitas comerciais" ), "@V", FORMAT ( _vis, "#,0", "pt-BR" ) ), "@S", FORMAT ( _conv, "0.0%", "pt-BR" ) & " viraram pedido" )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", "#10D4C4" ), "@L", "Campanhas ativas" ), "@V", FORMAT ( _camp + 0, "0" ) ), "@S", FORMAT ( _int + 0, "#,0", "pt-BR" ) & " interações · " & FORMAT ( _cvc + 0, "#,0", "pt-BR" ) & " conversões" )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", IF ( _otif < _metaOtif, "#FF7285", "#45D5A1" ) ), "@L", "Entregas" ), "@V", FORMAT ( _ent, "#,0", "pt-BR" ) ), "@S", "OTIF " & FORMAT ( _otif, "0.0%", "pt-BR" ) & " · meta " & FORMAT ( _metaOtif, "0%", "pt-BR" ) )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", IF ( ISBLANK ( _meta ), "#6F86A0", IF ( _ating >= 1, "#45D5A1", "#FFC66D" ) ) ), "@L", "Receita líquida" ), "@V", "R$ " & FORMAT ( _rec / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
                "@S", IF ( ISBLANK ( _meta ), "meta é mensal: selecione o mês inteiro", FORMAT ( _ating, "0.0%", "pt-BR" ) & " da meta do mês" ) )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", "#A9B9CA" ), "@L", "Dias com atividade" ), "@V", FORMAT ( COUNTROWS ( FILTER ( VALUES ( dCalendario[Data] ), NOT ISBLANK ( [Visitas] ) || NOT ISBLANK ( [Entregas] ) ) ), "0" ) ),
                "@S", "de " & COUNTROWS ( VALUES ( dCalendario[Data] ) ) & " dias no período" )
            & "</div>"
    )
```

### UX Tooltip Dia

Tooltip do dia no calendario.

Formato: ``

```dax
VAR _d = MAX ( dCalendario[Data] )
VAR _one = HASONEVALUE ( dCalendario[Data] )
VAR _r = "<tr><td>@L</td><td>@V</td></tr>"
VAR _vis = [Visitas]
RETURN
    IF (
        _one,
        "<style>.t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:10px 12px;height:100vh;box-sizing:border-box;background:#0A1C33;border:1px solid #173B5C;border-radius:8px}.h{font-size:12px;font-weight:600;margin-bottom:6px}.t table{width:100%;font-size:11px;border-collapse:collapse}.t td{padding:2px 0;color:#C9D6E3}.t td+td{text-align:right;color:#FFFFFF}</style><div class='t'><div class='h'>"
            & FORMAT ( _d, "dddd, dd/mm/yyyy", "pt-BR" ) & "</div><table>"
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Visitas" ), "@V", FORMAT ( _vis + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Pedidos nas visitas" ), "@V", FORMAT ( [Visitas com Pedido] + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Propostas / follow-up" ), "@V", FORMAT ( CALCULATE ( [Visitas], fVisitaComercial[Resultado] IN { "Proposta", "Follow-up" } ) + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Interações de campanha" ), "@V", FORMAT ( [Interações de Campanha] + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Entregas" ), "@V", FORMAT ( [Entregas] + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "OTIF" ), "@V", IF ( ISBLANK ( [OTIF %] ), "—", FORMAT ( [OTIF %], "0.0%", "pt-BR" ) ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Receita faturada" ), "@V", "R$ " & FORMAT ( [Receita Líquida] / 1e3, "#,0", "pt-BR" ) & " mil" )
            & "</table></div>"
    )
```

## 08 UX\Clientes

### UX Clientes Status

Painel da base de clientes na Data Referencia: 5 status exclusivos, churn, risco, reativacao, receita recuperada e recompra (medidas validadas).

Formato: ``

```dax
VAR _ref = [Data Referência]
VAR _hist = [Clientes com Histórico]
VAR _st =
    ADDCOLUMNS (
        ALL ( dStatusCliente[Status], dStatusCliente[Ordem] ),
        "@n", CALCULATE ( [Clientes por Status] ),
        "@c", SWITCH ( dStatusCliente[Status], "Novo", "#7FE6DD", "Ativo", "#45D5A1", "Reativado", "#5FA8E6", "Em risco", "#FFC66D", "#FF7285" )
    )
VAR _seg = CONCATENATEX ( _st, "<span style='flex:" & FORMAT ( [@n], "0", "en-US" ) & ";background:" & [@c] & "'></span>", "", dStatusCliente[Ordem], ASC )
VAR _rows =
    CONCATENATEX (
        _st,
        "<div class='nx-sr'><span class='nx-sd' style='background:" & [@c] & "'></span><span class='nx-sn'>" & dStatusCliente[Status] & "</span><b>" & FORMAT ( [@n], "#,0", "pt-BR" ) & "</b><span class='nx-sp'>" & FORMAT ( DIVIDE ( [@n], _hist ), "0.0%", "pt-BR" ) & "</span></div>",
        "", dStatusCliente[Ordem], ASC
    )
VAR _css = "<style>.nx-s{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:16px 20px;display:flex;flex-direction:column;gap:12px;animation:nxIn .6s ease-out both}.nx-st{font-size:13px;font-weight:600;text-align:center}.nx-sh{font-size:10px;letter-spacing:.12em;color:#A9B9CA;text-transform:uppercase}.nx-sk{font-size:30px;font-weight:600;line-height:1.05}.nx-sk small{font-size:12px;color:#A9B9CA;font-weight:400;margin-left:6px}.nx-bar{display:flex;height:10px;border-radius:5px;overflow:hidden;gap:2px;margin:6px 0 4px}.nx-sr{display:flex;align-items:center;gap:8px;font-size:12px;padding:4px 0;border-bottom:1px solid #12304F}.nx-sd{width:9px;height:9px;border-radius:50%}.nx-sn{flex:1;color:#C9D6E3}.nx-sr b{font-weight:600;width:60px;text-align:right}.nx-sp{width:46px;text-align:right;color:#A9B9CA}.nx-g2{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}.nx-g2 .nx-sk{font-size:20px}.nx-blk{border-left:3px solid #173B5C;padding-left:10px}.nx-blk.r{border-color:#FF7285}.nx-blk.a{border-color:#FFC66D}.nx-blk.g{border-color:#45D5A1}.nx-blk.b{border-color:#5FA8E6}.nx-nt{font-size:10px;color:#6F86A0}@keyframes nxIn{from{opacity:0}to{opacity:1}}@media (prefers-reduced-motion:reduce){.nx-s{animation:none}}</style>"
RETURN
    IF (
        NOT ISBLANK ( _ref ),
        _css & "<div class='nx-s'><div class='nx-st'>Base de clientes em " & FORMAT ( _ref, "dd/mm/yyyy" ) & "</div>"
            & "<div><div class='nx-sh'>Clientes com histórico</div><div class='nx-sk'>" & FORMAT ( _hist, "#,0", "pt-BR" ) & "</div><div class='nx-bar'>" & _seg & "</div>" & _rows & "</div>"
            & "<div class='nx-g2'><div class='nx-blk r'><div class='nx-sh'>Taxa de churn</div><div class='nx-sk'>" & FORMAT ( [Taxa de Churn %], "0.0%", "pt-BR" ) & "</div><div class='nx-nt'>sem compra há " & [Limite Churn (dias)] & "+ dias</div></div>"
            & "<div class='nx-blk a'><div class='nx-sh'>Em risco</div><div class='nx-sk'>" & FORMAT ( [Clientes em Risco %], "0.0%", "pt-BR" ) & "</div><div class='nx-nt'>" & [Limite Ativo (dias)] & " a " & ( [Limite Churn (dias)] - 1 ) & " dias</div></div></div>"
            & "<div class='nx-g2'><div class='nx-blk b'><div class='nx-sh'>Reativações no período</div><div class='nx-sk'>" & FORMAT ( [Reativações no Período], "#,0", "pt-BR" ) & "</div><div class='nx-nt'>retorno após " & [Limite Churn (dias)] & "+ dias sem compra</div></div>"
            & "<div class='nx-blk b'><div class='nx-sh'>Receita recuperada</div><div class='nx-sk'>R$ " & FORMAT ( [Receita Recuperada] / 1e6, "#,0.0", "pt-BR" ) & " mi</div><div class='nx-nt'>faturas de reativados no período</div></div></div>"
            & "<div class='nx-g2'><div class='nx-blk g'><div class='nx-sh'>Taxa de recompra</div><div class='nx-sk'>" & FORMAT ( [Taxa de Recompra %], "0.0%", "pt-BR" ) & "</div><div class='nx-nt'>clientes com 2+ faturas no período</div></div>"
            & "<div class='nx-blk g'><div class='nx-sh'>Intervalo entre compras</div><div class='nx-sk'>" & FORMAT ( [Intervalo Médio entre Compras (dias)], "#,0", "pt-BR" ) & " <small>dias (mediana " & FORMAT ( [Intervalo Mediano entre Compras (dias)], "#,0", "pt-BR" ) & ")</small></div><div class='nx-nt'>" & FORMAT ( [Compras por Cliente], "0.00", "pt-BR" ) & " compras por cliente</div></div></div>"
            & "</div>"
    )
```

### UX Clientes Freq Valor

Grade frequencia (faturas no periodo: 1, 2, 3-4, 5+) x valor (quartis da receita do periodo). Faixas de exibicao, nao pontuacao RFM.

Formato: ``

```dax
VAR _t =
    FILTER (
        ADDCOLUMNS (
            SUMMARIZE ( fFaturamento, fFaturamento[ClienteID] ),
            "@f", CALCULATE ( COUNTROWS ( fFaturamento ) ),
            "@v", CALCULATE ( SUM ( fFaturamento[ReceitaLiquida] ) )
        ),
        [@v] > 0
    )
VAR _n = COUNTROWS ( _t )
VAR _tot = SUMX ( _t, [@v] )
VAR _q1 = PERCENTILEX.INC ( _t, [@v], 0.25 )
VAR _q2 = PERCENTILEX.INC ( _t, [@v], 0.5 )
VAR _q3 = PERCENTILEX.INC ( _t, [@v], 0.75 )
VAR _b =
    ADDCOLUMNS (
        _t,
        "@fb", SWITCH ( TRUE (), [@f] = 1, 1, [@f] = 2, 2, [@f] <= 4, 3, 4 ),
        "@vb", SWITCH ( TRUE (), [@v] > _q3, 4, [@v] > _q2, 3, [@v] > _q1, 2, 1 )
    )
VAR _g = GROUPBY ( _b, [@vb], [@fb], "@cn", COUNTX ( CURRENTGROUP (), 1 ), "@rv", SUMX ( CURRENTGROUP (), [@v] ) )
VAR _max = MAXX ( _g, [@cn] )
VAR _hdr = "<div></div><div class='nx-fh'>1 compra</div><div class='nx-fh'>2</div><div class='nx-fh'>3–4</div><div class='nx-fh'>5+</div>"
VAR _lbl = SELECTCOLUMNS ( { ( 4, "Valor Q4 (maior)" ), ( 3, "Valor Q3" ), ( 2, "Valor Q2" ), ( 1, "Valor Q1 (menor)" ) }, "vb", [Value1], "lb", [Value2] )
VAR _grid =
    CONCATENATEX (
        _lbl,
        VAR _vb = [vb]
        RETURN
            "<div class='nx-fl'>" & [lb] & "</div>"
                & CONCATENATEX (
                    { 1, 2, 3, 4 },
                    VAR _fb = [Value]
                    VAR _c = MAXX ( FILTER ( _g, [@vb] = _vb && [@fb] = _fb ), [@cn] )
                    VAR _r = MAXX ( FILTER ( _g, [@vb] = _vb && [@fb] = _fb ), [@rv] )
                    VAR _a = FORMAT ( 0.12 + 0.78 * DIVIDE ( _c, _max ), "0.00", "en-US" )
                    VAR _hl = IF ( _vb = 4 && _fb = 1, " nx-hl", "" )
                    RETURN "<div class='nx-fc" & _hl & "' style='background:rgba(16,212,196," & _a & ")'><b>" & FORMAT ( _c, "#,0", "pt-BR" ) & "</b><span>" & FORMAT ( DIVIDE ( _r, _tot ), "0%", "pt-BR" ) & " rec.</span></div>",
                    "", [Value], ASC
                ),
        "", [vb], DESC
    )
VAR _hv = MAXX ( FILTER ( _g, [@vb] = 4 && [@fb] = 1 ), [@cn] )
VAR _hr = MAXX ( FILTER ( _g, [@vb] = 4 && [@fb] = 1 ), [@rv] )
VAR _css = "<style>.nx-f{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:12px 16px;display:flex;flex-direction:column}.nx-ft{font-size:13px;font-weight:600;text-align:center}.nx-fs{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 8px}.nx-fg{display:grid;grid-template-columns:92px repeat(4,1fr);gap:4px;flex:1}.nx-fh{font-size:10px;color:#A9B9CA;text-align:center;align-self:end}.nx-fl{font-size:10px;color:#A9B9CA;display:flex;align-items:center}.nx-fc{border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px}.nx-fc b{font-weight:600}.nx-fc span{font-size:9.5px;color:#E8F7F5}.nx-hl{outline:2px solid #FFC66D}.nx-fn{font-size:10.5px;color:#C9D6E3;margin-top:8px}.nx-fn b{color:#FFC66D}</style>"
RETURN
    IF (
        _n > 0,
        _css & "<div class='nx-f'><div class='nx-ft'>Frequência × valor dos clientes no período</div><div class='nx-fs'>" & FORMAT ( _n, "#,0", "pt-BR" ) & " clientes com fatura · valor em quartis · célula = clientes e % da receita</div>"
            & "<div class='nx-fg'>" & _hdr & _grid & "</div>"
            & "<div class='nx-fn'><b>" & FORMAT ( _hv, "#,0", "pt-BR" ) & "</b> clientes de maior valor compraram uma única vez (" & FORMAT ( DIVIDE ( _hr, _tot ), "0.0%", "pt-BR" ) & " da receita): candidatos a recompra.</div></div>"
    )
```

## 08 UX\Comercial

### UX Comercial KPIs

Faixa de 4 KPIs comerciais com variacao vs ano anterior (ate o corte) e barras atual x anterior. Desconto maior e desfavoravel.

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _rec = [Receita (até corte)]
VAR _recLY = [Receita LY]
VAR _mg = [Margem Bruta %]
VAR _mgLY = [Margem Bruta % LY]
VAR _ds = [Desconto Médio Ponderado %]
VAR _dsLY = CALCULATE ( CALCULATE ( [Desconto Médio Ponderado %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _cl = [Clientes Positivados]
VAR _clLY = CALCULATE ( CALCULATE ( [Clientes Positivados], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _css = "<style>.nx-r{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(4,1fr);height:100vh;box-sizing:border-box;gap:16px}.nx-c{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:12px 18px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-cl{font-size:10px;letter-spacing:.12em;color:#A9B9CA;text-transform:uppercase}.nx-cv{font-size:26px;font-weight:600;color:#FFFFFF;line-height:1.15;margin-top:3px}.nx-cd{font-size:11px;font-weight:600;margin-top:2px}.nx-cd span{color:#6F86A0;font-weight:400}.nx-cb{width:100%;height:20px;margin-top:6px}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-c{animation:none}}</style>"
RETURN
    _css & "<div class='nx-r'>"
        & "<div class='nx-c' style='animation-delay:0.00s'><div class='nx-cl'>Receita líquida</div><div class='nx-cv'>" & "R$ " & FORMAT ( [Receita Líquida] / 1e6, "#,0.0", "pt-BR" ) & " mi" & "</div>"
        & IF ( _umAno && NOT ISBLANK ( _recLY ),
            "<div class='nx-cd' style='color:" & IF ( _rec >= _recLY, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _rec - _recLY, _recLY ), "▲ 0.0%;▼ 0.0%", "pt-BR" ) & " <span>vs ano anterior</span></div>"
                & "<svg class='nx-cb' viewBox='0 0 200 22' preserveAspectRatio='none'><rect x='0' y='2' height='7' rx='2' fill='#10D4C4' width='" & FORMAT ( 200 * DIVIDE ( _rec, MAX ( _rec, _recLY ) ), "0", "en-US" ) & "'/><rect x='0' y='13' height='7' rx='2' fill='#3E5C7A' width='" & FORMAT ( 200 * DIVIDE ( _recLY, MAX ( _rec, _recLY ) ), "0", "en-US" ) & "'/></svg>",
            "<div class='nx-cd' style='color:#A9B9CA'>Selecione um único ano para comparar</div>" )
        & "</div>"
        & "<div class='nx-c' style='animation-delay:0.07s'><div class='nx-cl'>Margem bruta</div><div class='nx-cv'>" & FORMAT ( _mg, "0.0%", "pt-BR" ) & "</div>"
        & IF ( _umAno && NOT ISBLANK ( _mgLY ),
            "<div class='nx-cd' style='color:" & IF ( _mg >= _mgLY, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( ( _mg - _mgLY ) * 100, "▲ 0.0;▼ 0.0", "pt-BR" ) & " p.p." & " <span>vs ano anterior</span></div>"
                & "<svg class='nx-cb' viewBox='0 0 200 22' preserveAspectRatio='none'><rect x='0' y='2' height='7' rx='2' fill='#10D4C4' width='" & FORMAT ( 200 * DIVIDE ( _mg, MAX ( _mg, _mgLY ) ), "0", "en-US" ) & "'/><rect x='0' y='13' height='7' rx='2' fill='#3E5C7A' width='" & FORMAT ( 200 * DIVIDE ( _mgLY, MAX ( _mg, _mgLY ) ), "0", "en-US" ) & "'/></svg>",
            "<div class='nx-cd' style='color:#A9B9CA'>Selecione um único ano para comparar</div>" )
        & "</div>"
        & "<div class='nx-c' style='animation-delay:0.14s'><div class='nx-cl'>Desconto médio ponderado</div><div class='nx-cv'>" & FORMAT ( _ds, "0.0%", "pt-BR" ) & "</div>"
        & IF ( _umAno && NOT ISBLANK ( _dsLY ),
            "<div class='nx-cd' style='color:" & IF ( _ds <= _dsLY, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( ( _ds - _dsLY ) * 100, "▲ 0.0;▼ 0.0", "pt-BR" ) & " p.p." & " <span>vs ano anterior</span></div>"
                & "<svg class='nx-cb' viewBox='0 0 200 22' preserveAspectRatio='none'><rect x='0' y='2' height='7' rx='2' fill='#10D4C4' width='" & FORMAT ( 200 * DIVIDE ( _ds, MAX ( _ds, _dsLY ) ), "0", "en-US" ) & "'/><rect x='0' y='13' height='7' rx='2' fill='#3E5C7A' width='" & FORMAT ( 200 * DIVIDE ( _dsLY, MAX ( _ds, _dsLY ) ), "0", "en-US" ) & "'/></svg>",
            "<div class='nx-cd' style='color:#A9B9CA'>Selecione um único ano para comparar</div>" )
        & "</div>"
        & "<div class='nx-c' style='animation-delay:0.21s'><div class='nx-cl'>Clientes positivados</div><div class='nx-cv'>" & FORMAT ( _cl, "#,0", "pt-BR" ) & "</div>"
        & IF ( _umAno && NOT ISBLANK ( _clLY ),
            "<div class='nx-cd' style='color:" & IF ( _cl >= _clLY, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _cl - _clLY, _clLY ), "▲ 0.0%;▼ 0.0%", "pt-BR" ) & " <span>vs ano anterior</span></div>"
                & "<svg class='nx-cb' viewBox='0 0 200 22' preserveAspectRatio='none'><rect x='0' y='2' height='7' rx='2' fill='#10D4C4' width='" & FORMAT ( 200 * DIVIDE ( _cl, MAX ( _cl, _clLY ) ), "0", "en-US" ) & "'/><rect x='0' y='13' height='7' rx='2' fill='#3E5C7A' width='" & FORMAT ( 200 * DIVIDE ( _clLY, MAX ( _cl, _clLY ) ), "0", "en-US" ) & "'/></svg>",
            "<div class='nx-cd' style='color:#A9B9CA'>Selecione um único ano para comparar</div>" )
        & "</div>"
        & "</div>"
```

### UX Barra Participação

Barra SVG da participacao na receita, escalada pelo maior item do mesmo nivel (categoria ou subcategoria).

Formato: ``

```dax
VAR _p = [Participação Receita %]
VAR _max =
    SWITCH (
        TRUE (),
        ISINSCOPE ( dProduto[Subcategoria] ), MAXX ( ALLSELECTED ( dProduto[Subcategoria] ), [Participação Receita %] ),
        ISINSCOPE ( dProduto[Categoria] ), MAXX ( ALLSELECTED ( dProduto[Categoria] ), [Participação Receita %] ),
        _p
    )
VAR _w = FORMAT ( 110 * DIVIDE ( _p, _max ), "0", "en-US" )
RETURN
    IF (
        NOT ISBLANK ( _p ) && ( ISINSCOPE ( dProduto[Categoria] ) || ISINSCOPE ( dProduto[Subcategoria] ) ),
        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='16'><rect x='0' y='4' width='110' height='8' rx='3' fill='%2312304F'/><rect x='0' y='4' width='" & _w & "' height='8' rx='3' fill='%2310D4C4'/></svg>"
    )
```

### UX Comercial Oportunidades

Diagnostico: subcategorias em queda vs ano anterior, vendedores com desconto acima do 3o quartil e margem abaixo da mediana, concentracao da receita nos 20% maiores vendedores.

Formato: ``

```dax
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _v =
    FILTER (
        ADDCOLUMNS (
            VALUES ( dVendedor[Vendedor] ),
            "@r", [Receita Líquida],
            "@d", [Desconto Médio Ponderado %],
            "@m", [Margem Bruta %]
        ),
        [@r] > 0
    )
VAR _n = COUNTROWS ( _v )
VAR _p75 = PERCENTILEX.INC ( _v, [@d], 0.75 )
VAR _med = MEDIANX ( _v, [@m] )
VAR _crit = FILTER ( _v, [@d] > _p75 && [@m] < _med )
VAR _tot = SUMX ( _v, [@r] )
VAR _top = TOPN ( ROUNDUP ( _n * 0.2, 0 ), _v, [@r], DESC )
VAR _conc = DIVIDE ( SUMX ( _top, [@r] ), _tot )
VAR _sub =
    FILTER (
        ADDCOLUMNS ( VALUES ( dProduto[Subcategoria] ), "@dy", [Receita YoY Δ], "@py", [Receita YoY %] ),
        NOT ISBLANK ( [@dy] ) && [@dy] < 0
    )
VAR _subTxt =
    IF (
        NOT _umAno, "<div class='nx-o-e'>Selecione um único ano para comparar com o anterior.</div>",
        IF (
            ISEMPTY ( _sub ), "<div class='nx-o-e'>Nenhuma subcategoria abaixo do ano anterior.</div>",
            CONCATENATEX (
                TOPN ( 3, _sub, [@dy], ASC ),
                "<div class='nx-o-l'><span>" & dProduto[Subcategoria] & "</span><b style='color:#FF7285'>" & FORMAT ( [@dy] / 1e6, "#,0.0", "pt-BR" ) & " mi · " & FORMAT ( [@py], "0.0%", "pt-BR" ) & "</b></div>",
                "", [@dy], ASC
            )
        )
    )
VAR _vendTxt =
    CONCATENATEX (
        TOPN ( 3, _crit, [@r], DESC ),
        "<div class='nx-o-l'><span>" & dVendedor[Vendedor] & "</span><b>" & FORMAT ( [@d], "0.0%", "pt-BR" ) & " desc. · " & FORMAT ( [@m], "0.0%", "pt-BR" ) & " marg.</b></div>",
        "", [@r], DESC
    )
VAR _css = "<style>.nx-o{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 20px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr;gap:10px 22px}.nx-o-t{grid-column:1/3;font-size:13px;font-weight:600;text-align:center}.nx-o-b{border-left:3px solid #FFC66D;padding-left:12px}.nx-o-b.n{border-color:#FF7285}.nx-o-b.i{border-color:#5FA8E6}.nx-o-h{font-size:10px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin-bottom:6px}.nx-o-k{font-size:24px;font-weight:600}.nx-o-s{font-size:11px;color:#A9B9CA;margin-bottom:6px}.nx-o-l{display:flex;justify-content:space-between;font-size:11.5px;padding:3px 0;border-bottom:1px solid #12304F;color:#C9D6E3}.nx-o-l b{font-weight:600;color:#FFFFFF}.nx-o-e{font-size:11px;color:#6F86A0}</style>"
RETURN
    _css & "<div class='nx-o'><div class='nx-o-t'>Oportunidades e exceções comerciais</div>"
        & "<div class='nx-o-b n'><div class='nx-o-h'>Subcategorias em queda</div>" & _subTxt & "</div>"
        & "<div><div class='nx-o-b'><div class='nx-o-h'>Desconto alto e margem baixa</div><div class='nx-o-k'>" & COUNTROWS ( _crit ) & " <span style='font-size:13px;color:#A9B9CA'>de " & _n & " vendedores</span></div>"
        & "<div class='nx-o-s'>desconto acima do 3º quartil (" & FORMAT ( _p75, "0.0%", "pt-BR" ) & ") e margem abaixo da mediana (" & FORMAT ( _med, "0.0%", "pt-BR" ) & ")</div>" & _vendTxt & "</div>"
        & "<div class='nx-o-b i' style='margin-top:12px'><div class='nx-o-h'>Concentração</div><div class='nx-o-s' style='margin:0'><b style='color:#FFFFFF;font-size:15px'>" & FORMAT ( _conc, "0.0%", "pt-BR" ) & "</b> da receita vem dos 20% maiores vendedores (" & ROUNDUP ( _n * 0.2, 0 ) & ")</div></div></div></div>"
```

## 08 UX\Componentes

### UX Cabeçalho

Cabeçalho HTML reutilizável: título e subtítulo de dPaginaUX (filtro de visual por página), período do contexto limitado ao corte e data do último refresh.

Formato: ``

```dax
VAR _pagina = SELECTEDVALUE ( dPaginaUX[Pagina], "NEXUS 360" )
VAR _sub = SELECTEDVALUE ( dPaginaUX[Subtitulo] )
VAR _corte = [Data Corte]
VAR _ini = CALCULATE ( MIN ( dCalendario[Data] ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _fim = [Data Referência]
VAR _periodo =
    IF ( ISBLANK ( _fim ), "sem realizado no período", FORMAT ( _ini, "mmm/yyyy", "pt-BR" ) & " – " & FORMAT ( _fim, "mmm/yyyy", "pt-BR" ) )
VAR _atual = [Data Atualização]
VAR _css = "<style>.nx-h{font-family:'Segoe UI',sans-serif;display:flex;align-items:center;justify-content:space-between;height:100%;padding:0 34px 0 22px;box-sizing:border-box;color:#FFFFFF;animation:nxFade .6s ease-out both}.nx-h1{font-size:24px;font-weight:600;line-height:1.15}.nx-h2{font-size:12px;color:#A9B9CA;margin-top:3px}.nx-m{text-align:right;font-size:11px;color:#A9B9CA;line-height:1.6;white-space:nowrap}.nx-m b{color:#FFFFFF;font-weight:600}.nx-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#10D4C4;margin-right:6px;vertical-align:middle}@keyframes nxFade{from{opacity:0}to{opacity:1}}@media (prefers-reduced-motion:reduce){.nx-h{animation:none}}</style>"
RETURN
    _css & "<div class='nx-h'><div><div class='nx-h1'>" & _pagina & "</div><div class='nx-h2'>" & _sub & "</div></div>"
        & "<div class='nx-m'><div>Período <b>" & _periodo & "</b></div><div><span class='nx-dot'></span>Histórico até " & FORMAT ( _corte, "dd/mm/yyyy" ) & " · atualizado " & FORMAT ( _atual, "dd/mm/yyyy hh:nn" ) & "</div></div></div>"
```

### UX Filtros Ativos

Barra HTML de filtros ativos: período, região, filial e categoria refletem o contexto DAX real (seleção múltipla, ausência de filtro e filtro cruzado). Chip em destaque quando o filtro está aplicado.

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _ini = CALCULATE ( MIN ( dCalendario[Data] ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _fim = [Data Referência]
VAR _perOn = ISCROSSFILTERED ( dCalendario )
VAR _periodo = IF ( ISBLANK ( _fim ), "SEM REALIZADO", UPPER ( FORMAT ( _ini, "mmm/yyyy", "pt-BR" ) & " – " & FORMAT ( _fim, "mmm/yyyy", "pt-BR" ) ) )
VAR _regOn = ISFILTERED ( dFilial[Regiao] )
VAR _regiao = IF ( _regOn, UPPER ( CONCATENATEX ( VALUES ( dFilial[Regiao] ), dFilial[Regiao], ", ", dFilial[Regiao], ASC ) ), "TODAS" )
VAR _nFil = COUNTROWS ( VALUES ( dFilial[Filial] ) )
VAR _filOn = ISCROSSFILTERED ( dFilial[Filial] )
VAR _filial =
    SWITCH (
        TRUE (),
        ISFILTERED ( dFilial[Filial] ),
            UPPER (
                IF (
                    _nFil <= 2,
                    CONCATENATEX ( VALUES ( dFilial[Filial] ), SUBSTITUTE ( dFilial[Filial], "Unidade ", "" ), ", ", dFilial[Filial], ASC ),
                    CONCATENATEX ( TOPN ( 2, VALUES ( dFilial[Filial] ), dFilial[Filial], ASC ), SUBSTITUTE ( dFilial[Filial], "Unidade ", "" ), ", ", dFilial[Filial], ASC ) & " +" & ( _nFil - 2 )
                )
            ),
        _filOn, _nFil & " DE " & COUNTROWS ( ALL ( dFilial[Filial] ) ),
        "TODAS"
    )
VAR _nCat = COUNTROWS ( VALUES ( dProduto[Categoria] ) )
VAR _catOn = ISCROSSFILTERED ( dProduto )
VAR _cat =
    SWITCH (
        TRUE (),
        ISFILTERED ( dProduto[Categoria] ),
            UPPER (
                IF (
                    _nCat <= 2,
                    CONCATENATEX ( VALUES ( dProduto[Categoria] ), dProduto[Categoria], ", ", dProduto[Categoria], ASC ),
                    CONCATENATEX ( TOPN ( 2, VALUES ( dProduto[Categoria] ), dProduto[Categoria], ASC ), dProduto[Categoria], ", ", dProduto[Categoria], ASC ) & " +" & ( _nCat - 2 )
                )
            ),
        _catOn, "FILTRADA",
        "TODAS"
    )
VAR _css = "<style>.nx-f{font-family:'Segoe UI',sans-serif;display:flex;align-items:center;gap:10px;height:100%;padding:0 12px;box-sizing:border-box;overflow:hidden}.nx-c{font-size:12px;color:#FFFFFF;padding:6px 12px;border:1px solid #173B5C;border-radius:8px;white-space:nowrap;background:rgba(7,21,40,.55)}.nx-c i{font-style:normal;font-size:10px;letter-spacing:.08em;color:#A9B9CA;margin-right:8px;font-weight:600}.nx-c.on{border-color:#10D4C4}.nx-w{margin-left:auto;font-size:11px;color:#FFC66D;white-space:nowrap}</style>"
RETURN
    _css & "<div class='nx-f' role='status' aria-label='Filtros ativos'>"
        & "<span class='nx-c" & IF ( _perOn, " on" ) & "'><i>PERÍODO</i>" & _periodo & "</span>"
        & "<span class='nx-c" & IF ( _regOn, " on" ) & "'><i>REGIÃO</i>" & _regiao & "</span>"
        & "<span class='nx-c" & IF ( _filOn, " on" ) & "'><i>FILIAL</i>" & _filial & "</span>"
        & "<span class='nx-c" & IF ( _catOn, " on" ) & "'><i>CATEGORIA</i>" & _cat & "</span>"
        & IF ( [Filtro de Produto Ativo], "<span class='nx-w'>▲ Despesas, frete, devoluções e metas não têm produto: indisponíveis com este filtro</span>" )
        & "</div>"
```

### UX Info Página

Conteúdo do painel de informações da página (dPaginaUX).

Formato: ``

```dax
VAR _obj = SELECTEDVALUE ( dPaginaUX[Objetivo] )
VAR _kpis = SELECTEDVALUE ( dPaginaUX[KPIs] )
VAR _fonte = SELECTEDVALUE ( dPaginaUX[Fonte] )
VAR _regras = SELECTEDVALUE ( dPaginaUX[Regras] )
VAR _lim = SELECTEDVALUE ( dPaginaUX[Limitacoes] )
VAR _css = "<style>.nx-i{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:22px 24px;box-sizing:border-box;font-size:12px;line-height:1.55}.nx-it{font-size:16px;font-weight:600;margin-bottom:4px}.nx-i h4{font-size:10px;letter-spacing:.1em;color:#10D4C4;margin:16px 0 6px;font-weight:600}.nx-i p{margin:0;color:#C9D6E3}.nx-i ul{margin:0;padding-left:16px;color:#C9D6E3}.nx-i li{margin-bottom:4px}.nx-i b{color:#FFFFFF;font-weight:600}</style>"
VAR _li = "<ul><li>" & SUBSTITUTE ( _kpis, "|", "</li><li>" ) & "</li></ul>"
RETURN
    IF (
        NOT ISBLANK ( _obj ),
        _css & "<div class='nx-i'><div class='nx-it'>Sobre esta página</div>"
            & "<h4>OBJETIVO</h4><p>" & _obj & "</p>"
            & "<h4>INDICADORES</h4>" & _li
            & "<h4>FONTE E PERÍODO</h4><p>" & _fonte & " Dados até " & FORMAT ( [Data Corte], "dd/mm/yyyy" ) & ".</p>"
            & "<h4>REGRAS</h4><ul><li>" & SUBSTITUTE ( _regras, "|", "</li><li>" ) & "</li></ul>"
            & "<h4>LIMITAÇÕES</h4><ul><li>" & SUBSTITUTE ( _lim, "|", "</li><li>" ) & "</li></ul></div>"
    )
```

### UX Card KPI

Card KPI HTML/SVG reutilizável, parametrizado por dKPI (Receita, Margem, Resultado, OTIF, Clientes). Valor, comparação com o ano anterior (limitada ao corte), meta e sparkline de 12 meses até a Data Referência. Borda semântica: verde/vermelho conforme meta ou ano anterior; neutra quando não há regra. Animações CSS discretas com prefers-reduced-motion.

Formato: ``

```dax
VAR _kpi = SELECTEDVALUE ( dKPI[KPI] )
VAR _corte = [Data Corte]
VAR _ref = [Data Referência]
VAR _prod = [Filtro de Produto Ativo]
VAR _umAno = CALCULATE ( DISTINCTCOUNT ( dCalendario[Ano] ), KEEPFILTERS ( dCalendario[Data] <= _corte ) ) = 1
VAR _semBase = IF ( _umAno, "Sem base no ano anterior", "Selecione um único ano para comparar" )
VAR cPos = "#45D5A1"
VAR cNeg = "#FF7285"
VAR cAte = "#FFC66D"
VAR cNeu = "#A9B9CA"
VAR cTeal = "#10D4C4"
-- sparkline: 12 meses encerrando na Data Referencia
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            VAR _i = EOMONTH ( _f, -1 ) + 1
            RETURN
                CALCULATE (
                    SWITCH ( _kpi, "Receita", [Receita Líquida], "Margem", [Margem Bruta %], "Resultado", [Resultado Gerencial Simplificado], "OTIF", [OTIF %] ),
                    REMOVEFILTERS ( dCalendario ),
                    dCalendario[Data] >= _i,
                    dCalendario[Data] <= _f
                )
    )
VAR _ok = FILTER ( _serie, NOT ISBLANK ( [@V] ) )
VAR _n = COUNTROWS ( _ok )
VAR _min = MINX ( _ok, [@V] )
VAR _max = MAXX ( _ok, [@V] )
VAR _rng = IF ( _max = _min, 1, _max - _min )
VAR _pts = CONCATENATEX ( _ok, FORMAT ( ( 11 - [Value] ) / 11 * 120, "0.0", "en-US" ) & "," & FORMAT ( 32 - ( [@V] - _min ) / _rng * 28, "0.0", "en-US" ), " ", [Value], DESC )
VAR _vUlt = MAXX ( FILTER ( _ok, [Value] = 0 ), [@V] )
VAR _spark =
    IF (
        _n >= 2,
        "<svg width='128' height='36' viewBox='-4 0 128 36' role='img' aria-label='Tendência dos últimos 12 meses'><polyline points='" & _pts & "' fill='none' stroke='" & cTeal & "' stroke-width='1.8' stroke-linejoin='round' stroke-linecap='round' class='nx-draw'/>"
            & IF ( NOT ISBLANK ( _vUlt ), "<circle cx='120' cy='" & FORMAT ( 32 - ( _vUlt - _min ) / _rng * 28, "0.0", "en-US" ) & "' r='3' fill='" & cTeal & "'/>" )
            & "</svg>"
    )
-- Receita
VAR rV = [Receita Líquida]
VAR rYoY = IF ( _umAno, [Receita YoY %] )
VAR rAt = [Atingimento Meta Faturamento %]
VAR rTxt =
    IF ( ISBLANK ( rV ), "—",
        "R$ " & SWITCH ( TRUE (),
            ABS ( rV ) >= 1e9, FORMAT ( rV / 1e9, "#,0.00", "pt-BR" ) & " bi",
            ABS ( rV ) >= 1e6, FORMAT ( rV / 1e6, "#,0.0", "pt-BR" ) & " mi",
            ABS ( rV ) >= 1e3, FORMAT ( rV / 1e3, "#,0.0", "pt-BR" ) & " mil",
            FORMAT ( rV, "#,0", "pt-BR" ) ) )
VAR rL1 = IF ( ISBLANK ( rYoY ), _semBase, "<span style='color:" & IF ( rYoY >= 0, cPos, cNeg ) & "'>" & IF ( rYoY >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( rYoY ), "0.0%", "pt-BR" ) & "</span> vs ano anterior" )
VAR rCorAt = SWITCH ( TRUE (), rAt >= 1, cPos, rAt >= 0.95, cAte, cNeg )
VAR rL2 =
    IF ( ISBLANK ( rAt ),
        IF ( _prod, "Meta indisponível com filtro de produto", "Sem meta no período" ),
        "<div class='nx-pb'><div class='nx-tr'><div class='nx-fl' style='width:" & FORMAT ( MIN ( rAt, 1 ) * 100, "0.0", "en-US" ) & "%;background:" & rCorAt & "'></div></div><span><b style='color:" & rCorAt & "'>" & FORMAT ( rAt, "0.0%", "pt-BR" ) & "</b> da meta</span></div>" )
-- Margem
VAR mV = [Margem Bruta %]
VAR mPP = IF ( _umAno, [Margem Bruta % YoY (p.p.)] )
VAR mMeta = CALCULATE ( [Meta Margem Bruta % (ponderada)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR mDev = [Desvio Margem vs Meta (p.p.)]
VAR mL1 = IF ( ISBLANK ( mPP ), _semBase, "<span style='color:" & IF ( mPP >= 0, cPos, cNeg ) & "'>" & IF ( mPP >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( mPP ), "0.00", "pt-BR" ) & " p.p.</span> vs ano anterior" )
VAR mL2 = IF ( ISBLANK ( mDev ), IF ( _prod, "Meta indisponível com filtro de produto", "Sem meta no período" ), "Meta " & FORMAT ( mMeta, "0.0%", "pt-BR" ) & " · <b style='color:" & IF ( mDev >= 0, cPos, cNeg ) & "'>" & FORMAT ( mDev, "+0.0;-0.0", "pt-BR" ) & " p.p.</b>" )
-- Resultado gerencial
VAR sV = [Resultado Gerencial Simplificado]
VAR sAt = CALCULATE ( [Resultado Gerencial Simplificado], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR sLY = CALCULATE ( CALCULATE ( [Resultado Gerencial Simplificado], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR sVar = IF ( _umAno, DIVIDE ( sAt - sLY, ABS ( sLY ) ) )
VAR sTxt =
    IF ( ISBLANK ( sV ), "—",
        "R$ " & SWITCH ( TRUE (),
            ABS ( sV ) >= 1e6, FORMAT ( sV / 1e6, "#,0.0", "pt-BR" ) & " mi",
            ABS ( sV ) >= 1e3, FORMAT ( sV / 1e3, "#,0.0", "pt-BR" ) & " mil",
            FORMAT ( sV, "#,0", "pt-BR" ) ) )
VAR sL1 = IF ( ISBLANK ( sV ), IF ( _prod, "Indisponível com filtro de produto", "Sem dados no período" ), FORMAT ( [Resultado Gerencial %], "0.0%", "pt-BR" ) & " da receita · não contábil" )
VAR sL2 = IF ( ISBLANK ( sVar ), _semBase, "<b style='color:" & IF ( sVar >= 0, cPos, cNeg ) & "'>" & IF ( sVar >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( sVar ), "0.0%", "pt-BR" ) & "</b> vs ano anterior" )
-- OTIF
VAR oV = [OTIF %]
VAR oAt = CALCULATE ( [OTIF %], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR oLY = CALCULATE ( CALCULATE ( [OTIF %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR oPP = IF ( _umAno && NOT ISBLANK ( oLY ) && NOT ISBLANK ( oAt ), ( oAt - oLY ) * 100 )
VAR oMeta = CALCULATE ( [Meta OTIF % (média simples)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR oDev = [Desvio OTIF vs Meta (p.p.)]
VAR oL1 = IF ( ISBLANK ( oPP ), _semBase, "<span style='color:" & IF ( oPP >= 0, cPos, cNeg ) & "'>" & IF ( oPP >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( oPP ), "0.0", "pt-BR" ) & " p.p.</span> vs ano anterior" )
VAR oL2 = IF ( ISBLANK ( oDev ), "Sem meta no período", "Meta " & FORMAT ( oMeta, "0.0%", "pt-BR" ) & " · <b style='color:" & IF ( oDev >= 0, cPos, cNeg ) & "'>" & FORMAT ( oDev, "+0.0;-0.0", "pt-BR" ) & " p.p.</b>" )
-- Clientes (status na Data Referencia)
VAR kNovo = [Clientes Novos (status)]
VAR kAtv = [Clientes Ativos Recorrentes]
VAR kReat = [Clientes Reativados (status)]
VAR kRisco = [Clientes em Risco]
VAR kChurn = [Clientes em Churn]
VAR kHist = kNovo + kAtv + kReat + kRisco + kChurn
VAR kTaxa = DIVIDE ( kChurn, kHist )
VAR kSeg =
    "<span title='Novos " & FORMAT ( kNovo, "#,0", "pt-BR" ) & "' style='width:" & FORMAT ( DIVIDE ( kNovo, kHist ) * 100, "0.00", "en-US" ) & "%;background:#7FE6DD'></span>"
        & "<span title='Ativos " & FORMAT ( kAtv, "#,0", "pt-BR" ) & "' style='width:" & FORMAT ( DIVIDE ( kAtv, kHist ) * 100, "0.00", "en-US" ) & "%;background:#10D4C4'></span>"
        & "<span title='Reativados " & FORMAT ( kReat, "#,0", "pt-BR" ) & "' style='width:" & FORMAT ( DIVIDE ( kReat, kHist ) * 100, "0.00", "en-US" ) & "%;background:#0878C9'></span>"
        & "<span title='Em risco " & FORMAT ( kRisco, "#,0", "pt-BR" ) & "' style='width:" & FORMAT ( DIVIDE ( kRisco, kHist ) * 100, "0.00", "en-US" ) & "%;background:#FFC66D'></span>"
        & "<span title='Churn " & FORMAT ( kChurn, "#,0", "pt-BR" ) & "' style='width:" & FORMAT ( DIVIDE ( kChurn, kHist ) * 100, "0.00", "en-US" ) & "%;background:#FF7285'></span>"
VAR kL1 = IF ( kHist = 0, "Sem clientes no contexto", "<span style='color:" & cAte & "'>" & FORMAT ( kRisco, "#,0", "pt-BR" ) & "</span> em risco · " & FORMAT ( kNovo + kAtv + kReat, "#,0", "pt-BR" ) & " ativos" )
VAR kL2 = IF ( kHist = 0, "", "<div class='nx-sb' role='img' aria-label='Novos " & kNovo & ", ativos " & kAtv & ", reativados " & kReat & ", em risco " & kRisco & ", churn " & kChurn & "'>" & kSeg & "</div>" )
-- montagem
VAR _lbl = SWITCH ( _kpi, "Receita", "RECEITA LÍQUIDA", "Margem", "MARGEM BRUTA", "Resultado", "RESULTADO GERENCIAL", "OTIF", "ENTREGAS OTIF", "Clientes", "TAXA DE CHURN · " & [Limite Churn (dias)] & " DIAS" )
VAR _val = SWITCH ( _kpi, "Receita", rTxt, "Margem", IF ( ISBLANK ( mV ), "—", FORMAT ( mV, "0.0%", "pt-BR" ) ), "Resultado", sTxt, "OTIF", IF ( ISBLANK ( oV ), "—", FORMAT ( oV, "0.0%", "pt-BR" ) ), "Clientes", IF ( kHist = 0, "—", FORMAT ( kTaxa, "0.0%", "pt-BR" ) ) )
VAR _l1 = SWITCH ( _kpi, "Receita", rL1, "Margem", mL1, "Resultado", sL1, "OTIF", oL1, "Clientes", kL1 )
VAR _l2 = SWITCH ( _kpi, "Receita", rL2, "Margem", mL2, "Resultado", IF ( ISBLANK ( sV ), "", sL2 ), "OTIF", oL2, "Clientes", kL2 )
VAR _cor =
    SWITCH ( _kpi,
        "Receita", IF ( ISBLANK ( rYoY ), cNeu, IF ( rYoY >= 0, cPos, cNeg ) ),
        "Margem", IF ( ISBLANK ( mDev ), cNeu, IF ( mDev >= 0, cPos, cNeg ) ),
        "Resultado", IF ( ISBLANK ( sVar ), cNeu, IF ( sVar >= 0, cPos, cNeg ) ),
        "OTIF", IF ( ISBLANK ( oDev ), cNeu, IF ( oDev >= 0, cPos, cNeg ) ),
        cNeu )
VAR _css = "<style>.nx-card{font-family:'Segoe UI',sans-serif;box-sizing:border-box;height:100%;padding:14px 16px 12px 18px;border-left:3px solid #A9B9CA;border-radius:12px;background:rgba(10,28,51,.82);color:#FFFFFF;display:flex;flex-direction:column;justify-content:space-between;animation:nxIn .5s ease-out both}.nx-lbl{font-size:11px;letter-spacing:.08em;color:#A9B9CA;font-weight:600}.nx-row{display:flex;align-items:flex-end;justify-content:space-between;gap:10px}.nx-val{font-size:30px;font-weight:600;line-height:1.1;white-space:nowrap}.nx-sub{font-size:12px;color:#A9B9CA;margin-top:4px;white-space:nowrap}.nx-foot{font-size:11px;color:#A9B9CA;min-height:14px}.nx-foot b{font-weight:600}.nx-pb{display:flex;align-items:center;gap:10px}.nx-tr{flex:1;height:6px;border-radius:3px;background:#173B5C;overflow:hidden}.nx-fl{height:100%;border-radius:3px;transform-origin:left;animation:nxGrow .9s ease-out .15s both}.nx-sb{display:flex;height:8px;border-radius:4px;overflow:hidden;gap:2px}.nx-sb span{display:block;height:100%}.nx-draw{stroke-dasharray:420;animation:nxDraw 1.1s ease-out .2s both}@keyframes nxIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@keyframes nxDraw{from{stroke-dashoffset:420}to{stroke-dashoffset:0}}@keyframes nxGrow{from{transform:scaleX(0)}to{transform:scaleX(1)}}@media (prefers-reduced-motion:reduce){.nx-card,.nx-draw,.nx-fl{animation:none}}</style>"
RETURN
    IF (
        NOT ISBLANK ( _kpi ),
        _css & "<div class='nx-card' style='border-left-color:" & _cor & "' aria-label='" & _lbl & " " & _val & "'><div class='nx-lbl'>" & _lbl & "</div><div class='nx-row'><div><div class='nx-val'>" & _val & "</div><div class='nx-sub'>" & _l1 & "</div></div>"
            & IF ( _kpi <> "Clientes" && NOT ( _kpi = "Resultado" && _prod ), _spark ) & "</div><div class='nx-foot'>" & _l2 & "</div></div>"
    )
```

### UX Tooltip Filial

Microanálise para a página de tooltip de filial: receita 12 meses (barras SVG), YoY, atingimento de meta, margem vs meta e OTIF vs meta.

Formato: ``

```dax
VAR _filial = SELECTEDVALUE ( dFilial[Filial] )
VAR _ref = [Data Referência]
VAR _rec = [Receita Líquida]
VAR _yoy = [Receita YoY %]
VAR _marg = [Margem Bruta %]
VAR _dev = [Desvio Margem vs Meta (p.p.)]
VAR _otif = [OTIF %]
VAR _odev = [Desvio OTIF vs Meta (p.p.)]
VAR _ating = [Atingimento Meta Faturamento %]
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _ok = FILTER ( _serie, NOT ISBLANK ( [@V] ) )
VAR _min = MINX ( _ok, [@V] )
VAR _max = MAXX ( _ok, [@V] )
VAR _rng = IF ( _max = _min, 1, _max - _min )
VAR _bars = CONCATENATEX ( _ok, VAR _h = 4 + ( [@V] - _min ) / _rng * 30 RETURN "<rect x='" & ( 11 - [Value] ) * 22 & "' y='" & FORMAT ( 36 - _h, "0.0", "en-US" ) & "' width='16' height='" & FORMAT ( _h, "0.0", "en-US" ) & "' rx='2' fill='" & IF ( [Value] = 0, "#10D4C4", "#0878C9" ) & "'/>", "" )
VAR _cP = "#45D5A1"
VAR _cN = "#FF7285"
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:14px 16px;box-sizing:border-box;background:#0A1C33;height:100%;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600}.nx-ts{font-size:10px;color:#A9B9CA;letter-spacing:.08em;margin-bottom:10px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:15px;font-weight:600}.nx-tv small{font-size:11px;font-weight:600;margin-left:4px}</style>"
RETURN
    IF (
        NOT ISBLANK ( _filial ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _filial & "</div><div class='nx-ts'>RECEITA ÚLTIMOS 12 MESES ATÉ " & UPPER ( FORMAT ( _ref, "mmm/yyyy", "pt-BR" ) ) & "</div>"
            & "<svg width='260' height='38' viewBox='0 0 260 38' aria-hidden='true'>" & _bars & "</svg>"
            & "<div class='nx-tg' style='margin-top:10px'>"
            & "<div><div class='nx-tk'>Receita</div><div class='nx-tv'>R$ " & FORMAT ( _rec / 1e6, "#,0.0", "pt-BR" ) & " mi" & IF ( NOT ISBLANK ( _yoy ), "<small style='color:" & IF ( _yoy >= 0, _cP, _cN ) & "'>" & FORMAT ( _yoy, "+0.0%;-0.0%", "pt-BR" ) & "</small>" ) & "</div></div>"
            & "<div><div class='nx-tk'>Atingimento da meta</div><div class='nx-tv'>" & IF ( ISBLANK ( _ating ), "—", FORMAT ( _ating, "0.0%", "pt-BR" ) ) & "</div></div>"
            & "<div><div class='nx-tk'>Margem bruta</div><div class='nx-tv'>" & FORMAT ( _marg, "0.0%", "pt-BR" ) & IF ( NOT ISBLANK ( _dev ), "<small style='color:" & IF ( _dev >= 0, _cP, _cN ) & "'>" & FORMAT ( _dev, "+0.0;-0.0", "pt-BR" ) & " p.p.</small>" ) & "</div></div>"
            & "<div><div class='nx-tk'>OTIF</div><div class='nx-tv'>" & FORMAT ( _otif, "0.0%", "pt-BR" ) & IF ( NOT ISBLANK ( _odev ), "<small style='color:" & IF ( _odev >= 0, _cP, _cN ) & "'>" & FORMAT ( _odev, "+0.0;-0.0", "pt-BR" ) & " p.p.</small>" ) & "</div></div>"
            & "</div></div>"
    )
```

### UX Título DRE

Verde se margem >= meta, vermelho se abaixo. Titulo da cascata DRE: avisa que a DRE nao existe com filtro de produto (despesas e impostos sem grao de produto).

Formato: ``

```dax
IF ( [Filtro de Produto Ativo], "DRE gerencial indisponível com filtro de produto", "Da receita ao resultado gerencial (R$ mi, não contábil)" )
```

### UX Tooltip Vendedor

Tooltip de vendedor: equipe, filial, ranking, receita 12 meses, margem e desconto vs media.

Formato: ``

```dax
VAR _vend = SELECTEDVALUE ( dVendedor[Vendedor] )
VAR _eq = SELECTEDVALUE ( dVendedor[Equipe] )
VAR _fil = CALCULATE ( SELECTEDVALUE ( dFilial[Cidade] ), TREATAS ( VALUES ( dVendedor[FilialID] ), dFilial[FilialID] ) )
VAR _ref = [Data Referência]
VAR _rec = [Receita Líquida]
VAR _yoy = IF ( HASONEVALUE ( dCalendario[Ano] ), [Receita YoY %] )
VAR _mg = [Margem Bruta %]
VAR _mgRef = CALCULATE ( [Margem Bruta %], REMOVEFILTERS ( dVendedor ) )
VAR _ds = [Desconto Médio Ponderado %]
VAR _dsRef = CALCULATE ( [Desconto Médio Ponderado %], REMOVEFILTERS ( dVendedor ) )
VAR _cl = [Clientes Positivados]
VAR _rk = IF ( NOT ISBLANK ( _vend ), RANKX ( FILTER ( ALL ( dVendedor[Vendedor] ), [Receita Líquida] > 0 ), [Receita Líquida], , DESC ) )
VAR _nv = COUNTROWS ( FILTER ( ALL ( dVendedor[Vendedor] ), [Receita Líquida] > 0 ) )
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _ok = FILTER ( _serie, NOT ISBLANK ( [@V] ) )
VAR _min = MINX ( _ok, [@V] )
VAR _max = MAXX ( _ok, [@V] )
VAR _rng = IF ( _max = _min, 1, _max - _min )
VAR _bars = CONCATENATEX ( _ok, VAR _h = 4 + ( [@V] - _min ) / _rng * 26 RETURN "<rect x='" & ( 11 - [Value] ) * 22 & "' y='" & FORMAT ( 32 - _h, "0.0", "en-US" ) & "' width='16' height='" & FORMAT ( _h, "0.0", "en-US" ) & "' rx='2' fill='" & IF ( [Value] = 0, "#10D4C4", "#0878C9" ) & "'/>", "" )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600}.nx-ts{font-size:10px;color:#A9B9CA;letter-spacing:.06em;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin-top:8px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}.nx-tv small{font-size:10.5px;font-weight:600;margin-left:4px}</style>"
RETURN
    IF (
        NOT ISBLANK ( _vend ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _vend & "</div><div class='nx-ts'>" & UPPER ( _eq ) & " · " & UPPER ( _fil ) & " · " & _rk & "º DE " & _nv & " EM RECEITA</div>"
            & "<svg width='260' height='34' viewBox='0 0 260 34' aria-hidden='true'>" & _bars & "</svg>"
            & "<div class='nx-tg'>"
            & "<div><div class='nx-tk'>Receita</div><div class='nx-tv'>R$ " & FORMAT ( _rec / 1e6, "#,0.00", "pt-BR" ) & " mi" & IF ( NOT ISBLANK ( _yoy ), "<small style='color:" & IF ( _yoy >= 0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _yoy, "+0.0%;-0.0%", "pt-BR" ) & "</small>" ) & "</div></div>"
            & "<div><div class='nx-tk'>Clientes positivados</div><div class='nx-tv'>" & FORMAT ( _cl, "#,0", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Margem bruta (média " & FORMAT ( _mgRef, "0.0%", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _mg >= _mgRef, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _mg, "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Desconto (média " & FORMAT ( _dsRef, "0.0%", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _ds <= _dsRef, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _ds, "0.0%", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
```

### UX Tooltip Cliente

Tooltip de cliente: segmento, potencial, status, ultima compra, dias sem compra, receita e faturas 12 meses, intervalo medio, barras mensais.

Formato: ``

```dax
VAR _cli = SELECTEDVALUE ( dCliente[RazaoSocial] )
VAR _ref = [Data Referência]
VAR _ult = CALCULATE ( MAX ( fFaturamento[DataFaturamento] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
VAR _dias = [Dias sem Compra (Data Ref.)]
VAR _st = CALCULATE ( MAXX ( FILTER ( VALUES ( dStatusCliente[Status] ), [Clientes por Status] = 1 ), dStatusCliente[Status] ), ALL ( dStatusCliente ) )
VAR _rec12 = [Receita 12M (Data Ref.)]
VAR _fat12 = CALCULATE ( COUNTROWS ( fFaturamento ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] > EDATE ( _ref, -12 ), dCalendario[Data] <= _ref )
VAR _int = CALCULATE ( [Intervalo Médio entre Compras (dias)], REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( SUM ( fFaturamento[ReceitaLiquida] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _max = MAXX ( _serie, [@V] )
VAR _bars = CONCATENATEX ( _serie, VAR _h = IF ( ISBLANK ( [@V] ), 1, 3 + DIVIDE ( [@V], _max ) * 25 ) RETURN "<rect x='" & ( 11 - [Value] ) * 22 & "' y='" & FORMAT ( 30 - _h, "0.0", "en-US" ) & "' width='16' height='" & FORMAT ( _h, "0.0", "en-US" ) & "' rx='2' fill='" & IF ( ISBLANK ( [@V] ), "#173B5C", "#0878C9" ) & "'/>", "" )
VAR _cst = SWITCH ( _st, "Novo", "#7FE6DD", "Ativo", "#45D5A1", "Reativado", "#5FA8E6", "Em risco", "#FFC66D", "Churn", "#FF7285", "#A9B9CA" )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nx-ts{font-size:10px;color:#A9B9CA;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin-top:8px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}.nx-pill{display:inline-block;padding:1px 8px;border-radius:9px;font-size:10px;font-weight:600;color:#071528}</style>"
RETURN
    IF (
        NOT ISBLANK ( _cli ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _cli & "</div><div class='nx-ts'>" & SELECTEDVALUE ( dCliente[Segmento] ) & " · potencial " & SELECTEDVALUE ( dCliente[ClassePotencial] ) & " · <span class='nx-pill' style='background:" & _cst & "'>" & _st & "</span></div>"
            & "<svg width='260' height='30' viewBox='0 0 260 30' aria-hidden='true'>" & _bars & "</svg>"
            & "<div class='nx-tg'>"
            & "<div><div class='nx-tk'>Última compra</div><div class='nx-tv'>" & FORMAT ( _ult, "dd/mm/yyyy" ) & "</div></div>"
            & "<div><div class='nx-tk'>Dias sem compra</div><div class='nx-tv' style='color:" & _cst & "'>" & FORMAT ( _dias, "#,0", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Receita 12 meses</div><div class='nx-tv'>R$ " & FORMAT ( _rec12 / 1e3, "#,0", "pt-BR" ) & " mil · " & _fat12 & " fat.</div></div>"
            & "<div><div class='nx-tk'>Intervalo médio</div><div class='nx-tv'>" & IF ( ISBLANK ( _int ), "1ª compra", FORMAT ( _int, "#,0", "pt-BR" ) & " dias" ) & "</div></div>"
            & "</div></div>"
    )
```

### UX Tooltip Transportadora

Tooltip de transportadora: modal, entregas, OTIF 12 meses, OTIF e frete por entrega vs total geral, no prazo, in full, atraso e ocorrencia.

Formato: ``

```dax
VAR _tr = SELECTEDVALUE ( dTransportadora[Transportadora] )
VAR _ref = [Data Referência]
VAR _otif = [OTIF %]
VAR _otifRef = CALCULATE ( [OTIF %], REMOVEFILTERS ( dTransportadora ) )
VAR _fe = [Frete por Entrega]
VAR _feRef = CALCULATE ( [Frete por Entrega], REMOVEFILTERS ( dTransportadora ) )
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( [OTIF %], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _ok = FILTER ( _serie, NOT ISBLANK ( [@V] ) )
VAR _min = MINX ( _ok, [@V] ) - 0.02
VAR _max = MAXX ( _ok, [@V] ) + 0.02
VAR _pts = CONCATENATEX ( _ok, FORMAT ( ( 11 - [Value] ) * 23 + 4, "0", "en-US" ) & "," & FORMAT ( 30 - ( [@V] - _min ) / ( _max - _min ) * 26, "0.0", "en-US" ), " ", [Value], DESC )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600}.nx-ts{font-size:10px;color:#A9B9CA;margin-bottom:4px}.nx-tg{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px 12px;margin-top:6px}.nx-tk{font-size:9.5px;color:#A9B9CA}.nx-tv{font-size:13px;font-weight:600}</style>"
RETURN
    IF (
        NOT ISBLANK ( _tr ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _tr & "</div><div class='nx-ts'>" & SELECTEDVALUE ( dTransportadora[Modal] ) & " · " & FORMAT ( [Entregas], "#,0", "pt-BR" ) & " entregas · OTIF 12 meses</div>"
            & "<svg width='264' height='32' viewBox='0 0 264 32'><polyline points='" & _pts & "' fill='none' stroke='#10D4C4' stroke-width='2'/></svg>"
            & "<div class='nx-tg'>"
            & "<div><div class='nx-tk'>OTIF (geral " & FORMAT ( _otifRef, "0.0%", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _otif >= _otifRef, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _otif, "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>No prazo</div><div class='nx-tv'>" & FORMAT ( [No Prazo %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Completas</div><div class='nx-tv'>" & FORMAT ( [In Full %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Atraso médio</div><div class='nx-tv'>" & FORMAT ( [Atraso Médio (dias)], "0.0", "pt-BR" ) & " d</div></div>"
            & "<div><div class='nx-tk'>Ocorrência</div><div class='nx-tv'>" & FORMAT ( [Ocorrência %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Frete/entrega (geral R$ " & FORMAT ( _feRef, "#,0", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _fe <= _feRef, "#45D5A1", "#FF7285" ) & "'>R$ " & FORMAT ( _fe, "#,0", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
```

### UX Tooltip Mês Financeiro

Tooltip mensal: recebido, pago, saldo, receita, margem e resultado gerencial.

Formato: ``

```dax
VAR _mes = SELECTEDVALUE ( dCalendario[MesAno] )
VAR _rec = [Receita Líquida]
VAR _rs = [Resultado Gerencial Simplificado]
VAR _in = [Recebimentos (Data Pagamento)]
VAR _out = [Pagamentos (Data Pagamento)]
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}</style>"
RETURN
    IF (
        NOT ISBLANK ( _mes ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _mes & "</div><div class='nx-tg'>"
            & "<div><div class='nx-tk'>Recebido</div><div class='nx-tv' style='color:#10D4C4'>R$ " & FORMAT ( _in / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Pago a fornecedores</div><div class='nx-tv'>R$ " & FORMAT ( _out / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Saldo do mês</div><div class='nx-tv' style='color:" & IF ( _in >= _out, "#45D5A1", "#FF7285" ) & "'>R$ " & FORMAT ( ( _in - _out ) / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Receita (competência)</div><div class='nx-tv'>R$ " & FORMAT ( _rec / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Margem bruta</div><div class='nx-tv'>" & FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Resultado gerencial</div><div class='nx-tv' style='color:" & IF ( _rs >= 0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _rs, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
```

### UX Tooltip Estoque Mês

Tooltip mensal de estoque: entradas, saidas, saldo, valor, ruptura e parados.

Formato: ``

```dax
VAR _mes = SELECTEDVALUE ( dCalendario[MesAno] )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}</style>"
RETURN
    IF (
        NOT ISBLANK ( _mes ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _mes & " · estoque (amostra)</div><div class='nx-tg'>"
            & "<div><div class='nx-tk'>Entradas</div><div class='nx-tv' style='color:#10D4C4'>" & FORMAT ( [Entradas Estoque (un)], "#,0", "pt-BR" ) & " un</div></div>"
            & "<div><div class='nx-tk'>Saídas</div><div class='nx-tv'>" & FORMAT ( [Saídas Estoque (un)], "#,0", "pt-BR" ) & " un</div></div>"
            & "<div><div class='nx-tk'>Saldo no fim do mês</div><div class='nx-tv'>" & FORMAT ( [Saldo Estoque Amostra (un)], "#,0", "pt-BR" ) & " un</div></div>"
            & "<div><div class='nx-tk'>Valor em estoque</div><div class='nx-tv'>R$ " & FORMAT ( [Valor Estoque Amostra] / 1e6, "#,0.0", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Ruptura</div><div class='nx-tv' style='color:#FF7285'>" & FORMAT ( [Ruptura % (amostra)], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Parados 90+ dias</div><div class='nx-tv' style='color:#FFC66D'>" & FORMAT ( [Produtos Parados 90+ (amostra)], "#,0", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
```

## 08 UX\Cores

### UX Cor Desvio Margem

Formato: ``

```dax
VAR _d = [Desvio Margem vs Meta (p.p.)]
RETURN SWITCH ( TRUE (), ISBLANK ( _d ), "#A9B9CA", _d >= 0, "#45D5A1", "#FF7285" )
```

### UX Cor Desvio OTIF

Verde se OTIF >= meta, vermelho se abaixo.

Formato: ``

```dax
VAR _d = [Desvio OTIF vs Meta (p.p.)]
RETURN SWITCH ( TRUE (), ISBLANK ( _d ), "#A9B9CA", _d >= 0, "#45D5A1", "#FF7285" )
```

### UX Cor Inadimplência

Âmbar quando acima da média da seleção (sem limite de negócio documentado, apenas comparação relativa).

Formato: ``

```dax
VAR _v = [Inadimplência % (Data Ref.)]
VAR _media = CALCULATE ( [Inadimplência % (Data Ref.)], ALLSELECTED ( dFilial ) )
RETURN SWITCH ( TRUE (), ISBLANK ( _v ), "#A9B9CA", _v > _media, "#FFC66D", "#FFFFFF" )
```

### UX Cor Margem vs Média

Verde/vermelho quando a margem do item difere em 0,5 p.p. ou mais da margem da selecao (ALLSELECTED); azul na faixa neutra.

Formato: ``

```dax
VAR _m = [Margem Bruta %]
VAR _ref = CALCULATE ( [Margem Bruta %], ALLSELECTED () )
RETURN SWITCH ( TRUE (), ISBLANK ( _m ), "#A9B9CA", _m - _ref >= 0.005, "#45D5A1", _m - _ref <= -0.005, "#FF7285", "#5FA8E6" )
```

### UX Cor Receita YoY

Verde para crescimento, vermelho para queda vs ano anterior.

Formato: ``

```dax
VAR _v = [Receita YoY %]
RETURN SWITCH ( TRUE (), ISBLANK ( _v ), "#A9B9CA", _v >= 0, "#45D5A1", "#FF7285" )
```

### UX Cor Janela Churn

Destaca a janela igual ao limite de churn vigente.

Formato: ``

```dax
IF ( SELECTEDVALUE ( 'Param Janela Comparativa'[Janela (dias)] ) = [Limite Churn (dias)], "#10D4C4", "#3E5C7A" )
```

### UX Cor OTIF Relativo

Verde/vermelho quando o OTIF difere 1 p.p. ou mais do OTIF da selecao de transportadoras; branco na faixa neutra.

Formato: ``

```dax
VAR _o = [OTIF %]
VAR _ref = CALCULATE ( [OTIF %], ALLSELECTED ( dTransportadora ) )
RETURN SWITCH ( TRUE (), ISBLANK ( _o ), "#A9B9CA", _o - _ref >= 0.01, "#45D5A1", _o - _ref <= -0.01, "#FF7285", "#FFFFFF" )
```

## 08 UX\Financeiro

### UX Financeiro DRE

DRE gerencial HTML: realizado, % da receita, ano anterior, variacao, orcado e desvio (orcamento so existe para receita e despesa total).

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _rec = [Receita (até corte)]
VAR _recLY = [Receita LY]
VAR _recO = CALCULATE ( [Orçamento Receita], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _cmv = - CALCULATE ( [CMV], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _cmvLY = - CALCULATE ( CALCULATE ( [CMV], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _mb = _rec + _cmv
VAR _mbLY = _recLY + _cmvLY
VAR _d0 = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Pessoal" ) )
VAR _d0ly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Pessoal" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _d1 = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Aluguel" ) )
VAR _d1ly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Aluguel" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _d2 = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Energia" ) )
VAR _d2ly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Energia" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _d3 = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Marketing" ) )
VAR _d3ly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Marketing" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _d4 = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "TI" ) )
VAR _d4ly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "TI" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _d5 = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Administrativo" ) )
VAR _d5ly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "Administrativo" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _dt = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _dtLY = - CALCULATE ( CALCULATE ( [Despesas Operacionais], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _dtO = - CALCULATE ( [Orçamento Despesa Operacional], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _rs = _mb + _dt
VAR _rsLY = _mbLY + _dtLY
VAR _css = "<style>.nx-d{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;display:flex;flex-direction:column}.nx-dt{font-size:13px;font-weight:600;text-align:center}.nx-ds{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 10px}.nx-d table{width:100%;border-collapse:collapse;font-size:11.5px}.nx-d th{font-size:9.5px;font-weight:600;color:#A9B9CA;text-align:right;padding:4px 4px;border-bottom:1px solid #173B5C;letter-spacing:.04em}.nx-d th:first-child,.nx-d td:first-child{text-align:left}.nx-d td{text-align:right;padding:5px 4px;border-bottom:1px solid #12304F;color:#C9D6E3}.nx-d tr.s td{color:#FFFFFF;font-weight:600;background:rgba(18,48,79,.55)}.nx-d tr.r td{color:#10D4C4;font-weight:600;background:rgba(18,48,79,.85);border-bottom:none}.nx-d tr.i td:first-child{padding-left:16px}.nx-k{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:auto}.nx-kb{border-left:3px solid #173B5C;padding-left:10px}.nx-kl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:20px;font-weight:600}</style>"
VAR _hd = "<tr><th>R$ mi</th><th>Realizado</th><th>% rec.</th><th>Ano ant.</th><th>Var.</th><th>Orçado</th><th>Desvio</th></tr>"
RETURN
    IF (
        [Filtro de Produto Ativo],
        _css & "<div class='nx-d'><div class='nx-dt'>DRE gerencial</div><div class='nx-ds'>Indisponível com filtro de produto: despesas e impostos não têm produto.</div></div>",
        _css & "<div class='nx-d'><div class='nx-dt'>DRE gerencial (não contábil)</div><div class='nx-ds'>competência até " & FORMAT ( MIN ( _corte, MAX ( dCalendario[Data] ) ), "dd/mm/yyyy" ) & " · variação e desvio favoráveis em verde</div><table>" & _hd
            & "<tr class='s'><td>Receita líquida</td><td>" & FORMAT ( _rec / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _rec, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _recLY ), "<td>" & FORMAT ( _recLY / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _rec ) >= ABS ( _recLY ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _rec ) - ABS ( _recLY ), ABS ( _recLY ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & IF ( NOT ISBLANK ( _recO ), "<td>" & FORMAT ( _recO / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _rec ) >= ABS ( _recO ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _rec ) - ABS ( _recO ), ABS ( _recO ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "</tr>"
            & "<tr class='i'><td>(−) CMV</td><td>" & FORMAT ( _cmv / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _cmv, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _cmvLY ), "<td>" & FORMAT ( _cmvLY / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _cmv ) <= ABS ( _cmvLY ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _cmv ) - ABS ( _cmvLY ), ABS ( _cmvLY ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='s'><td>Margem bruta</td><td>" & FORMAT ( _mb / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _mb, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _mbLY ), "<td>" & FORMAT ( _mbLY / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _mb ) >= ABS ( _mbLY ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _mb ) - ABS ( _mbLY ), ABS ( _mbLY ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='i'><td>(−) Pessoal</td><td>" & FORMAT ( _d0 / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _d0, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _d0ly ), "<td>" & FORMAT ( _d0ly / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _d0 ) <= ABS ( _d0ly ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _d0 ) - ABS ( _d0ly ), ABS ( _d0ly ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='i'><td>(−) Aluguel</td><td>" & FORMAT ( _d1 / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _d1, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _d1ly ), "<td>" & FORMAT ( _d1ly / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _d1 ) <= ABS ( _d1ly ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _d1 ) - ABS ( _d1ly ), ABS ( _d1ly ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='i'><td>(−) Energia</td><td>" & FORMAT ( _d2 / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _d2, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _d2ly ), "<td>" & FORMAT ( _d2ly / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _d2 ) <= ABS ( _d2ly ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _d2 ) - ABS ( _d2ly ), ABS ( _d2ly ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='i'><td>(−) Marketing</td><td>" & FORMAT ( _d3 / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _d3, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _d3ly ), "<td>" & FORMAT ( _d3ly / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _d3 ) <= ABS ( _d3ly ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _d3 ) - ABS ( _d3ly ), ABS ( _d3ly ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='i'><td>(−) TI</td><td>" & FORMAT ( _d4 / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _d4, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _d4ly ), "<td>" & FORMAT ( _d4ly / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _d4 ) <= ABS ( _d4ly ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _d4 ) - ABS ( _d4ly ), ABS ( _d4ly ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='i'><td>(−) Administrativo</td><td>" & FORMAT ( _d5 / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _d5, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _d5ly ), "<td>" & FORMAT ( _d5ly / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _d5 ) <= ABS ( _d5ly ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _d5 ) - ABS ( _d5ly ), ABS ( _d5ly ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "<tr class='s'><td>Despesas operacionais</td><td>" & FORMAT ( _dt / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _dt, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _dtLY ), "<td>" & FORMAT ( _dtLY / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _dt ) <= ABS ( _dtLY ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _dt ) - ABS ( _dtLY ), ABS ( _dtLY ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & IF ( NOT ISBLANK ( _dtO ), "<td>" & FORMAT ( _dtO / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _dt ) <= ABS ( _dtO ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _dt ) - ABS ( _dtO ), ABS ( _dtO ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "</tr>"
            & "<tr class='r'><td>Resultado gerencial</td><td>" & FORMAT ( _rs / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & FORMAT ( DIVIDE ( _rs, _rec ), "0.0%", "pt-BR" ) & "</td>" & IF ( _umAno && NOT ISBLANK ( _rsLY ), "<td>" & FORMAT ( _rsLY / 1e6, "#,0.0", "pt-BR" ) & "</td><td style='color:" & IF ( ABS ( _rs ) >= ABS ( _rsLY ), "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( ABS ( _rs ) - ABS ( _rsLY ), ABS ( _rsLY ) ), "+0.0%;-0.0%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" ) & "<td>—</td><td></td>" & "</tr>"
            & "</table><div class='nx-k'>"
            & "<div class='nx-kb' style='border-color:#10D4C4'><div class='nx-kl'>Margem bruta</div><div class='nx-kv'>" & FORMAT ( DIVIDE ( _mb, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "<div class='nx-kb' style='border-color:#5FA8E6'><div class='nx-kl'>Despesas / receita</div><div class='nx-kv'>" & FORMAT ( DIVIDE ( - _dt, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "<div class='nx-kb' style='border-color:" & IF ( _rs >= 0, "#45D5A1", "#FF7285" ) & "'><div class='nx-kl'>Resultado / receita</div><div class='nx-kv'>" & FORMAT ( DIVIDE ( _rs, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
```

### UX Financeiro Recebíveis

Saldo a receber (vencido x a vencer) na Data Referencia, inadimplencia, prazo medio, recebido e pago no periodo, titulos inconsistentes.

Formato: ``

```dax
VAR _ref = [Data Referência]
VAR _venc = [Saldo Vencido em Aberto (Data Ref.)]
VAR _av = [Saldo a Vencer em Aberto (Data Ref.)]
VAR _ab = _venc + _av
VAR _wv = FORMAT ( 100 * DIVIDE ( _venc, _ab ), "0.0", "en-US" )
VAR _css = "<style>.nx-r{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:12px 16px;display:flex;flex-direction:column;gap:9px}.nx-rt{font-size:13px;font-weight:600;text-align:center}.nx-rg{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px}.nx-rl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-rv{font-size:19px;font-weight:600}.nx-rs{font-size:10px;color:#A9B9CA}.nx-bar{display:flex;height:9px;border-radius:5px;overflow:hidden;background:#12304F;margin-top:4px}.nx-dq{font-size:10px;color:#C9D6E3;border-left:3px solid #FFC66D;padding-left:8px}</style>"
RETURN
    _css & "<div class='nx-r'><div class='nx-rt'>Recebíveis e pagamentos em " & FORMAT ( _ref, "dd/mm/yyyy" ) & "</div>"
        & "<div><div class='nx-rl'>Saldo a receber em aberto</div><div class='nx-rv'>R$ " & FORMAT ( _ab / 1e6, "#,0.00", "pt-BR" ) & " mi</div>"
        & "<div class='nx-bar'><span style='width:" & _wv & "%;background:#FF7285'></span><span style='flex:1;background:#5FA8E6'></span></div>"
        & "<div class='nx-rs'><span style='color:#FF7285'>vencido R$ " & FORMAT ( _venc / 1e6, "#,0.00", "pt-BR" ) & " mi</span> · a vencer R$ " & FORMAT ( _av / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
        & "<div class='nx-rg'>"
        & "<div><div class='nx-rl'>Inadimplência</div><div class='nx-rv'>" & FORMAT ( [Inadimplência % (Data Ref.)], "0.00%", "pt-BR" ) & "</div><div class='nx-rs'>vencido em aberto ÷ vencido até a data</div></div>"
        & "<div><div class='nx-rl'>Prazo médio de recebimento</div><div class='nx-rv'>" & FORMAT ( [Prazo Médio Recebimento (dias)], "0.0", "pt-BR" ) & " dias</div><div class='nx-rs'>da fatura ao pagamento</div></div>"
        & "<div><div class='nx-rl'>Recebido no período</div><div class='nx-rv'>R$ " & FORMAT ( [Recebimentos (Data Pagamento)] / 1e6, "#,0.0", "pt-BR" ) & " mi</div><div class='nx-rs'>pela data do pagamento</div></div>"
        & "<div><div class='nx-rl'>Pago a fornecedores</div><div class='nx-rv'>R$ " & FORMAT ( [Pagamentos (Data Pagamento)] / 1e6, "#,0.0", "pt-BR" ) & " mi</div><div class='nx-rs'>em aberto R$ " & FORMAT ( [Valor em Aberto (CP)] / 1e6, "#,0.0", "pt-BR" ) & " mi</div></div>"
        & "</div><div class='nx-dq'>Qualidade: " & FORMAT ( [Títulos Inconsistentes], "#,0", "pt-BR" ) & " títulos inconsistentes (R$ " & FORMAT ( [Valor Títulos Inconsistentes] / 1e6, "#,0.0", "pt-BR" ) & " mi) ficam fora do recebido.</div></div>"
```

## 08 UX\Home

### UX Home Mapa

Mapa SVG independente: contorno do Brasil (Natural Earth) e as filiais de dFilial posicionadas por latitude/longitude; tamanho pela receita; lista ordenada por receita.

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        VALUES ( dFilial[FilialID] ),
        "@cid", CALCULATE ( SELECTEDVALUE ( dFilial[Cidade] ) ),
        "@uf", CALCULATE ( SELECTEDVALUE ( dFilial[UF] ) ),
        "@reg", CALCULATE ( SELECTEDVALUE ( dFilial[Regiao] ) ),
        "@x", CALCULATE ( ( SELECTEDVALUE ( dFilial[Longitude] ) + 74.2 ) * 12 * 0.970296 ),
        "@y", CALCULATE ( ( 5.6 - SELECTEDVALUE ( dFilial[Latitude] ) ) * 12 ),
        "@rec", [Receita Líquida],
        "@at", [Atingimento Meta Faturamento %]
    )
VAR _max = MAXX ( _t, [@rec] )
VAR _tot = SUMX ( _t, [@rec] )
VAR _pts =
    CONCATENATEX (
        _t,
        VAR _r = 3 + 6 * SQRT ( DIVIDE ( [@rec], _max ) )
        VAR _c = SWITCH ( [@reg], "Sudeste", "#10D4C4", "Sul", "#5FA8E6", "#FFC66D" )
        VAR _cx = FORMAT ( [@x], "0.0", "en-US" )
        VAR _cy = FORMAT ( [@y], "0.0", "en-US" )
        RETURN
            "<g><circle class='nx-hl' cx='" & _cx & "' cy='" & _cy & "' r='" & FORMAT ( _r * 1.9, "0.0", "en-US" ) & "' fill='" & _c & "' style='animation-delay:" & FORMAT ( MOD ( [FilialID] * 0.37, 3 ), "0.00", "en-US" ) & "s'/>"
                & "<circle cx='" & _cx & "' cy='" & _cy & "' r='" & FORMAT ( _r, "0.0", "en-US" ) & "' fill='" & _c & "' stroke='#071528' stroke-width='1.2'/></g>",
        "",
        [@rec], ASC
    )
VAR _lista =
    CONCATENATEX (
        TOPN ( 12, _t, [@rec], DESC ),
        VAR _c = SWITCH ( [@reg], "Sudeste", "#10D4C4", "Sul", "#5FA8E6", "#FFC66D" )
        RETURN
            "<div class='nx-li'><span class='nx-dt' style='background:" & _c & "'></span><span class='nx-ci'>" & [@cid] & "</span><span class='nx-bw'><span class='nx-b' style='width:" & FORMAT ( 100 * DIVIDE ( [@rec], _max ), "0", "en-US" ) & "%;background:" & _c & "'></span></span><span class='nx-v'>" & FORMAT ( [@rec] / 1e6, "#,0" ) & "</span></div>",
        "",
        [@rec], DESC
    )
VAR _leg =
    CONCATENATEX (
        DISTINCT ( SELECTCOLUMNS ( _t, "@rg", [@reg] ) ),
        VAR _rr = [@rg]
        VAR _n = COUNTROWS ( FILTER ( _t, [@reg] = _rr ) )
        VAR _c = SWITCH ( _rr, "Sudeste", "#10D4C4", "Sul", "#5FA8E6", "#FFC66D" )
        RETURN "<span class='nx-lg'><span class='nx-dt' style='background:" & _c & "'></span>" & _rr & " · " & _n & "</span>",
        "", [@rg], ASC
    )
VAR _css = "<style>.nx-m{font-family:'Segoe UI',sans-serif;color:#FFFFFF;box-sizing:border-box;height:100vh;padding:18px 22px;background:rgba(7,21,40,.95);border:1px solid #173B5C;border-radius:16px;animation:nxIn .8s ease-out both}.nx-t{font-size:16px;font-weight:600}.nx-s{font-size:11px;color:#A9B9CA;margin:2px 0 8px}.nx-g{display:flex;gap:14px;align-items:flex-start}.nx-l{flex:1;padding-top:4px}.nx-li{display:flex;align-items:center;gap:7px;font-size:11.5px;height:24px}.nx-ci{width:92px;color:#C9D6E3;white-space:nowrap;overflow:hidden}.nx-bw{flex:1;height:5px;background:#12304F;border-radius:3px}.nx-b{display:block;height:5px;border-radius:3px;opacity:.85}.nx-v{width:26px;text-align:right;color:#FFFFFF;font-weight:600}.nx-dt{display:inline-block;width:7px;height:7px;border-radius:50%}.nx-lgs{display:flex;gap:14px;font-size:10px;color:#A9B9CA;margin-top:8px}.nx-lg{display:flex;align-items:center;gap:5px}.nx-u{font-size:9px;color:#6F86A0;text-align:right;margin-top:2px}.nx-hl{opacity:.0;transform-box:fill-box;transform-origin:center;animation:nxP 3.2s ease-out infinite}@keyframes nxP{0%{opacity:.45;transform:scale(.45)}70%{opacity:0;transform:scale(1.35)}100%{opacity:0}}@keyframes nxIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-hl{animation:none}.nx-m{animation:none}}</style>"
RETURN
    _css & "<div class='nx-m'><div class='nx-t'>Rede de filiais</div><div class='nx-s'>" & COUNTROWS ( _t ) & " unidades · receita líquida de " & FORMAT ( CALCULATE ( MIN ( dCalendario[Data] ), dCalendario[Data] <= _corte ), "mmm/yyyy", "pt-BR" ) & " a " & FORMAT ( _corte, "mmm/yyyy", "pt-BR" ) & "</div>"
        & "<div class='nx-g'><svg width='318' height='328' viewBox='0 0 465 480' role='img' aria-label='Mapa do Brasil com as filiais'><path d='" & "M85 53 L91 58 L99 55 L102 59 L106 54 L116 49 L119 44 L125 41 L126 38 L118 37 L116 24 L110 16 L112 18 L117 18 L119 20 L126 20 L132 24 L134 19 L137 18 L140 18 L147 16 L150 13 L154 13 L158 8 L157 5 L158 5 L164 4 L165 6 L164 13 L169 15 L168 16 L171 20 L167 24 L165 35 L168 40 L169 46 L179 53 L183 52 L185 48 L188 49 L189 47 L193 47 L199 43 L202 45 L212 45 L213 43 L210 40 L212 37 L215 38 L224 36 L228 39 L234 42 L238 39 L241 40 L243 39 L244 41 L247 41 L251 38 L255 29 L265 15 L268 18 L273 42 L276 45 L282 47 L283 53 L273 65 L267 68 L259 84 L251 86 L259 86 L271 78 L274 88 L277 91 L282 89 L285 90 L290 88 L286 99 L288 97 L291 90 L294 89 L297 85 L300 87 L301 85 L300 84 L300 81 L304 76 L310 75 L312 76 L312 75 L314 75 L335 83 L336 88 L339 85 L343 88 L343 89 L344 88 L345 92 L343 94 L344 96 L347 93 L347 96 L345 98 L343 106 L347 103 L349 97 L350 97 L349 101 L352 98 L358 97 L359 96 L372 101 L376 100 L381 102 L393 101 L399 102 L416 112 L421 118 L426 122 L430 124 L431 126 L438 128 L450 129 L454 134 L459 155 L457 168 L455 174 L449 182 L446 183 L446 185 L440 193 L434 197 L429 204 L429 202 L425 212 L419 221 L416 223 L413 219 L412 221 L413 222 L409 230 L410 231 L409 236 L411 236 L409 243 L411 258 L407 273 L408 280 L402 286 L401 302 L398 304 L394 314 L389 318 L387 322 L387 331 L378 335 L375 338 L374 343 L364 343 L361 340 L361 343 L353 344 L355 343 L353 342 L344 344 L344 346 L345 346 L336 350 L335 353 L329 353 L318 358 L305 368 L306 369 L303 372 L303 371 L300 370 L300 373 L297 372 L297 373 L300 374 L297 377 L298 381 L296 382 L299 394 L298 404 L296 410 L285 420 L278 432 L271 442 L258 453 L258 449 L262 449 L267 445 L268 441 L270 440 L271 438 L274 436 L273 432 L275 432 L275 430 L270 432 L267 428 L268 432 L267 436 L266 435 L264 440 L259 444 L256 450 L257 453 L251 465 L243 472 L241 471 L241 465 L245 460 L240 456 L238 452 L233 449 L228 445 L222 443 L217 437 L212 440 L211 437 L202 428 L199 429 L198 431 L193 429 L203 420 L213 408 L216 408 L215 406 L222 402 L226 398 L231 396 L237 393 L239 383 L236 375 L233 373 L228 374 L232 356 L228 353 L223 355 L219 355 L216 339 L214 335 L209 334 L207 332 L205 334 L201 334 L189 333 L191 319 L187 309 L190 307 L187 304 L192 296 L191 294 L195 286 L191 277 L184 274 L183 268 L185 263 L163 262 L163 253 L159 248 L162 248 L159 233 L153 229 L145 230 L141 225 L133 223 L130 219 L126 219 L122 217 L114 216 L113 214 L107 211 L103 202 L103 199 L102 193 L104 189 L103 184 L89 186 L75 195 L71 196 L65 201 L58 199 L41 199 L43 180 L34 187 L23 187 L21 181 L12 180 L14 175 L8 167 L5 162 L6 161 L2 158 L3 156 L6 155 L5 150 L12 145 L11 140 L14 135 L15 129 L27 121 L38 119 L40 117 L44 117 L46 119 L49 119 L56 82 L53 73 L48 69 L48 60 L55 58 L59 59 L57 55 L51 54 L51 47 L70 47 L70 43 L73 46 L79 42 L83 48 L83 53 L85 53Z M286 70 L292 69 L300 71 L295 84 L293 85 L291 84 L291 86 L288 85 L287 88 L284 89 L281 88 L276 89 L273 82 L275 80 L273 78 L274 70 L279 69 L286 70Z M350 345 L347 345 L349 344 L350 345Z M298 384 L297 383 L299 381 L298 384Z M337 354 L335 354 L336 352 L337 354Z M346 102 L345 104 L346 100 L346 102Z M413 224 L414 222 L414 223 L413 224Z M341 83 L340 84 L340 82 L341 83Z M285 64 L283 67 L278 67 L279 64 L285 64Z M278 44 L276 44 L276 42 L278 42 L278 44Z M274 69 L271 71 L270 70 L272 68 L274 69Z M288 69 L284 68 L288 66 L289 67 L288 69Z M277 66 L277 67 L274 67 L275 65 L277 60 L278 64 L277 66Z M280 62 L279 63 L279 61 L281 60 L280 62Z M260 84 L259 85 L264 75 L267 74 L268 75 L267 79 L260 84Z M299 400 L299 401 L299 398 L300 396 L299 400Z" & "' fill='#0A2540' stroke='#10D4C4' stroke-opacity='.55' stroke-width='1.4'/>" & _pts & "</svg>"
        & "<div class='nx-l'>" & _lista & "<div class='nx-u'>R$ milhões</div></div></div><div class='nx-lgs'>" & _leg & "</div></div>"
```

### UX Home KPIs

Faixa de indicadores da Home com medidas reais: receita, margem, clientes ativos, entregas (com OTIF) e filiais com receita.

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _ini = CALCULATE ( MIN ( dCalendario[Data] ), dCalendario[Data] <= _corte )
VAR _filiais = COUNTROWS ( FILTER ( VALUES ( dFilial[FilialID] ), [Receita Líquida] > 0 ) )
VAR _item = "<div class='nx-k' style='animation-delay:@@ds'><div class='nx-kl'>@@L</div><div class='nx-kv'>@@V</div><div class='nx-ks'>@@S</div></div>"
VAR _css = "<style>.nx-ks-w{font-family:'Segoe UI',sans-serif;display:flex;height:100%;box-sizing:border-box;align-items:stretch;background:rgba(7,21,40,.78);border:1px solid #173B5C;border-radius:14px;padding:14px 8px}.nx-k{flex:1;padding:0 20px;border-left:1px solid #173B5C;animation:nxUp .7s ease-out both}.nx-k:first-child{border-left:none}.nx-kl{font-size:10px;letter-spacing:.12em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:26px;font-weight:600;color:#FFFFFF;margin-top:4px;line-height:1.1}.nx-ks{font-size:10px;color:#6F86A0;margin-top:4px}@keyframes nxUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
VAR _per = FORMAT ( _ini, "mmm/yy", "pt-BR" ) & " – " & FORMAT ( _corte, "mmm/yy", "pt-BR" )
RETURN
    _css & "<div class='nx-ks-w'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0" ), "@@L", "Receita líquida" ), "@@V", "R$ " & FORMAT ( [Receita Líquida] / 1e6, "#,0.0" ) & " mi" ), "@@S", _per )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.08" ), "@@L", "Margem bruta" ), "@@V", FORMAT ( [Margem Bruta %], "0.0%" ) ), "@@S", _per )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.16" ), "@@L", "Clientes ativos" ), "@@V", FORMAT ( [Clientes Ativos (total)], "#,0" ) ), "@@S", "compra há menos de " & [Limite Ativo (dias)] & " dias em " & FORMAT ( _corte, "dd/mm/yy" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.24" ), "@@L", "Entregas" ), "@@V", FORMAT ( [Entregas], "#,0" ) ), "@@S", "OTIF " & FORMAT ( [OTIF %], "0.0%" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.32" ), "@@L", "Filiais" ), "@@V", _filiais ), "@@S", "Sudeste, Sul e Centro-Oeste" )
        & "</div>"
```

## 08 UX\Logística

### UX Logística KPIs

Faixa de KPIs logisticos: OTIF com bullet vs meta (media simples das metas filial-mes ate o corte), no prazo, in full, ocorrencia, atraso medio, lead time e frete por entrega.

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _otif = [OTIF %]
VAR _meta = CALCULATE ( [Meta OTIF % (média simples)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _otifLY = CALCULATE ( CALCULATE ( [OTIF %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _fe = [Frete por Entrega]
VAR _feLY = CALCULATE ( CALCULATE ( [Frete por Entrega], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _atr = DIVIDE ( [Entregas] - [Entregas No Prazo], [Entregas] )
VAR _w = FORMAT ( 100 * MIN ( _otif, 1 ), "0.0", "en-US" )
VAR _wm = FORMAT ( 100 * MIN ( _meta, 1 ), "0.0", "en-US" )
VAR _cO = IF ( _otif >= _meta, "#45D5A1", IF ( _otif >= _meta - 0.05, "#FFC66D", "#FF7285" ) )
VAR _t = "<div class='nx-k'><div class='nx-kl'>@L</div><div class='nx-kv'>@V</div><div class='nx-ks'>@S</div></div>"
VAR _css = "<style>.nx-l{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:1.6fr repeat(6,1fr);gap:12px;height:100vh;box-sizing:border-box}.nx-k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:12px 16px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-kl{font-size:10px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:24px;font-weight:600;color:#FFFFFF;margin-top:3px;line-height:1.1}.nx-ks{font-size:10.5px;color:#A9B9CA;margin-top:3px}.nx-bl{position:relative;height:10px;background:#12304F;border-radius:5px;margin-top:9px}.nx-bf{position:absolute;left:0;top:0;bottom:0;border-radius:5px}.nx-bm{position:absolute;top:-4px;width:2px;height:18px;background:#FFFFFF}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
RETURN
    _css & "<div class='nx-l'>"
        & "<div class='nx-k' style='border-left:4px solid " & _cO & "'><div class='nx-kl'>OTIF (no prazo e completo)</div><div class='nx-kv' style='color:" & _cO & "'>" & FORMAT ( _otif, "0.0%", "pt-BR" ) & " <span style='font-size:12px;color:#A9B9CA;font-weight:400'>meta " & FORMAT ( _meta, "0.0%", "pt-BR" ) & "</span></div>"
        & "<div class='nx-bl'><div class='nx-bf' style='width:" & _w & "%;background:" & _cO & "'></div><div class='nx-bm' style='left:" & _wm & "%'></div></div>"
        & "<div class='nx-ks'>" & IF ( _umAno && NOT ISBLANK ( _otifLY ), FORMAT ( ( _otif - _otifLY ) * 100, "▲ 0.0;▼ 0.0", "pt-BR" ) & " p.p. vs ano anterior", "Selecione um único ano para comparar" ) & "</div></div>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "No prazo" ), "@V", FORMAT ( [No Prazo %], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [Entregas No Prazo], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Completas (in full)" ), "@V", FORMAT ( [In Full %], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [Entregas In Full], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Com ocorrência" ), "@V", FORMAT ( [Ocorrência %], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [Entregas com Ocorrência], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Atraso médio" ), "@V", FORMAT ( [Atraso Médio (dias)], "0.0", "pt-BR" ) & " dias" ), "@S", FORMAT ( _atr, "0.0%", "pt-BR" ) & " das entregas fora do prazo" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Lead time pedido→entrega" ), "@V", FORMAT ( [Lead Time Médio (dias)], "0.0", "pt-BR" ) & " dias" ), "@S", FORMAT ( [Entregas], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Frete por entrega" ), "@V", "R$ " & FORMAT ( _fe, "#,0", "pt-BR" ) ), "@S", IF ( _umAno && NOT ISBLANK ( _feLY ), FORMAT ( DIVIDE ( _fe - _feLY, _feLY ), "▲ 0.0%;▼ 0.0%", "pt-BR" ) & " vs ano ant. · ", "" ) & FORMAT ( [Frete % Receita], "0.0%", "pt-BR" ) & " da receita" )
        & "</div>"
```

### UX Logística Mapa

Mapa SVG das filiais (lat/long de dFilial) com OTIF e desvio vs meta; tamanho pelas entregas. Sem rotas: a fonte nao tem destino geografico.

Formato: ``

```dax
VAR _corte = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        VALUES ( dFilial[FilialID] ),
        "@cid", CALCULATE ( SELECTEDVALUE ( dFilial[Cidade] ) ),
        "@x", CALCULATE ( ( SELECTEDVALUE ( dFilial[Longitude] ) + 74.2 ) * 12 * 0.970296 ),
        "@y", CALCULATE ( ( 5.6 - SELECTEDVALUE ( dFilial[Latitude] ) ) * 12 ),
        "@e", [Entregas],
        "@o", [OTIF %],
        "@d", [Desvio OTIF vs Meta (p.p.)]
    )
VAR _ok = FILTER ( _t, [@e] > 0 )
VAR _max = MAXX ( _ok, [@e] )
VAR _pts =
    CONCATENATEX (
        _ok,
        VAR _r = 4 + 6 * SQRT ( DIVIDE ( [@e], _max ) )
        VAR _c = SWITCH ( TRUE (), ISBLANK ( [@d] ), "#A9B9CA", [@d] >= 0, "#45D5A1", [@d] >= -5, "#FFC66D", "#FF7285" )
        RETURN "<circle cx='" & FORMAT ( [@x], "0.0", "en-US" ) & "' cy='" & FORMAT ( [@y], "0.0", "en-US" ) & "' r='" & FORMAT ( _r, "0.0", "en-US" ) & "' fill='" & _c & "' fill-opacity='.9' stroke='#071528' stroke-width='1.2'/>",
        "", [@e], DESC
    )
VAR _lista =
    CONCATENATEX (
        _ok,
        VAR _c = SWITCH ( TRUE (), ISBLANK ( [@d] ), "#A9B9CA", [@d] >= 0, "#45D5A1", [@d] >= -5, "#FFC66D", "#FF7285" )
        RETURN "<div class='nx-li'><span class='nx-ci'>" & [@cid] & "</span><b style='color:" & _c & "'>" & FORMAT ( [@o], "0.0%", "pt-BR" ) & "</b><span class='nx-dv'>" & FORMAT ( [@d], "+0.0;-0.0", "pt-BR" ) & "</span></div>",
        "", [@o], ASC
    )
VAR _css = "<style>.nx-m{font-family:'Segoe UI',sans-serif;color:#FFFFFF;box-sizing:border-box;height:100vh;padding:12px 16px;display:flex;flex-direction:column}.nx-t{font-size:13px;font-weight:600;text-align:center}.nx-s{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 6px}.nx-g{display:flex;gap:10px;flex:1;align-items:center}.nx-l{flex:1}.nx-li{display:flex;align-items:center;font-size:11px;height:20px;border-bottom:1px solid #12304F}.nx-ci{flex:1;color:#C9D6E3}.nx-li b{width:46px;text-align:right}.nx-dv{width:40px;text-align:right;color:#6F86A0;font-size:10px}.nx-lg{display:flex;gap:12px;justify-content:center;font-size:10px;color:#A9B9CA;margin-top:6px}.nx-lg i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}</style>"
RETURN
    IF (
        NOT ISEMPTY ( _ok ),
        _css & "<div class='nx-m'><div class='nx-t'>OTIF por filial de origem</div><div class='nx-s'>tamanho = entregas · Δ em p.p. vs meta da filial</div>"
            & "<div class='nx-g'><svg width='230' height='238' viewBox='120 160 340 330' role='img' aria-label='Mapa das filiais com OTIF'><path d='" & "M85 53 L91 58 L99 55 L102 59 L106 54 L116 49 L119 44 L125 41 L126 38 L118 37 L116 24 L110 16 L112 18 L117 18 L119 20 L126 20 L132 24 L134 19 L137 18 L140 18 L147 16 L150 13 L154 13 L158 8 L157 5 L158 5 L164 4 L165 6 L164 13 L169 15 L168 16 L171 20 L167 24 L165 35 L168 40 L169 46 L179 53 L183 52 L185 48 L188 49 L189 47 L193 47 L199 43 L202 45 L212 45 L213 43 L210 40 L212 37 L215 38 L224 36 L228 39 L234 42 L238 39 L241 40 L243 39 L244 41 L247 41 L251 38 L255 29 L265 15 L268 18 L273 42 L276 45 L282 47 L283 53 L273 65 L267 68 L259 84 L251 86 L259 86 L271 78 L274 88 L277 91 L282 89 L285 90 L290 88 L286 99 L288 97 L291 90 L294 89 L297 85 L300 87 L301 85 L300 84 L300 81 L304 76 L310 75 L312 76 L312 75 L314 75 L335 83 L336 88 L339 85 L343 88 L343 89 L344 88 L345 92 L343 94 L344 96 L347 93 L347 96 L345 98 L343 106 L347 103 L349 97 L350 97 L349 101 L352 98 L358 97 L359 96 L372 101 L376 100 L381 102 L393 101 L399 102 L416 112 L421 118 L426 122 L430 124 L431 126 L438 128 L450 129 L454 134 L459 155 L457 168 L455 174 L449 182 L446 183 L446 185 L440 193 L434 197 L429 204 L429 202 L425 212 L419 221 L416 223 L413 219 L412 221 L413 222 L409 230 L410 231 L409 236 L411 236 L409 243 L411 258 L407 273 L408 280 L402 286 L401 302 L398 304 L394 314 L389 318 L387 322 L387 331 L378 335 L375 338 L374 343 L364 343 L361 340 L361 343 L353 344 L355 343 L353 342 L344 344 L344 346 L345 346 L336 350 L335 353 L329 353 L318 358 L305 368 L306 369 L303 372 L303 371 L300 370 L300 373 L297 372 L297 373 L300 374 L297 377 L298 381 L296 382 L299 394 L298 404 L296 410 L285 420 L278 432 L271 442 L258 453 L258 449 L262 449 L267 445 L268 441 L270 440 L271 438 L274 436 L273 432 L275 432 L275 430 L270 432 L267 428 L268 432 L267 436 L266 435 L264 440 L259 444 L256 450 L257 453 L251 465 L243 472 L241 471 L241 465 L245 460 L240 456 L238 452 L233 449 L228 445 L222 443 L217 437 L212 440 L211 437 L202 428 L199 429 L198 431 L193 429 L203 420 L213 408 L216 408 L215 406 L222 402 L226 398 L231 396 L237 393 L239 383 L236 375 L233 373 L228 374 L232 356 L228 353 L223 355 L219 355 L216 339 L214 335 L209 334 L207 332 L205 334 L201 334 L189 333 L191 319 L187 309 L190 307 L187 304 L192 296 L191 294 L195 286 L191 277 L184 274 L183 268 L185 263 L163 262 L163 253 L159 248 L162 248 L159 233 L153 229 L145 230 L141 225 L133 223 L130 219 L126 219 L122 217 L114 216 L113 214 L107 211 L103 202 L103 199 L102 193 L104 189 L103 184 L89 186 L75 195 L71 196 L65 201 L58 199 L41 199 L43 180 L34 187 L23 187 L21 181 L12 180 L14 175 L8 167 L5 162 L6 161 L2 158 L3 156 L6 155 L5 150 L12 145 L11 140 L14 135 L15 129 L27 121 L38 119 L40 117 L44 117 L46 119 L49 119 L56 82 L53 73 L48 69 L48 60 L55 58 L59 59 L57 55 L51 54 L51 47 L70 47 L70 43 L73 46 L79 42 L83 48 L83 53 L85 53Z M286 70 L292 69 L300 71 L295 84 L293 85 L291 84 L291 86 L288 85 L287 88 L284 89 L281 88 L276 89 L273 82 L275 80 L273 78 L274 70 L279 69 L286 70Z M350 345 L347 345 L349 344 L350 345Z M298 384 L297 383 L299 381 L298 384Z M337 354 L335 354 L336 352 L337 354Z M346 102 L345 104 L346 100 L346 102Z M413 224 L414 222 L414 223 L413 224Z M341 83 L340 84 L340 82 L341 83Z M285 64 L283 67 L278 67 L279 64 L285 64Z M278 44 L276 44 L276 42 L278 42 L278 44Z M274 69 L271 71 L270 70 L272 68 L274 69Z M288 69 L284 68 L288 66 L289 67 L288 69Z M277 66 L277 67 L274 67 L275 65 L277 60 L278 64 L277 66Z M280 62 L279 63 L279 61 L281 60 L280 62Z M260 84 L259 85 L264 75 L267 74 L268 75 L267 79 L260 84Z M299 400 L299 401 L299 398 L300 396 L299 400Z" & "' fill='#0A2540' stroke='#10D4C4' stroke-opacity='.45' stroke-width='1.6'/>" & _pts & "</svg>"
            & "<div class='nx-l'>" & _lista & "</div></div>"
            & "<div class='nx-lg'><span><i style='background:#45D5A1'></i>na meta</span><span><i style='background:#FFC66D'></i>até 5 p.p. abaixo</span><span><i style='background:#FF7285'></i>mais de 5 p.p. abaixo</span></div></div>"
    )
```

## 08 UX\Preditiva

### UX Preditiva Resumo

Resumo: projecao nov-dez vs meta, previsao da fonte do 1o semestre seguinte vs realizado, projecao x previsao, tendencia, sazonalidade e erro do metodo.

Formato: ``

```dax
VAR _c = [Data Corte]
VAR _nd = CALCULATETABLE ( VALUES ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] > _c, dCalendario[Data] <= DATE ( YEAR ( _c ), 12, 31 ) )
VAR _projND = CALCULATE ( [Projeção Sazonal Receita], REMOVEFILTERS ( dCalendario ), _nd )
VAR _metaND = CALCULATE ( [Meta Faturamento], REMOVEFILTERS ( dCalendario ), _nd )
VAR _h1 = CALCULATETABLE ( VALUES ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= DATE ( YEAR ( _c ) + 1, 1, 1 ), dCalendario[Data] <= DATE ( YEAR ( _c ) + 1, 6, 30 ) )
VAR _prev = CALCULATE ( [Receita Prevista], REMOVEFILTERS ( dCalendario ), _h1 )
VAR _projH1 = CALCULATE ( [Projeção Sazonal Receita], REMOVEFILTERS ( dCalendario ), _h1 )
VAR _baseH1 = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= DATE ( YEAR ( _c ), 1, 1 ), dCalendario[Data] <= DATE ( YEAR ( _c ), 6, 30 ) )
VAR _g = [Fator Tendência 12M]
VAR _sig = [Projeção Erro σ (backtest)]
VAR _mape = [Projeção MAPE (backtest)]
VAR _n = [Projeção Meses no Backtest]
VAR _saz =
    ADDCOLUMNS (
        FILTER ( CALCULATETABLE ( VALUES ( dCalendario[Mes] ), REMOVEFILTERS ( dCalendario ) ), NOT ISBLANK ( dCalendario[Mes] ) ),
        "@nm", VAR _m1 = dCalendario[Mes] RETURN CALCULATE ( SELECTEDVALUE ( dCalendario[NomeMesPT] ), REMOVEFILTERS ( dCalendario ), dCalendario[Mes] = _m1 ),
        "@ix",
            VAR _mm = dCalendario[Mes]
            RETURN AVERAGEX (
                { YEAR ( _c ) - 2, YEAR ( _c ) - 1 },
                VAR _y = [Value]
                RETURN DIVIDE (
                    CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Ano] = _y, dCalendario[Mes] = _mm ),
                    CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Ano] = _y ) / 12
                )
            )
    )
VAR _pico = TOPN ( 1, _saz, [@ix], DESC )
VAR _vale = TOPN ( 1, _saz, [@ix], ASC )
VAR _t = "<div class='nx-k'><div class='nx-kl'>@L</div><div class='nx-kv'>@V</div><div class='nx-ks'>@S</div></div>"
VAR _css = "<style>.nx-p{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(5,1fr);gap:12px;height:100vh;box-sizing:border-box}.nx-k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:11px 16px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-kl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:22px;font-weight:600;color:#FFFFFF;margin-top:3px;line-height:1.1}.nx-ks{font-size:10px;color:#A9B9CA;margin-top:3px}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
VAR _gap = DIVIDE ( _projND - _metaND, _metaND )
RETURN
    _css & "<div class='nx-p'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Projeção nov–dez/" & YEAR ( _c ) ), "@V", "R$ " & FORMAT ( _projND / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
            "@S", "<span style='color:" & IF ( _gap >= 0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _gap, "+0.0%;-0.0%", "pt-BR" ) & " vs meta</span> (R$ " & FORMAT ( _metaND / 1e6, "#,0.0", "pt-BR" ) & " mi)" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Previsão da fonte 1º sem/" & ( YEAR ( _c ) + 1 ) ), "@V", "R$ " & FORMAT ( _prev / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
            "@S", FORMAT ( DIVIDE ( _prev, _baseH1 ) - 1, "+0.0%;-0.0%", "pt-BR" ) & " vs 1º sem/" & YEAR ( _c ) & " realizado" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Projeção sazonal 1º sem/" & ( YEAR ( _c ) + 1 ) ), "@V", "R$ " & FORMAT ( _projH1 / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
            "@S", "previsão da fonte " & FORMAT ( DIVIDE ( _prev, _projH1 ) - 1, "+0.0%;-0.0%", "pt-BR" ) & " vs projeção" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Tendência 12 meses" ), "@V", FORMAT ( _g - 1, "+0.0%;-0.0%", "pt-BR" ) ),
            "@S", "pico: " & MAXX ( _pico, [@nm] ) & " · vale: " & MAXX ( _vale, [@nm] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Erro do método (backtest)" ), "@V", FORMAT ( _mape, "0.0%", "pt-BR" ) & " <span style='font-size:12px;color:#A9B9CA;font-weight:400'>MAPE</span>" ),
            "@S", "σ " & FORMAT ( _sig, "0.0%", "pt-BR" ) & " · " & _n & " meses · faixa de 90%" )
        & "</div>"
```

## 08 UX\Simulador

### UX Simulador Aviso

Rodape dos controles: base do cenario e aviso de que a simulacao nao e previsao.

Formato: ``

```dax
VAR _ini = CALCULATE ( MIN ( dCalendario[Data] ), FILTER ( VALUES ( dCalendario[Data] ), NOT ISBLANK ( [Receita Líquida] ) ) )
VAR _fim = MIN ( MAX ( dCalendario[Data] ), [Data Corte] )
RETURN
    "<div style='font-family:Segoe UI,sans-serif;font-size:10px;line-height:1.45;color:#A9B9CA;padding:2px 2px'>Base: "
        & FORMAT ( _ini, "dd/mm/yyyy" ) & " a " & FORMAT ( _fim, "dd/mm/yyyy" )
        & " (período e filiais do painel de filtros).<br><span style='color:#FFC66D'>Cálculo sob premissas, sem elasticidade. Não é previsão.</span></div>"
```

### UX Simulador Resumo

Comparacao base x simulado, margem operacional, volume de equilibrio e premissas.

Formato: ``

```dax
VAR _c = [Data Corte]
VAR _R0 = [Receita (até corte)]
VAR _C0 = CALCULATE ( [CMV], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _F0 = CALCULATE ( [Custo Frete], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _D0 = CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _dsc0 = CALCULATE ( [Desconto Médio Ponderado %], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _p = SELECTEDVALUE ( 'Sim Preço'[Preço %], 0 )
VAR _dd = SELECTEDVALUE ( 'Sim Desconto'[Desconto p.p.], 0 ) / 100
VAR _v = SELECTEDVALUE ( 'Sim Volume'[Volume %], 0 )
VAR _cc = SELECTEDVALUE ( 'Sim Custo'[Custo %], 0 )
VAR _f = SELECTEDVALUE ( 'Sim Frete'[Frete %], 0 )
VAR _e = SELECTEDVALUE ( 'Sim Despesas'[Despesas %], 0 )
VAR _k = DIVIDE ( 1 - ( _dsc0 + _dd ), 1 - _dsc0 )
VAR _R1 = _R0 * ( 1 + _p ) * _k * ( 1 + _v )
VAR _C1 = _C0 * ( 1 + _v ) * ( 1 + _cc )
VAR _F1 = _F0 * ( 1 + _v ) * ( 1 + _f )
VAR _D1 = _D0 * ( 1 + _e )
VAR _Res0 = _R0 - _C0 - _F0 - _D0
VAR _Res1 = _R1 - _C1 - _F1 - _D1
VAR _veq = DIVIDE ( _Res0 + _D1, _R0 * ( 1 + _p ) * _k - _C0 * ( 1 + _cc ) - _F0 * ( 1 + _f ) ) - 1
VAR _mg0 = DIVIDE ( _R0 - _C0, _R0 )
VAR _mg1 = DIVIDE ( _R1 - _C1, _R1 )
VAR _css = "<style>.nx-s{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 20px;display:flex;flex-direction:column;gap:10px}.nx-st{font-size:13px;font-weight:600;text-align:center}.nx-ss{font-size:10.5px;color:#FFC66D;text-align:center}.nx-s table{width:100%;border-collapse:collapse;font-size:12.5px}.nx-s th{font-size:10px;color:#A9B9CA;font-weight:600;text-align:right;padding:5px 6px;border-bottom:1px solid #173B5C}.nx-s th:first-child,.nx-s td:first-child{text-align:left}.nx-s td{text-align:right;padding:7px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.nx-s tr.r td{color:#FFFFFF;font-weight:600;font-size:14px;background:rgba(18,48,79,.6)}.nx-eq{display:grid;grid-template-columns:1fr 1fr;gap:12px}.nx-b{border-left:3px solid #5FA8E6;padding-left:10px}.nx-bl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-bv{font-size:20px;font-weight:600}.nx-bs{font-size:10px;color:#A9B9CA}.nx-pr{font-size:10px;color:#6F86A0;line-height:1.5}</style>"
VAR _d = _Res1 - _Res0
RETURN
    IF (
        [Filtro de Produto Ativo] || ISBLANK ( _R0 ),
        _css & "<div class='nx-s'><div class='nx-st'>Simulação indisponível</div><div class='nx-ss'>Remova o filtro de produto: frete e despesas não têm produto.</div></div>",
        _css & "<div class='nx-s'><div class='nx-st'>Cenário simulado vs base do período</div><div class='nx-ss'>Simulação sob premissas declaradas. Não é previsão nem recomendação.</div>"
            & "<table><tr><th></th><th>Base</th><th>Simulado</th><th>Variação</th></tr>"
            & "<tr><td>Receita líquida</td><td>R$ " & FORMAT ( _R0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _R1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _R1 >= _R0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _R1, _R0 ) - 1, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</td></tr>"
            & "<tr><td>Margem bruta</td><td>" & FORMAT ( _mg0, "0.0%", "pt-BR" ) & "</td><td>" & FORMAT ( _mg1, "0.0%", "pt-BR" ) & "</td><td style='color:" & IF ( _mg1 >= _mg0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( ( _mg1 - _mg0 ) * 100, "+0.0;-0.0;0.0", "pt-BR" ) & " p.p.</td></tr>"
            & "<tr><td>Frete</td><td>R$ " & FORMAT ( _F0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _F1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _F1 <= _F0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _F1, _F0 ) - 1, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</td></tr>"
            & "<tr><td>Despesas operacionais</td><td>R$ " & FORMAT ( _D0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _D1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _D1 <= _D0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _D1, _D0 ) - 1, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</td></tr>"
            & "<tr class='r'><td>Resultado operacional</td><td>R$ " & FORMAT ( _Res0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _Res1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _d >= 0, "#45D5A1", "#FF7285" ) & "'>" & IF ( _d >= 0, "+", "−" ) & "R$ " & FORMAT ( ABS ( _d ) / 1e6, "#,0.0", "pt-BR" ) & " mi</td></tr></table>"
            & "<div class='nx-eq'><div class='nx-b'><div class='nx-bl'>Margem operacional</div><div class='nx-bv'>" & FORMAT ( DIVIDE ( _Res0, _R0 ), "0.0%", "pt-BR" ) & " → " & FORMAT ( DIVIDE ( _Res1, _R1 ), "0.0%", "pt-BR" ) & "</div><div class='nx-bs'>resultado ÷ receita</div></div>"
            & "<div class='nx-b' style='border-color:#FFC66D'><div class='nx-bl'>Volume para manter o resultado</div><div class='nx-bv'>" & FORMAT ( _veq, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</div><div class='nx-bs'>com os demais parâmetros escolhidos</div></div></div>"
            & "<div class='nx-pr'>Premissas: preço e desconto alteram a receita; volume escala receita, custo e frete; despesas não escalam com volume; sem elasticidade preço × volume. Resultado operacional = receita − CMV − frete − despesas (difere da DRE gerencial, que não subtrai frete).</div></div>"
    )
```

## 09 Qualidade\Corte temporal

### Despesas Pós-Corte (qtd)

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fDespesa ), REMOVEFILTERS ( dCalendario ), fDespesa[ElegivelHistorico] = 0 )
```

### Despesas Pós-Corte (R$)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fDespesa[Valor] ), REMOVEFILTERS ( dCalendario ), fDespesa[ElegivelHistorico] = 0 )
```

### Compras Pós-Corte (qtd)

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fCompra ), REMOVEFILTERS ( dCalendario ), fCompra[ElegivelHistorico] = 0 )
```

### Compras Pós-Corte (R$)

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fCompra[ValorCompra] ), REMOVEFILTERS ( dCalendario ), fCompra[ElegivelHistorico] = 0 )
```

### Contas a Pagar Pós-Corte (qtd)

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fContasPagar ), REMOVEFILTERS ( dCalendario ), fContasPagar[ElegivelHistorico] = 0 )
```

### Contas a Pagar Pós-Corte (R$)

Titulos de compras pos-corte (mesmo valor das compras; nao somar com Compras Pos-Corte).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), REMOVEFILTERS ( dCalendario ), fContasPagar[ElegivelHistorico] = 0 )
```

### Estoque Pós-Corte (qtd)

Snapshots; valor nao e somavel entre meses, por isso so contagem.

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fEstoqueMensal ), REMOVEFILTERS ( dCalendario ), fEstoqueMensal[ElegivelHistorico] = 0 )
```

### Movimentos Pós-Corte (qtd)

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fMovimentoEstoque ), REMOVEFILTERS ( dCalendario ), fMovimentoEstoque[ElegivelHistorico] = 0 )
```

### Ocupação WMS Pós-Corte (qtd)

Formato: `#,0`

```dax
CALCULATE ( COUNTROWS ( fOcupacaoArmazem ), REMOVEFILTERS ( dCalendario ), fOcupacaoArmazem[ElegivelHistorico] = 0 )
```

### Registros Pós-Corte (total)

Formato: `#,0`

```dax
[Despesas Pós-Corte (qtd)] + [Compras Pós-Corte (qtd)] + [Contas a Pagar Pós-Corte (qtd)]
    + [Estoque Pós-Corte (qtd)] + [Movimentos Pós-Corte (qtd)] + [Ocupação WMS Pós-Corte (qtd)]
```

### Valor Financeiro Pós-Corte (R$)

Despesas + compras. Contas a pagar fora para nao duplicar as compras.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
[Despesas Pós-Corte (R$)] + [Compras Pós-Corte (R$)]
```

### Data Máxima Encontrada

Maior data nas fatos realizadas com registros pos-corte (previsao, metas e orcamento fora).

Formato: `dd/MM/yyyy`

```dax
VAR _d1 = CALCULATE ( MAX ( fDespesa[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
VAR _d2 = CALCULATE ( MAX ( fCompra[DataCompra] ), REMOVEFILTERS ( dCalendario ) )
VAR _d3 = CALCULATE ( MAX ( fEstoqueMensal[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
VAR _d4 = CALCULATE ( MAX ( fMovimentoEstoque[DataMovimento] ), REMOVEFILTERS ( dCalendario ) )
VAR _d5 = CALCULATE ( MAX ( fOcupacaoArmazem[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
RETURN
    MAXX ( { _d1, _d2, _d3, _d4, _d5 }, [Value] )
```

### Data Máxima Previsão

Formato: `dd/MM/yyyy`

```dax
CALCULATE ( MAX ( fPrevisao[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
```

## 09 Qualidade\Parametros

### Data Corte

Data maxima historica (parametro pDataCorte).

Formato: `dd/MM/yyyy`

```dax
MAX ( _Parametros[DataCorte] )
```

### Data Referência

Ultima data do contexto limitada a Data Corte; BLANK quando o contexto inteiro e posterior ao corte (sem realizado). Base das medidas as-of.

Formato: `dd/MM/yyyy`

```dax
VAR _min = MIN ( dCalendario[Data] )
VAR _max = MAX ( dCalendario[Data] )
VAR _corte = [Data Corte]
RETURN
    SWITCH (
        TRUE (),
        _min > _corte, BLANK (),
        ISBLANK ( _max ) || _max > _corte, _corte,
        _max
    )
```

### Filtro de Produto Ativo

TRUE quando ha filtro em dProduto. Usado para anular medidas que combinam receita por item com bases sem produto (frete, devolucao, despesa, metas, impostos).

Formato: `"""Sim"";""Sim"";""Não"""`

```dax
ISCROSSFILTERED ( dProduto )
```

### Data Atualização

Momento do ultimo refresh do modelo.

Formato: `dd/MM/yyyy HH:mm`

```dax
MAX ( _Parametros[AtualizadoEm] )
```

## 09 Qualidade\Recebimento

### Títulos Inconsistentes

Formato: `#,0`

```dax
CALCULATE ( [Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Inconsistente" ) )
```

### Valor Títulos Inconsistentes

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Valor Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Inconsistente" ) )
```

### Valor Pago Declarado em Inconsistentes

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( SUM ( fContasReceber[ValorPago] ), KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Inconsistente" ) )
```

### % Títulos Inconsistentes

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [Títulos Inconsistentes], [Títulos] )
```

### % Valor Inconsistente

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [Valor Títulos Inconsistentes], [Valor Títulos] )
```

## 10 Previsão

### Fator Tendência 12M

Receita dos 12 meses ate o corte / receita dos 12 meses anteriores.

Formato: `0.000`

```dax
VAR _s = EOMONTH ( [Data Corte], 0 ) + 1
VAR _a = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _s, -12 ), dCalendario[Data] < _s )
VAR _b = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _s, -24 ), dCalendario[Data] < EDATE ( _s, -12 ) )
RETURN DIVIDE ( _a, _b )
```

### Projeção Sazonal Receita

Meses apos o corte: receita do mesmo mes no ano anterior x Fator Tendencia 12M. Nao e a previsao da fonte.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _c = [Data Corte]
VAR _g = [Fator Tendência 12M]
VAR _meses = FILTER ( VALUES ( dCalendario[InicioMes] ), dCalendario[InicioMes] > _c )
RETURN
    IF (
        NOT ISEMPTY ( _meses ),
        SUMX (
            _meses,
            VAR _m = dCalendario[InicioMes]
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] <= EOMONTH ( _m, -12 ) )
        ) * _g
    )
```

### Projeção Erro σ (backtest)

Desvio-padrao dos erros relativos do metodo aplicado aos meses do ano do corte (G calculado ate o mes anterior).

Formato: `0.0%`

```dax
VAR _c = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        CALCULATETABLE ( VALUES ( dCalendario[InicioMes] ), REMOVEFILTERS ( dCalendario ), dCalendario[InicioMes] >= DATE ( YEAR ( _c ), 1, 1 ), dCalendario[InicioMes] <= _c ),
        "@r",
            VAR _m = dCalendario[InicioMes]
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= _m, dCalendario[Data] <= EOMONTH ( _m, 0 ) ),
        "@p",
            VAR _m = dCalendario[InicioMes]
            VAR _ly = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] <= EOMONTH ( _m, -12 ) )
            VAR _g = DIVIDE (
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] < _m ),
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -24 ), dCalendario[Data] < EDATE ( _m, -12 ) )
            )
            RETURN _ly * _g
    )
VAR _e = FILTER ( ADDCOLUMNS ( _t, "@err", DIVIDE ( [@r], [@p] ) - 1 ), NOT ISBLANK ( [@r] ) && NOT ISBLANK ( [@p] ) )
RETURN STDEVX.S ( _e, [@err] )
```

### Projeção MAPE (backtest)

Erro percentual absoluto medio do backtest.

Formato: `0.0%`

```dax
VAR _c = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        CALCULATETABLE ( VALUES ( dCalendario[InicioMes] ), REMOVEFILTERS ( dCalendario ), dCalendario[InicioMes] >= DATE ( YEAR ( _c ), 1, 1 ), dCalendario[InicioMes] <= _c ),
        "@r",
            VAR _m = dCalendario[InicioMes]
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= _m, dCalendario[Data] <= EOMONTH ( _m, 0 ) ),
        "@p",
            VAR _m = dCalendario[InicioMes]
            VAR _ly = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] <= EOMONTH ( _m, -12 ) )
            VAR _g = DIVIDE (
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] < _m ),
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -24 ), dCalendario[Data] < EDATE ( _m, -12 ) )
            )
            RETURN _ly * _g
    )
VAR _e = FILTER ( ADDCOLUMNS ( _t, "@err", DIVIDE ( [@r], [@p] ) - 1 ), NOT ISBLANK ( [@r] ) && NOT ISBLANK ( [@p] ) )
RETURN AVERAGEX ( _e, ABS ( [@err] ) )
```

### Projeção Meses no Backtest

Quantidade de meses usados no backtest.

Formato: `0`

```dax
VAR _c = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        CALCULATETABLE ( VALUES ( dCalendario[InicioMes] ), REMOVEFILTERS ( dCalendario ), dCalendario[InicioMes] >= DATE ( YEAR ( _c ), 1, 1 ), dCalendario[InicioMes] <= _c ),
        "@r",
            VAR _m = dCalendario[InicioMes]
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= _m, dCalendario[Data] <= EOMONTH ( _m, 0 ) ),
        "@p",
            VAR _m = dCalendario[InicioMes]
            VAR _ly = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] <= EOMONTH ( _m, -12 ) )
            VAR _g = DIVIDE (
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] < _m ),
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -24 ), dCalendario[Data] < EDATE ( _m, -12 ) )
            )
            RETURN _ly * _g
    )
VAR _e = FILTER ( ADDCOLUMNS ( _t, "@err", DIVIDE ( [@r], [@p] ) - 1 ), NOT ISBLANK ( [@r] ) && NOT ISBLANK ( [@p] ) )
RETURN COUNTROWS ( _e )
```

### Projeção Limite Inferior 90%

Projecao x (1 - 1,833 x sigma); t de Student com 9 gl.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _p = [Projeção Sazonal Receita] RETURN IF ( NOT ISBLANK ( _p ), _p * ( 1 - 1.833 * [Projeção Erro σ (backtest)] ) )
```

### Projeção Limite Superior 90%

Projecao x (1 + 1,833 x sigma); t de Student com 9 gl.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _p = [Projeção Sazonal Receita] RETURN IF ( NOT ISBLANK ( _p ), _p * ( 1 + 1.833 * [Projeção Erro σ (backtest)] ) )
```

### Receita Base Ano Anterior

Receita do mesmo periodo do ano anterior sem limitar ao corte (base para comparar periodos futuros, ex.: previsao 2027 vs 2026).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
CALCULATE ( [Receita Líquida], SAMEPERIODLASTYEAR ( dCalendario[Data] ) )
```

## 11 Simulador

### Sim Valor Etapa

Ponte do resultado operacional: base e efeito sequencial de preco, desconto, volume, custo, frete e despesas (soma = simulado).

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _c = [Data Corte]
VAR _R0 = [Receita (até corte)]
VAR _C0 = CALCULATE ( [CMV], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _F0 = CALCULATE ( [Custo Frete], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _D0 = CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _dsc0 = CALCULATE ( [Desconto Médio Ponderado %], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _p = SELECTEDVALUE ( 'Sim Preço'[Preço %], 0 )
VAR _dd = SELECTEDVALUE ( 'Sim Desconto'[Desconto p.p.], 0 ) / 100
VAR _v = SELECTEDVALUE ( 'Sim Volume'[Volume %], 0 )
VAR _cc = SELECTEDVALUE ( 'Sim Custo'[Custo %], 0 )
VAR _f = SELECTEDVALUE ( 'Sim Frete'[Frete %], 0 )
VAR _e = SELECTEDVALUE ( 'Sim Despesas'[Despesas %], 0 )
VAR _k = DIVIDE ( 1 - ( _dsc0 + _dd ), 1 - _dsc0 )
VAR _R1 = _R0 * ( 1 + _p ) * _k * ( 1 + _v )
VAR _C1 = _C0 * ( 1 + _v ) * ( 1 + _cc )
VAR _F1 = _F0 * ( 1 + _v ) * ( 1 + _f )
VAR _D1 = _D0 * ( 1 + _e )
VAR _Res0 = _R0 - _C0 - _F0 - _D0
VAR _Res1 = _R1 - _C1 - _F1 - _D1
VAR _o = SELECTEDVALUE ( 'Sim Etapa'[Ordem] )
RETURN
    IF (
        NOT [Filtro de Produto Ativo] && NOT ISBLANK ( _R0 ),
        SWITCH (
            _o,
            1, _Res0,
            2, _R0 * _p,
            3, _R0 * ( 1 + _p ) * ( _k - 1 ),
            4, _v * ( _R0 * ( 1 + _p ) * _k - _C0 - _F0 ),
            5, - _C0 * ( 1 + _v ) * _cc,
            6, - _F0 * ( 1 + _v ) * _f,
            7, - _D0 * _e
        )
    )
```

### Sim Δ Resultado (grade)

Variacao do resultado operacional para cada par preco x volume da grade, com os demais parametros dos controles.

Formato: `R$ #,0.00;-R$ #,0.00;R$ #,0.00`

```dax
VAR _c = [Data Corte]
VAR _R0 = [Receita (até corte)]
VAR _C0 = CALCULATE ( [CMV], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _F0 = CALCULATE ( [Custo Frete], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _D0 = CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _dsc0 = CALCULATE ( [Desconto Médio Ponderado %], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _p = SELECTEDVALUE ( 'Sim Preço'[Preço %], 0 )
VAR _dd = SELECTEDVALUE ( 'Sim Desconto'[Desconto p.p.], 0 ) / 100
VAR _v = SELECTEDVALUE ( 'Sim Volume'[Volume %], 0 )
VAR _cc = SELECTEDVALUE ( 'Sim Custo'[Custo %], 0 )
VAR _f = SELECTEDVALUE ( 'Sim Frete'[Frete %], 0 )
VAR _e = SELECTEDVALUE ( 'Sim Despesas'[Despesas %], 0 )
VAR _k = DIVIDE ( 1 - ( _dsc0 + _dd ), 1 - _dsc0 )
VAR _R1 = _R0 * ( 1 + _p ) * _k * ( 1 + _v )
VAR _C1 = _C0 * ( 1 + _v ) * ( 1 + _cc )
VAR _F1 = _F0 * ( 1 + _v ) * ( 1 + _f )
VAR _D1 = _D0 * ( 1 + _e )
VAR _Res0 = _R0 - _C0 - _F0 - _D0
VAR _Res1 = _R1 - _C1 - _F1 - _D1
VAR _gp = SELECTEDVALUE ( 'Sim Grade Preço'[Preço grade %] )
VAR _gv = SELECTEDVALUE ( 'Sim Grade Volume'[Volume grade %] )
VAR _Rg = _R0 * ( 1 + _gp ) * _k * ( 1 + _gv )
VAR _Resg = _Rg - _C0 * ( 1 + _gv ) * ( 1 + _cc ) - _F0 * ( 1 + _gv ) * ( 1 + _f ) - _D1
RETURN IF ( NOT [Filtro de Produto Ativo] && NOT ISBLANK ( _gp ) && NOT ISBLANK ( _gv ), _Resg - _Res0 )
```

## 12 Operações

### Visitas

Visitas comerciais registradas (fVisitaComercial), pela DataVisita.

Formato: `#,0`

```dax
COUNTROWS ( fVisitaComercial )
```

### Visitas com Pedido

Visitas com Resultado = Pedido.

Formato: `#,0`

```dax
IF ( NOT ISBLANK ( [Visitas] ), CALCULATE ( [Visitas], KEEPFILTERS ( fVisitaComercial[Resultado] = "Pedido" ) ) + 0 )
```

### Conversão de Visitas %

Visitas com pedido / visitas.

Formato: `0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Visitas com Pedido], [Visitas] )
```

### Interações de Campanha

Interacoes de clientes com campanhas, pela DataInteracao.

Formato: `#,0`

```dax
COUNTROWS ( fInteracaoCampanha )
```

### Conversões de Campanha

Interacoes do tipo Conversao.

Formato: `#,0`

```dax
CALCULATE ( [Interações de Campanha], KEEPFILTERS ( fInteracaoCampanha[TipoInteracao] = "Conversão" ) )
```

### Campanhas Ativas (período)

Campanhas cujo intervalo Inicio-Fim cruza o periodo do contexto (campanha e intervalo, nao evento diario).

Formato: `#,0`

```dax
VAR _i = MIN ( dCalendario[Data] )
VAR _f = MAX ( dCalendario[Data] )
RETURN COUNTROWS ( FILTER ( dCampanha, dCampanha[Inicio] <= _f && dCampanha[Fim] >= _i ) )
```

### Campanha no Período

1 quando a campanha da linha cruza o periodo selecionado (usado pelo cronograma).

Formato: `0`

```dax
VAR _i = CALCULATE ( MIN ( dCalendario[Data] ), ALLSELECTED ( dCampanha ) )
VAR _f = CALCULATE ( MAX ( dCalendario[Data] ), ALLSELECTED ( dCampanha ) )
RETURN IF ( HASONEVALUE ( dCampanha[CampanhaID] ) && SELECTEDVALUE ( dCampanha[Inicio] ) <= _f && SELECTEDVALUE ( dCampanha[Fim] ) >= _i, 1 )
```

### Período Início

Primeiro dia do mes do calendario (ignora o dia clicado na matriz).

Formato: `dd/mm/yyyy`

```dax
CALCULATE ( MIN ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario[Data], dCalendario[SemanaDoMes], dCalendario[DiaSemanaAbrev], dCalendario[DiaSemana] ), ALLSELECTED ( dCampanha ) )
```

### Período Fim

Ultimo dia do mes do calendario (ignora o dia clicado na matriz).

Formato: `dd/mm/yyyy`

```dax
CALCULATE ( MAX ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario[Data], dCalendario[SemanaDoMes], dCalendario[DiaSemanaAbrev], dCalendario[DiaSemana] ), ALLSELECTED ( dCampanha ) )
```

### Dia Selecionado

Data quando um unico dia esta no contexto (marcador do cronograma).

Formato: `dd/mm/yyyy`

```dax
IF ( COUNTROWS ( VALUES ( dCalendario[Data] ) ) = 1, MAX ( dCalendario[Data] ) )
```
