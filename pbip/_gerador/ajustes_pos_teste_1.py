# Ajustes apos 1o teste no Desktop: botoes Fechar maiores, estilo do navegador de paginas
import json, sys, os
P = sys.argv[1]
lit = lambda v: {'expr': {'Literal': {'Value': v}}}
s = lambda v: lit("'" + v + "'")
col = lambda c: {'solid': {'color': s(c)}}
def rw(n, f):
    p = os.path.join(P, n, 'visual.json'); v = json.load(open(p, encoding='utf-8')); f(v)
    json.dump(v, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
larg = {'nxFiltrosFechar': 380, 'nxInfoFechar': 480, 'nxNavFechar': 340}
for n, w in larg.items():
    def f(v, w=w):
        v['position'].update({'x': w - 130, 'y': 14, 'width': 112, 'height': 40})
    rw(n, f)
def nav(v):
    st = lambda sel, fill, tr, fc, oc: {'properties': {'fillColor': col(fill), 'transparency': lit(f'{tr}D'), 'fontColor': col(fc), 'lineColor': col(oc)}, 'selector': {'id': sel}}
    v['visual']['objects'] = {
        'fill': [{'properties': {'show': lit('true'), 'fillColor': col('#0A1C33'), 'transparency': lit('0D')}, 'selector': {'id': 'default'}},
                 {'properties': {'fillColor': col('#10D4C4'), 'transparency': lit('80D')}, 'selector': {'id': 'hover'}},
                 {'properties': {'fillColor': col('#10D4C4'), 'transparency': lit('70D')}, 'selector': {'id': 'selected'}}],
        'text': [{'properties': {'show': lit('true'), 'fontColor': col('#C9D6E3'), 'fontSize': lit('11D'), 'fontFamily': s('Segoe UI Semibold'), 'horizontalAlignment': s('left')}, 'selector': {'id': 'default'}},
                 {'properties': {'fontColor': col('#FFFFFF')}, 'selector': {'id': 'selected'}}],
        'outline': [{'properties': {'show': lit('true'), 'lineColor': col('#173B5C'), 'weight': lit('1D'), 'transparency': lit('0D')}, 'selector': {'id': 'default'}},
                    {'properties': {'lineColor': col('#10D4C4')}, 'selector': {'id': 'selected'}}],
        'shape': [{'properties': {'tileShape': s('rectangleRounded'), 'rectangleRoundedCurve': lit('8L')}}],
        'layout': [{'properties': {'orientation': lit('1D'), 'cellPadding': lit('6D')}}],
        'pages': [{'properties': {'showHiddenPages': lit('false'), 'showTooltipPages': lit('false')}}]}
    v['position'].update({'height': 60})
rw('nxNavegador', nav)
print('ok')
# Texto de botao: o PBIR exige uma entrada 'show' sem seletor alem da entrada do estado default
for n in ('nxFiltrosFechar', 'nxInfoFechar', 'nxNavFechar', 'nxFiltrosLimpar'):
    def f(v):
        t = v['visual']['objects']['text']
        if not any('selector' not in e for e in t):
            t.append({'properties': {'show': lit('true')}})
    rw(n, f)
print('texto ok')
# Pagina de tooltip: pageBinding Tooltip + oculta no modo leitura
import glob
for pj in glob.glob(os.path.join(P, '..', '..', '*', 'page.json')):
    pg = json.load(open(pj, encoding='utf-8'))
    if pg.get('type') == 'Tooltip':
        pass  # o Desktop nao grava pageBinding em paginas de tooltip
        pg['visibility'] = 'HiddenInViewMode'
        json.dump(pg, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('tooltip page', pg['name'])
