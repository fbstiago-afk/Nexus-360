# NEXUS 360 - Gerador da tabela de medidas _Medidas.tmdl
# Uso: python3 -I gerar_medidas.py <pasta_definition_saida>
import sys, os, uuid, csv

OUT = sys.argv[1]
T = '\t'
MOEDA = 'R$ #,0.00;-R$ #,0.00;R$ #,0.00'
PCT = '0.0%;-0.0%;0.0%'
PCT2 = '0.00%;-0.00%;0.00%'
INT = '#,0'
DEC1 = '#,0.0'
DEC2 = '#,0.00'
PP = '+0.0;-0.0;0.0'
DATA = 'dd/MM/yyyy'

M = []  # (pasta, nome, formato, expressao, descricao)


def m(pasta, nome, fmt, expr, desc=''):
    M.append((pasta, nome, fmt, expr.strip('\n'), desc))


# ---------------- 09 Qualidade \ Parametros
Q = '09 Qualidade'
m(Q + '\\Parametros', 'Data Corte', DATA, 'MAX ( _Parametros[DataCorte] )', 'Data maxima historica (parametro pDataCorte).')
m(Q + '\\Parametros', 'Janela Churn (dias)', '0', 'MAX ( _Parametros[JanelaChurnDias] )', 'Janela de inatividade (parametro pJanelaChurnDias, PROPOSTA 90 dias).')
m(Q + '\\Parametros', 'Data Referência', DATA, '''
VAR _max = MAX ( dCalendario[Data] )
VAR _corte = [Data Corte]
RETURN
    IF ( ISBLANK ( _max ) || _max > _corte, _corte, _max )''', 'Ultima data do contexto, limitada a Data Corte. Base das medidas as-of.')

# ---------------- 00 Base
B = '00 Base'
m(B, 'Receita Líquida', MOEDA, 'SUM ( fFaturamento[ReceitaLiquida] )', 'Soma de fFaturamento[ReceitaLiquida]. Data ativa: DataFaturamento.')
m(B, 'CMV', MOEDA, 'SUM ( fFaturamento[CMV] )')
m(B, 'Impostos', MOEDA, 'SUM ( fFaturamento[Impostos] )')
m(B, 'Margem Bruta', MOEDA, '[Receita Líquida] - [CMV]')
m(B, 'Margem Bruta %', PCT2, 'DIVIDE ( [Margem Bruta], [Receita Líquida] )')
m(B, 'Faturas', INT, 'COUNTROWS ( fFaturamento )')
m(B, 'Ticket Médio Faturado', MOEDA, 'DIVIDE ( [Receita Líquida], [Faturas] )')
m(B, 'Pedidos', INT, 'COUNTROWS ( fPedido )', 'Todos os status. Data ativa: DataPedido.')
m(B, 'Pedidos Faturados', INT, 'CALCULATE ( [Pedidos], KEEPFILTERS ( fPedido[StatusPedido] = "Faturado" ) )')
m(B, 'Pedidos Cancelados', INT, 'CALCULATE ( [Pedidos], KEEPFILTERS ( fPedido[StatusPedido] = "Cancelado" ) )')
m(B, 'Pedidos Pendentes', INT, 'CALCULATE ( [Pedidos], KEEPFILTERS ( fPedido[StatusPedido] = "Pendente" ) )')
m(B, 'Taxa de Cancelamento %', PCT, 'DIVIDE ( [Pedidos Cancelados], [Pedidos] )')
m(B, 'Valor Itens (todos os status)', MOEDA, 'SUM ( fItemPedido[ValorLiquido] )', 'Inclui pedidos cancelados e pendentes. Nao somar com Receita Liquida.')
m(B, 'Valor Itens Faturados', MOEDA, 'CALCULATE ( [Valor Itens (todos os status)], KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )',
  'Igual a Receita Liquida no total (validado), porem datado por DataPedido.')
