# NEXUS 360 - Etapa C: Customer Intelligence (PBIR)
# Pergunta: quem deixou de comprar, quem esta em risco e quem vale a pena recuperar?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, tooltip_page, cat_filter, realizado, COR, DENEB, DCONF, deneb)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG, TT = 'pgCustomer', 'ttCliente'
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}

SL = [('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
      ('nxSlMes', 'dCalendario', 'MesAno', 'Mês (data de referência)', 'Dropdown', False, None, 70, True),
      ('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Dropdown', False, None, 70, False),
      ('nxSlLimAtivo', 'Param Limite Ativo', 'Dias', 'Limite ativo (dias) · padrão 180', 'Dropdown', False, None, 70, False),
      ('nxSlLimChurn', 'Param Limite Churn', 'Dias', 'Limite churn (dias) · padrão 365', 'Dropdown', False, None, 70, False)]

p = Pagina(PG, 'Customer Intelligence')
p.chrome(slicers=SL)

# Painel de status (KPIs verticais)
p.html('nxStatus', 46, 212, 420, 844, 'UX Clientes Status')
p.vis['nxStatus']['visual']['visualContainerObjects'] = dict(CARD)

# Cohort de retencao (Deneb) - historico completo: slicers de periodo nao filtram (Tamanho Cohort vem de dCliente)
COH = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Meses desde 1a Compra'] >= 1 && datum['Meses desde 1a Compra'] <= 12 && isValid(datum['Retenção Cohort %']) && datum['Tamanho Cohort'] > 0"}],
    "mark": {"type": "rect", "cornerRadius": 2, "stroke": "#071528", "strokeWidth": 1},
    "encoding": {
        "x": {"field": "Meses desde 1a Compra", "type": "ordinal", "title": "Meses desde a 1ª compra", "axis": {"labelAngle": 0, "orient": "top"}},
        "y": {"field": "Cohort", "type": "ordinal", "title": None, "sort": "ascending", "axis": {"labelFontSize": 9}},
        "color": {"field": "Retenção Cohort %", "type": "quantitative", "title": "Retenção",
                  "scale": {"range": ["#0A2540", "#0878C9", "#10D4C4"], "domainMin": 0},
                  "legend": {"orient": "right", "direction": "vertical", "format": ".0%", "gradientLength": 160, "title": "Retenção"}},
        "tooltip": [{"field": "Cohort", "title": "Cohort (1ª compra)"}, {"field": "Meses desde 1a Compra", "title": "Mês"},
                    {"field": "Retenção Cohort %", "title": "Retenção", "formatType": "pbiFormat", "format": "0.0%"},
                    {"field": "Tamanho Cohort", "title": "Clientes no cohort", "formatType": "pbiFormat", "format": "#,0"}]}}
deneb(p, 'nxCohort', 482, 212, 900, 384,
      [col('dCliente', 'Cohort'), col('dCohortOffset', 'Meses desde 1a Compra'), meas('Retenção Cohort %'), meas('Tamanho Cohort')],
      COH, 'Retenção por cohort de 1ª compra (histórico completo, meses 1–12)')
p.vis['nxCohort']['filterConfig'] = {'filters': [{'name': 'fOffset', 'field': col('dCohortOffset', 'Meses desde 1a Compra'), 'type': 'Advanced',
    'filter': {'Version': 2, 'From': [{'Name': 'o', 'Entity': 'dCohortOffset', 'Type': 0}],
               'Where': [{'Condition': {'Comparison': {'ComparisonKind': 4, 'Left': {'Column': {'Expression': {'SourceRef': {'Source': 'o'}}, 'Property': 'Meses desde 1a Compra'}},
                                                       'Right': {'Literal': {'Value': '12L'}}}}}]}}]}
for sl in ('nxSlAno', 'nxSlMes'):
    p.interactions.append((sl, 'nxCohort'))

# Prioridade de contato: clientes em risco com maior receita 12M (nativo, tooltip de cliente)
topn = {'name': 'fTopRisco', 'field': col('dCliente', 'RazaoSocial'), 'type': 'TopN',
        'filter': {'Version': 2, 'From': [
            {'Name': 'subquery', 'Expression': {'Subquery': {'Query': {'Version': 2,
                'From': [{'Name': 'c', 'Entity': 'dCliente', 'Type': 0}, {'Name': 'm', 'Entity': '_Medidas', 'Type': 0}],
                'Select': [{'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'RazaoSocial'}, 'Name': 'field'}],
                'OrderBy': [{'Direction': 2, 'Expression': {'Measure': {'Expression': {'SourceRef': {'Source': 'm'}}, 'Property': 'Prioridade Risco (Receita 12M)'}}}],
                'Top': 10}}}, 'Type': 2},
            {'Name': 'c', 'Entity': 'dCliente', 'Type': 0}],
            'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'RazaoSocial'}}],
                                            'Table': {'SourceRef': {'Source': 'subquery'}}}}}]}}
