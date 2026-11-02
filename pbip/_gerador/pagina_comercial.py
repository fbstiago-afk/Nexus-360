# NEXUS 360 - Etapa B: Commercial Intelligence (PBIR)
# Pergunta: quem vende mais, com qual mix e a que custo de desconto?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, tooltip_page, COR, DENEB, NOCHROME, DCONF, deneb)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG, TT = 'pgCommercial', 'ttVendedor'
p = Pagina(PG, 'Commercial Intelligence')
p.chrome()

# 1. Faixa de KPIs (HTML unico, 4 indicadores)
p.html('nxComKPIs', 46, 212, 1828, 112, 'UX Comercial KPIs')

# 2a. Top 15 vendedores (nativo: filtro cruzado e tooltip de pagina)
topn = {'name': 'fTop12', 'field': col('dVendedor', 'Vendedor'), 'type': 'TopN',
        'filter': {'Version': 2, 'From': [
            {'Name': 'subquery', 'Expression': {'Subquery': {'Query': {'Version': 2,
                'From': [{'Name': 'd', 'Entity': 'dVendedor', 'Type': 0}, {'Name': 'm', 'Entity': '_Medidas', 'Type': 0}],
                'Select': [{'Column': {'Expression': {'SourceRef': {'Source': 'd'}}, 'Property': 'Vendedor'}, 'Name': 'field'}],
                'OrderBy': [{'Direction': 2, 'Expression': {'Measure': {'Expression': {'SourceRef': {'Source': 'm'}}, 'Property': 'Receita Líquida'}}}],
                'Top': 12}}}, 'Type': 2},
            {'Name': 'd', 'Entity': 'dVendedor', 'Type': 0}],
            'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 'd'}}, 'Property': 'Vendedor'}}],
                                            'Table': {'SourceRef': {'Source': 'subquery'}}}}}]}}
p.add('nxTopVendedores', 46, 340, 560, 356, {
    'visualType': 'clusteredBarChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('dVendedor', 'Vendedor'), 'Vendedor', active=True)]},
                             'Y': {'projections': [proj(meas('Receita Líquida'), 'Receita')]}},
              'sortDefinition': {'sort': [{'field': meas('Receita Líquida'), 'direction': 'Descending'}]}},
    'objects': {'dataPoint': [{'properties': {'fill': {'solid': {'color': {'expr': meas('UX Cor Margem vs Média')}}}},
                               'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}]}}],
                'labels': [{'properties': {'show': lit('true'), 'labelDisplayUnits': num(1000), 'labelPrecision': lit('0L'), 'color': color('#FFFFFF'), 'fontSize': num(9)}}],
                'valueAxis': [{'properties': {'show': lit('false'), 'gridlineShow': lit('false')}}],
                'categoryAxis': [{'properties': {'show': lit('true'), 'fontSize': num(9), 'labelColor': color(COR['claro'])}}],
                'legend': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Top 12 vendedores · cor: margem vs média da seleção'), 'visualTooltip': tooltip_page(TT),
               'padding': [{'properties': {'top': lit('6D'), 'bottom': lit('2D'), 'left': lit('10D'), 'right': lit('10D')}}]},
    filters=[topn])

# 2b. Dispersao desconto x margem por vendedor (Deneb, quadrantes = regra do cartao de oportunidades)
SCATTER = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Receita Líquida'] > 0"},
                  {"joinaggregate": [{"op": "q3", "field": "Desconto Médio Ponderado %", "as": "q3d"},
                                     {"op": "median", "field": "Margem Bruta %", "as": "medm"}]},
                  {"calculate": "datum['Desconto Médio Ponderado %'] > datum.q3d && datum['Margem Bruta %'] < datum.medm ? 'Desconto alto e margem baixa' : datum.Equipe", "as": "grupo"}],
    "layer": [
        {"mark": {"type": "rule", "strokeDash": [4, 4], "color": "#6F86A0"}, "encoding": {"x": {"aggregate": "max", "field": "q3d", "type": "quantitative"}}},
        {"mark": {"type": "rule", "strokeDash": [4, 4], "color": "#6F86A0"}, "encoding": {"y": {"aggregate": "max", "field": "medm", "type": "quantitative"}}},
        {"mark": {"type": "circle", "opacity": 0.85, "stroke": "#071528", "strokeWidth": 0.6},
         "encoding": {
             "x": {"field": "Desconto Médio Ponderado %", "type": "quantitative", "scale": {"zero": False}, "title": "Desconto médio ponderado",
                   "axis": {"format": ".1%", "grid": True, "tickCount": 6}},
             "y": {"field": "Margem Bruta %", "type": "quantitative", "scale": {"zero": False}, "title": "Margem bruta",
                   "axis": {"format": ".1%", "grid": True, "tickCount": 5}},
             "size": {"field": "Receita Líquida", "type": "quantitative", "scale": {"range": [12, 220]}, "legend": None},
             "color": {"field": "grupo", "type": "nominal",
                       "scale": {"domain": ["Farmer", "Hunter", "Key Account", "Desconto alto e margem baixa"],
                                 "range": ["#5FA8E6", "#10D4C4", "#C9D6E3", "#FF7285"]}},
             "tooltip": [{"field": "Vendedor"}, {"field": "Equipe"},
                         {"field": "Receita Líquida", "title": "Receita", "formatType": "pbiFormat", "format": "R$ #,0"},
                         {"field": "Margem Bruta %", "title": "Margem", "formatType": "pbiFormat", "format": "0.0%"},
                         {"field": "Desconto Médio Ponderado %", "title": "Desconto", "formatType": "pbiFormat", "format": "0.0%"}]}},
        {"mark": {"type": "text", "align": "right", "baseline": "bottom", "dx": -4, "dy": -4, "fontSize": 10, "color": "#FF7285"},
         "encoding": {"x": {"aggregate": "max", "field": "Desconto Médio Ponderado %", "type": "quantitative"},
                      "y": {"aggregate": "min", "field": "Margem Bruta %", "type": "quantitative"},
                      "text": {"value": "desconto alto · margem baixa"}}}]}
