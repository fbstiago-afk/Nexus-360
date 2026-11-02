# NEXUS 360 - Aplica UMA VEZ o padrao de nx_estilo aos arquivos ja gerados (visuais, medidas, formatos, tema).
# Os geradores aplicam o mesmo padrao na escrita; este script so atualiza o que ja existe. Protegido por marcador.
import os, sys, json, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nx_estilo

RAIZ = sys.argv[1]
MARCA = os.path.join(RAIZ, 'pbip', '_gerador', '.estilo_aplicado_20261102')
if os.path.exists(MARCA):
    raise SystemExit('padrao ja aplicado (%s)' % MARCA)
SM = os.path.join(RAIZ, 'pbip', 'NEXUS360.SemanticModel', 'definition')
RP = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report')
n = {'visuais': 0, 'tmdl': 0, 'tema': 0}

# visuais
for f in glob.glob(os.path.join(RP, 'definition', 'pages', '*', 'visuals', '*', 'visual.json')):
    v = json.load(open(f, encoding='utf-8'))
    json.dump(nx_estilo.visual(v), open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    n['visuais'] += 1

# TMDL: formatos de todas as tabelas; HTML/FORMAT nas medidas
for f in glob.glob(os.path.join(SM, 'tables', '*.tmdl')):
    raw = open(f, encoding='utf-8-sig').read()
    t = re.sub(r'(formatString: )(.*)', lambda m: m.group(1) + nx_estilo.fmt(m.group(2)), raw)
    if os.path.basename(f) == '_Medidas.tmdl':
        t = nx_estilo.dax(t)
    if t != raw:
        open(f, 'w', encoding='utf-8').write(t)
        n['tmdl'] += 1

# tema (copia registrada no relatorio e copia em tema/)
for f in [os.path.join(RP, 'StaticResources', 'RegisteredResources', 'NEXUS360_Theme.json'), os.path.join(RAIZ, 'tema', 'NEXUS360_Theme.json')]:
    if os.path.exists(f):
        t = json.load(open(f, encoding='utf-8'))
        json.dump(nx_estilo.tema(t), open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        n['tema'] += 1

open(MARCA, 'w').write(json.dumps(n))
print(n)