m(B, 'Custo Itens Faturados', MOEDA, 'CALCULATE ( SUM ( fItemPedido[CustoMercadoria] ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )')
m(B, 'Quantidade Itens Faturados', INT, 'CALCULATE ( SUM ( fItemPedido[Quantidade] ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )')
m(B, 'Margem Itens Faturados %', PCT2, 'DIVIDE ( [Valor Itens Faturados] - [Custo Itens Faturados], [Valor Itens Faturados] )')
m(B, 'Valor Devolvido', MOEDA, 'SUM ( fDevolucao[ValorDevolvido] )')
m(B, 'Devoluções', INT, 'COUNTROWS ( fDevolucao )')
m(B, 'Receita Ajustada por Devoluções', MOEDA, '[Receita Líquida] - [Valor Devolvido]', 'Devolucoes deduzidas uma unica vez (data da devolucao).')
m(B, 'Devolução % Receita', PCT2, 'DIVIDE ( [Valor Devolvido], [Receita Líquida] )')
m(B, 'Despesas Operacionais', MOEDA, 'CALCULATE ( SUM ( fDespesa[Valor] ), KEEPFILTERS ( fDespesa[ElegivelHistorico] = 1 ) )',
  'Apenas registros elegiveis (<= Data Corte). Despesas sinteticas, nao auditaveis.')
m(B, 'Resultado Gerencial Simplificado', MOEDA, '[Margem Bruta] - [Despesas Operacionais]', 'DRE gerencial simplificada; nao contabil.')
m(B, 'Resultado Gerencial %', PCT2, 'DIVIDE ( [Resultado Gerencial Simplificado], [Receita Líquida] )')

# ---------------- 01 Comercial
C = '01 Comercial'
m(C, 'Desconto Médio Ponderado %', PCT2, 'DIVIDE ( SUMX ( fFaturamento, fFaturamento[ReceitaLiquida] * fFaturamento[DescontoPercentual] ), [Receita Líquida] )',
  'Desconto do pedido ponderado pela receita faturada (desconto ja embutido no valor).')
m(C, 'Clientes Positivados', INT, 'DISTINCTCOUNT ( fFaturamento[ClienteID] )')
m(C, 'Vendedores com Venda', INT, 'DISTINCTCOUNT ( fFaturamento[VendedorID] )')
m(C, 'Receita por Vendedor', MOEDA, 'DIVIDE ( [Receita Líquida], [Vendedores com Venda] )')
m(C, 'SKUs Vendidos', INT, 'CALCULATE ( DISTINCTCOUNT ( fItemPedido[ProdutoID] ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) )')
m(C, 'Itens por Pedido Faturado', DEC2, 'DIVIDE ( CALCULATE ( COUNTROWS ( fItemPedido ), KEEPFILTERS ( fItemPedido[StatusPedido] = "Faturado" ) ), [Pedidos Faturados] )')
m(C, 'Participação Receita %', PCT, 'DIVIDE ( [Receita Líquida], CALCULATE ( [Receita Líquida], ALLSELECTED () ) )')

# ---------------- 02 Clientes
K = '02 Clientes'
m(K, 'Clientes com Histórico', INT, '''
VAR _ref = [Data Referência]
RETURN
    CALCULATE (
        DISTINCTCOUNT ( fFaturamento[ClienteID] ),
        REMOVEFILTERS ( dCalendario ),
        dCalendario[Data] <= _ref
    )''', 'Clientes com ao menos uma fatura ate a Data Referencia.')
m(K, 'Clientes Ativos (Janela)', INT, '''
VAR _ref = [Data Referência]
VAR _ini = _ref - [Janela Churn (dias)] + 1
RETURN
    CALCULATE (
        DISTINCTCOUNT ( fFaturamento[ClienteID] ),
        REMOVEFILTERS ( dCalendario ),
        dCalendario[Data] >= _ini,
        dCalendario[Data] <= _ref
    )''', 'Clientes com fatura nos ultimos N dias (janela) ate a Data Referencia.')
m(K, 'Clientes Inativos (Janela)', INT, '[Clientes com Histórico] - [Clientes Ativos (Janela)]', 'Com historico e sem fatura na janela. Cliente novo nunca entra aqui.')
m(K, 'Churn % (Janela)', PCT, 'DIVIDE ( [Clientes Inativos (Janela)], [Clientes com Histórico] )')
m(K, 'Clientes Novos', INT, '''
VAR _corte = [Data Corte]
VAR _ini = MIN ( dCalendario[Data] )
VAR _fim = MIN ( MAX ( dCalendario[Data] ), _corte )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( fFaturamento[ClienteID] ),
        KEEPFILTERS ( dCalendario[Data] <= _corte ),
        KEEPFILTERS ( dCliente[PrimeiraCompra] >= _ini ),
        KEEPFILTERS ( dCliente[PrimeiraCompra] <= _fim )
    )''', 'Clientes cuja primeira fatura ocorre no periodo (DataCadastro nao e usada - C6).')
