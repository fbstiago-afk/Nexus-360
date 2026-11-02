# 03 — Modelo semântico e catálogo DAX

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## 1. Estratégia de modelo
Criar esquema estrela com dimensões `dCalendario`, `dCliente`, `dProduto`, `dFilial`, `dVendedor`, `dCampanha`, `dFornecedor`, `dTransportadora`, `dPosicaoArmazem`. Fatos permanecem separados por grão. O CSV contém **candidatas**, não o desenho final.

**PROPOSTA de engenharia:** criar `dPedido` a partir de `fPedido` com `PedidoID` único e atributos de cliente/filial/vendedor/campanha/data, para filtrar `fItemPedido`, `fFaturamento`, `fEntrega`, `fContasReceber` e `fDevolucao` sem fatos encadeadas. Evitar duplicar caminhos ativos com relações diretas das mesmas dimensões. Em alternativa, materializar chaves das dimensões em cada fato via Power Query e usar estrelas independentes. Escolher um desenho, validar caminhos, não combinar ambos indiscriminadamente.

**Datas:** relação principal por evento para cada fato; datas alternativas com `USERELATIONSHIP` ou calendários role-playing. Para contas, vencimento e pagamento são papéis distintos. Não ativar simultaneamente `fEntrega[DataEntrega]` e `fEntrega[DataPrometida]` para o mesmo calendário.

## 2. Medidas DAX fundamentadas (exemplos)
```dax
Receita Líquida = SUM ( fFaturamento[ReceitaLiquida] )
CMV = SUM ( fFaturamento[CMV] )
Margem Bruta = [Receita Líquida] - [CMV]
Margem Bruta % = DIVIDE ( [Margem Bruta], [Receita Líquida] )
Impostos = SUM ( fFaturamento[Impostos] )
Pedidos = DISTINCTCOUNT ( fPedido[PedidoID] )
Faturas = DISTINCTCOUNT ( fFaturamento[FaturaID] )
Valor Pedidos Itens = SUM ( fItemPedido[ValorLiquido] )
Quantidade Vendida Itens = SUM ( fItemPedido[Quantidade] )
Ticket Médio Faturado = DIVIDE ( [Receita Líquida], [Faturas] )
Despesas Operacionais = SUM ( fDespesa[Valor] )
Resultado Gerencial Simplificado = [Margem Bruta] - [Despesas Operacionais]
Valor Devolvido = SUM ( fDevolucao[ValorDevolvido] )
Receita Ajustada por Devoluções = [Receita Líquida] - [Valor Devolvido]
Entregas = COUNTROWS ( fEntrega )
Entregas OTIF = CALCULATE ( [Entregas], fEntrega[NoPrazo] = 1, fEntrega[InFull] = 1 )
OTIF % = DIVIDE ( [Entregas OTIF], [Entregas] )
Meta Valor = SUM ( fMeta[ValorMeta] )
Orçamento Valor = SUM ( fOrcamento[ValorOrcado] )
Receita Prevista = SUM ( fPrevisao[ReceitaPrevista] )
```

> **Cuidado:** `[Meta Valor]` só é comparável com uma medida realizada depois de filtrar `fMeta[Indicador]` pelo indicador correspondente. `fOrcamento[Conta]` exige mapeamento explícito antes de comparar. `[Entregas]` deve excluir registros inelegíveis se o teste de `StatusEntrega` identificar casos não concluídos. A receita ajustada assume que devoluções não foram previamente deduzidas.

## 3. Medidas condicionadas a validação
```dax
-- PROPOSTA: usar somente após validar elegibilidade de entrega
Entregas Elegíveis =
CALCULATE ( COUNTROWS ( fEntrega ), NOT ISBLANK ( fEntrega[DataEntrega] ) )
OTIF Elegível % =
DIVIDE (
    CALCULATE ( [Entregas Elegíveis], fEntrega[NoPrazo] = 1, fEntrega[InFull] = 1 ),
    [Entregas Elegíveis]
)

-- Saldo de títulos como visão atual, não histórico as-of
Saldo Títulos Atual =
SUMX ( fContasReceber, fContasReceber[ValorTitulo] - fContasReceber[ValorPago] )
```

## 4. Regras avançadas
- **Churn:** `PROPOSTA` janela de 90 dias; usar clientes com compra histórica, respeitar data de corte e separar novo, ativo, inativo e reativado. Definir compra como pedido ou faturamento antes da implementação.
- **Inadimplência histórica:** usar vencimento <= data de corte e pagamento posterior à data de corte como não pago naquele momento; `ValorPago` agregado sem histórico de pagamentos pode não reconstruir saldo as-of confiável. Rotular limitações.
- **Estoque:** `SaldoUnidades` é snapshot; usar última data disponível, nunca somar meses. Valor de estoque é amostral.
- **Ocupação:** snapshot por `PosicaoID` e `DataReferencia`; não extrapolar para todo o armazém.
- **Metas:** filtrar `Indicador`, alinhar granularidade mês-filial; não usar valor único sem segmentação.
- **Previsão:** datas posteriores a 2026-10-31 não podem entrar em realizado.
- **Time intelligence:** usar `dCalendario[Data]` marcada como tabela de datas, garantindo continuidade.

## 5. Organização de medidas
Pastas sugeridas (não são tabelas do banco): `00_Base`, `01_Comercial`, `02_Clientes`, `03_Logistica`, `04_WMS`, `05_Financeiro`, `06_Planejamento`, `07_Tempo`, `08_Simulacoes`, `09_UI_SVG`, `99_QA`.

## 6. Regras de filtro e riscos
Preferir dimensão -> fato, direção única, cardinalidade 1:N. Não ligar fatos em muitos-para-muitos; evitar caminhos concorrentes `dCliente` -> `fPedido` -> `fContasReceber` e `dCliente` -> `fContasReceber`. Documentar relações inativas, datas alternativas, medidas que usam `REMOVEFILTERS`, `ALLSELECTED`, `TREATAS`, `USERELATIONSHIP`, `ISINSCOPE`.

## 7. Reconciliações mínimas
Validar com SQL: `SUM(ReceitaLiquida)`, `SUM(CMV)`, `SUM(ValorDevolvido)`, `COUNT(DISTINCT PedidoID)`, `COUNT(*)` por fato, e comparações por filial/período. O total visual não deve variar quando uma dimensão sem relação aplicável é filtrada; se houver necessidade de propagação, criar a relação correta, não mascarar via DAX.
