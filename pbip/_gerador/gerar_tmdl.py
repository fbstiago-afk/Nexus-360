# NEXUS 360 - Gerador do modelo semantico TMDL (fonte: CSV)
# Uso: python3 -I gerar_tmdl.py <pasta_definition_saida> [<pasta_csv>]
# Gera tables/*.tmdl, expressions.tmdl, relationships.tmdl e relacionamentos_gerados.csv
import sys, os, uuid

OUT = sys.argv[1]
PASTA = sys.argv[2] if len(sys.argv) > 2 else 'E:\\Projetos BI\\18 - Nexus 360\\dados\\NEXUS360\\csv\\'
os.makedirs(os.path.join(OUT, 'tables'), exist_ok=True)
T = '\t'


def lt():
    return str(uuid.uuid4())


MONEY = {'CustoReferencia', 'PrecoTabela', 'InvestimentoPrevisto', 'LimiteCredito', 'ValorCompra', 'ValorTitulo', 'ValorPago',
         'Valor', 'ValorDevolvido', 'CustoFrete', 'ValorEstoque', 'ReceitaLiquida', 'Impostos', 'CMV', 'PrecoUnitario',
         'ValorLiquido', 'CustoMercadoria', 'ValorOrcado', 'ReceitaPrevista'}
PCT = {'DescontoPercentual', 'Confiabilidade', 'IndiceServico', 'MargemErroEstimada'}

# Esquema real dos CSV (ordem original). i=int, d=data, s=texto, n=numero (decimal se monetario, senao double)
SCH = {
    'dCalendario': 'Data:d Ano:i Mes:i NomeMes:s Trimestre:i DiaSemana:i DiaUtil:i SemanaISO:i',
    'dCampanha': 'CampanhaID:i Campanha:s Inicio:d Fim:d Canal:s InvestimentoPrevisto:n',
    'dCliente': 'ClienteID:i RazaoSocial:s Segmento:s FilialID:i ClassePotencial:s DataCadastro:d LimiteCredito:n CondicaoPagamento:s Inativo:i',
    'dFilial': 'FilialID:i Filial:s Cidade:s UF:s Regiao:s Latitude:n Longitude:n CapacidadePaletes:i',
    'dFornecedor': 'FornecedorID:i Fornecedor:s UF:s LeadTimeMedio:i Confiabilidade:n',
    'dPosicaoArmazem': 'PosicaoID:i FilialID:i EnderecoWMS:s EixoX:i EixoY:i EixoZ:i Zona:s',
    'dProduto': 'ProdutoID:i Produto:s Categoria:s Subcategoria:s Marca:s Unidade:s CustoReferencia:n PrecoTabela:n LeadTimeDias:i Descontinuado:i',
    'dTransportadora': 'TransportadoraID:i Transportadora:s Modal:s IndiceServico:n',
    'dVendedor': 'VendedorID:i Vendedor:s FilialID:i Equipe:s DataAdmissao:d Ativo:i',
    'fCompra': 'CompraID:i FornecedorID:i FilialID:i ProdutoID:i DataCompra:d Quantidade:i ValorCompra:n StatusCompra:s',
    'fContasPagar': 'PagamentoID:i CompraID:i ValorTitulo:n Vencimento:d DataPagamento:d',
    'fContasReceber': 'TituloID:i PedidoID:i ClienteID:i ValorTitulo:n Vencimento:d DataPagamento:d ValorPago:n FormaPagamento:s',
    'fDespesa': 'DespesaID:i DataReferencia:d FilialID:i Conta:s Tipo:s Valor:n',
    'fDevolucao': 'DevolucaoID:i PedidoID:i DataDevolucao:d ValorDevolvido:n Motivo:s',
    'fEntrega': 'EntregaID:i PedidoID:i TransportadoraID:i DataPrometida:d DataEntrega:d PesoKg:n CustoFrete:n NoPrazo:i InFull:i StatusEntrega:s',
    'fEstoqueMensal': 'EstoqueID:i DataReferencia:d FilialID:i ProdutoID:i SaldoUnidades:i EstoqueMinimo:i ValorEstoque:n Ruptura:i DiasSemMovimento:i',
    'fFaturamento': 'FaturaID:i PedidoID:i DataFaturamento:d ReceitaLiquida:n Impostos:n CMV:n',
    'fInteracaoCampanha': 'InteracaoID:i CampanhaID:i ClienteID:i DataInteracao:d TipoInteracao:s',
    'fItemPedido': 'ItemPedidoID:i PedidoID:i ProdutoID:i Quantidade:i PrecoUnitario:n ValorLiquido:n CustoMercadoria:n Tributacao:s',
    'fMeta': 'MetaID:i DataReferencia:d FilialID:i Indicador:s ValorMeta:n',
    'fMovimentoEstoque': 'MovimentoID:i DataMovimento:d FilialID:i ProdutoID:i TipoMovimento:s QuantidadeAssinada:i Origem:s',
    'fOcupacaoArmazem': 'OcupacaoID:i DataReferencia:d PosicaoID:i ProdutoID:i Paletes:i StatusPosicao:s',
    'fOrcamento': 'OrcamentoID:i DataReferencia:d FilialID:i Conta:s ValorOrcado:n',
    'fPedido': 'PedidoID:i ClienteID:i FilialID:i VendedorID:i DataPedido:d StatusPedido:s DescontoPercentual:n CampanhaID:i Canal:s',
    'fPrevisao': 'PrevisaoID:i DataReferencia:d FilialID:i ReceitaPrevista:n MargemErroEstimada:n',
    'fVisitaComercial': 'VisitaID:i VendedorID:i ClienteID:i DataVisita:d TipoContato:s Resultado:s',
}


