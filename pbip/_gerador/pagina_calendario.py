# NEXUS 360 - Etapa I: Operations Calendar (PBIR)
# Pergunta: quando acontecem campanhas, visitas e entregas, e em que dias a operacao falha?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, tooltip_page, cat_filter, realizado, COR, NOCHROME, deneb)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG, TT = 'pgCalendar', 'ttDia'
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}
SL = [('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Basic', False, None, 300, False),
      ('nxSlCanal', 'dCampanha', 'Canal', 'Canal da campanha', 'Basic', False, None, 110, False),
      ('nxSlEquipe', 'dVendedor', 'Equipe', 'Equipe comercial (visitas)', 'Dropdown', False, None, 70, False)]

p = Pagina(PG, 'Operations Calendar')
# Mes visivel, selecao unica (o calendario mostra um mes por vez); nao sincroniza com as outras paginas
p.slicer('nxSlMes', 46, 212, 300, 104, 'dCalendario', 'MesAno', 'Mês do calendário', mode='Dropdown', default=["'out/2026'"], periodo=True, sync=False)
v = p.vis['nxSlMes']['visual']
v['objects']['selection'] = [{'properties': {'selectAllCheckboxEnabled': lit('false'), 'singleSelect': lit('true'), 'strictSingleSelect': lit('true')}}]
v['objects']['header'] = [{'properties': {'show': lit('true'), 'fontColor': color(COR['claro']), 'textSize': num(10)}}]
v['objects']['items'] = [{'properties': {'fontColor': color('#FFFFFF'), 'background': color(COR['card']), 'textSize': num(13)}}]
v['visualContainerObjects'] = dict(CARD, padding=[{'properties': {k: lit('10D') for k in ('top', 'bottom', 'left', 'right')}}])
p.chrome(slicers=SL)
p.html('nxCalKPIs', 362, 212, 1512, 104, 'UX Calendário KPIs')

# Calendario: matriz nativa (semana do mes x dia da semana), celula SVG
p.add('nxCalendario', 46, 332, 1180, 724, {
    'visualType': 'pivotTable',
    'query': {'queryState': {'Rows': {'projections': [proj(col('dCalendario', 'SemanaDoMes'), 'Semana', active=True)]},
                             'Columns': {'projections': [proj(col('dCalendario', 'DiaSemanaAbrev'), 'Dia', active=True)]},
                             'Values': {'projections': [proj(meas('UX Calendário Dia'), ' ')]}},
              'sortDefinition': {'sort': [{'field': col('dCalendario', 'SemanaDoMes'), 'direction': 'Ascending'}]}},
    'objects': {'grid': [{'properties': {'imageHeight': num(96), 'imageWidth': num(134), 'rowPadding': num(2), 'textSize': num(10),
                                         'gridVertical': lit('false'), 'gridHorizontal': lit('false'), 'outlineColor': color(COR['navy'])}}],
                'columnHeaders': [{'properties': {'alignment': s('Center'), 'fontSize': num(11), 'fontColor': color(COR['claro']),
                                                  'backColor': color(COR['card']), 'columnAdjustment': s('growToFit')}}],
                'rowHeaders': [{'properties': {'fontSize': num(9), 'fontColor': color('#6F86A0'), 'backColor': color(COR['card'])}}],
                'values': [{'properties': {'backColor': color(COR['card']), 'fontColor': color('#FFFFFF')}}],
                'subTotals': [{'properties': {'rowSubtotals': lit('false'), 'columnSubtotals': lit('false')}}],
                'rowTotal': [{'properties': {'show': lit('false')}}], 'columnTotal': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container=dict(CARD, title=title('Calendário operacional: campanhas, visitas e entregas (borda vermelha = OTIF 5 p.p. abaixo da média do mês)'),
                   visualTooltip=tooltip_page(TT)))

# Cronograma de campanhas no periodo (Deneb, recorte no mes)
GT = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Campanha no Período'] == 1"},
                  {"calculate": "toDate(datum['Inicio'])", "as": "ini"}, {"calculate": "toDate(datum['Fim'])", "as": "fim"},
                  {"calculate": "toDate(datum['Período Início'])", "as": "pi"}, {"calculate": "toDate(datum['Período Fim'])", "as": "pf"},
                  {"calculate": "max(datum.ini, datum.pi)", "as": "x0"}, {"calculate": "min(datum.fim, datum.pf) + 86400000", "as": "x1"}],
    "layer": [
        {"mark": {"type": "bar", "cornerRadius": 3, "height": {"band": 0.55}},
         "encoding": {"y": {"field": "Campanha", "type": "nominal", "sort": {"field": "ini"}, "title": None,
                       "axis": {"labelLimit": 150, "labelColor": "#C9D6E3", "labelFontSize": 10}}, "x": {"field": "x0", "type": "temporal", "title": None, "axis": {"format": "%d/%m", "grid": True, "tickCount": 6}},
                      "x2": {"field": "x1"},
                      "color": {"field": "Canal", "type": "nominal", "scale": {"domain": ["Digital", "Equipe Comercial", "Trade"], "range": ["#5FA8E6", "#10D4C4", "#FFC66D"]}},
                      "tooltip": [{"field": "Campanha"}, {"field": "Canal"}, {"field": "ini", "type": "temporal", "title": "Início", "format": "%d/%m/%Y"},
                                  {"field": "fim", "type": "temporal", "title": "Fim", "format": "%d/%m/%Y"},
                                  {"field": "Interações de Campanha", "title": "Interações no período", "formatType": "pbiFormat", "format": "#,0"},
                                  {"field": "Conversões de Campanha", "title": "Conversões no período", "formatType": "pbiFormat", "format": "#,0"}]}},
        {"transform": [{"filter": "isValid(datum['Dia Selecionado'])"}, {"calculate": "time(toDate(datum['Dia Selecionado'])) + 43200000", "as": "ds"}],
         "mark": {"type": "rule", "color": "#FFFFFF", "strokeDash": [3, 3], "strokeWidth": 1.5},
         "encoding": {"x": {"aggregate": "max", "field": "ds", "type": "temporal"}}},
        {"mark": {"type": "text", "align": "left", "dx": 4, "fontSize": 10, "color": "#FFFFFF"},
         "transform": [{"filter": "isValid(datum['Conversões de Campanha'])"}],
         "encoding": {"y": {"field": "Campanha", "type": "nominal", "sort": {"field": "ini"}}, "x": {"field": "x1", "type": "temporal"}, "text": {"field": "Conversões de Campanha", "type": "quantitative", "format": ",.0f"}}}]}