COLS = [(col('dCliente', 'RazaoSocial'), 'Cliente'), (col('dCliente', 'Segmento'), 'Segmento'), (col('dCliente', 'ClassePotencial'), 'Potencial'),
        (meas('Dias sem Compra (Data Ref.)'), 'Dias sem compra'), (meas('Prioridade Risco (Receita 12M)'), 'Receita 12 meses')]
p.add('nxRiscoClientes', 482, 612, 900, 444, {
    'visualType': 'tableEx',
    'query': {'queryState': {'Values': {'projections': [proj(f, d) for f, d in COLS]}},
              'sortDefinition': {'sort': [{'field': meas('Prioridade Risco (Receita 12M)'), 'direction': 'Descending'}]}},
    'objects': {'values': [{'properties': {'fontColor': color(COR['alerta'])}, 'selector': {'metadata': '_Medidas.Dias sem Compra (Data Ref.)'}}],
                'columnHeaders': [{'properties': {'alignment': s('Center'), 'wordWrap': lit('true'), 'fontSize': num(10), 'columnAdjustment': s('growToFit')}}],
                'grid': [{'properties': {'rowPadding': num(4), 'textSize': num(10)}}],
                'total': [{'properties': {'totals': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Prioridade de contato: clientes em risco com maior receita nos últimos 12 meses'), 'visualTooltip': tooltip_page(TT)},
    filters=[topn])

# Frequencia x valor (HTML)
p.html('nxFreqValor', 1398, 212, 476, 300, 'UX Clientes Freq Valor')
p.vis['nxFreqValor']['visual']['visualContainerObjects'] = dict(CARD)

# Evolucao mensal dos status (colunas empilhadas)
CST = {'Novo': '#7FE6DD', 'Ativo': '#45D5A1', 'Reativado': '#5FA8E6', 'Em risco': '#FFC66D', 'Churn': '#FF7285'}
dp = [{'properties': {'fill': color(c)}, 'selector': {'data': [{'scopeId': {'Comparison': {'ComparisonKind': 0, 'Left': col('dStatusCliente', 'Status'),
                                                                                          'Right': {'Literal': {'Value': "'%s'" % k}}}}}]}} for k, c in CST.items()]
p.add('nxEvolStatus', 1398, 528, 476, 260, {
    'visualType': 'columnChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('dCalendario', 'MesAno'), 'Mês', active=True)]},
                             'Series': {'projections': [proj(col('dStatusCliente', 'Status'), 'Status')]},
                             'Y': {'projections': [proj(meas('Clientes por Status'), 'Clientes')]}},
              'sortDefinition': {'sort': [{'field': col('dCalendario', 'MesAno'), 'direction': 'Ascending'}]}},
    'objects': {'dataPoint': dp, 'legend': [{'properties': {'show': lit('true'), 'position': s('Top'), 'fontSize': num(9)}}],
                'valueAxis': [{'properties': {'show': lit('true'), 'labelDisplayUnits': num(1000), 'gridlineShow': lit('true')}}],
                'categoryAxis': [{'properties': {'fontSize': num(9)}}], 'labels': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Status dos clientes no fim de cada mês')}, filters=[realizado()])

# Churn conforme a janela
p.add('nxJanelas', 1398, 804, 476, 252, {
    'visualType': 'clusteredColumnChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('Param Janela Comparativa', 'Janela (dias)'), 'Janela (dias)', active=True)]},
                             'Y': {'projections': [proj(meas('Taxa de Churn (Janela Comparativa) %'), 'Churn')]}},
              'sortDefinition': {'sort': [{'field': col('Param Janela Comparativa', 'Janela (dias)'), 'direction': 'Ascending'}]}},
    'objects': {'dataPoint': [{'properties': {'fill': {'solid': {'color': {'expr': meas('UX Cor Janela Churn')}}}},
                               'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}]}}],
                'labels': [{'properties': {'show': lit('true'), 'labelPrecision': lit('1L'), 'color': color('#FFFFFF'), 'fontSize': num(9)}}],
                'valueAxis': [{'properties': {'show': lit('false'), 'gridlineShow': lit('false')}}],
                'categoryAxis': [{'properties': {'fontSize': num(9), 'showAxisTitle': lit('true'), 'axisType': s('Categorical')}}],
                'legend': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Churn por limite de dias sem compra')})
p.write(DEF, overwrite=True)

t = Pagina(TT, 'TT Cliente', fundo=None, tipo='Tooltip', w=320, h=200)
t.html('nxTooltipCliente', 0, 0, 320, 200, 'UX Tooltip Cliente')
t.write(DEF, overwrite=True)

register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente'])
print('customer ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