def parse(s):
    return [tuple(x.split(':')) for x in s.split()]


def mtype(c, k):
    if k == 'i':
        return 'Int64.Type'
    if k == 'd':
        return 'type date'
    if k == 's':
        return 'type text'
    return 'Currency.Type' if c in MONEY else 'type number'


def typestep(cols, src):
    pairs = ', '.join('{"%s", %s}' % (c, mtype(c, k)) for c, k in cols)
    return 'Table.TransformColumnTypes(%s, {%s}, "en-US")' % (src, pairs)


# Colunas derivadas (nome, tipo, descricao)
DER = {
    'fItemPedido': [('ClienteID', 'i', 'Materializado de fPedido (1:1 por PedidoID)'), ('FilialID', 'i', 'Filial transacional do pedido'),
                    ('VendedorID', 'i', 'Materializado de fPedido'), ('CampanhaID', 'i', 'Materializado de fPedido; atribuicao de campanha nao confiavel (C7)'),
                    ('DataPedido', 'd', 'Data do pedido (data ativa desta fato)'), ('StatusPedido', 's', 'Status do pedido'), ('Canal', 's', 'Canal do pedido')],
    'fFaturamento': [('ClienteID', 'i', 'Materializado de fPedido'), ('FilialID', 'i', 'Filial transacional do pedido'),
                     ('VendedorID', 'i', 'Materializado de fPedido'), ('CampanhaID', 'i', 'Materializado de fPedido (C7)'),
                     ('DataPedido', 'd', 'Data do pedido (relacao inativa)'), ('DescontoPercentual', 'n', 'Desconto do pedido, atributo (M3)'),
                     ('Canal', 's', 'Canal do pedido')],
    'fEntrega': [('ClienteID', 'i', 'Materializado de fPedido'), ('FilialID', 'i', 'Filial transacional do pedido'),
                 ('VendedorID', 'i', 'Materializado de fPedido'), ('DataPedido', 'd', 'Data do pedido'),
                 ('DiasAtraso', 'i', 'DataEntrega - DataPrometida em dias'),
                 ('LeadTimePedidoDias', 'i', 'DataEntrega - DataPedido em dias (faturamento nao usado como base, C6)'),
                 ('EntregaOTIF', 'i', '1 quando NoPrazo = 1 e InFull = 1')],
    'fDevolucao': [('ClienteID', 'i', 'Materializado de fPedido'), ('FilialID', 'i', 'Filial transacional do pedido'),
                   ('VendedorID', 'i', 'Materializado de fPedido')],
    'fContasReceber': [('FilialID', 'i', 'Materializado de fPedido'), ('VendedorID', 'i', 'Materializado de fPedido'),
                       ('DataFaturamento', 'd', 'Data da fatura do pedido (relacao inativa)'),
                       ('StatusRecebimento', 's', 'Recebido | Em aberto | Inconsistente (regra D1)'),
                       ('MotivoInconsistencia', 's', 'Motivo quando StatusRecebimento = Inconsistente')],
    'fContasPagar': [('FilialID', 'i', 'Materializado de fCompra'), ('FornecedorID', 'i', 'Materializado de fCompra'),
                     ('ProdutoID', 'i', 'Materializado de fCompra'), ('DataCompra', 'd', 'Data da compra de origem'),
                     ('ElegivelHistorico', 'i', '1 quando DataCompra <= pDataCorte')],
    'fCompra': [('ElegivelHistorico', 'i', '1 quando DataCompra <= pDataCorte')],
    'fDespesa': [('ElegivelHistorico', 'i', '1 quando DataReferencia <= pDataCorte')],
    'fEstoqueMensal': [('ElegivelHistorico', 'i', '1 quando DataReferencia <= pDataCorte')],
    'fMovimentoEstoque': [('ElegivelHistorico', 'i', '1 quando DataMovimento <= pDataCorte')],
    'fOcupacaoArmazem': [('FilialID', 'i', 'Materializado de dPosicaoArmazem'), ('ElegivelHistorico', 'i', '1 quando DataReferencia <= pDataCorte')],
    'fVisitaComercial': [('FilialID', 'i', 'Filial cadastral do cliente (= filial transacional em 100% dos pedidos)')],
    'fInteracaoCampanha': [('FilialID', 'i', 'Filial cadastral do cliente')],
    'dCalendario': [('OrigemLinha', 's', 'Fonte ou Extensao PQ'), ('NomeMesPT', 's', 'Nome do mes em portugues'), ('MesAbrev', 's', 'jan..dez'),
                    ('AnoMes', 'i', 'AAAAMM'), ('MesAno', 's', 'jan/2026'), ('InicioMes', 'd', 'Primeiro dia do mes'),
                    ('TrimestreNome', 's', 'T1..T4'), ('DiaSemanaNome', 's', 'Segunda..Domingo'), ('DiaSemanaAbrev', 's', 'Seg..Dom'),
                    ('SemanaDoMes', 'i', 'Semana do mes, segunda a domingo'), ('FlagRealizado', 'i', '1 quando Data <= pDataCorte')],
}


