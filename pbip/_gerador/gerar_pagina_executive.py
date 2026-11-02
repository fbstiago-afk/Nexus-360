# NEXUS 360 - Gera a pagina Executive Command Center (PBIR) + tema + fundo
# Uso: python3 -I gerar_pagina_executive.py <raiz_projeto>
import sys, os, json, shutil

RAIZ = sys.argv[1]
REP = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report')
DEF = os.path.join(REP, 'definition')
SV = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json'
SP = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json'
PAGE = 'pgExecutive'
HTML = 'htmlContent443BE3AD55E043BF878BED274D3A6865'
DENEB = 'deneb7E15AEF80B9E4D4F8E12924291ECE89A'


def lit(v):
    return {'expr': {'Literal': {'Value': v}}}


def s(v):
    return lit("'" + str(v).replace("'", "''") + "'")


def num(v):
    return lit('%sD' % v)


def color(c):
    return {'solid': {'color': s(c)}}


def meas(p):
    return {'Measure': {'Expression': {'SourceRef': {'Entity': '_Medidas'}}, 'Property': p}}


def col(t, c):
    return {'Column': {'Expression': {'SourceRef': {'Entity': t}}, 'Property': c}}


def proj(field, display=None):
    k = 'Measure' if 'Measure' in field else 'Column'
    ent = field[k]['Expression']['SourceRef']['Entity']
    prop = field[k]['Property']
    p = {'field': field, 'queryRef': '%s.%s' % (ent, prop), 'nativeQueryRef': prop}
    if display:
        p['displayName'] = display
    return p


def cat_filter(name, table, column, values):
    vals = [[{'Literal': {'Value': v}}] for v in values]
    return {'name': name, 'field': col(table, column), 'type': 'Categorical',
            'filter': {'Version': 2, 'From': [{'Name': 't', 'Entity': table, 'Type': 0}],
                       'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 't'}}, 'Property': column}}],
                                                       'Values': vals}}}]}}


def title(text, show=True):
    return [{'properties': {'show': lit('true' if show else 'false'), 'text': s(text)}}]


VIS = {}
GROUPS = {}


def add(name, x, y, w, h, z, visual, container=None, filters=None, hidden=False, parent=None, extra=None):
    if parent:  # PBIR: posicao de filhos e relativa ao grupo
        x, y = x - GROUPS[parent][0], y - GROUPS[parent][1]
    v = {'$schema': SV, 'name': name, 'position': {'x': x, 'y': y, 'z': z, 'height': h, 'width': w, 'tabOrder': z}}
    if visual is not None:
        if container:
            visual['visualContainerObjects'] = container
        v['visual'] = visual
    if filters:
        v['filterConfig'] = {'filters': filters}
    if hidden:
        v['isHidden'] = True
    if parent:
        v['parentGroupName'] = parent
    if extra:
        v.update(extra)
    VIS[name] = v


def html_visual(measure):
    return {'visualType': HTML, 'query': {'queryState': {'content': {'projections': [proj(meas(measure))]}}},
            'objects': {'compatibility': [{'properties': {'legacyRendering': lit('false')}}]}, 'drillFilterOtherVisuals': True}


def group(name, display, x, y, w, h, z, hidden=True):
    GROUPS[name] = (x, y)
    v = {'$schema': SV, 'name': name, 'position': {'x': x, 'y': y, 'z': z, 'height': h, 'width': w, 'tabOrder': z},
         'visualGroup': {'displayName': display, 'groupMode': 'ScaleMode'}}
    if hidden:
        v['isHidden'] = True
    VIS[name] = v


def panel_bg(name, x, y, w, h, z, parent):
    add(name, x, y, w, h, z, {'visualType': 'shape', 'objects': {
        'shape': [{'properties': {'tileShape': s('rectangleRounded')}}],
        'fill': [{'properties': {'show': lit('false')}}],
        'outline': [{'properties': {'show': lit('false')}}]}},
        container={'background': [{'properties': {'show': lit('true'), 'color': color('#0A1C33'), 'transparency': num(2)}}],
                   'border': [{'properties': {'show': lit('true'), 'color': color('#10D4C4'), 'radius': num(12)}}],
                   'title': [{'properties': {'show': lit('false')}}],
                   'visualHeader': [{'properties': {'show': lit('false')}}]}, parent=parent)


