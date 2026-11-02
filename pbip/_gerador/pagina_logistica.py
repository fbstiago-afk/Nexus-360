# NEXUS 360 - Etapa D: Logistics Control Tower (PBIR)
# Pergunta: onde e por que a entrega falha, e quanto custa?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, tooltip_page, realizado, COR, deneb)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG, TT = 'pgLogistics', 'ttTransportadora'
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}
SL = [('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
      ('nxSlMes', 'dCalendario', 'MesAno', 'Mês (data da entrega)', 'Dropdown', False, None, 70, True),
      ('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Dropdown', False, None, 70, False),
      ('nxSlModal', 'dTransportadora', 'Modal', 'Modal', 'Basic', False, None, 90, False),
      ('nxSlTransp', 'dTransportadora', 'Transportadora', 'Transportadora', 'Dropdown', False, None, 70, False)]

p = Pagina(PG, 'Logistics Control Tower')
p.chrome(slicers=SL)
p.html('nxLogKPIs', 46, 212, 1828, 112, 'UX Logística KPIs')

# Mapa de OTIF por filial
p.html('nxLogMapa', 46, 340, 520, 356, 'UX Logística Mapa')
p.vis['nxLogMapa']['visual']['visualContainerObjects'] = dict(CARD)

# Timeline: OTIF mensal vs meta e volume
p.add('nxOtifMensal', 582, 340, 720, 356, {
    'visualType': 'lineClusteredColumnComboChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('dCalendario', 'MesAno'), 'Mês', active=True)]},
                             'Y': {'projections': [proj(meas('Entregas'), 'Entregas')]},
                             'Y2': {'projections': [proj(meas('OTIF %'), 'OTIF'), proj(meas('Meta OTIF % (média simples)'), 'Meta OTIF')]}},
              'sortDefinition': {'sort': [{'field': col('dCalendario', 'MesAno'), 'direction': 'Ascending'}]}},
    'objects': {'dataPoint': [{'properties': {'fill': color('#173B5C')}, 'selector': {'metadata': '_Medidas.Entregas'}},
                              {'properties': {'fill': color(COR['teal'])}, 'selector': {'metadata': '_Medidas.OTIF %'}},
                              {'properties': {'fill': color(COR['alerta'])}, 'selector': {'metadata': '_Medidas.Meta OTIF % (média simples)'}}],
                'lineStyles': [{'properties': {'strokeWidth': num(2), 'showMarker': lit('true'), 'lineChartType': s('linear')}},
                               {'properties': {'lineStyle': s('dashed'), 'showMarker': lit('false')}, 'selector': {'metadata': '_Medidas.Meta OTIF % (média simples)'}}],
                'valueAxis': [{'properties': {'show': lit('true'), 'secShow': lit('true'), 'labelDisplayUnits': num(1000)}}],
                'legend': [{'properties': {'show': lit('true'), 'position': s('Top')}}],
                'categoryAxis': [{'properties': {'fontSize': num(9)}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('OTIF mensal vs meta (linhas) e volume de entregas (colunas)')}, filters=[realizado()])

# Distribuicao dos dias em relacao ao prometido (Deneb)
DIST = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "isValid(datum['DiasAtraso']) && datum['Entregas'] > 0"},
                  {"joinaggregate": [{"op": "sum", "field": "Entregas", "as": "tot"}]},
                  {"calculate": "datum['Entregas'] / datum.tot", "as": "pct"},
                  {"calculate": "datum['DiasAtraso'] <= 0 ? 'No prazo ou antes' : 'Atrasada'", "as": "faixa"}],
    "encoding": {"x": {"field": "DiasAtraso", "type": "ordinal", "title": "Dias entre a entrega e a data prometida (negativo = antes)", "axis": {"labelAngle": 0}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadiusEnd": 3, "width": {"band": 0.72}},
         "encoding": {"y": {"field": "Entregas", "type": "quantitative", "title": None, "axis": None},
                      "color": {"field": "faixa", "type": "nominal", "scale": {"domain": ["No prazo ou antes", "Atrasada"], "range": ["#10D4C4", "#FF7285"]}},
                      "tooltip": [{"field": "DiasAtraso", "title": "Dias"}, {"field": "Entregas", "formatType": "pbiFormat", "format": "#,0"},
                                  {"field": "pct", "title": "Participação", "formatType": "pbiFormat", "format": "0.0%"}]}},
        {"mark": {"type": "text", "dy": -7, "fontSize": 10, "color": "#C9D6E3"},
         "encoding": {"y": {"field": "Entregas", "type": "quantitative"}, "text": {"field": "pct", "formatType": "pbiFormat", "format": "0%"}}}]}
deneb(p, 'nxDistAtraso', 1318, 340, 556, 356, [col('fEntrega', 'DiasAtraso'), meas('Entregas')], DIST, 'Entregas por dias de atraso')

