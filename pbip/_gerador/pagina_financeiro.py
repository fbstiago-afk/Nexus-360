# NEXUS 360 - Etapa F: Financial & Profitability (PBIR)
# Pergunta: onde a margem se perde e como o caixa acompanha o resultado?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, tooltip_page, realizado, COR, deneb)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG, TT = 'pgFinancial', 'ttMesFinanceiro'
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}
SL = [('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
      ('nxSlMes', 'dCalendario', 'MesAno', 'Mês', 'Dropdown', False, None, 70, True),
      ('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Basic', False, None, 300, False)]

p = Pagina(PG, 'Financial & Profitability')
p.chrome(slicers=SL)

# DRE gerencial (HTML, coluna esquerda)
p.html('nxDRE', 46, 212, 640, 844, 'UX Financeiro DRE')
p.vis['nxDRE']['visual']['visualContainerObjects'] = dict(CARD)

# Ponte do resultado: ano anterior -> atual por linha da DRE (Deneb)
PONTE = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [
        {"filter": "isValid(datum['Valor DRE Gerencial']) && isValid(datum['Valor DRE Gerencial LY'])"},
        {"calculate": "datum['Valor DRE Gerencial'] - datum['Valor DRE Gerencial LY']", "as": "delta"},
        {"joinaggregate": [{"op": "sum", "field": "Valor DRE Gerencial LY", "as": "base"}, {"op": "sum", "field": "Valor DRE Gerencial", "as": "final"}]},
        {"window": [{"op": "sum", "field": "delta", "as": "cum"}], "sort": [{"field": "Ordem"}], "frame": [None, 0]},
        {"calculate": "datum.base + datum.cum", "as": "fim"}, {"calculate": "datum.fim - datum.delta", "as": "ini"},
        {"calculate": "datum.delta >= 0 ? 'Aumenta o resultado' : 'Reduz o resultado'", "as": "efeito"},
        {"calculate": "(datum.delta >= 0 ? '+' : '') + pbiFormat(datum.delta / 1000, '#,0') + ' mil'", "as": "rot"},
        {"calculate": "'resultado ano anterior: R$ ' + pbiFormat(datum.base / 1000000, '#,0.0') + ' mi'", "as": "lblBase"},
        {"calculate": "'resultado atual: R$ ' + pbiFormat(datum.final / 1000000, '#,0.0') + ' mi'", "as": "lblFinal"}],
    "encoding": {"x": {"field": "Linha", "type": "nominal", "sort": {"field": "Ordem"}, "title": None, "axis": {"labelAngle": 0, "labelFontSize": 10, "labelColor": "#C9D6E3", "grid": False}}},
    "layer": [
        {"mark": {"type": "rule", "strokeDash": [5, 4], "color": "#A9B9CA"}, "encoding": {"y": {"aggregate": "max", "field": "base", "type": "quantitative"}}},
        {"mark": {"type": "rule", "color": "#10D4C4", "strokeWidth": 1.5}, "encoding": {"y": {"aggregate": "max", "field": "final", "type": "quantitative"}}},
        {"mark": {"type": "bar", "cornerRadius": 2, "width": {"band": 0.62}},
         "encoding": {"y": {"field": "ini", "type": "quantitative", "title": None, "scale": {"zero": False},
                            "axis": {"labelExpr": "pbiFormat(datum.value / 1000000, '#,0') + ' mi'", "grid": True, "tickCount": 5}},
                      "y2": {"field": "fim"},
                      "color": {"field": "efeito", "type": "nominal", "scale": {"domain": ["Aumenta o resultado", "Reduz o resultado"], "range": ["#45D5A1", "#FF7285"]}},
                      "tooltip": [{"field": "Linha"}, {"field": "Valor DRE Gerencial", "title": "Atual", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "Valor DRE Gerencial LY", "title": "Ano anterior", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "delta", "title": "Efeito no resultado", "formatType": "pbiFormat", "format": "+R$ #,0;-R$ #,0"}]}},
        {"mark": {"type": "text", "dy": -8, "fontSize": 10.5, "fontWeight": 600, "color": "#FFFFFF"},
         "encoding": {"y": {"field": "fim", "type": "quantitative"}, "text": {"field": "rot"}}},
        {"transform": [{"filter": "datum.Ordem == 1"}], "mark": {"type": "text", "align": "left", "x": 4, "dy": -6, "fontSize": 10, "color": "#A9B9CA"},
         "encoding": {"x": None, "y": {"field": "base", "type": "quantitative"}, "text": {"field": "lblBase"}}},
        {"transform": [{"filter": "datum.Ordem == 1"}], "mark": {"type": "text", "align": "right", "x": {"expr": "width - 4"}, "dy": -6, "fontSize": 10, "color": "#10D4C4"},
         "encoding": {"x": None, "y": {"field": "final", "type": "quantitative"}, "text": {"field": "lblFinal"}}}]}