m(K, 'Clientes Reativados', INT, '''
VAR _corte = [Data Corte]
VAR _ini = MIN ( dCalendario[Data] )
VAR _janela = [Janela Churn (dias)]
VAR _clientes =
    CALCULATETABLE ( VALUES ( fFaturamento[ClienteID] ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
RETURN
    COUNTROWS (
        FILTER (
            _clientes,
            VAR _ultima =
                CALCULATE (
                    MAX ( fFaturamento[DataFaturamento] ),
                    REMOVEFILTERS ( dCalendario ),
                    dCalendario[Data] < _ini
                )
            RETURN
                NOT ISBLANK ( _ultima ) && _ini - _ultima > _janela
        )
    )''', 'Compraram no periodo e estavam inativos no inicio dele (ultima fatura anterior ha mais de N dias).')

# ---------------- 03 Logistica
L = '03 Logistica'
m(L, 'Entregas', INT, 'COUNTROWS ( fEntrega )', 'Todas as entregas (DataEntrega sem nulos: todas elegiveis). Data ativa: DataEntrega.')
m(L, 'Entregas OTIF', INT, 'CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[NoPrazo] = 1 ), KEEPFILTERS ( fEntrega[InFull] = 1 ) )')
m(L, 'OTIF %', PCT, 'DIVIDE ( [Entregas OTIF], [Entregas] )', 'NoPrazo = 1 e InFull = 1 / entregas.')
m(L, 'Entregas No Prazo', INT, 'CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[NoPrazo] = 1 ) )')
m(L, 'No Prazo %', PCT, 'DIVIDE ( [Entregas No Prazo], [Entregas] )')
m(L, 'Entregas In Full', INT, 'CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[InFull] = 1 ) )')
m(L, 'In Full %', PCT, 'DIVIDE ( [Entregas In Full], [Entregas] )')
m(L, 'Entregas com Ocorrência', INT, 'CALCULATE ( [Entregas], KEEPFILTERS ( fEntrega[StatusEntrega] = "Ocorrência" ) )', 'StatusEntrega independe de OTIF (M1).')
m(L, 'Ocorrência %', PCT, 'DIVIDE ( [Entregas com Ocorrência], [Entregas] )')
m(L, 'Custo Frete', MOEDA, 'SUM ( fEntrega[CustoFrete] )')
m(L, 'Frete por Entrega', MOEDA, 'DIVIDE ( [Custo Frete], [Entregas] )')
m(L, 'Frete % Receita', PCT2, 'DIVIDE ( [Custo Frete], [Receita Líquida] )', 'Frete datado por entrega e receita por faturamento (defasagem curta).')
m(L, 'Atraso Médio (dias)', DEC1, 'CALCULATE ( AVERAGE ( fEntrega[DiasAtraso] ), KEEPFILTERS ( fEntrega[NoPrazo] = 0 ) )', 'Media de dias de atraso apenas das entregas fora do prazo.')
m(L, 'Lead Time Médio (dias)', DEC1, 'AVERAGE ( fEntrega[LeadTimePedidoDias] )', 'Pedido ate entrega. Inclui 7 casos negativos da fonte (C6).')
m(L, 'Peso Entregue (kg)', DEC1, 'SUM ( fEntrega[PesoKg] )')

# ---------------- 04 Estoque e WMS
E = '04 Estoque e WMS'
m(E + '\\Estoque', 'Data Último Snapshot Estoque', DATA, 'CALCULATE ( MAX ( fEstoqueMensal[DataReferencia] ), KEEPFILTERS ( fEstoqueMensal[ElegivelHistorico] = 1 ) )')
SNAP = 'VAR _d = [Data Último Snapshot Estoque]\nRETURN\n    '
m(E + '\\Estoque', 'Saldo Estoque Amostra (un)', INT, SNAP + 'CALCULATE ( SUM ( fEstoqueMensal[SaldoUnidades] ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) )',
  'Snapshot do ultimo mes elegivel do contexto. Amostra de 200 SKUs por filial.')
