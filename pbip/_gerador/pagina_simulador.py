# NEXUS 360 - Etapa H: Decision Simulator (PBIR)
# Pergunta: se eu mexer em preco, desconto, volume, custo, frete ou despesas, o que acontece com o resultado operacional?
import os, sys, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, hid, COR, NOCHROME, deneb, SB)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG = 'pgSimulator'
# base do cenario: periodo e filiais (sem categoria: frete e despesas nao tem grao de produto)
SL = [('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
      ('nxSlMes', 'dCalendario', 'MesAno', 'Mês', 'Dropdown', False, None, 70, True),
      ('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Basic', False, None, 300, False)]
PARAM = [('nxSimPreco', 'Sim Preço', 'Preço %', 'Preço'),
         ('nxSimDesconto', 'Sim Desconto', 'Desconto p.p.', 'Desconto médio (p.p.)'),
         ('nxSimVolume', 'Sim Volume', 'Volume %', 'Volume'),
         ('nxSimCusto', 'Sim Custo', 'Custo %', 'Custo da mercadoria'),
         ('nxSimFrete', 'Sim Frete', 'Frete %', 'Tarifa de frete'),
         ('nxSimDespesas', 'Sim Despesas', 'Despesas %', 'Despesas operacionais')]

p = Pagina(PG, 'Decision Simulator')
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}

# Controles do cenario (coluna esquerda): sliders de valor unico, padrao 0
def zero(table, column):
    return {'filter': {'Version': 2, 'From': [{'Name': 't', 'Entity': table, 'Type': 0}],
                       'Where': [{'Condition': {'Comparison': {'ComparisonKind': 0,
                                                               'Left': {'Column': {'Expression': {'SourceRef': {'Source': 't'}}, 'Property': column}},
                                                               'Right': {'Literal': {'Value': '0D'}}}}}]}}


p.panel_bg('nxSimPainel', 46, 212, 380, 844, None, transp=8)
p.textbox('nxSimTitulo', 62, 218, 348, 32, 'Premissas do cenário', size='13pt')
y = 254
for (nm, t, c, rot) in PARAM:
    p.slicer(nm, 62, y, 348, 114, t, c, rot, mode='Single', sync=False)
    v = p.vis[nm]['visual']
    v['objects']['header'] = [{'properties': {'show': lit('true'), 'fontColor': color(COR['claro']), 'textSize': num(10)}}]
    v['objects']['numericInputStyle'] = [{'properties': {'fontColor': color('#FFFFFF'), 'background': color(COR['card']), 'textSize': num(11)}}]
    v['objects']['slider'] = [{'properties': {'color': color(COR['teal'])}}]
    v['objects'].pop('selection', None)
    v['objects']['general'][0]['properties']['filter'] = zero(t, c)
    v['objects']['data'][0]['properties']['numericStart'] = lit('0D')  # sem isso o slider exibe o minimo
    y += 116
p.button('nxSimZerar', 62, 954, 348, 36, 'Voltar todas as premissas a 0 (mantém período e filiais)', label='Zerar cenário')
p.html('nxSimAviso', 62, 994, 348, 62, 'UX Simulador Aviso')
for nm in ('nxSimTitulo',):
    pass

# o reset padrao ("Limpar filtros") tambem zera o cenario
p.chrome(slicers=SL)

# favorito "Zerar cenario": so os sliders
rb = [b for b in p.bookmarks if b['displayName'].endswith('Redefinir filtros')][0]
for (nm, t, c, rot) in PARAM:
    mg = rb['explorationState']['sections'][PG]['visualContainers'][nm]['singleVisual']['objects']['merge']
    mg['general'] = [{'properties': {'filter': zero(t, c)}}]
    mg['data'][0]['properties']['numericStart'] = lit('0D')
zb = copy.deepcopy(rb)
zb['name'] = hid(PG, 'zerar')
zb['displayName'] = 'Decision Simulator · Zerar cenário'
names = [x[0] for x in PARAM]
zb['options']['targetVisualNames'] = names
vc = zb['explorationState']['sections'][PG]['visualContainers']
for k in list(vc):
    if k not in names:
        vc.pop(k)
p.bookmarks.append(zb)
p.vis['nxSimZerar']['visual']['visualContainerObjects']['visualLink'][0]['properties'].update({'type': s('Bookmark'), 'bookmark': s(zb['name'])})

# Resumo base x simulado
p.html('nxSimResumo', 442, 212, 720, 470, 'UX Simulador Resumo')
p.vis['nxSimResumo']['visual']['visualContainerObjects'] = dict(CARD)