def dkind(t, names):
    D = {c: k for c, k, _ in DER.get(t, [])}
    return [(c, D[c]) for c in names]


def join(src, stg, key, names, t):
    lst = ', '.join('"%s"' % c for c in names)
    return ['Mesclado = Table.NestedJoin(%s, {"%s"}, %s, {"%s"}, "Ref", JoinKind.LeftOuter)' % (src, key, stg, key),
            'Expandido = Table.ExpandTableColumn(Mesclado, "Ref", {%s}, {%s})' % (lst, lst),
            'Retipado = ' + typestep(dkind(t, names), 'Expandido')]


def elig(col):
    return 'Table.AddColumn(Tipado, "ElegivelHistorico", each if [%s] <= pDataCorte then 1 else 0, Int64.Type)' % col


CAL_STEPS = [
    'UltimaFonte = List.Max(Tipado[Data])',
    'FimNecessario = List.Max({UltimaFonte, Date.EndOfMonth(List.Max(stgPrevisaoDatas))})',
    'NovasDatas = if FimNecessario > UltimaFonte then List.Dates(Date.AddDays(UltimaFonte, 1), Duration.Days(FimNecessario - UltimaFonte), #duration(1, 0, 0, 0)) else {}',
    'Extensao = Table.FromRecords(List.Transform(NovasDatas, (d) => let dw = Date.DayOfWeek(d, Day.Monday) + 1 in [Data = d, Ano = Date.Year(d), Mes = Date.Month(d), NomeMes = Date.ToText(d, "MMMM", "en-US"), Trimestre = Date.QuarterOfYear(d), DiaSemana = dw, DiaUtil = if dw <= 5 then 1 else 0, SemanaISO = Number.RoundDown((Date.DayOfYear(d) - dw + 10) / 7)]), type table [Data = date, Ano = Int64.Type, Mes = Int64.Type, NomeMes = text, Trimestre = Int64.Type, DiaSemana = Int64.Type, DiaUtil = Int64.Type, SemanaISO = Int64.Type])',
    'Origem = Table.AddColumn(Tipado, "OrigemLinha", each "Fonte", type text)',
    'OrigemExt = Table.AddColumn(Extensao, "OrigemLinha", each "Extensao PQ", type text)',
    'Unido = Table.Combine({Origem, OrigemExt})',
    'MesesPT = {"janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"}',
    'DiasPT = {"Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"}',
    'C1 = Table.AddColumn(Unido, "NomeMesPT", each MesesPT{[Mes] - 1}, type text)',
    'C2 = Table.AddColumn(C1, "MesAbrev", each Text.Start(MesesPT{[Mes] - 1}, 3), type text)',
    'C3 = Table.AddColumn(C2, "AnoMes", each [Ano] * 100 + [Mes], Int64.Type)',
    'C4 = Table.AddColumn(C3, "MesAno", each [MesAbrev] & "/" & Text.From([Ano]), type text)',
    'C5 = Table.AddColumn(C4, "InicioMes", each Date.StartOfMonth([Data]), type date)',
    'C6 = Table.AddColumn(C5, "TrimestreNome", each "T" & Text.From([Trimestre]), type text)',
    'C7 = Table.AddColumn(C6, "DiaSemanaNome", each DiasPT{[DiaSemana] - 1}, type text)',
    'C8 = Table.AddColumn(C7, "DiaSemanaAbrev", each Text.Start(DiasPT{[DiaSemana] - 1}, 3), type text)',
    'C9 = Table.AddColumn(C8, "SemanaDoMes", each Number.RoundDown((Date.Day([Data]) - 1 + Date.DayOfWeek(Date.StartOfMonth([Data]), Day.Monday)) / 7) + 1, Int64.Type)',
    'C10 = Table.AddColumn(C9, "FlagRealizado", each if [Data] <= pDataCorte then 1 else 0, Int64.Type)',
]


