# NEXUS 360 - Biblioteca de componentes PBIR (paginas, visuais, paineis ocultos, favoritos)
# Consolida o gerador da pagina executiva e as licoes dos testes no Desktop 2.159 (out/2026):
#  - filhos de grupo usam posicao relativa ao grupo
#  - botao com texto precisa de uma entrada text.show sem seletor
#  - tooltip de pagina: visualTooltip.type = 'Canvas' ('ReportPage' nao aciona)
#  - favoritos de painel: so exibicao (suppressData), sem preserveNewVisualVisibility
#  - favorito "Redefinir filtros": so dados, so slicers, restaura o ano padrao
#  - slicers de periodo filtrados por FlagRealizado = 1
import nx_estilo
import os, json, hashlib, shutil

SV = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json'
SP = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json'
SB = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json'
HTML = 'htmlContent443BE3AD55E043BF878BED274D3A6865'
DENEB = 'deneb7E15AEF80B9E4D4F8E12924291ECE89A'
TT_FILIAL = '2a6aff4ae45b2ec75c15'
BG_ANALITICO = 'bg_analitico_1920x1080.jpg'
COR = dict(navy='#071528', card='#0A1C33', borda='#173B5C', teal='#10D4C4', azul='#0878C9', cinza='#A9B9CA', claro='#C9D6E3',
           pos='#45D5A1', alerta='#FFC66D', neg='#FF7285', azul2='#5FA8E6')


def lit(v):
    return {'expr': {'Literal': {'Value': v}}}


def s(v):
    return lit("'" + str(v).replace("'", "''") + "'")


def num(v):
    return lit('%sD' % v)


def color(c):
    return {'solid': {'color': s(c)}}


def meas(p, ent='_Medidas'):
    return {'Measure': {'Expression': {'SourceRef': {'Entity': ent}}, 'Property': p}}


def col(t, c):
    return {'Column': {'Expression': {'SourceRef': {'Entity': t}}, 'Property': c}}


def proj(field, display=None, active=None):
    k = 'Measure' if 'Measure' in field else 'Column'
    ent = field[k]['Expression']['SourceRef']['Entity']
    prop = field[k]['Property']
    p = {'field': field, 'queryRef': '%s.%s' % (ent, prop), 'nativeQueryRef': prop}
    if display:
        p['displayName'] = display
    if active is not None:
        p['active'] = active
    return p


def cat_filter(name, table, column, values):
    vals = [[{'Literal': {'Value': v}}] for v in values]
    return {'name': name, 'field': col(table, column), 'type': 'Categorical',
            'filter': {'Version': 2, 'From': [{'Name': 't', 'Entity': table, 'Type': 0}],
                       'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 't'}}, 'Property': column}}],
                                                       'Values': vals}}}]}}


def realizado():
    return cat_filter('fRealizado', 'dCalendario', 'FlagRealizado', ['1L'])


def title(text, show=True, measure=None):
    p = {'show': lit('true' if show else 'false')}
    if measure:
        p['text'] = {'expr': meas(measure)}
    elif text:
        p['text'] = s(text)
    return [{'properties': p}]


NOCHROME = {'title': [{'properties': {'show': lit('false')}}], 'background': [{'properties': {'show': lit('false')}}],
            'border': [{'properties': {'show': lit('false')}}], 'visualHeader': [{'properties': {'show': lit('false')}}]}


def hid(*parts):
    return hashlib.md5('|'.join(parts).encode()).hexdigest()[:20]


def tooltip_page(section=TT_FILIAL):
    return [{'properties': {'show': lit('true'), 'type': s('Canvas'), 'section': s(section)}}]