# Dispersao transportadoras: frete por entrega x OTIF (Deneb)
SC = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Entregas'] > 0"},
                  {"joinaggregate": [{"op": "median", "field": "OTIF %", "as": "mo"}, {"op": "median", "field": "Frete por Entrega", "as": "mf"}]},
                  {"calculate": "datum['OTIF %'] < datum.mo && datum['Frete por Entrega'] > datum.mf ? 'Caro e abaixo da mediana de OTIF' : datum.Modal", "as": "grupo"}],
    "layer": [
        {"mark": {"type": "rule", "strokeDash": [4, 4], "color": "#6F86A0"}, "encoding": {"x": {"aggregate": "max", "field": "mf", "type": "quantitative"}}},
        {"mark": {"type": "rule", "strokeDash": [4, 4], "color": "#6F86A0"}, "encoding": {"y": {"aggregate": "max", "field": "mo", "type": "quantitative"}}},
        {"mark": {"type": "circle", "opacity": 0.9, "stroke": "#071528", "strokeWidth": 0.8},
         "encoding": {"x": {"field": "Frete por Entrega", "type": "quantitative", "scale": {"zero": False}, "title": "Frete por entrega (R$)",
                            "axis": {"format": ",.0f", "grid": True, "tickCount": 5}},
                      "y": {"field": "OTIF %", "type": "quantitative", "scale": {"zero": False}, "title": "OTIF", "axis": {"format": ".0%", "grid": True, "tickCount": 5}},
                      "size": {"field": "Entregas", "type": "quantitative", "scale": {"range": [40, 320]}, "legend": None},
                      "color": {"field": "grupo", "type": "nominal", "scale": {"domain": ["Frota própria", "Rodoviário", "Caro e abaixo da mediana de OTIF"],
                                                                              "range": ["#10D4C4", "#5FA8E6", "#FF7285"]}},
                      "tooltip": [{"field": "Transportadora"}, {"field": "Modal"}, {"field": "Entregas", "formatType": "pbiFormat", "format": "#,0"},
                                  {"field": "OTIF %", "title": "OTIF", "formatType": "pbiFormat", "format": "0.0%"},
                                  {"field": "Frete por Entrega", "title": "Frete/entrega", "formatType": "pbiFormat", "format": "R$ #,0.00"}]}},
        {"mark": {"type": "text", "align": "left", "dx": 7, "fontSize": 9, "color": "#C9D6E3"},
         "transform": [{"filter": "datum.grupo == 'Caro e abaixo da mediana de OTIF'"}],
         "encoding": {"x": {"field": "Frete por Entrega", "type": "quantitative"}, "y": {"field": "OTIF %", "type": "quantitative"},
                      "text": {"field": "Transportadora"}}}]}
deneb(p, 'nxTranspDisp', 46, 712, 700, 344,
      [col('dTransportadora', 'Transportadora'), col('dTransportadora', 'Modal'), meas('Entregas'), meas('OTIF %'), meas('Frete por Entrega')],
      SC, 'Transportadoras: frete por entrega × OTIF (tamanho = entregas)')

# Ranking das transportadoras com menor OTIF (nativo, tooltip de transportadora)
bottom = {'name': 'fBottom12', 'field': col('dTransportadora', 'Transportadora'), 'type': 'TopN',
          'filter': {'Version': 2, 'From': [
              {'Name': 'subquery', 'Expression': {'Subquery': {'Query': {'Version': 2,
                  'From': [{'Name': 't', 'Entity': 'dTransportadora', 'Type': 0}, {'Name': 'm', 'Entity': '_Medidas', 'Type': 0}],
                  'Select': [{'Column': {'Expression': {'SourceRef': {'Source': 't'}}, 'Property': 'Transportadora'}, 'Name': 'field'}],
                  'OrderBy': [{'Direction': 1, 'Expression': {'Measure': {'Expression': {'SourceRef': {'Source': 'm'}}, 'Property': 'OTIF %'}}}],
                  'Top': 8}}}, 'Type': 2},
              {'Name': 't', 'Entity': 'dTransportadora', 'Type': 0}],
              'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 't'}}, 'Property': 'Transportadora'}}],
                                              'Table': {'SourceRef': {'Source': 'subquery'}}}}}]}}
COLS = [(col('dTransportadora', 'Transportadora'), 'Transportadora'), (col('dTransportadora', 'Modal'), 'Modal'), (meas('Entregas'), 'Entregas'),
        (meas('OTIF %'), 'OTIF'), (meas('No Prazo %'), 'No prazo'), (meas('In Full %'), 'Completas'), (meas('Atraso Médio (dias)'), 'Atraso (d)'),
        (meas('Ocorrência %'), 'Ocorrência'), (meas('Frete por Entrega'), 'Frete/entrega')]
p.add('nxTranspRank', 762, 712, 1112, 344, {
    'visualType': 'tableEx',
    'query': {'queryState': {'Values': {'projections': [proj(f, d) for f, d in COLS]}},
              'sortDefinition': {'sort': [{'field': meas('OTIF %'), 'direction': 'Ascending'}]}},
    'objects': {'values': [{'properties': {'fontColor': {'solid': {'color': {'expr': meas('UX Cor OTIF Relativo')}}}},
                            'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': '_Medidas.OTIF %'}}],
                'columnHeaders': [{'properties': {'alignment': s('Center'), 'wordWrap': lit('true'), 'fontSize': num(10), 'columnAdjustment': s('growToFit')}}],
                'grid': [{'properties': {'rowPadding': num(2), 'textSize': num(10)}}],
                'total': [{'properties': {'totals': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('8 transportadoras com menor OTIF · cor vs seleção'), 'visualTooltip': tooltip_page(TT)},
    filters=[bottom])
p.write(DEF, overwrite=True)

t = Pagina(TT, 'TT Transportadora', fundo=None, tipo='Tooltip', w=320, h=200)
t.html('nxTooltipTransp', 0, 0, 320, 200, 'UX Tooltip Transportadora')
t.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora'])
print('logistics ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