deneb(p, 'nxPonte', 702, 212, 680, 408,
      [col('dLinhaDRE', 'Linha'), col('dLinhaDRE', 'Ordem'), meas('Valor DRE Gerencial'), meas('Valor DRE Gerencial LY')],
      PONTE, 'O que mudou no resultado vs ano anterior (rótulos em R$ mil)')

# Caixa mensal: recebimentos x pagamentos e saldo (nativo, tooltip mensal)
p.add('nxCaixa', 702, 636, 680, 420, {
    'visualType': 'lineClusteredColumnComboChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('dCalendario', 'MesAno'), 'Mês', active=True)]},
                             'Y': {'projections': [proj(meas('Recebimentos (Data Pagamento)'), 'Recebido de clientes'),
                                                   proj(meas('Pagamentos (Data Pagamento)'), 'Pago a fornecedores')]},
                             'Y2': {'projections': [proj(meas('Saldo Recebimentos - Pagamentos'), 'Saldo')]}},
              'sortDefinition': {'sort': [{'field': col('dCalendario', 'MesAno'), 'direction': 'Ascending'}]}},
    'objects': {'dataPoint': [{'properties': {'fill': color(COR['teal'])}, 'selector': {'metadata': '_Medidas.Recebimentos (Data Pagamento)'}},
                              {'properties': {'fill': color('#3E5C7A')}, 'selector': {'metadata': '_Medidas.Pagamentos (Data Pagamento)'}},
                              {'properties': {'fill': color(COR['alerta'])}, 'selector': {'metadata': '_Medidas.Saldo Recebimentos - Pagamentos'}}],
                'lineStyles': [{'properties': {'strokeWidth': num(2), 'showMarker': lit('true'), 'lineChartType': s('linear')}}],
                'valueAxis': [{'properties': {'show': lit('true'), 'secShow': lit('true'), 'labelDisplayUnits': num(1000000)}}],
                'legend': [{'properties': {'show': lit('true'), 'position': s('Top')}}],
                'categoryAxis': [{'properties': {'fontSize': num(9)}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Caixa: recebido × pago (data do pagamento)'), 'visualTooltip': tooltip_page(TT)},
    filters=[realizado()])

# Recebiveis (HTML)
p.html('nxRecebiveis', 1398, 212, 476, 300, 'UX Financeiro Recebíveis')
p.vis['nxRecebiveis']['visual']['visualContainerObjects'] = dict(CARD)

# Desvio de despesa vs orcamento por filial (barras divergentes, Deneb)
DESV = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "isValid(datum['Desvio Despesa vs Orçamento']) && datum['Orçamento Despesa Operacional (até corte)'] > 0"},
                  {"calculate": "datum['Desvio Despesa vs Orçamento'] / datum['Orçamento Despesa Operacional (até corte)']", "as": "pct"},
                  {"calculate": "datum.pct > 0 ? 'Acima do orçado' : 'Dentro do orçado'", "as": "sit"}],
    "encoding": {"y": {"field": "Cidade", "type": "nominal", "sort": {"field": "pct", "op": "max", "order": "descending"}, "title": None,
                       "axis": {"labelFontSize": 10, "labelColor": "#C9D6E3"}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadiusEnd": 2, "height": {"band": 0.62}},
         "encoding": {"x": {"field": "pct", "type": "quantitative", "title": None, "axis": {"format": "+.0%", "grid": True, "tickCount": 5}},
                      "color": {"field": "sit", "type": "nominal", "scale": {"domain": ["Acima do orçado", "Dentro do orçado"], "range": ["#FF7285", "#45D5A1"]}},
                      "tooltip": [{"field": "Cidade", "title": "Filial"}, {"field": "pct", "title": "Desvio", "formatType": "pbiFormat", "format": "+0.0%;-0.0%"},
                                  {"field": "Desvio Despesa vs Orçamento", "title": "Desvio R$", "formatType": "pbiFormat", "format": "+R$ #,0;-R$ #,0"}]}},
        {"mark": {"type": "rule", "color": "#A9B9CA"}, "encoding": {"x": {"datum": 0}}}]}
