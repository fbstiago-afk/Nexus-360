# NEXUS 360 - Ajustes P2/P3 da pagina Executive (02/11/2026)
# - combo com linhas lineares (o tema base Fluent2 define lineChartType=smooth para todos os visuais)
# - faixa inferior mais alta para a matriz caber as 12 filiais sem rolagem
# - cascata sem eixo de valores (rotulos de dados ja trazem os valores) e rotulos de categoria menores
import json, os, sys
R = sys.argv[1]  # pasta NEXUS360.Report
V = os.path.join(R, 'definition', 'pages', 'pgExecutive', 'visuals')
lit = lambda v: {'expr': {'Literal': {'Value': v}}}
def rw(n, f):
    p = os.path.join(V, n, 'visual.json'); v = json.load(open(p, encoding='utf-8')); f(v)
    json.dump(v, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
# grade vertical: linha de graficos 378-690 (312), faixa inferior 706-1056 (350)
POS = {'nxEvolucao': (46, 378, 1100, 312), 'nxBulletFiliais': (1162, 378, 712, 312),
       'nxDRE': (46, 706, 900, 350), 'nxRiscos': (962, 706, 912, 350)}
for n, (x, y, w, h) in POS.items():
    rw(n, lambda v, x=x, y=y, w=w, h=h: v['position'].update({'x': x, 'y': y, 'width': w, 'height': h}))
def combo(v):
    ls = v['visual']['objects'].setdefault('lineStyles', [{'properties': {}}])
    base = [e for e in ls if 'selector' not in e][0]
    base['properties']['lineChartType'] = lit("'linear'")
rw('nxEvolucao', combo)
def dre(v):
    o = v['visual']['objects']
    o['valueAxis'] = [{'properties': {'show': lit('false')}}]
    o['categoryAxis'] = [{'properties': {'show': lit('true'), 'fontSize': lit('9D'), 'labelColor': {'solid': {'color': lit("'#A9B9CA'")}}}}]
    o.setdefault('gridlines', [{'properties': {}}])
rw('nxDRE', dre)
def mat(v):
    g = v['visual']['objects'].setdefault('grid', [{'properties': {}}])[0]['properties']
    g['rowPadding'] = lit('2D')
rw('nxRiscos', mat)
# tema: interpolacao linear explicita
T = [os.path.join(R, 'StaticResources', 'RegisteredResources', 'NEXUS360_Theme.json')] + sys.argv[2:]
for t in T:
    th = json.load(open(t, encoding='utf-8'))
    vs = th['visualStyles']
    vs['*']['*']['lineStyles'] = [{'lineChartType': 'linear'}]
    vs['lineClusteredColumnComboChart']['*']['lineStyles'][0]['lineChartType'] = 'linear'
    json.dump(th, open(t, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok')
# titulos dos paineis: o traco de 4 px era a barra de rolagem da caixa de texto (15pt + preenchimento padrao > 40 px)
for n in ('nxFiltrosTitulo', 'nxNavTitulo'):
    def f(v):
        v['visual']['visualContainerObjects']['padding'] = [{'properties': {k: lit('0D') for k in ('top', 'bottom', 'left', 'right')}}]
        v['visual']['objects']['general'][0]['properties']['paragraphs'][0]['textRuns'][0]['textStyle']['fontSize'] = '14pt'
        v['position'].update({'y': 18, 'height': 36})
    rw(n, f)
print('titulos ok')