m(E + '\\Estoque', 'Valor Estoque Amostra', MOEDA, SNAP + 'CALCULATE ( SUM ( fEstoqueMensal[ValorEstoque] ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) )')
m(E + '\\Estoque', 'SKU-Filial Amostrados', INT, SNAP + 'CALCULATE ( COUNTROWS ( fEstoqueMensal ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) )')
m(E + '\\Estoque', 'SKUs em Ruptura (amostra)', INT, SNAP + 'CALCULATE ( COUNTROWS ( fEstoqueMensal ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ), KEEPFILTERS ( fEstoqueMensal[Ruptura] = 1 ) )')
m(E + '\\Estoque', 'Ruptura % (amostra)', PCT2, 'DIVIDE ( [SKUs em Ruptura (amostra)], [SKU-Filial Amostrados] )')
m(E + '\\Estoque', 'SKUs Abaixo do Mínimo (amostra)', INT, SNAP + '''COUNTROWS (
        FILTER (
            CALCULATETABLE ( fEstoqueMensal, KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ) ),
            fEstoqueMensal[SaldoUnidades] < fEstoqueMensal[EstoqueMinimo]
        )
    )''', 'Saldo abaixo do estoque minimo (inclui rupturas).')
m(E + '\\Estoque', 'Abaixo do Mínimo % (amostra)', PCT, 'DIVIDE ( [SKUs Abaixo do Mínimo (amostra)], [SKU-Filial Amostrados] )')
m(E + '\\Movimentacao', 'Entradas Estoque (un)', INT, 'CALCULATE ( SUM ( fMovimentoEstoque[QuantidadeAssinada] ), KEEPFILTERS ( fMovimentoEstoque[QuantidadeAssinada] > 0 ), KEEPFILTERS ( fMovimentoEstoque[ElegivelHistorico] = 1 ) )')
m(E + '\\Movimentacao', 'Saídas Estoque (un)', INT, '- CALCULATE ( SUM ( fMovimentoEstoque[QuantidadeAssinada] ), KEEPFILTERS ( fMovimentoEstoque[QuantidadeAssinada] < 0 ), KEEPFILTERS ( fMovimentoEstoque[ElegivelHistorico] = 1 ) )',
  'Saidas, ajustes e transferencias (quantidade assinada negativa), em valor absoluto.')
m(E + '\\Compras', 'Compras', INT, 'CALCULATE ( COUNTROWS ( fCompra ), KEEPFILTERS ( fCompra[ElegivelHistorico] = 1 ) )')
m(E + '\\Compras', 'Valor Compras', MOEDA, 'CALCULATE ( SUM ( fCompra[ValorCompra] ), KEEPFILTERS ( fCompra[ElegivelHistorico] = 1 ) )')
m(E + '\\Compras', 'Compras Atrasadas %', PCT, 'DIVIDE ( CALCULATE ( [Compras], KEEPFILTERS ( fCompra[StatusCompra] = "Atrasado" ) ), [Compras] )')
m(E + '\\WMS', 'Data Último Snapshot WMS', DATA, 'CALCULATE ( MAX ( fOcupacaoArmazem[DataReferencia] ), KEEPFILTERS ( fOcupacaoArmazem[ElegivelHistorico] = 1 ) )')
WSNAP = 'VAR _d = [Data Último Snapshot WMS]\nRETURN\n    '
m(E + '\\WMS', 'Registros WMS (amostra)', INT, WSNAP + 'CALCULATE ( COUNTROWS ( fOcupacaoArmazem ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )',
  'Registros posicao x produto do ultimo snapshot elegivel. Amostra; nao representa a filial (C9).')