deneb(p, 'nxDesvio', 1398, 528, 476, 260,
      [col('dFilial', 'Cidade'), meas('Desvio Despesa vs Orçamento'), meas('Orçamento Despesa Operacional (até corte)')], DESV, 'Despesa operacional vs orçado por filial')

# Pareto de margem bruta por subcategoria (Deneb)
PAR = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Margem Bruta'] > 0"},
                  {"window": [{"op": "sum", "field": "Margem Bruta", "as": "acum"}], "sort": [{"field": "Margem Bruta", "order": "descending"}], "frame": [None, 0]},
                  {"joinaggregate": [{"op": "sum", "field": "Margem Bruta", "as": "tot"}]},
                  {"calculate": "datum.acum / datum.tot", "as": "pc"}],
    "encoding": {"x": {"field": "Subcategoria", "type": "nominal", "sort": {"field": "Margem Bruta", "order": "descending"}, "title": None,
                       "axis": {"labelAngle": -40, "labelFontSize": 9, "labelColor": "#C9D6E3"}}},
    "layer": [
        {"mark": {"type": "bar", "color": "#0878C9", "cornerRadiusEnd": 2},
         "encoding": {"y": {"field": "Margem Bruta", "type": "quantitative", "title": None, "axis": None},
                      "tooltip": [{"field": "Subcategoria"}, {"field": "Margem Bruta", "title": "Margem bruta", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "pc", "title": "Acumulado", "formatType": "pbiFormat", "format": "0.0%"}]}},
        {"mark": {"type": "line", "color": "#FFC66D", "point": {"filled": True, "size": 22, "color": "#FFC66D"}},
         "encoding": {"y": {"field": "pc", "type": "quantitative", "scale": {"domain": [0, 1]}, "title": None, "axis": {"format": ".0%", "orient": "right", "tickCount": 3}}}},
        {"mark": {"type": "rule", "strokeDash": [3, 3], "color": "#A9B9CA"}, "encoding": {"y": {"datum": 0.8, "scale": {"domain": [0, 1]}, "axis": None}}}],
    "resolve": {"scale": {"y": "independent"}}}
deneb(p, 'nxPareto', 1398, 804, 476, 252, [col('dProduto', 'Subcategoria'), meas('Margem Bruta')], PAR,
      'Pareto da margem bruta por subcategoria')
p.write(DEF, overwrite=True)

t = Pagina(TT, 'TT Mês Financeiro', fundo=None, tipo='Tooltip', w=320, h=170)
t.html('nxTooltipMes', 0, 0, 320, 170, 'UX Tooltip Mês Financeiro')
t.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgFinancial',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora', 'ttMesFinanceiro'])
print('financial ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