# Ponte do resultado (Deneb: base e total em azul, efeitos em verde/vermelho; soma fecha no simulado)
ETAPAS = ["Resultado base", "Preço", "Desconto", "Volume", "Custo da mercadoria", "Frete", "Despesas", "Resultado simulado"]
WF = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "isValid(datum['Sim Valor Etapa'])"},
                  {"calculate": "datum['Sim Valor Etapa'] / 1000", "as": "v"},
                  {"window": [{"op": "sum", "field": "v", "as": "fim"}], "sort": [{"field": "Ordem"}], "frame": [None, 0]},
                  {"calculate": "datum.fim - datum.v", "as": "ini"},
                  {"calculate": "datum.Ordem == 1 ? 'total' : (datum.v >= 0 ? 'pos' : 'neg')", "as": "tipo"}],
    "encoding": {"x": {"field": "Etapa", "type": "nominal", "sort": ETAPAS, "title": None,
                       "scale": {"domain": ETAPAS, "paddingInner": 0.3},
                       "axis": {"labelAngle": 0, "labelColor": "#C9D6E3", "labelFontSize": 10, "labelLimit": 120,
                                "labelExpr": "{'Custo da mercadoria': ['Custo da', 'mercadoria'], 'Resultado base': ['Resultado', 'base'], 'Resultado simulado': ['Resultado', 'simulado']}[datum.label] || datum.label"}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadius": 2},
         "encoding": {"y": {"field": "ini", "type": "quantitative", "title": None, "axis": {"labelExpr": "pbiFormat(datum.value, '#,0') + ' mil'", "grid": True, "tickCount": 5}},
                      "y2": {"field": "fim"},
                      "color": {"field": "tipo", "type": "nominal", "legend": None,
                                "scale": {"domain": ["total", "pos", "neg"], "range": ["#5FA8E6", "#45D5A1", "#FF7285"]}},
                      "tooltip": [{"field": "Etapa"}, {"field": "Sim Valor Etapa", "title": "Efeito (R$)", "formatType": "pbiFormat", "format": "R$ #,0"}]}},
        {"mark": {"type": "text", "dy": -8, "fontSize": 11, "color": "#FFFFFF"},
         "encoding": {"y": {"field": "fim", "type": "quantitative"}, "text": {"field": "v", "type": "quantitative", "formatType": "pbiFormat", "format": "+#,0;-#,0;0"}}},
        {"transform": [{"aggregate": [{"op": "sum", "field": "v", "as": "fim"}]}, {"calculate": "'Resultado simulado'", "as": "Etapa"},
                       {"calculate": "0", "as": "ini"}],
         "layer": [{"mark": {"type": "bar", "cornerRadius": 2, "color": "#5FA8E6"},
                    "encoding": {"y": {"field": "ini", "type": "quantitative"}, "y2": {"field": "fim"},
                                 "tooltip": [{"field": "Etapa"}, {"field": "fim", "title": "R$ mil", "formatType": "pbiFormat", "format": "#,0"}]}},
                   {"mark": {"type": "text", "dy": -8, "fontSize": 11, "fontWeight": 600, "color": "#FFFFFF"},
                    "encoding": {"y": {"field": "fim", "type": "quantitative"}, "text": {"field": "fim", "type": "quantitative", "formatType": "pbiFormat", "format": "#,0"}}}]},
        {"mark": {"type": "rule", "color": "#A9B9CA"}, "encoding": {"y": {"datum": 0}}}]}
deneb(p, 'nxSimPonte', 1178, 212, 696, 470,
      [col('Sim Etapa', 'Etapa'), col('Sim Etapa', 'Ordem'), meas('Sim Valor Etapa')], WF,
      'Do resultado base ao simulado: efeito de cada premissa (R$ mil)')

# Sensibilidade preco x volume (Deneb)
HM = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "isValid(datum['Sim Δ Resultado (grade)'])"},
                  {"calculate": "datum['Sim Δ Resultado (grade)'] / 1000000", "as": "mi"}],
    "encoding": {"x": {"field": "Preço grade %", "type": "ordinal", "title": "Variação de preço", "axis": {"format": "+.0%", "labelAngle": 0, "orient": "top"}},
                 "y": {"field": "Volume grade %", "type": "ordinal", "title": "Variação de volume", "sort": "descending", "axis": {"format": "+.0%"}}},
    "layer": [
        {"mark": {"type": "rect", "cornerRadius": 3, "stroke": "#071528", "strokeWidth": 2},
         "encoding": {"color": {"field": "mi", "type": "quantitative", "title": "Δ resultado (R$ mi)",
                                "scale": {"type": "symlog", "domainMid": 0, "range": ["#FF7285", "#12304F", "#45D5A1"]},
                                "legend": {"orient": "right", "direction": "vertical", "gradientLength": 180, "format": ",.0f"}},
                      "tooltip": [{"field": "Preço grade %", "title": "Preço", "format": "+.0%"}, {"field": "Volume grade %", "title": "Volume", "format": "+.0%"},
                                  {"field": "Sim Δ Resultado (grade)", "title": "Δ resultado", "formatType": "pbiFormat", "format": "R$ #,0"}]}},
        {"mark": {"type": "text", "fontSize": 10},
         "encoding": {"text": {"field": "mi", "type": "quantitative", "format": "+,.1f"},
                      "color": {"condition": {"test": "abs(datum.mi) < 1", "value": "#A9B9CA"}, "value": "#FFFFFF"}}}]}
deneb(p, 'nxSimGrade', 442, 698, 1432, 358,
      [col('Sim Grade Preço', 'Preço grade %'), col('Sim Grade Volume', 'Volume grade %'), meas('Sim Δ Resultado (grade)')], HM,
      'Sensibilidade: variação do resultado operacional por preço × volume (R$ mi), com desconto, custo, frete e despesas dos controles')
p.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgWarehouse', 'pgFinancial', 'pgPredictive', 'pgSimulator',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora', 'ttMesFinanceiro', 'ttEstoqueMes'])
print('simulator ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