m(E + '\\WMS', 'Posições Amostradas', INT, WSNAP + 'CALCULATE ( DISTINCTCOUNT ( fOcupacaoArmazem[PosicaoID] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )')
m(E + '\\WMS', 'Paletes (amostra)', INT, WSNAP + 'CALCULATE ( SUM ( fOcupacaoArmazem[Paletes] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )')
for st in ('Ocupada', 'Bloqueada', 'Disponível'):
    m(E + '\\WMS', 'Registros %s %%' % st, PCT, 'DIVIDE ( CALCULATE ( [Registros WMS (amostra)], KEEPFILTERS ( fOcupacaoArmazem[StatusPosicao] = "%s" ) ), [Registros WMS (amostra)] )' % st)

# ---------------- 05 Financeiro
F = '05 Financeiro'
m(F + '\\Receber', 'Títulos', INT, 'COUNTROWS ( fContasReceber )', 'Data ativa: Vencimento.')
m(F + '\\Receber', 'Valor Títulos', MOEDA, 'SUM ( fContasReceber[ValorTitulo] )')
m(F + '\\Receber', 'Títulos Recebidos', INT, 'CALCULATE ( [Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Recebido" ) )')
m(F + '\\Receber', 'Valor Recebido Confirmado', MOEDA, 'CALCULATE ( SUM ( fContasReceber[ValorPago] ), KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Recebido" ) )',
  'Somente titulos com valor pago > 0 E data de pagamento valida (>= faturamento). Regra D1.')
m(F + '\\Receber', 'Títulos em Aberto', INT, 'CALCULATE ( [Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Em aberto" ) )')
m(F + '\\Receber', 'Valor em Aberto (status atual)', MOEDA, 'CALCULATE ( [Valor Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Em aberto" ) )')
m(F + '\\Receber', 'Prazo Médio Recebimento (dias)', DEC1, '''
CALCULATE (
    AVERAGEX ( fContasReceber, DATEDIFF ( fContasReceber[DataFaturamento], fContasReceber[DataPagamento], DAY ) ),
    KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Recebido" )
)''')
ABERTO = '''
VAR _ref = [Data Referência]
RETURN
    CALCULATE (
        SUM ( fContasReceber[ValorTitulo] ),
        REMOVEFILTERS ( dCalendario ),
        fContasReceber[DataFaturamento] <= _ref,
        fContasReceber[Vencimento] %s _ref,
        FILTER (
            ALL ( fContasReceber[StatusRecebimento], fContasReceber[DataPagamento] ),
            fContasReceber[StatusRecebimento] = "Em aberto"
                || ( fContasReceber[StatusRecebimento] = "Recebido" && fContasReceber[DataPagamento] > _ref )
        )
    )'''
m(F + '\\Receber', 'Saldo Vencido em Aberto (Data Ref.)', MOEDA, ABERTO % '<',
  'As-of: faturado ate a Data Referencia, vencido antes dela e nao pago ate ela. Exclui Inconsistentes.')
m(F + '\\Receber', 'Saldo a Vencer em Aberto (Data Ref.)', MOEDA, ABERTO % '>=')
m(F + '\\Receber', 'Saldo em Aberto (Data Ref.)', MOEDA, '[Saldo Vencido em Aberto (Data Ref.)] + [Saldo a Vencer em Aberto (Data Ref.)]')
m(F + '\\Receber', 'Valor Vencido até Data Ref. (base)', MOEDA, '''
VAR _ref = [Data Referência]
RETURN
    CALCULATE (
        SUM ( fContasReceber[ValorTitulo] ),
        REMOVEFILTERS ( dCalendario ),
        fContasReceber[DataFaturamento] <= _ref,
        fContasReceber[Vencimento] < _ref,
        fContasReceber[StatusRecebimento] <> "Inconsistente"
    )''', 'Denominador da inadimplencia: titulos validos vencidos ate a Data Referencia.')
m(F + '\\Receber', 'Inadimplência % (Data Ref.)', PCT2, 'DIVIDE ( [Saldo Vencido em Aberto (Data Ref.)], [Valor Vencido até Data Ref. (base)] )')
m(F + '\\Pagar', 'Valor Contas a Pagar', MOEDA, 'CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), KEEPFILTERS ( fContasPagar[ElegivelHistorico] = 1 ) )', 'Data ativa: Vencimento. Exclui titulos de compras pos-corte.')
m(F + '\\Pagar', 'Valor Pago (CP)', MOEDA, 'CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), KEEPFILTERS ( fContasPagar[ElegivelHistorico] = 1 ), KEEPFILTERS ( NOT ISBLANK ( fContasPagar[DataPagamento] ) ) )')
m(F + '\\Pagar', 'Valor em Aberto (CP)', MOEDA, 'CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), KEEPFILTERS ( fContasPagar[ElegivelHistorico] = 1 ), KEEPFILTERS ( ISBLANK ( fContasPagar[DataPagamento] ) ) )')

