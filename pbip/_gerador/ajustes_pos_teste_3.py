# NEXUS 360 - 02/11/2026: correcao do tooltip de pagina e do botao Limpar filtros
# Causa do tooltip: o Desktop grava "Pagina de relatorio" como type 'Canvas'. O valor 'ReportPage'
# e exibido no painel de formato como "Pagina de relatorio", mas nao aciona a pagina de tooltip.
import json, os, sys
D = sys.argv[1]  # pasta definition do relatorio
V = os.path.join(D, 'pages', 'pgExecutive', 'visuals')
lit = lambda v: {'expr': {'Literal': {'Value': v}}}
s = lambda v: lit("'" + v + "'")
def rw(p, f):
    v = json.load(open(p, encoding='utf-8')); f(v); json.dump(v, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
TT = '2a6aff4ae45b2ec75c15'
def tip(v):
    v['visual'].setdefault('visualContainerObjects', {})['visualTooltip'] = [{'properties': {'show': lit('true'), 'type': s('Canvas'), 'section': s(TT)}}]
rw(os.path.join(V, 'nxRiscos', 'visual.json'), tip)
for n in ('nxDRE', 'nxBulletFiliais'):  # experimentos desfeitos: tooltip padrao
    rw(os.path.join(V, n, 'visual.json'), lambda v: v['visual'].get('visualContainerObjects', {}).pop('visualTooltip', None))
# matriz: 12 filiais + cabecalho + total sem rolagem
def mat(v):
    o = v['visual']['objects']
    o.setdefault('grid', [{'properties': {}}])[0]['properties'].update({'rowPadding': lit('1D')})
    v['visual'].setdefault('visualContainerObjects', {})['padding'] = [{'properties': {'top': lit('8D'), 'bottom': lit('4D'), 'left': lit('12D'), 'right': lit('12D')}}]
rw(os.path.join(V, 'nxRiscos', 'visual.json'), mat)
# paginas: remove a pagina de teste da ordem
pj = os.path.join(D, 'pages', 'pages.json')
rw(pj, lambda p: p.update({'pageOrder': [x for x in p['pageOrder'] if os.path.isdir(os.path.join(D, 'pages', x))], 'activePageName': 'pgExecutive'}))
# favorito de redefinicao: so dados, so slicers, restaura Ano = 2026
B = os.path.join(D, 'bookmarks')
SL = ['nxSlAno', 'nxSlMes', 'nxSlRegiao', 'nxSlFilial', 'nxSlCategoria']
for f in os.listdir(B):
    if not f.endswith('.bookmark.json'): continue
    p = os.path.join(B, f); b = json.load(open(p, encoding='utf-8'))
    if b['displayName'] in ('Indicador 5', 'Redefinir filtros'):
        b['displayName'] = 'Redefinir filtros'
        b['options'] = {'targetVisualNames': SL, 'applyOnlyToTargetVisuals': True, 'suppressDisplay': True}
        json.dump(b, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        RESET = b['name']
def lim(v):
    vl = v['visual']['visualContainerObjects']['visualLink'][0]['properties']
    vl.update({'type': s('Bookmark'), 'bookmark': s(RESET), 'tooltip': s('Limpar seleções e voltar ao período padrão (2026)')})
rw(os.path.join(V, 'nxFiltrosLimpar', 'visual.json'), lim)
print('reset', RESET)
# titulo dinamico da cascata (medida UX Titulo DRE)
rw(os.path.join(V, 'nxDRE', 'visual.json'), lambda v: v['visual'].setdefault('visualContainerObjects', {}).setdefault('title', [{'properties': {}}])[0]['properties'].update(
    {'text': {'expr': {'Measure': {'Expression': {'SourceRef': {'Entity': '_Medidas'}}, 'Property': 'UX Título DRE'}}}}))