def textbox(name, x, y, w, h, z, text, size='15pt', parent=None, colorhex='#FFFFFF'):
    add(name, x, y, w, h, z, {'visualType': 'textbox', 'objects': {'general': [{'properties': {'paragraphs': [
        {'textRuns': [{'value': text, 'textStyle': {'fontFamily': 'Segoe UI Semibold', 'fontSize': size, 'color': colorhex}}]}]}}]}},
        container={'background': [{'properties': {'show': lit('false')}}], 'title': [{'properties': {'show': lit('false')}}],
                   'visualHeader': [{'properties': {'show': lit('false')}}]}, parent=parent)


def button(name, x, y, w, h, z, tooltip, parent=None, label=None, link=None):
    objs = {
        'icon': [{'properties': {'show': lit('false')}}],
        'outline': [{'properties': {'show': lit('false')}}],
        'fill': [{'properties': {'show': lit('true'), 'fillColor': color('#10D4C4'), 'transparency': num(100)}, 'selector': {'id': 'default'}},
                 {'properties': {'fillColor': color('#10D4C4'), 'transparency': num(84)}, 'selector': {'id': 'hover'}},
                 {'properties': {'fillColor': color('#10D4C4'), 'transparency': num(72)}, 'selector': {'id': 'selected'}}],
    }
    if label:
        objs['text'] = [{'properties': {'show': lit('true'), 'text': s(label), 'fontColor': color('#C9D6E3'), 'fontSize': num(11), 'fontFamily': s('Segoe UI Semibold')}}]
    else:
        objs['text'] = [{'properties': {'show': lit('false')}}]
    cont = {'title': [{'properties': {'show': lit('false')}}], 'background': [{'properties': {'show': lit('false')}}],
            'border': [{'properties': {'show': lit('false')}}], 'visualHeader': [{'properties': {'show': lit('false')}}]}
    vl = {'show': lit('true'), 'tooltip': s(tooltip)}
    if link:
        vl.update(link)
    cont['visualLink'] = [{'properties': vl}]
    add(name, x, y, w, h, z, {'visualType': 'actionButton', 'objects': objs, 'drillFilterOtherVisuals': True}, container=cont, parent=parent)


def slicer(name, x, y, w, h, z, table, column, display, mode='Basic', horizontal=False, default=None, parent=None):
    general = {'orientation': num(1 if horizontal else 0)}
    if default:
        f = cat_filter('x', table, column, default)['filter']
        general['filter'] = {'filter': f}
    add(name, x, y, w, h, z, {'visualType': 'slicer',
                             'query': {'queryState': {'Values': {'projections': [dict(proj(col(table, column), display), active=True)]}}},
                             'objects': {'data': [{'properties': {'mode': s(mode)}}],
                                         'general': [{'properties': general}],
                                         'selection': [{'properties': {'selectAllCheckboxEnabled': lit('false'), 'singleSelect': lit('false')}}],
                                         'header': [{'properties': {'show': lit('true'), 'fontColor': color('#A9B9CA'), 'textSize': num(10)}}],
                                         'items': [{'properties': {'fontColor': color('#FFFFFF'), 'background': color('#0A1C33'), 'textSize': num(10)}}]},
                             'drillFilterOtherVisuals': True},
        container={'title': [{'properties': {'show': lit('false')}}], 'background': [{'properties': {'show': lit('false')}}],
                   'border': [{'properties': {'show': lit('false')}}], 'visualHeader': [{'properties': {'show': lit('false')}}]}, parent=parent)


# ---------------- layout (canvas 1920x1080; fundo analitico ampliado 1,148x)
# Cabecalho no slot do titulo do fundo (586-1596 x 23-99)
add('nxHeader', 600, 30, 966, 62, 1000, html_visual('UX Cabeçalho'),
    filters=[cat_filter('fPagina', 'dPaginaUX', 'Pagina', ["'Executive Command Center'"])])