def mcode(t):
    cols = parse(SCH[t])
    st = ['Fonte = fxLerCsv("%s")' % t, 'Tipado = ' + typestep(cols, 'Fonte')]
    last = 'Tipado'
    if t in ('fItemPedido', 'fFaturamento', 'fEntrega', 'fDevolucao'):
        names = [c for c, _, _ in DER[t] if c not in ('DiasAtraso', 'LeadTimePedidoDias', 'EntregaOTIF')]
        st += join('Tipado', 'stgPedido', 'PedidoID', names, t)
        last = 'Retipado'
        if t == 'fEntrega':
            st += ['Atraso = Table.AddColumn(Retipado, "DiasAtraso", each Duration.Days([DataEntrega] - [DataPrometida]), Int64.Type)',
                   'LeadTime = Table.AddColumn(Atraso, "LeadTimePedidoDias", each Duration.Days([DataEntrega] - [DataPedido]), Int64.Type)',
                   'OTIF = Table.AddColumn(LeadTime, "EntregaOTIF", each if [NoPrazo] = 1 and [InFull] = 1 then 1 else 0, Int64.Type)']
            last = 'OTIF'
    elif t == 'fContasReceber':
        st += ['MescladoP = Table.NestedJoin(Tipado, {"PedidoID"}, stgPedido, {"PedidoID"}, "P", JoinKind.LeftOuter)',
               'ExpandidoP = Table.ExpandTableColumn(MescladoP, "P", {"FilialID", "VendedorID"}, {"FilialID", "VendedorID"})',
               'MescladoF = Table.NestedJoin(ExpandidoP, {"PedidoID"}, stgFaturaData, {"PedidoID"}, "F", JoinKind.LeftOuter)',
               'ExpandidoF = Table.ExpandTableColumn(MescladoF, "F", {"DataFaturamento"}, {"DataFaturamento"})',
               'Retipado = Table.TransformColumnTypes(ExpandidoF, {{"FilialID", Int64.Type}, {"VendedorID", Int64.Type}, {"DataFaturamento", type date}})',
               'Status = Table.AddColumn(Retipado, "StatusRecebimento", each if [ValorPago] > 0 and [DataPagamento] <> null and [DataPagamento] >= [DataFaturamento] then "Recebido" else if [ValorPago] = 0 and [DataPagamento] = null then "Em aberto" else "Inconsistente", type text)',
               'Motivo = Table.AddColumn(Status, "MotivoInconsistencia", each if [StatusRecebimento] <> "Inconsistente" then null else if [ValorPago] = 0 then "Data de pagamento sem valor pago" else if [DataPagamento] = null then "Valor pago sem data de pagamento" else "Pagamento anterior ao faturamento", type text)']
        last = 'Motivo'
    elif t == 'fContasPagar':
        st += join('Tipado', 'stgCompra', 'CompraID', ['FilialID', 'FornecedorID', 'ProdutoID', 'DataCompra'], t)
        st += ['Elegivel = Table.AddColumn(Retipado, "ElegivelHistorico", each if [DataCompra] <= pDataCorte then 1 else 0, Int64.Type)']
        last = 'Elegivel'
    elif t == 'fOcupacaoArmazem':
        st += join('Tipado', 'stgPosicao', 'PosicaoID', ['FilialID'], t)
        st += ['Elegivel = Table.AddColumn(Retipado, "ElegivelHistorico", each if [DataReferencia] <= pDataCorte then 1 else 0, Int64.Type)']
        last = 'Elegivel'
    elif t in ('fVisitaComercial', 'fInteracaoCampanha'):
        st += join('Tipado', 'stgClienteFilial', 'ClienteID', ['FilialID'], t)
        last = 'Retipado'
    elif t in ('fCompra', 'fDespesa', 'fEstoqueMensal', 'fMovimentoEstoque'):
        dc = {'fCompra': 'DataCompra', 'fDespesa': 'DataReferencia', 'fEstoqueMensal': 'DataReferencia', 'fMovimentoEstoque': 'DataMovimento'}[t]
        st += ['Elegivel = ' + elig(dc)]
        last = 'Elegivel'
    elif t == 'dCalendario':
        st += CAL_STEPS
        last = 'C10'
    return st, last