deneb(p, 'nxCampanhas', 1242, 332, 632, 352,
      [col('dCampanha', 'Campanha'), col('dCampanha', 'Inicio'), col('dCampanha', 'Fim'), col('dCampanha', 'Canal'),
       meas('Campanha no Período'), meas('Período Início'), meas('Período Fim'), meas('Dia Selecionado'), meas('Interações de Campanha'), meas('Conversões de Campanha')],
      GT, 'Campanhas no mês (tracejado = dia)')
p.vis['nxCampanhas']['visual']['visualContainerObjects'].update(CARD)

# Visitas por vendedor no periodo/dia selecionado (Top 10 por visitas, sem rolagem)
TOPV = {'name': 'fTopVisitas', 'field': col('dVendedor', 'Vendedor'), 'type': 'TopN',
        'filter': {'Version': 2, 'From': [
            {'Name': 'subquery', 'Expression': {'Subquery': {'Query': {'Version': 2,
                'From': [{'Name': 'v', 'Entity': 'dVendedor', 'Type': 0}, {'Name': 'm', 'Entity': '_Medidas', 'Type': 0}],
                'Select': [{'Column': {'Expression': {'SourceRef': {'Source': 'v'}}, 'Property': 'Vendedor'}, 'Name': 'field'}],
                'OrderBy': [{'Direction': 2, 'Expression': {'Measure': {'Expression': {'SourceRef': {'Source': 'm'}}, 'Property': 'Visitas'}}}],
                'Top': 8}}}, 'Type': 2},
            {'Name': 'v', 'Entity': 'dVendedor', 'Type': 0}],
            'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 'v'}}, 'Property': 'Vendedor'}}],
                                            'Table': {'SourceRef': {'Source': 'subquery'}}}}}]}}
COLS = [('Visitas', 'Visitas'), ('Visitas com Pedido', 'Pedidos'), ('Conversão de Visitas %', 'Conversão')]
p.add('nxVisitasVend', 1242, 700, 632, 356, {
    'visualType': 'tableEx',
    'query': {'queryState': {'Values': {'projections': [proj(col('dVendedor', 'Vendedor'), 'Vendedor')] + [proj(meas(m), d) for m, d in COLS]}},
              'sortDefinition': {'sort': [{'field': meas('Visitas'), 'direction': 'Descending'}]}},
    'objects': {'columnHeaders': [{'properties': {'alignment': s('Center'), 'fontSize': num(10), 'fontColor': color(COR['claro'])}}],
                'values': [{'properties': {'fontSize': num(10), 'fontColor': color('#FFFFFF')}}],
                'grid': [{'properties': {'rowPadding': num(1), 'textSize': num(9), 'gridHorizontal': lit('true'), 'gridHorizontalColor': color(COR['borda'])}}],
                'total': [{'properties': {'totals': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container=dict(CARD, title=title('8 vendedores com mais visitas')), filters=[TOPV])
p.write(DEF, overwrite=True)

t = Pagina(TT, 'TT Dia', fundo=None, tipo='Tooltip', w=300, h=200)
t.html('nxTooltipDia', 0, 0, 300, 200, 'UX Tooltip Dia')
t.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgWarehouse', 'pgFinancial', 'pgPredictive', 'pgSimulator', 'pgCalendar',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora', 'ttMesFinanceiro', 'ttEstoqueMes', 'ttDia'])
print('calendar ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