# Barra de filtros ativos (46-1889 x 126-195; icone ate x=150)
add('nxFiltrosAtivos', 162, 134, 1712, 54, 1001, html_visual('UX Filtros Ativos'))

# Cards KPI
KPIS = ['Receita', 'Margem', 'Resultado', 'OTIF', 'Clientes']
for i, k in enumerate(KPIS):
    add('nxCard%s' % k, 46 + i * 369, 212, 352, 150, 1010 + i, html_visual('UX Card KPI'),
        filters=[cat_filter('fKPI', 'dKPI', 'KPI', ["'%s'" % k])])

# Evolucao mensal (combo nativo)
add('nxEvolucao', 46, 378, 1100, 330, 1100, {
    'visualType': 'lineClusteredColumnComboChart',
    'query': {'queryState': {
        'Category': {'projections': [dict(proj(col('dCalendario', 'MesAno'), 'Mês'), active=True)]},
        'Y': {'projections': [proj(meas('Receita Líquida'))]},
        'Y2': {'projections': [proj(meas('Margem Bruta %')), proj(meas('Meta Margem Bruta % (ponderada)'), 'Meta de margem')]}},
        'sortDefinition': {'sort': [{'field': col('dCalendario', 'MesAno'), 'direction': 'Ascending'}]}},
    'objects': {
        'dataPoint': [{'properties': {'fill': color('#0878C9')}, 'selector': {'metadata': '_Medidas.Receita Líquida'}},
                      {'properties': {'fill': color('#10D4C4')}, 'selector': {'metadata': '_Medidas.Margem Bruta %'}},
                      {'properties': {'fill': color('#FFC66D')}, 'selector': {'metadata': '_Medidas.Meta Margem Bruta % (ponderada)'}}],
        'lineStyles': [{'properties': {'strokeWidth': num(2), 'showMarker': lit('false')}},
                       {'properties': {'lineStyle': s('dashed')}, 'selector': {'metadata': '_Medidas.Meta Margem Bruta % (ponderada)'}}],
        'valueAxis': [{'properties': {'show': lit('true'), 'secShow': lit('true'), 'labelDisplayUnits': num(1000000), 'gridlineShow': lit('true')}}],
        'legend': [{'properties': {'show': lit('true'), 'position': s('Top')}}],
        'labels': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Receita líquida e margem bruta por mês')},
    filters=[cat_filter('fRealizado', 'dCalendario', 'FlagRealizado', ['1L'])])

# Bullet Deneb: receita vs meta por filial
SPEC = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"name": "dataset"},
    "transform": [
        {"filter": "isValid(datum['Meta Faturamento (até corte)']) && datum['Meta Faturamento (até corte)'] > 0"},
        {"calculate": "replace(datum['Filial'], 'Unidade ', '')", "as": "fil"},
        {"calculate": "datum['Receita Líquida'] / datum['Meta Faturamento (até corte)']", "as": "ating"},
        {"calculate": "datum.ating >= 1 ? 'Meta atingida' : (datum.ating >= 0.95 ? 'Até 5% abaixo' : 'Mais de 5% abaixo')", "as": "faixa"},
        {"calculate": "max(datum['Receita Líquida'], datum['Meta Faturamento (até corte)'])", "as": "xlabel"}
    ],
    "width": "container",
    "height": "container",
    "encoding": {
        "y": {"field": "fil", "type": "nominal", "sort": {"field": "ating", "op": "max", "order": "ascending"},
              "axis": {"title": None, "domain": False, "ticks": False, "labelPadding": 8, "labelColor": "#C9D6E3", "labelFontSize": 11}}
    },
    "layer": [
        {"mark": {"type": "bar", "color": "#173B5C", "cornerRadiusEnd": 3, "height": {"band": 0.7}},
         "encoding": {"x": {"field": "Meta Faturamento (até corte)", "type": "quantitative", "title": None,
                            "axis": {"labelExpr": "pbiFormat(datum.value / 1000000, '#,0') + ' mi'", "labelColor": "#A9B9CA", "grid": True,
                                     "gridColor": "#173B5C", "gridDash": [2, 3], "domain": False, "ticks": False, "tickCount": 5}}}},
        {"mark": {"type": "bar", "cornerRadiusEnd": 2, "height": {"band": 0.34}},
         "encoding": {"x": {"field": "Receita Líquida", "type": "quantitative"},
                      "color": {"field": "faixa", "type": "nominal",
                                "scale": {"domain": ["Meta atingida", "Até 5% abaixo", "Mais de 5% abaixo"], "range": ["#45D5A1", "#FFC66D", "#FF7285"]},
                                "legend": {"orient": "top", "title": None, "labelColor": "#A9B9CA", "symbolType": "square", "labelFontSize": 11}},
                      "tooltip": [{"field": "Filial", "title": "Filial"},
                                  {"field": "Receita Líquida", "title": "Receita", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "Meta Faturamento (até corte)", "title": "Meta", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "ating", "title": "Atingimento", "formatType": "pbiFormat", "format": "0.0%"}]}},
        {"mark": {"type": "tick", "color": "#FFFFFF", "thickness": 2, "size": 16},
         "encoding": {"x": {"field": "Meta Faturamento (até corte)", "type": "quantitative"}}},
        {"mark": {"type": "text", "align": "left", "dx": 8, "fontSize": 11, "fontWeight": 600},
         "encoding": {"x": {"field": "xlabel", "type": "quantitative"},
                      "text": {"field": "ating", "formatType": "pbiFormat", "format": "0.0%"},
                      "color": {"field": "faixa", "type": "nominal", "legend": None,
                                "scale": {"domain": ["Meta atingida", "Até 5% abaixo", "Mais de 5% abaixo"], "range": ["#45D5A1", "#FFC66D", "#FF7285"]}}}}
    ]
}
CONFIG = {"autosize": {"type": "fit", "contains": "padding"}, "view": {"stroke": None}, "font": "Segoe UI", "background": None,
          "padding": {"left": 4, "right": 46, "top": 4, "bottom": 4}, "legend": {"labelFont": "Segoe UI"}, "axis": {"labelFont": "Segoe UI"}}