def mblock(steps, last, ind):
    lines = ['let'] + ['    ' + s + (',' if i < len(steps) - 1 else '') for i, s in enumerate(steps)] + ['in', '    ' + last]
    return '\n'.join(ind + l for l in lines)


SORTBY = {'NomeMesPT': 'Mes', 'MesAbrev': 'Mes', 'MesAno': 'AnoMes', 'DiaSemanaNome': 'DiaSemana', 'DiaSemanaAbrev': 'DiaSemana', 'TrimestreNome': 'Trimestre'}
NOFMT_INT = {'Ano', 'Mes', 'AnoMes', 'Trimestre', 'DiaSemana', 'SemanaISO', 'SemanaDoMes', 'EixoX', 'EixoY', 'EixoZ', 'DiaUtil',
             'Inativo', 'Ativo', 'Descontinuado', 'NoPrazo', 'InFull', 'Ruptura', 'ElegivelHistorico', 'FlagRealizado', 'EntregaOTIF'}
SUM_INT = {'Quantidade', 'SaldoUnidades', 'Paletes', 'QuantidadeAssinada'}
DESC_TABLE = {
    'dCalendario': 'Calendario: fonte (2024-01-01 a 2027-04-30) + extensao deterministica no PQ ate o fim do mes da ultima previsao (C3).',
    'dCliente': 'Clientes. FilialID e atributo cadastral sem relacao. PrimeiraCompra = 1a fatura (C6).',
    'dVendedor': 'Vendedores. FilialID = filial de lotacao, sem relacao (M2).',
    'dPosicaoArmazem': 'Grade WMS 10x10x4 por filial. FilialID e atributo; a filial chega a fOcupacaoArmazem materializada.',
    'fContasReceber': '1 titulo por pedido faturado. StatusRecebimento aplica a regra D1.',
    'fOcupacaoArmazem': 'Amostra WMS (35 posicoes por filial/mes). Grao posicao x produto x mes (C9).',
    'fEstoqueMensal': 'Amostra de 200 SKUs por filial/mes. Snapshot: nao somar meses.',
    'fMeta': 'Metas filial-mes-indicador. Margem Bruta e OTIF sao razoes (C8).',
    'fPrevisao': 'Previsao sintetica jan-jun/2027. Nao e realizado.',
}


def own_key(t):
    return {'fItemPedido': 'ItemPedidoID', 'fFaturamento': 'FaturaID', 'fEntrega': 'EntregaID', 'fContasReceber': 'TituloID',
            'fContasPagar': 'PagamentoID', 'fCompra': 'CompraID', 'fDespesa': 'DespesaID', 'fDevolucao': 'DevolucaoID',
            'fEstoqueMensal': 'EstoqueID', 'fInteracaoCampanha': 'InteracaoID', 'fMeta': 'MetaID', 'fMovimentoEstoque': 'MovimentoID',
            'fOcupacaoArmazem': 'OcupacaoID', 'fOrcamento': 'OrcamentoID', 'fPedido': 'PedidoID', 'fPrevisao': 'PrevisaoID',
            'fVisitaComercial': 'VisitaID'}.get(t)


