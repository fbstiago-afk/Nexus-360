# NEXUS 360 - Ajustes de layout apos fontes maiores (02/11/2026): Executive (matriz sem rolagem) e subtitulo do cabecalho com reticencias.
import os, sys, json, re
RAIZ = sys.argv[1]
PG = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition', 'pages', 'pgExecutive', 'visuals')
POS = {'nxEvolucao': (46, 378, 780, 222), 'nxDRE': (842, 378, 1032, 222), 'nxBulletFiliais': (46, 616, 800, 440), 'nxRiscos': (862, 616, 1012, 440)}
for n, (x, y, w, h) in POS.items():
    f = os.path.join(PG, n, 'visual.json')
    v = json.load(open(f, encoding='utf-8'))
    v['position'].update({'x': x, 'y': y, 'width': w, 'height': h})
    json.dump(v, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
tm = os.path.join(RAIZ, 'pbip', 'NEXUS360.SemanticModel', 'definition', 'tables', '_Medidas.tmdl')
t = open(tm, encoding='utf-8-sig').read()
old = '.nx-h2{font-size:14.4px;color:#A9B9CA;margin-top:3px}'
if old in t:
    t = t.replace(old, '.nx-h2{font-size:14.4px;color:#A9B9CA;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:600px}')
    open(tm, 'w', encoding='utf-8').write(t)
    print('cabecalho ok')
print('layout ok')