add('nxBulletFiliais', 1162, 378, 712, 330, 1101, {
    'visualType': DENEB,
    'query': {'queryState': {'dataset': {'projections': [
        dict(proj(col('dFilial', 'Filial')), active=True),
        proj(meas('Receita Líquida')), proj(meas('Meta Faturamento (até corte)')), proj(meas('Atingimento Meta Faturamento %'))]}}},
    'objects': {'vega': [{'properties': {
        'provider': s('vegaLite'), 'jsonSpec': s(json.dumps(SPEC, ensure_ascii=False)), 'jsonConfig': s(json.dumps(CONFIG)),
        'renderMode': s('svg'), 'isNewDialogOpen': lit('false'), 'enableTooltips': lit('true'), 'enableContextMenu': lit('true'),
        'enableSelection': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Receita vs meta por filial (até o corte)')})

# Waterfall DRE gerencial
add('nxDRE', 46, 724, 900, 332, 1102, {
    'visualType': 'waterfallChart',
    'query': {'queryState': {
        'Category': {'projections': [dict(proj(col('dLinhaDRE', 'Linha'), 'Linha'), active=True)]},
        'Y': {'projections': [proj(meas('Valor DRE Gerencial'), 'Valor')]}},
        'sortDefinition': {'sort': [{'field': col('dLinhaDRE', 'Linha'), 'direction': 'Ascending'}]}},
    'objects': {'labels': [{'properties': {'show': lit('true'), 'labelDisplayUnits': num(1000000), 'labelPrecision': lit('1L'), 'color': color('#FFFFFF')}}],
                'valueAxis': [{'properties': {'show': lit('true'), 'labelDisplayUnits': num(1000000)}}],
                'categoryAxis': [{'properties': {'show': lit('true')}}],
                'legend': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Da receita ao resultado gerencial (R$ mi, não contábil)')})

# Matriz de sinais de risco
VALS = [('Margem Bruta %', 'Margem'), ('Desvio Margem vs Meta (p.p.)', 'Δ meta (p.p.)'), ('OTIF %', 'OTIF'),
        ('Desvio OTIF vs Meta (p.p.)', 'Δ meta OTIF (p.p.)'), ('Inadimplência % (Data Ref.)', 'Inadimplência'), ('Devolução % Receita', 'Devolução')]
COLORS = {'Desvio Margem vs Meta (p.p.)': 'UX Cor Desvio Margem', 'Desvio OTIF vs Meta (p.p.)': 'UX Cor Desvio OTIF',
          'Inadimplência % (Data Ref.)': 'UX Cor Inadimplência'}
values_objs = [{'properties': {'fontColor': {'solid': {'color': {'expr': meas(cm)}}}},
                'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': '_Medidas.' + m}} for m, cm in COLORS.items()]
add('nxRiscos', 962, 724, 912, 332, 1103, {
    'visualType': 'pivotTable',
    'query': {'queryState': {
        'Rows': {'projections': [dict(proj(col('dFilial', 'Cidade'), 'Filial'), active=True)]},
        'Values': {'projections': [proj(meas(m), d) for m, d in VALS]}},
        'sortDefinition': {'sort': [{'field': meas('Desvio Margem vs Meta (p.p.)'), 'direction': 'Ascending'}]}},
    'objects': {'values': values_objs,
                'columnHeaders': [{'properties': {'alignment': s('Center'), 'wordWrap': lit('true'), 'fontSize': num(10)}}],
                'grid': [{'properties': {'rowPadding': num(2), 'textSize': num(10)}}],
                'rowHeaders': [{'properties': {'alignment': s('Left')}}],
                'subTotals': [{'properties': {'rowSubtotals': lit('true')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Sinais de risco por filial')})

# Botoes sobre os icones do fundo (transparentes, realce no hover)
button('nxBtnFiltros', 1637, 22, 74, 78, 2000, 'Abrir painel de filtros')
button('nxBtnInfo', 1729, 22, 76, 78, 2001, 'Sobre esta página')
button('nxBtnHome', 1823, 22, 74, 78, 2002, 'Ir para a Home')
button('nxBtnNav', 60, 136, 82, 50, 2003, 'Navegar entre páginas')

# Painel de filtros (oculto)
group('grpFiltros', 'Painel Filtros', 1494, 212, 380, 844, 3000)
panel_bg('nxFiltrosFundo', 1494, 212, 380, 844, 3001, 'grpFiltros')
textbox('nxFiltrosTitulo', 1514, 226, 220, 40, 3002, 'Filtros', parent='grpFiltros')
button('nxFiltrosFechar', 1774, 230, 84, 32, 3003, 'Fechar painel', parent='grpFiltros', label='Fechar  ✕')
slicer('nxSlAno', 1514, 276, 340, 76, 3004, 'dCalendario', 'Ano', 'Ano', horizontal=True, default=['2026L'], parent='grpFiltros')
slicer('nxSlMes', 1514, 360, 340, 70, 3005, 'dCalendario', 'MesAno', 'Mês', mode='Dropdown', parent='grpFiltros')
slicer('nxSlRegiao', 1514, 440, 340, 120, 3006, 'dFilial', 'Regiao', 'Região', parent='grpFiltros')
slicer('nxSlFilial', 1514, 568, 340, 300, 3007, 'dFilial', 'Filial', 'Filial', parent='grpFiltros')
slicer('nxSlCategoria', 1514, 876, 340, 100, 3008, 'dProduto', 'Categoria', 'Categoria', mode='Dropdown', parent='grpFiltros')
button('nxFiltrosLimpar', 1514, 992, 340, 40, 3009, 'Limpar todas as seleções', parent='grpFiltros', label='Limpar filtros',
       link={'type': s('ClearAllSlicers')})

# Painel de informacoes (oculto)
group('grpInfo', 'Painel Info', 1394, 212, 480, 844, 3100)
panel_bg('nxInfoFundo', 1394, 212, 480, 844, 3101, 'grpInfo')
button('nxInfoFechar', 1774, 230, 84, 32, 3103, 'Fechar painel', parent='grpInfo', label='Fechar  ✕')
add('nxInfoConteudo', 1404, 262, 460, 784, 3102, html_visual('UX Info Página'), parent='grpInfo',
    filters=[cat_filter('fPagina', 'dPaginaUX', 'Pagina', ["'Executive Command Center'"])])

# Painel de navegacao (oculto)
group('grpNav', 'Painel Navegacao', 46, 212, 340, 260, 3200)
panel_bg('nxNavFundo', 46, 212, 340, 260, 3201, 'grpNav')
textbox('nxNavTitulo', 66, 226, 200, 40, 3202, 'Páginas', parent='grpNav')
button('nxNavFechar', 286, 230, 84, 32, 3203, 'Fechar painel', parent='grpNav', label='Fechar  ✕')
add('nxNavegador', 66, 276, 300, 180, 3204, {'visualType': 'pageNavigator', 'drillFilterOtherVisuals': True},
    container={'title': [{'properties': {'show': lit('false')}}], 'background': [{'properties': {'show': lit('false')}}],
               'border': [{'properties': {'show': lit('false')}}], 'visualHeader': [{'properties': {'show': lit('false')}}]},
    parent='grpNav')

# ---------------- escrita
pdir = os.path.join(DEF, 'pages', PAGE)
if os.path.exists(pdir):
    raise SystemExit('pagina ja existe: ' + pdir)
os.makedirs(os.path.join(pdir, 'visuals'))
page = {'$schema': SP, 'name': PAGE, 'displayName': 'Executive Command Center', 'displayOption': 'FitToPage', 'height': 1080, 'width': 1920,
        'objects': {
            'background': [{'properties': {'image': {'image': {'name': s('bg_analitico_1920x1080.jpg'),
                                                               'url': {'expr': {'ResourcePackageItem': {'PackageName': 'RegisteredResources', 'PackageType': 1, 'ItemName': 'bg_analitico_1920x1080.jpg'}}},
                                                               'scaling': s('Fit')}},
                                           'transparency': num(0)}}],
            'outspace': [{'properties': {'color': color('#071528'), 'transparency': num(0)}}]}}
json.dump(page, open(os.path.join(pdir, 'page.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
for n, v in VIS.items():
    d = os.path.join(pdir, 'visuals', n)
    os.makedirs(d)
    json.dump(v, open(os.path.join(d, 'visual.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

pj = os.path.join(DEF, 'pages', 'pages.json')
pages = json.load(open(pj, encoding='utf-8'))
pages['pageOrder'] = [PAGE] + [p for p in pages['pageOrder'] if p != PAGE]
pages['activePageName'] = PAGE
json.dump(pages, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# tema e imagem como recursos registrados
rr = os.path.join(REP, 'StaticResources', 'RegisteredResources')
os.makedirs(rr, exist_ok=True)
shutil.copyfile(os.path.join(RAIZ, 'tema', 'NEXUS360_Theme.json'), os.path.join(rr, 'NEXUS360_Theme.json'))
shutil.copyfile(os.path.join(RAIZ, 'assets', 'img', 'bg_analitico_1920x1080.jpg'), os.path.join(rr, 'bg_analitico_1920x1080.jpg'))
rj = os.path.join(DEF, 'report.json')
rep = json.load(open(rj, encoding='utf-8'))
rep['themeCollection']['customTheme'] = {'name': 'NEXUS360_Theme.json', 'reportVersionAtImport': rep['themeCollection']['baseTheme']['reportVersionAtImport'],
                                         'type': 'RegisteredResources'}
pk = [p for p in rep['resourcePackages'] if p['name'] != 'RegisteredResources']
pk.append({'name': 'RegisteredResources', 'type': 'RegisteredResources', 'items': [
    {'name': 'NEXUS360_Theme.json', 'path': 'NEXUS360_Theme.json', 'type': 'CustomTheme'},
    {'name': 'bg_analitico_1920x1080.jpg', 'path': 'bg_analitico_1920x1080.jpg', 'type': 'Image'}]})
rep['resourcePackages'] = pk
json.dump(rep, open(rj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('visuais', len(VIS))