def write_table(t):
    cols = parse(SCH[t]) + [(c, k) for c, k, _ in DER.get(t, [])]
    ddesc = {c: d for c, _, d in DER.get(t, [])}
    out = []
    if t in DESC_TABLE:
        out.append('/// ' + DESC_TABLE[t])
    out.append('table ' + t)
    if t == 'dCalendario':
        out.append(T + 'dataCategory: Time')
    out += [T + 'lineageTag: ' + lt(), '']
    isfact = t.startswith('f')
    for c, k in cols:
        if c in ddesc:
            out.append(T + '/// ' + ddesc[c])
        out.append(T + 'column ' + c)
        if t == 'dCalendario' and c == 'Data':
            out.append(T * 2 + 'isKey')
        dt = {'i': 'int64', 'd': 'dateTime', 's': 'string'}.get(k) or ('decimal' if c in MONEY else 'double')
        out.append(T * 2 + 'dataType: ' + dt)
        if k == 'd':
            out.append(T * 2 + 'formatString: dd/MM/yyyy')
        elif dt == 'decimal':
            out.append(T * 2 + 'formatString: R$ #,0.00;-R$ #,0.00;R$ #,0.00')
        elif c in PCT:
            out.append(T * 2 + 'formatString: 0.0%;-0.0%;0.0%')
        elif dt == 'int64' and (c.endswith('ID') or c in NOFMT_INT):
            out.append(T * 2 + 'formatString: 0')
        elif dt == 'int64':
            out.append(T * 2 + 'formatString: #,0')
        if c == 'Latitude':
            out.append(T * 2 + 'dataCategory: Latitude')
        if c == 'Longitude':
            out.append(T * 2 + 'dataCategory: Longitude')
        hide = (isfact and c.endswith('ID') and c != own_key(t)) or (c == 'FilialID' and t in ('dCliente', 'dVendedor', 'dPosicaoArmazem'))
        if hide:
            out.append(T * 2 + 'isHidden')
        out.append(T * 2 + 'lineageTag: ' + lt())
        summ = 'sum' if isfact and (dt == 'decimal' or c in SUM_INT) else 'none'
        out.append(T * 2 + 'summarizeBy: ' + summ)
        out.append(T * 2 + 'sourceColumn: ' + c)
        if c in SORTBY:
            out.append(T * 2 + 'sortByColumn: ' + SORTBY[c])
        if k == 'd':
            out += ['', T * 2 + 'annotation UnderlyingDateTimeDataType = Date']
        out.append('')
    if t == 'dCliente':
        out += [T + '/// Data da primeira fatura do cliente (base de Clientes Novos; DataCadastro e invalida - C6)',
                T + 'column PrimeiraCompra = CALCULATE ( MIN ( fFaturamento[DataFaturamento] ) )',
                T * 2 + 'dataType: dateTime', T * 2 + 'formatString: dd/MM/yyyy', T * 2 + 'lineageTag: ' + lt(),
                T * 2 + 'summarizeBy: none', '', T * 2 + 'annotation UnderlyingDateTimeDataType = Date', '']
    steps, last = mcode(t)
    grp = 'Dimensoes' if t.startswith('d') else 'Fatos'
    out += [T + 'partition %s = m' % t, T * 2 + 'mode: import', T * 2 + 'queryGroup: ' + grp, T * 2 + 'source =',
            mblock(steps, last, T * 4), '', T + 'annotation PBI_ResultType = Table']
    with open(os.path.join(OUT, 'tables', t + '.tmdl'), 'w', encoding='utf-8', newline='\r\n') as fh:
        fh.write('\n'.join(out) + '\n')


for t in SCH:
    write_table(t)

