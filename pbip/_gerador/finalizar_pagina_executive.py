# NEXUS 360 - Ajustes pos-UI da pagina Executive: favoritos (exibicao apenas), acoes dos botoes, slicers, tooltip de filial
import json, os, glob, sys
D = sys.argv[1]
P = os.path.join(D, 'pages', 'pgExecutive', 'visuals')
lit = lambda v: {'expr': {'Literal': {'Value': v}}}
s = lambda v: lit("'" + v + "'")
def load(n): return json.load(open(os.path.join(P, n, 'visual.json'), encoding='utf-8'))
def save(n, v): json.dump(v, open(os.path.join(P, n, 'visual.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
# 1) favoritos: nomes e somente exibicao (sem dados)
BM = {}
nomes = {'grpFiltros': 'Painel Filtros', 'grpInfo': 'Painel Informações', 'grpNav': 'Painel Navegação'}
for f in glob.glob(os.path.join(D, 'bookmarks', '*.bookmark.json')):
    b = json.load(open(f, encoding='utf-8'))
    sec = b['explorationState']['sections']['pgExecutive']
    vis = [g for g, st in sec['visualContainerGroups'].items() if not st['isHidden']]
    key = vis[0] if vis else 'padrao'
    b['displayName'] = nomes.get(key, 'Padrão (painéis fechados)')
    b['options'] = {'targetVisualNames': [], 'suppressData': True}
    sec['visualContainers'] = {}
    BM[key] = b['name']
    json.dump(b, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('favoritos', BM)
# 2) acoes dos botoes
def link(btn, bookmark):
    v = load(btn)
    vl = v['visual']['visualContainerObjects']['visualLink'][0]['properties']
    vl['type'] = s('Bookmark'); vl['bookmark'] = s(bookmark)
    save(btn, v)
link('nxBtnFiltros', BM['grpFiltros']); link('nxBtnInfo', BM['grpInfo']); link('nxBtnNav', BM['grpNav'])
for b in ('nxFiltrosFechar', 'nxInfoFechar', 'nxNavFechar'):
    link(b, BM['padrao'])
v = load('nxBtnHome'); v['visual']['visualContainerObjects']['visualLink'][0]['properties']['tooltip'] = s('Home (disponível quando a página inicial for construída)'); save('nxBtnHome', v)
# 3) slicers de periodo somente com realizado (remove ano em branco e 2027)
flt = lambda: {'name': 'fRealizado', 'field': {'Column': {'Expression': {'SourceRef': {'Entity': 'dCalendario'}}, 'Property': 'FlagRealizado'}}, 'type': 'Categorical',
               'filter': {'Version': 2, 'From': [{'Name': 'c', 'Entity': 'dCalendario', 'Type': 0}],
                          'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'FlagRealizado'}}], 'Values': [[{'Literal': {'Value': '1L'}}]]}}}]}}
for n in ('nxSlAno', 'nxSlMes'):
    v = load(n); v['filterConfig'] = {'filters': [flt()]}; save(n, v)
# reposiciona Regiao/Filial (posicoes relativas ao grupo 1494,212)
v = load('nxSlRegiao'); v['position'].update({'y': 228, 'height': 140}); save('nxSlRegiao', v)
v = load('nxSlFilial'); v['position'].update({'y': 376, 'height': 280}); save('nxSlFilial', v)
# 4) pagina de tooltip de filial
tt = [p for p in glob.glob(os.path.join(D, 'pages', '*', 'page.json')) if json.load(open(p, encoding='utf-8')).get('type') == 'Tooltip'][0]
pg = json.load(open(tt, encoding='utf-8')); pg.update({'width': 320, 'height': 200, 'displayOption': 'ActualSize'})
pg['objects'] = {'background': [{'properties': {'color': {'solid': {'color': s('#0A1C33')}}, 'transparency': lit('0D')}}]}
json.dump(pg, open(tt, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
vd = os.path.join(os.path.dirname(tt), 'visuals', 'nxTooltipFilial'); os.makedirs(vd, exist_ok=True)
json.dump({'$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json',
           'name': 'nxTooltipFilial', 'position': {'x': 0, 'y': 0, 'z': 0, 'height': 200, 'width': 320, 'tabOrder': 0},
           'visual': {'visualType': 'htmlContent443BE3AD55E043BF878BED274D3A6865',
                      'query': {'queryState': {'content': {'projections': [{'field': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Medidas'}}, 'Property': 'UX Tooltip Filial'}},
                                                                             'queryRef': '_Medidas.UX Tooltip Filial', 'nativeQueryRef': 'UX Tooltip Filial'}]}}},
                      'objects': {'compatibility': [{'properties': {'legacyRendering': lit('false')}}]}, 'drillFilterOtherVisuals': True}},
          open(os.path.join(vd, 'visual.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
# 5) matriz usa o tooltip de filial
v = load('nxRiscos')
v['visual']['visualContainerObjects']['visualTooltip'] = [{'properties': {'show': lit('true'), 'type': s('ReportPage'), 'section': s(pg['name'])}}]
save('nxRiscos', v)
print('tooltip', pg['name'])
