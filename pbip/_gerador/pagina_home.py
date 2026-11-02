# NEXUS 360 - Etapa A: Home (capa oficial, INICIAR, mapa SVG das filiais reais, faixa de indicadores)
# Uso: python3 -I pagina_home.py <raiz_projeto>
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import Pagina, register_page, register_image, s, lit, num, color, COR, NOCHROME

RAIZ = sys.argv[1]
REP = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report')
DEF = os.path.join(REP, 'definition')

register_image(REP, os.path.join(RAIZ, 'assets', 'img', 'bg_home_1920x1080.jpg'), 'bg_home_1920x1080.jpg')

p = Pagina('pgHome', 'Home', fundo='bg_home_1920x1080.jpg')
# Mapa real cobre o mapa ilustrativo da capa (pontos e rotas da arte nao sao filiais reais)
p.html('nxHomeMapa', 1318, 36, 584, 566, 'UX Home Mapa')  # detalhe por filial via <title> do SVG
# Indicadores reais (faixa inferior, sobre o piso da imagem)
p.html('nxHomeKPIs', 108, 884, 1188, 116, 'UX Home KPIs')
# INICIAR: area transparente exatamente sobre o botao desenhado na capa
p.button('nxIniciar', 130, 728, 498, 106, 'Iniciar: Executive Command Center',
         link={'type': s('PageNavigation'), 'navigationSection': s('pgExecutive')})
b = p.vis['nxIniciar']['visual']['objects']
b['shape'] = [{'properties': {'tileShape': s('rectangleRounded'), 'rectangleRoundedCurve': lit('50L')}}]
for f in b['fill']:
    if f['selector']['id'] == 'hover':
        f['properties']['transparency'] = num(88)
p.write(DEF, overwrite=True)

# Executive: botao Home passa a navegar para a Home
vp = os.path.join(DEF, 'pages', 'pgExecutive', 'visuals', 'nxBtnHome', 'visual.json')
v = json.load(open(vp, encoding='utf-8'))
vl = v['visual']['visualContainerObjects']['visualLink'][0]['properties']
vl.update({'type': s('PageNavigation'), 'navigationSection': s('pgHome'), 'tooltip': s('Ir para a Home')})
json.dump(v, open(vp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# Executive: slicers sincronizados com as demais paginas
for n, (t, c) in {'nxSlAno': ('dCalendario', 'Ano'), 'nxSlMes': ('dCalendario', 'MesAno'), 'nxSlRegiao': ('dFilial', 'Regiao'),
                  'nxSlFilial': ('dFilial', 'Filial'), 'nxSlCategoria': ('dProduto', 'Categoria')}.items():
    vp = os.path.join(DEF, 'pages', 'pgExecutive', 'visuals', n, 'visual.json')
    v = json.load(open(vp, encoding='utf-8'))
    v['visual']['syncGroup'] = {'groupName': '%s.%s' % (t, c), 'fieldChanges': True, 'filterChanges': True}
    json.dump(v, open(vp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

register_page(DEF, 'pgHome', ['pgHome', 'pgExecutive', '2a6aff4ae45b2ec75c15'])
print('home ok', len(p.vis), 'visuais')