deneb(p, 'nxDispersao', 622, 340, 680, 356,
      [col('dVendedor', 'Vendedor'), col('dVendedor', 'Equipe'), meas('Receita Líquida'), meas('Margem Bruta %'), meas('Desconto Médio Ponderado %')],
      SCATTER, 'Desconto × margem por vendedor (tamanho: receita)')

# 2c. Marcas: receita vs ano anterior (halteres, Deneb)
DUMB = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "isValid(datum['Receita LY']) && datum['Receita LY'] > 0"},
                  {"calculate": "datum['Receita (até corte)'] / datum['Receita LY'] - 1", "as": "yoy"},
                  {"calculate": "datum.yoy >= 0 ? 'Cresceu' : 'Caiu'", "as": "sinal"},
                  {"calculate": "max(datum['Receita (até corte)'], datum['Receita LY'])", "as": "xr"}],
    "encoding": {"y": {"field": "Marca", "type": "nominal", "sort": {"field": "Receita (até corte)", "op": "max", "order": "descending"},
                       "axis": {"title": None, "labelColor": "#C9D6E3", "labelFontSize": 11, "labelPadding": 6}}},
    "layer": [
        {"mark": {"type": "rule", "color": "#3E5C7A", "strokeWidth": 3},
         "encoding": {"x": {"field": "Receita LY", "type": "quantitative", "scale": {"zero": False}, "title": None,
                            "axis": {"labelExpr": "pbiFormat(datum.value / 1000, '#,0') + ' mil'", "grid": True, "tickCount": 4}},
                      "x2": {"field": "Receita (até corte)"}}},
        {"mark": {"type": "circle", "size": 70, "color": "#6F86A0"}, "encoding": {"x": {"field": "Receita LY", "type": "quantitative"}}},
        {"mark": {"type": "circle", "size": 110, "opacity": 1},
         "encoding": {"x": {"field": "Receita (até corte)", "type": "quantitative"},
                      "color": {"field": "sinal", "type": "nominal", "scale": {"domain": ["Cresceu", "Caiu"], "range": ["#45D5A1", "#FF7285"]}},
                      "tooltip": [{"field": "Marca"}, {"field": "Receita (até corte)", "title": "Receita", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "Receita LY", "title": "Ano anterior", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "yoy", "title": "Variação", "formatType": "pbiFormat", "format": "+0.0%;-0.0%"}]}},
        {"mark": {"type": "text", "align": "left", "dx": 10, "fontSize": 10.5, "fontWeight": 600},
         "encoding": {"x": {"field": "xr", "type": "quantitative"}, "text": {"field": "yoy", "formatType": "pbiFormat", "format": "+0.0%;-0.0%"},
                      "color": {"field": "sinal", "type": "nominal", "legend": None, "scale": {"domain": ["Cresceu", "Caiu"], "range": ["#45D5A1", "#FF7285"]}}}}]}
