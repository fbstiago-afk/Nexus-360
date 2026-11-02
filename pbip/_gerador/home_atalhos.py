# NEXUS 360 - Home: 4 atalhos (doc 04: "Marca, periodo historico, botao iniciar e 4 atalhos"). Acrescenta visuais a pagina existente.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import Pagina, s, lit, num, color, COR

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
VDIR = os.path.join(DEF, 'pages', 'pgHome', 'visuals')
ATALHOS = [('nxAtalhoComercial', 'Comercial', 'pgCommercial'), ('nxAtalhoClientes', 'Clientes', 'pgCustomer'),
           ('nxAtalhoLogistica', 'Logística', 'pgLogistics'), ('nxAtalhoFinanceiro', 'Financeiro', 'pgFinancial')]
p = Pagina('pgHome', 'Home')
x = 660
for (nm, rot, pg) in ATALHOS:
    p.button(nm, x, 754, 148, 54, 'Ir para %s' % rot, label=rot, size=12, fill_default=82,
             link={'type': s('PageNavigation'), 'navigationSection': s(pg)})
    o = p.vis[nm]['visual']['objects']
    o['outline'] = [{'properties': {'show': lit('true'), 'lineColor': color(COR['teal']), 'transparency': num(45), 'weight': num(1)}}]
    o['shape'] = [{'properties': {'tileShape': s('rectangleRounded'), 'rectangleRoundedCurve': lit('27L')}}]
    o['text'][0]['properties']['fontColor'] = color('#FFFFFF')
    x += 158
for nm, v in p.vis.items():
    v['position']['z'] = 9000 + v['position']['z']
    v['position']['tabOrder'] = v['position']['z']
    d = os.path.join(VDIR, nm)
    os.makedirs(d, exist_ok=True)
    json.dump(v, open(os.path.join(d, 'visual.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('atalhos ok', len(p.vis))