# ---------------- 06 Planejamento
P = '06 Planejamento'
m(P, 'Meta Faturamento', MOEDA, 'CALCULATE ( SUM ( fMeta[ValorMeta] ), KEEPFILTERS ( fMeta[Indicador] = "Faturamento" ) )')
m(P, 'Meta Faturamento (até corte)', MOEDA, '''
VAR _corte = [Data Corte]
RETURN
    CALCULATE ( [Meta Faturamento], KEEPFILTERS ( dCalendario[Data] <= _corte ) )''', 'Meta restrita a meses com realizado, para comparacao.')
m(P, 'Atingimento Meta Faturamento %', PCT, 'DIVIDE ( [Receita Líquida], [Meta Faturamento (até corte)] )')
m(P, 'Gap Meta Faturamento', MOEDA, 'IF ( NOT ISBLANK ( [Meta Faturamento (até corte)] ), [Receita Líquida] - [Meta Faturamento (até corte)] )')
m(P, 'Meta Margem Bruta % (ponderada)', PCT2, '''
VAR _grao = SUMMARIZE ( fMeta, fMeta[DataReferencia], fMeta[FilialID] )
VAR _num =
    SUMX (
        _grao,
        CALCULATE ( SUM ( fMeta[ValorMeta] ), fMeta[Indicador] = "Faturamento" )
            * CALCULATE ( SUM ( fMeta[ValorMeta] ), fMeta[Indicador] = "Margem Bruta" )
    )
VAR _den = SUMX ( _grao, CALCULATE ( SUM ( fMeta[ValorMeta] ), fMeta[Indicador] = "Faturamento" ) )
RETURN
    DIVIDE ( _num, _den )''', 'Meta de margem (razao) ponderada pela meta de faturamento de cada filial-mes (C8).')
m(P, 'Desvio Margem vs Meta (p.p.)', PP, '''
VAR _corte = [Data Corte]
VAR _meta = CALCULATE ( [Meta Margem Bruta % (ponderada)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
RETURN
    IF ( NOT ISBLANK ( _meta ) && NOT ISBLANK ( [Margem Bruta %] ), ( [Margem Bruta %] - _meta ) * 100 )''')
m(P, 'Meta OTIF % (média simples)', PCT, 'CALCULATE ( AVERAGE ( fMeta[ValorMeta] ), KEEPFILTERS ( fMeta[Indicador] = "OTIF" ) )',
  'Media simples das metas filial-mes; nao ponderada (sem base de ponderacao definida na fonte).')
m(P, 'Orçamento Receita', MOEDA, 'CALCULATE ( SUM ( fOrcamento[ValorOrcado] ), KEEPFILTERS ( fOrcamento[Conta] = "Receita" ) )', 'Identico a Meta Faturamento em 100% das linhas (M8).')
m(P, 'Orçamento Despesa Operacional', MOEDA, 'CALCULATE ( SUM ( fOrcamento[ValorOrcado] ), KEEPFILTERS ( fOrcamento[Conta] = "Despesa Operacional" ) )')
m(P, 'Desvio Despesa vs Orçamento', MOEDA, '''
VAR _corte = [Data Corte]
VAR _orc = CALCULATE ( [Orçamento Despesa Operacional], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
RETURN
    IF ( NOT ISBLANK ( _orc ), [Despesas Operacionais] - _orc )''')
m(P, 'Receita Prevista', MOEDA, 'SUM ( fPrevisao[ReceitaPrevista] )', 'Projecao sintetica (jan-jun/2027). Nunca somar ao realizado.')
m(P, 'Margem Erro Estimada (média)', PCT, 'AVERAGE ( fPrevisao[MargemErroEstimada] )', 'Semantica da fonte pendente de validacao; nao usar como intervalo de confianca.')