deneb(p, 'nxMarcas', 1318, 340, 556, 356, [col('dProduto', 'Marca'), meas('Receita (até corte)'), meas('Receita LY')], DUMB,
      'Marcas: receita vs ano anterior (cinza = ano anterior)')

# 3a. Matriz de mix por categoria > subcategoria
VALS = [('Receita Líquida', 'Receita'), ('UX Barra Participação', 'Participação'), ('Participação Receita %', '%'),
        ('Margem Bruta %', 'Margem'), ('Desconto Médio Ponderado %', 'Desconto'), ('Receita YoY %', 'vs ano ant.')]
cores = [{'properties': {'fontColor': {'solid': {'color': {'expr': meas('UX Cor Margem vs Média')}}}},
          'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': '_Medidas.Margem Bruta %'}},
         {'properties': {'fontColor': {'solid': {'color': {'expr': meas('UX Cor Receita YoY')}}}},
          'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': '_Medidas.Receita YoY %'}}]
p.add('nxMix', 46, 712, 1100, 344, {
    'visualType': 'pivotTable',
    'query': {'queryState': {'Rows': {'projections': [proj(col('dProduto', 'Categoria'), 'Categoria', active=True),
                                                      proj(col('dProduto', 'Subcategoria'), 'Subcategoria', active=False)]},
                             'Values': {'projections': [proj(meas(m), d) for m, d in VALS]}},
              'sortDefinition': {'sort': [{'field': meas('Receita Líquida'), 'direction': 'Descending'}]}},
    'expansionStates': [{'roles': ['Rows'], 'levels': [{'queryRefs': ['dProduto.Categoria'], 'isCollapsed': True, 'isPinned': True},
                                                       {'queryRefs': ['dProduto.Subcategoria'], 'isCollapsed': True, 'isPinned': True}], 'root': {}}],
    'objects': {'values': cores,
                'columnHeaders': [{'properties': {'alignment': s('Center'), 'wordWrap': lit('true'), 'fontSize': num(10), 'columnAdjustment': s('growToFit')}}],
                'rowHeaders': [{'properties': {'alignment': s('Left'), 'showExpandCollapseButtons': lit('true')}}],
                'grid': [{'properties': {'rowPadding': num(3), 'textSize': num(10), 'imageHeight': num(16), 'imageWidth': num(120)}}],
                'subTotals': [{'properties': {'rowSubtotals': lit('true')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Mix por categoria e subcategoria (+ para abrir)'),
               'padding': [{'properties': {'top': lit('8D'), 'bottom': lit('4D'), 'left': lit('12D'), 'right': lit('12D')}}]})

# 3b. Oportunidades e excecoes
p.html('nxOportunidades', 1162, 712, 712, 344, 'UX Comercial Oportunidades')
p.vis['nxOportunidades']['visual']['visualContainerObjects'] = {
    'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
    'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}
p.write(DEF, overwrite=True)

# Pagina de tooltip de vendedor
t = Pagina(TT, 'TT Vendedor', fundo=None, tipo='Tooltip', w=320, h=210)
t.html('nxTooltipVendedor', 0, 0, 320, 210, 'UX Tooltip Vendedor')
t.write(DEF, overwrite=True)

register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', '2a6aff4ae45b2ec75c15', 'ttVendedor'])
print('commercial ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