# Tabela de parametros (fonte unica para o DAX)
P = ['/// Parametros de negocio expostos ao DAX (fonte unica: parametros M pDataCorte e pJanelaChurnDias).', 'table _Parametros',
     T + 'isHidden', T + 'lineageTag: ' + lt(), '',
     T + 'column DataCorte', T * 2 + 'dataType: dateTime', T * 2 + 'formatString: dd/MM/yyyy', T * 2 + 'lineageTag: ' + lt(),
     T * 2 + 'summarizeBy: none', T * 2 + 'sourceColumn: DataCorte', '', T * 2 + 'annotation UnderlyingDateTimeDataType = Date', '',
     T + 'column JanelaChurnDias', T * 2 + 'dataType: int64', T * 2 + 'formatString: 0', T * 2 + 'lineageTag: ' + lt(),
     T * 2 + 'summarizeBy: none', T * 2 + 'sourceColumn: JanelaChurnDias', '',
     T + 'partition _Parametros = m', T * 2 + 'mode: import', T * 2 + 'queryGroup: Parametros', T * 2 + 'source =',
     T * 4 + 'let', T * 4 + '    Fonte = #table(type table [DataCorte = date, JanelaChurnDias = Int64.Type], {{pDataCorte, pJanelaChurnDias}})',
     T * 4 + 'in', T * 4 + '    Fonte', '', T + 'annotation PBI_ResultType = Table']
with open(os.path.join(OUT, 'tables', '_Parametros.tmdl'), 'w', encoding='utf-8', newline='\r\n') as fh:
    fh.write('\n'.join(P) + '\n')


# Expressions: parametros, funcao e staging (nao carregados)
def expr_param(name, value, rtype, ptype):
    return ['expression %s = %s meta [IsParameterQuery=true, Type="%s", IsParameterQueryRequired=true]' % (name, value, ptype),
            T + 'lineageTag: ' + lt(), T + 'queryGroup: Parametros', '', T + 'annotation PBI_ResultType = ' + rtype, '']


def expr_body(name, lines, grp, rtype):
    return ['expression %s =' % name] + [T * 2 + l for l in lines] + [T + 'lineageTag: ' + lt(), T + 'queryGroup: ' + grp, '',
                                                                     T + 'annotation PBI_ResultType = ' + rtype, '']


def stg(name, t, keep):
    cols = [(c, k) for c, k in parse(SCH[t]) if c in keep]
    lst = ', '.join('"%s"' % c for c in keep)
    return expr_body(name, ['let', '    Fonte = fxLerCsv("%s"),' % t, '    Selecionado = Table.SelectColumns(Fonte, {%s}),' % lst,
                            '    Tipado = ' + typestep(cols, 'Selecionado') + ',', '    Buffer = Table.Buffer(Tipado)', 'in', '    Buffer'],
                     'Staging', 'Table')


E = []
E += expr_param('pPastaDados', '"' + PASTA + '"', 'Text', 'Text')
E += expr_param('pDataCorte', '#date(2026, 10, 31)', 'Date', 'Date')
E += expr_param('pJanelaChurnDias', '90', 'Number', 'Number')
E += expr_body('fxLerCsv', ['(nome as text) as table =>', 'let',
                            '    Arquivo = File.Contents(pPastaDados & nome & ".csv"),',
                            '    Csv = Csv.Document(Arquivo, [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),',
                            '    Cabecalho = Table.PromoteHeaders(Csv, [PromoteAllScalars = true]),',
                            '    SemBOM = Table.TransformColumnNames(Cabecalho, each Text.Replace(_, Character.FromNumber(65279), "")),',
                            '    VaziosNulos = Table.ReplaceValue(SemBOM, "", null, Replacer.ReplaceValue, Table.ColumnNames(SemBOM))',
                            'in', '    VaziosNulos'], 'Funcoes', 'Function')
E += stg('stgPedido', 'fPedido', ['PedidoID', 'ClienteID', 'FilialID', 'VendedorID', 'DataPedido', 'StatusPedido', 'DescontoPercentual', 'CampanhaID', 'Canal'])
E += stg('stgFaturaData', 'fFaturamento', ['PedidoID', 'DataFaturamento'])
E += stg('stgCompra', 'fCompra', ['CompraID', 'FornecedorID', 'FilialID', 'ProdutoID', 'DataCompra'])
E += stg('stgPosicao', 'dPosicaoArmazem', ['PosicaoID', 'FilialID'])
E += stg('stgClienteFilial', 'dCliente', ['ClienteID', 'FilialID'])
E += expr_body('stgPrevisaoDatas', ['let', '    Fonte = fxLerCsv("fPrevisao"),',
                                    '    Tipado = Table.TransformColumnTypes(Fonte, {{"DataReferencia", type date}}, "en-US"),',
                                    '    Datas = List.Distinct(Tipado[DataReferencia])', 'in', '    Datas'], 'Staging', 'List')