# ---------------- 07 Tempo
TT = '07 Tempo'
m(TT, 'Receita LY', MOEDA, '''
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Receita Líquida], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )''', 'Mesmo periodo do ano anterior, limitado as datas <= Data Corte (comparacao justa).')
m(TT, 'Receita (até corte)', MOEDA, '''
VAR _corte = [Data Corte]
RETURN
    CALCULATE ( [Receita Líquida], KEEPFILTERS ( dCalendario[Data] <= _corte ) )''')
m(TT, 'Receita YoY %', PCT, 'DIVIDE ( [Receita (até corte)] - [Receita LY], [Receita LY] )')
m(TT, 'Receita YoY Δ', MOEDA, 'IF ( NOT ISBLANK ( [Receita LY] ), [Receita (até corte)] - [Receita LY] )')
m(TT, 'Receita Mês Anterior', MOEDA, 'CALCULATE ( [Receita Líquida], DATEADD ( dCalendario[Data], -1, MONTH ) )')
m(TT, 'Receita MoM %', PCT, 'DIVIDE ( [Receita Líquida] - [Receita Mês Anterior], [Receita Mês Anterior] )')
m(TT, 'Receita YTD', MOEDA, '''
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Receita Líquida], DATESYTD ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )''')
m(TT, 'Receita YTD LY', MOEDA, '''
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE (
            CALCULATE ( [Receita Líquida], DATESYTD ( dCalendario[Data] ) ),
            SAMEPERIODLASTYEAR ( dCalendario[Data] )
        ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )''')
m(TT, 'Margem Bruta % LY', PCT2, '''
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Margem Bruta %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )''')
m(TT, 'Margem Bruta % YoY (p.p.)', PP, '''
VAR _corte = [Data Corte]
VAR _atual = CALCULATE ( [Margem Bruta %], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _ly = [Margem Bruta % LY]
RETURN
    IF ( NOT ISBLANK ( _ly ) && NOT ISBLANK ( _atual ), ( _atual - _ly ) * 100 )''')

# ---------------- 09 Qualidade \ Recebimento
R = Q + '\\Recebimento'
m(R, 'Títulos Inconsistentes', INT, 'CALCULATE ( [Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Inconsistente" ) )')
m(R, 'Valor Títulos Inconsistentes', MOEDA, 'CALCULATE ( [Valor Títulos], KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Inconsistente" ) )')
m(R, 'Valor Pago Declarado em Inconsistentes', MOEDA, 'CALCULATE ( SUM ( fContasReceber[ValorPago] ), KEEPFILTERS ( fContasReceber[StatusRecebimento] = "Inconsistente" ) )')
m(R, '% Títulos Inconsistentes', PCT2, 'DIVIDE ( [Títulos Inconsistentes], [Títulos] )')
m(R, '% Valor Inconsistente', PCT2, 'DIVIDE ( [Valor Títulos Inconsistentes], [Valor Títulos] )')

# ---------------- 09 Qualidade \ Corte temporal
CT = Q + '\\Corte temporal'
def pos(tab, flagcol='ElegivelHistorico'):
    return 'CALCULATE ( COUNTROWS ( %s ), REMOVEFILTERS ( dCalendario ), %s[%s] = 0 )' % (tab, tab, flagcol)
m(CT, 'Despesas Pós-Corte (qtd)', INT, pos('fDespesa'))
m(CT, 'Despesas Pós-Corte (R$)', MOEDA, 'CALCULATE ( SUM ( fDespesa[Valor] ), REMOVEFILTERS ( dCalendario ), fDespesa[ElegivelHistorico] = 0 )')
m(CT, 'Compras Pós-Corte (qtd)', INT, pos('fCompra'))
m(CT, 'Compras Pós-Corte (R$)', MOEDA, 'CALCULATE ( SUM ( fCompra[ValorCompra] ), REMOVEFILTERS ( dCalendario ), fCompra[ElegivelHistorico] = 0 )')
m(CT, 'Contas a Pagar Pós-Corte (qtd)', INT, pos('fContasPagar'))
m(CT, 'Contas a Pagar Pós-Corte (R$)', MOEDA, 'CALCULATE ( SUM ( fContasPagar[ValorTitulo] ), REMOVEFILTERS ( dCalendario ), fContasPagar[ElegivelHistorico] = 0 )',
  'Titulos de compras pos-corte (mesmo valor das compras; nao somar com Compras Pos-Corte).')