class Pagina:
    def __init__(self, nome, titulo, ux=None, fundo=BG_ANALITICO, tipo=None, w=1920, h=1080):
        self.nome, self.titulo, self.ux, self.fundo, self.tipo, self.w, self.h = nome, titulo, ux or titulo, fundo, tipo, w, h
        self.vis, self.groups, self.z = {}, {}, 1000
        self.bookmarks = []
        self.interactions = []

    # ---------- primitivas
    def nz(self):
        self.z += 1
        return self.z

    def add(self, name, x, y, w, h, visual, container=None, filters=None, hidden=False, parent=None, z=None):
        z = z or self.nz()
        if parent:
            gx, gy = self.groups[parent]
            x, y = x - gx, y - gy
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
        self.vis[name] = v
        return v

    def html(self, name, x, y, w, h, measure, filters=None, parent=None, tooltip=None, z=None):
        cont = None
        if tooltip:
            cont = {'visualTooltip': tooltip_page(tooltip)}
        return self.add(name, x, y, w, h, {'visualType': HTML, 'query': {'queryState': {'content': {'projections': [proj(meas(measure))]}}},
                                          'objects': {'compatibility': [{'properties': {'legacyRendering': lit('false')}}]},
                                          'drillFilterOtherVisuals': True}, container=cont, filters=filters, parent=parent, z=z)

    def ux_html(self, name, x, y, w, h, measure, parent=None):
        """HTML que depende da linha da pagina em dPaginaUX (cabecalho, informacoes)."""
        return self.html(name, x, y, w, h, measure, parent=parent,
                         filters=[cat_filter('fPagina', 'dPaginaUX', 'Pagina', ["'%s'" % self.ux.replace("'", "''")])])

    def group(self, name, display, x, y, w, h, hidden=True):
        self.groups[name] = (x, y)
        z = self.nz() + 20000
        v = {'$schema': SV, 'name': name, 'position': {'x': x, 'y': y, 'z': z, 'height': h, 'width': w, 'tabOrder': z},
             'visualGroup': {'displayName': display, 'groupMode': 'ScaleMode'}}
        if hidden:
            v['isHidden'] = True
        self.vis[name] = v

    def panel_bg(self, name, x, y, w, h, parent, transp=2):
        self.add(name, x, y, w, h, {'visualType': 'shape', 'objects': {
            'shape': [{'properties': {'tileShape': s('rectangleRounded')}}],
            'fill': [{'properties': {'show': lit('false')}}], 'outline': [{'properties': {'show': lit('false')}}]}},
            container={'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(transp)}}],
                       'border': [{'properties': {'show': lit('true'), 'color': color(COR['teal']), 'radius': num(12)}}],
                       'title': [{'properties': {'show': lit('false')}}], 'visualHeader': [{'properties': {'show': lit('false')}}]},
            parent=parent, z=1)

    def textbox(self, name, x, y, w, h, text, size='14pt', parent=None, colorhex='#FFFFFF'):
        self.add(name, x, y, w, h, {'visualType': 'textbox', 'objects': {'general': [{'properties': {'paragraphs': [
            {'textRuns': [{'value': text, 'textStyle': {'fontFamily': 'Segoe UI Semibold', 'fontSize': size, 'color': colorhex}}]}]}}]}},
            container={'background': [{'properties': {'show': lit('false')}}], 'title': [{'properties': {'show': lit('false')}}],
                       'visualHeader': [{'properties': {'show': lit('false')}}],
                       'padding': [{'properties': {k: lit('0D') for k in ('top', 'bottom', 'left', 'right')}}]}, parent=parent)

    def button(self, name, x, y, w, h, tooltip, parent=None, label=None, link=None, size=11, fill_default=100):
        objs = {'icon': [{'properties': {'show': lit('false')}}], 'outline': [{'properties': {'show': lit('false')}}],
                'fill': [{'properties': {'show': lit('true'), 'fillColor': color(COR['teal']), 'transparency': num(fill_default)}, 'selector': {'id': 'default'}},
                         {'properties': {'fillColor': color(COR['teal']), 'transparency': num(84)}, 'selector': {'id': 'hover'}},
                         {'properties': {'fillColor': color(COR['teal']), 'transparency': num(72)}, 'selector': {'id': 'selected'}}],
                'padding': [{'properties': {k: lit('0D') for k in ('top', 'bottom', 'left', 'right')}, 'selector': {'id': 'default'}}]}
        if label:
            objs['text'] = [{'properties': {'show': lit('true'), 'text': s(label), 'fontColor': color(COR['claro']), 'fontSize': num(size),
                                            'fontFamily': s('Segoe UI Semibold'), 'horizontalAlignment': s('center'), 'verticalAlignment': s('middle'),
                                            'padding': lit('0D'), 'bold': lit('false')}, 'selector': {'id': 'default'}},
                            {'properties': {'show': lit('true')}}]
        else:
            objs['text'] = [{'properties': {'show': lit('false')}}]
        cont = dict(NOCHROME)
        vl = {'show': lit('true'), 'tooltip': s(tooltip)}
        if link:
            vl.update(link)
        cont['visualLink'] = [{'properties': vl}]
        self.add(name, x, y, w, h, {'visualType': 'actionButton', 'objects': objs, 'drillFilterOtherVisuals': True}, container=cont, parent=parent)

    def slicer(self, name, x, y, w, h, table, column, display, mode='Basic', horizontal=False, default=None, parent=None, periodo=False, sync=True):
        general = {'orientation': num(1 if horizontal else 0)}
        if default:
            general['filter'] = {'filter': cat_filter('x', table, column, default)['filter']}
        visual = {'visualType': 'slicer',
                  'query': {'queryState': {'Values': {'projections': [proj(col(table, column), display, active=True)]}}},
                  'objects': {'data': [{'properties': {'mode': s(mode)}}], 'general': [{'properties': general}],
                              'selection': [{'properties': {'selectAllCheckboxEnabled': lit('false'), 'singleSelect': lit('false')}}],
                              'header': [{'properties': {'show': lit('true'), 'fontColor': color(COR['cinza']), 'textSize': num(10)}}],
                              'items': [{'properties': {'fontColor': color('#FFFFFF'), 'background': color(COR['card']), 'textSize': num(10)}}]},
                  'drillFilterOtherVisuals': True}
        if sync:
            visual['syncGroup'] = {'groupName': '%s.%s' % (table, column), 'fieldChanges': True, 'filterChanges': True}
        self.add(name, x, y, w, h, visual, container=dict(NOCHROME), parent=parent, filters=[realizado()] if periodo else None)
        self._slicers = getattr(self, '_slicers', []) + [(name, table, column, mode, default)]

    # ---------- estrutura comum das paginas analiticas
    def chrome(self, slicers=None, home='pgHome', info=True):
        """Cabecalho, barra de filtros ativos, botoes Filtros/Info/Home/Navegacao, paineis ocultos e favoritos."""
        P = self.nome
        self.ux_html('nxHeader', 600, 30, 966, 62, 'UX Cabeçalho')
        self.html('nxFiltrosAtivos', 162, 134, 1712, 54, 'UX Filtros Ativos')
        self.button('nxBtnFiltros', 1637, 22, 74, 78, 'Abrir painel de filtros')
        self.button('nxBtnInfo', 1729, 22, 76, 78, 'Sobre esta página')
        self.button('nxBtnHome', 1823, 22, 74, 78, 'Ir para a Home', link={'type': s('PageNavigation'), 'navigationSection': s(home)})
        self.button('nxBtnNav', 60, 136, 82, 50, 'Navegar entre páginas')
        # painel de filtros
        self.group('grpFiltros', 'Painel Filtros', 1494, 212, 380, 844)
        self.panel_bg('nxFiltrosFundo', 1494, 212, 380, 844, 'grpFiltros')
        self.textbox('nxFiltrosTitulo', 1514, 230, 220, 36, 'Filtros', parent='grpFiltros')
        self.button('nxFiltrosFechar', 1744, 226, 112, 40, 'Fechar painel', parent='grpFiltros', label='Fechar')
        slicers = slicers or STD_SLICERS
        y = 276
        for (nm, t, c, disp, mode, horiz, default, hgt, per) in slicers:
            self.slicer(nm, 1514, y, 340, hgt, t, c, disp, mode=mode, horizontal=horiz, default=default, parent='grpFiltros', periodo=per)
            y += hgt + 8
        self.button('nxFiltrosLimpar', 1514, 992, 340, 40, 'Limpar seleções e voltar ao período padrão (2026)', parent='grpFiltros', label='Limpar filtros')
        # painel de informacoes
        self.group('grpInfo', 'Painel Info', 1394, 212, 480, 844)
        self.panel_bg('nxInfoFundo', 1394, 212, 480, 844, 'grpInfo')
        self.button('nxInfoFechar', 1744, 226, 112, 40, 'Fechar painel', parent='grpInfo', label='Fechar')
        self.ux_html('nxInfoConteudo', 1404, 266, 460, 780, 'UX Info Página', parent='grpInfo')
        # painel de navegacao
        self.group('grpNav', 'Painel Navegacao', 46, 212, 340, 520)
        self.panel_bg('nxNavFundo', 46, 212, 340, 520, 'grpNav')
        self.textbox('nxNavTitulo', 66, 230, 200, 36, 'Páginas', parent='grpNav')
        self.button('nxNavFechar', 256, 226, 112, 40, 'Fechar painel', parent='grpNav', label='Fechar')
        self.add('nxNavegador', 66, 276, 300, 440, {'visualType': 'pageNavigator', 'objects': NAV_OBJS, 'drillFilterOtherVisuals': True},
                 container=dict(NOCHROME), parent='grpNav')
        # favoritos
        groups = ['grpFiltros', 'grpInfo', 'grpNav']
        bm = {}
        for key, disp in (('padrao', 'Padrão (painéis fechados)'), ('grpFiltros', 'Painel Filtros'), ('grpInfo', 'Painel Informações'), ('grpNav', 'Painel Navegação')):
            bid = hid(P, key)
            bm[key] = bid
            self.bookmarks.append({'$schema': SB, 'displayName': '%s · %s' % (self.titulo, disp), 'name': bid,
                                   'options': {'targetVisualNames': [], 'suppressData': True},
                                   'explorationState': {'version': '1.3', 'activeSection': P, 'sections': {P: {
                                       'visualContainers': {}, 'visualContainerGroups': {g: {'isHidden': g != key} for g in groups}}},
                                       'objects': {'merge': {'outspacePane': [{'properties': {'expanded': lit('false')}}]}}}})
        rid = hid(P, 'reset')
        vc = {}
        for (nm, t, c, mode, default) in self._slicers:
            byexpr = []
            if nm in ('nxSlAno', 'nxSlMes'):
                byexpr.append(dict(realizado(), expression=col('dCalendario', 'FlagRealizado'), howCreated=0))
                byexpr[-1].pop('field', None)
            byexpr.append({'name': hid(P, nm, 'f'), 'type': 'Categorical', 'expression': col(t, c), 'howCreated': 0})
            merge = {'data': [{'properties': {'mode': s(mode)}}]}
            if default:
                merge['general'] = [{'properties': {'filter': {'filter': cat_filter('x', t, c, default)['filter']}}}]
            vc[nm] = {'filters': {'byExpr': byexpr}, 'singleVisual': {'visualType': 'slicer', 'objects': {'merge': merge},
                                                                   'activeProjections': {'Values': [col(t, c)]}}}
        self.bookmarks.append({'$schema': SB, 'displayName': '%s · Redefinir filtros' % self.titulo, 'name': rid,
                               'options': {'targetVisualNames': [x[0] for x in self._slicers], 'applyOnlyToTargetVisuals': True, 'suppressDisplay': True},
                               'explorationState': {'version': '1.3', 'activeSection': P, 'sections': {P: {'visualContainers': vc}},
                                                    'objects': {'merge': {'outspacePane': [{'properties': {'expanded': lit('false')}}]}}}})
        link = lambda b: {'type': s('Bookmark'), 'bookmark': s(b)}
        for btn, key in (('nxBtnFiltros', 'grpFiltros'), ('nxBtnInfo', 'grpInfo'), ('nxBtnNav', 'grpNav'),
                         ('nxFiltrosFechar', 'padrao'), ('nxInfoFechar', 'padrao'), ('nxNavFechar', 'padrao')):
            self.vis[btn]['visual']['visualContainerObjects']['visualLink'][0]['properties'].update(link(bm[key]))
        self.vis['nxFiltrosLimpar']['visual']['visualContainerObjects']['visualLink'][0]['properties'].update(link(rid))

    # ---------- escrita
    def write(self, definition, overwrite=False):
        pdir = os.path.join(definition, 'pages', self.nome)
        if os.path.exists(pdir):
            if not overwrite:
                raise SystemExit('pagina ja existe: ' + pdir)
            # a pasta conectada nao permite excluir: a versao anterior vai para _to_delete
            import time
            lixo = os.path.abspath(os.path.join(definition, '..', '..', '..', '_to_delete', 'paginas'))
            os.makedirs(lixo, exist_ok=True)
            shutil.move(pdir, os.path.join(lixo, '%s_%s' % (self.nome, time.strftime('%Y%m%d_%H%M%S'))))
        os.makedirs(os.path.join(pdir, 'visuals'), exist_ok=True)
        page = {'$schema': SP, 'name': self.nome, 'displayName': self.titulo, 'displayOption': 'FitToPage', 'height': self.h, 'width': self.w}
        if self.tipo:
            page.update({'type': self.tipo, 'displayOption': 'ActualSize', 'visibility': 'HiddenInViewMode'})
        objs = {'outspace': [{'properties': {'color': color(COR['navy']), 'transparency': num(0)}}]}
        if self.fundo:
            objs['background'] = [{'properties': {'image': {'image': {'name': s(self.fundo), 'url': {'expr': {'ResourcePackageItem': {
                'PackageName': 'RegisteredResources', 'PackageType': 1, 'ItemName': self.fundo}}}, 'scaling': s('Fit')}}, 'transparency': num(0)}}]
        page['objects'] = objs
        if self.interactions:
            page['visualInteractions'] = [{'source': a, 'target': b, 'type': 'NoFilter'} for a, b in self.interactions]
        json.dump(page, open(os.path.join(pdir, 'page.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        for n, v in self.vis.items():
            d = os.path.join(pdir, 'visuals', n)
            os.makedirs(d, exist_ok=True)
            json.dump(nx_estilo.visual(v), open(os.path.join(d, 'visual.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        # favoritos
        bdir = os.path.join(definition, 'bookmarks')
        os.makedirs(bdir, exist_ok=True)
        meta_p = os.path.join(bdir, 'bookmarks.json')
        meta = json.load(open(meta_p, encoding='utf-8')) if os.path.exists(meta_p) else {
            '$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json', 'items': []}
        names = [i['name'] for i in meta['items']]
        for b in self.bookmarks:
            json.dump(b, open(os.path.join(bdir, b['name'] + '.bookmark.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            if b['name'] not in names:
                meta['items'].append({'name': b['name']})
        json.dump(meta, open(meta_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return pdir


ORDEM_PAGINAS = ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgWarehouse', 'pgFinancial', 'pgPredictive',
                 'pgSimulator', 'pgCalendar', 'pgAssistant', '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora',
                 'ttMesFinanceiro', 'ttEstoqueMes', 'ttDia']


def register_page(definition, nome, ordem):
    """ordem: lista completa desejada; paginas inexistentes sao ignoradas e as nao listadas vao para o fim."""
    pj = os.path.join(definition, 'pages', 'pages.json')
    pages = json.load(open(pj, encoding='utf-8'))
    exist = [p for p in os.listdir(os.path.join(definition, 'pages')) if os.path.isdir(os.path.join(definition, 'pages', p))]
    base = []
    for p in ORDEM_PAGINAS + list(ordem):  # ordem oficial primeiro: um gerador antigo nao reordena as paginas novas
        if p in exist and p not in base:
            base.append(p)
    order = base + [p for p in pages['pageOrder'] if p in exist and p not in base]
    pages['pageOrder'] = order
    pages['activePageName'] = order[0]
    json.dump(pages, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def register_image(report_dir, src, name):
    rr = os.path.join(report_dir, 'StaticResources', 'RegisteredResources')
    shutil.copyfile(src, os.path.join(rr, name))
    rj = os.path.join(report_dir, 'definition', 'report.json')
    rep = json.load(open(rj, encoding='utf-8'))
    for pk in rep['resourcePackages']:
        if pk['name'] == 'RegisteredResources' and not any(i['name'] == name for i in pk['items']):
            pk['items'].append({'name': name, 'path': name, 'type': 'Image'})
    json.dump(rep, open(rj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


NAV_OBJS = {
    'fill': [{'properties': {'show': lit('true'), 'fillColor': color(COR['card']), 'transparency': lit('0D')}, 'selector': {'id': 'default'}},
             {'properties': {'fillColor': color(COR['teal']), 'transparency': lit('80D')}, 'selector': {'id': 'hover'}},
             {'properties': {'fillColor': color(COR['teal']), 'transparency': lit('70D')}, 'selector': {'id': 'selected'}}],
    'text': [{'properties': {'show': lit('true'), 'fontColor': color(COR['claro']), 'fontSize': lit('11D'), 'fontFamily': s('Segoe UI Semibold'),
                             'horizontalAlignment': s('left')}, 'selector': {'id': 'default'}},
             {'properties': {'fontColor': color('#FFFFFF')}, 'selector': {'id': 'selected'}}],
    'outline': [{'properties': {'show': lit('true'), 'lineColor': color(COR['borda']), 'weight': lit('1D'), 'transparency': lit('0D')}, 'selector': {'id': 'default'}},
                {'properties': {'lineColor': color(COR['teal'])}, 'selector': {'id': 'selected'}}],
    'shape': [{'properties': {'tileShape': s('rectangleRounded'), 'rectangleRoundedCurve': lit('8L')}}],
    'layout': [{'properties': {'orientation': lit('1D'), 'cellPadding': lit('6D')}}],
    'pages': [{'properties': {'showHiddenPages': lit('false'), 'showTooltipPages': lit('false')}}]}

# (nome, tabela, coluna, rotulo, modo, horizontal, padrao, altura, periodo)
STD_SLICERS = [
    ('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
    ('nxSlMes', 'dCalendario', 'MesAno', 'Mês', 'Dropdown', False, None, 70, True),
    ('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
    ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Basic', False, None, 300, False),
    ('nxSlCategoria', 'dProduto', 'Categoria', 'Categoria', 'Dropdown', False, None, 90, False),
]


# ---------- Deneb (Vega-Lite) padrao NEXUS 360
DCONF = {"autosize": {"type": "fit", "contains": "padding"}, "view": {"stroke": None}, "font": "Segoe UI", "background": None,
         "padding": {"left": 4, "right": 12, "top": 6, "bottom": 4},
         "axis": {"labelFont": "Segoe UI", "labelColor": "#A9B9CA", "titleColor": "#A9B9CA", "titleFont": "Segoe UI", "titleFontWeight": 400,
                  "gridColor": "#173B5C", "gridDash": [2, 3], "domain": False, "ticks": False, "labelFontSize": 10, "titleFontSize": 10},
         "legend": {"labelFont": "Segoe UI", "labelColor": "#A9B9CA", "labelFontSize": 10, "orient": "top", "title": None, "symbolType": "circle"}}


def deneb(p, name, x, y, w, h, fields, spec, ttl):
    p.add(name, x, y, w, h, {
        'visualType': DENEB,
        'query': {'queryState': {'dataset': {'projections': [proj(f, active=True if 'Column' in f else None) for f in fields]}}},
        'objects': {'vega': [{'properties': {'provider': s('vegaLite'), 'jsonSpec': s(json.dumps(spec, ensure_ascii=False)),
                                             'jsonConfig': s(json.dumps(DCONF)), 'renderMode': s('svg'), 'isNewDialogOpen': lit('false'),
                                             'enableTooltips': lit('true'), 'enableContextMenu': lit('true'), 'enableSelection': lit('false')}}]},
        'drillFilterOtherVisuals': True}, container={'title': title(ttl)})