with open(os.path.join(OUT, 'expressions.tmdl'), 'w', encoding='utf-8', newline='\r\n') as fh:
    fh.write('\n'.join(E) + '\n')

# Relacionamentos: N:1, direcao unica dimensao -> fato
DIM = {'ClienteID': 'dCliente', 'FilialID': 'dFilial', 'VendedorID': 'dVendedor', 'CampanhaID': 'dCampanha', 'ProdutoID': 'dProduto',
       'TransportadoraID': 'dTransportadora', 'FornecedorID': 'dFornecedor', 'PosicaoID': 'dPosicaoArmazem'}
FKS = {
    'fPedido': ['ClienteID', 'FilialID', 'VendedorID', 'CampanhaID'],
    'fItemPedido': ['ProdutoID', 'ClienteID', 'FilialID', 'VendedorID', 'CampanhaID'],
    'fFaturamento': ['ClienteID', 'FilialID', 'VendedorID', 'CampanhaID'],
    'fEntrega': ['TransportadoraID', 'ClienteID', 'FilialID', 'VendedorID'],
    'fContasReceber': ['ClienteID', 'FilialID', 'VendedorID'],
    'fDevolucao': ['ClienteID', 'FilialID', 'VendedorID'],
    'fCompra': ['FornecedorID', 'FilialID', 'ProdutoID'],
    'fContasPagar': ['FornecedorID', 'FilialID', 'ProdutoID'],
    'fDespesa': ['FilialID'], 'fMeta': ['FilialID'], 'fOrcamento': ['FilialID'], 'fPrevisao': ['FilialID'],
    'fEstoqueMensal': ['FilialID', 'ProdutoID'], 'fMovimentoEstoque': ['FilialID', 'ProdutoID'],
    'fOcupacaoArmazem': ['PosicaoID', 'ProdutoID', 'FilialID'],
    'fVisitaComercial': ['ClienteID', 'VendedorID', 'FilialID'],
    'fInteracaoCampanha': ['CampanhaID', 'ClienteID', 'FilialID'],
}
DATES = {
    'fPedido': [('DataPedido', 1)], 'fItemPedido': [('DataPedido', 1)],
    'fFaturamento': [('DataFaturamento', 1), ('DataPedido', 0)],
    'fEntrega': [('DataEntrega', 1), ('DataPrometida', 0)],
    'fContasReceber': [('Vencimento', 1), ('DataPagamento', 0), ('DataFaturamento', 0)],
    'fDevolucao': [('DataDevolucao', 1)], 'fCompra': [('DataCompra', 1)],
    'fContasPagar': [('Vencimento', 1), ('DataPagamento', 0)],
    'fDespesa': [('DataReferencia', 1)], 'fMeta': [('DataReferencia', 1)], 'fOrcamento': [('DataReferencia', 1)],
    'fPrevisao': [('DataReferencia', 1)], 'fEstoqueMensal': [('DataReferencia', 1)], 'fMovimentoEstoque': [('DataMovimento', 1)],
    'fOcupacaoArmazem': [('DataReferencia', 1)], 'fVisitaComercial': [('DataVisita', 1)], 'fInteracaoCampanha': [('DataInteracao', 1)],
}
REL = []
for f, ks in FKS.items():
    for k in ks:
        REL.append((f, k, DIM[k], k, True))
for f, ds in DATES.items():
    for c, a in ds:
        REL.append((f, c, 'dCalendario', 'Data', bool(a)))
RL = []
for f, fc, tt, tc, a in REL:
    RL += ['relationship ' + lt()] + ([T + 'isActive: false'] if not a else []) + [T + 'fromColumn: %s.%s' % (f, fc), T + 'toColumn: %s.%s' % (tt, tc), '']
with open(os.path.join(OUT, 'relationships.tmdl'), 'w', encoding='utf-8', newline='\r\n') as fh:
    fh.write('\n'.join(RL) + '\n')
with open(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'relacionamentos_gerados.csv'), 'w', encoding='utf-8') as fh:
    fh.write('Fato,ColunaFato,Dimensao,ColunaDimensao,Ativo,Cardinalidade,Direcao\n')
    for f, fc, tt, tc, a in REL:
        fh.write('%s,%s,%s,%s,%d,N:1,Unica (dimensao->fato)\n' % (f, fc, tt, tc, a))
print('tabelas', len(SCH) + 1, 'relacoes', len(REL), 'ativas', sum(1 for x in REL if x[4]))