m(CT, 'Estoque Pós-Corte (qtd)', INT, pos('fEstoqueMensal'), 'Snapshots; valor nao e somavel entre meses, por isso so contagem.')
m(CT, 'Movimentos Pós-Corte (qtd)', INT, pos('fMovimentoEstoque'))
m(CT, 'Ocupação WMS Pós-Corte (qtd)', INT, pos('fOcupacaoArmazem'))
m(CT, 'Registros Pós-Corte (total)', INT, '''
[Despesas Pós-Corte (qtd)] + [Compras Pós-Corte (qtd)] + [Contas a Pagar Pós-Corte (qtd)]
    + [Estoque Pós-Corte (qtd)] + [Movimentos Pós-Corte (qtd)] + [Ocupação WMS Pós-Corte (qtd)]''')
m(CT, 'Valor Financeiro Pós-Corte (R$)', MOEDA, '[Despesas Pós-Corte (R$)] + [Compras Pós-Corte (R$)]', 'Despesas + compras. Contas a pagar fora para nao duplicar as compras.')
m(CT, 'Data Máxima Encontrada', DATA, '''
VAR _d1 = CALCULATE ( MAX ( fDespesa[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
VAR _d2 = CALCULATE ( MAX ( fCompra[DataCompra] ), REMOVEFILTERS ( dCalendario ) )
VAR _d3 = CALCULATE ( MAX ( fEstoqueMensal[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
VAR _d4 = CALCULATE ( MAX ( fMovimentoEstoque[DataMovimento] ), REMOVEFILTERS ( dCalendario ) )
VAR _d5 = CALCULATE ( MAX ( fOcupacaoArmazem[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )
RETURN
    MAXX ( { _d1, _d2, _d3, _d4, _d5 }, [Value] )''', 'Maior data nas fatos realizadas com registros pos-corte (previsao, metas e orcamento fora).')
m(CT, 'Data Máxima Previsão', DATA, 'CALCULATE ( MAX ( fPrevisao[DataReferencia] ), REMOVEFILTERS ( dCalendario ) )')

# ---------------- escrita
lines = ['/// Tabela de medidas do NEXUS 360. Medidas base em 00 Base; derivadas por composicao.', 'table _Medidas',
         T + 'lineageTag: ' + str(uuid.uuid4()), '']
for pasta, nome, fmt, expr, desc in M:
    if desc:
        lines.append(T + '/// ' + desc)
    if '\n' in expr:
        lines.append(T + "measure '%s' =" % nome)
        lines += [T * 3 + l if l.strip() else '' for l in expr.split('\n')]
    else:
        lines.append(T + "measure '%s' = %s" % (nome, expr))
    lines += [T * 2 + 'formatString: ' + fmt, T * 2 + 'displayFolder: ' + pasta, T * 2 + 'lineageTag: ' + str(uuid.uuid4()), '']
lines += [T + 'column Ref', T * 2 + 'dataType: int64', T * 2 + 'isHidden', T * 2 + 'formatString: 0', T * 2 + 'lineageTag: ' + str(uuid.uuid4()),
          T * 2 + 'summarizeBy: none', T * 2 + 'sourceColumn: Ref', '',
          T + 'partition _Medidas = m', T * 2 + 'mode: import', T * 2 + 'queryGroup: Parametros', T * 2 + 'source =',
          T * 4 + 'let', T * 4 + '    Fonte = #table(type table [Ref = Int64.Type], {})', T * 4 + 'in', T * 4 + '    Fonte', '',
          T + 'annotation PBI_ResultType = Table']
os.makedirs(os.path.join(OUT, 'tables'), exist_ok=True)
with open(os.path.join(OUT, 'tables', '_Medidas.tmdl'), 'w', encoding='utf-8', newline='\r\n') as fh:
    fh.write('\n'.join(lines) + '\n')
with open(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'catalogo_medidas.csv'), 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['Pasta', 'Medida', 'Formato', 'Descricao', 'DAX'])
    for pasta, nome, fmt, expr, desc in M:
        w.writerow([pasta, nome, fmt, desc, expr])
print('medidas', len(M))
