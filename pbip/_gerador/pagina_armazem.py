# NEXUS 360 - Etapa E: Warehouse Digital Twin (2D funcional no Power BI)
# Pergunta: onde ha gargalo de ocupacao e estoque parado?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, tooltip_page, realizado, cat_filter, COR, NOCHROME)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG, TT = 'pgWarehouse', 'ttEstoqueMes'
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}
SL = [('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
      ('nxSlMes', 'dCalendario', 'MesAno', 'Mês do snapshot', 'Dropdown', False, None, 70, True),
      ('nxSlZona', 'dPosicaoArmazem', 'Zona', 'Zona', 'Basic', False, None, 110, False),
      ('nxSlCategoria', 'dProduto', 'Categoria', 'Categoria (estoque e movimentos)', 'Dropdown', False, None, 90, False)]

p = Pagina(PG, 'Warehouse Digital Twin')
p.chrome(slicers=SL)
p.html('nxArmKPIs', 46, 212, 1828, 104, 'UX Armazém KPIs')

# Grade 2D (gemeo digital)
p.html('nxGrade', 46, 332, 1270, 508, 'UX Armazém Grade')
p.vis['nxGrade']['visual']['visualContainerObjects'] = dict(CARD)

# Seletor de filial visivel (selecao unica, nao sincronizado: o mapa exige uma filial)
p.slicer('nxSlCidade', 1332, 332, 542, 150, 'dFilial', 'Cidade', 'Filial do armazém', mode='Basic', horizontal=True,
         default=["'Campinas'"], sync=False)
v = p.vis['nxSlCidade']['visual']
v['objects']['selection'] = [{'properties': {'selectAllCheckboxEnabled': lit('false'), 'singleSelect': lit('true'), 'strictSingleSelect': lit('true')}}]
v['objects']['items'] = [{'properties': {'fontColor': color('#FFFFFF'), 'background': color(COR['card']), 'textSize': num(10), 'outline': s('Frame'), 'outlineColor': color(COR['borda'])}}]
v['visualContainerObjects'] = dict(CARD)
p._slicers = [x for x in p._slicers if x[0] != 'nxSlCidade']

# Status por zona (matriz)
VALS = [('Posições Amostradas', 'Lidas'), ('Registros Ocupada %', 'Ocupada'), ('Registros Bloqueada %', 'Bloqueada'),
        ('Registros Disponível %', 'Disponível'), ('Paletes (amostra)', 'Paletes')]
p.add('nxZonas', 1332, 498, 542, 342, {
    'visualType': 'pivotTable',
    'query': {'queryState': {'Rows': {'projections': [proj(col('dPosicaoArmazem', 'Zona'), 'Zona', active=True)]},
                             'Values': {'projections': [proj(meas(m), d) for m, d in VALS]}}},
    'objects': {'values': [{'properties': {'fontColor': color(COR['neg'])}, 'selector': {'metadata': '_Medidas.Registros Bloqueada %'}},
                           {'properties': {'fontColor': color(COR['teal'])}, 'selector': {'metadata': '_Medidas.Registros Ocupada %'}}],
                'columnHeaders': [{'properties': {'alignment': s('Center'), 'wordWrap': lit('true'), 'fontSize': num(10), 'columnAdjustment': s('growToFit')}}],
                'grid': [{'properties': {'rowPadding': num(6), 'textSize': num(11)}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Leituras do snapshot por zona (amostra)')})

# Evolucao do status das leituras (100% empilhado)
CST = {'Ocupada': COR['teal'], 'Bloqueada': COR['neg'], 'Disponível': COR['azul2']}
dp = [{'properties': {'fill': color(c)}, 'selector': {'data': [{'scopeId': {'Comparison': {'ComparisonKind': 0, 'Left': col('fOcupacaoArmazem', 'StatusPosicao'),
                                                                                          'Right': {'Literal': {'Value': "'%s'" % k}}}}}]}} for k, c in CST.items()]
p.add('nxStatusMes', 46, 856, 900, 200, {
    'visualType': 'hundredPercentStackedColumnChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('dCalendario', 'MesAno'), 'Mês', active=True)]},
                             'Series': {'projections': [proj(col('fOcupacaoArmazem', 'StatusPosicao'), 'Status')]},
                             'Y': {'projections': [proj(meas('Registros WMS (amostra)'), 'Leituras')]}},
              'sortDefinition': {'sort': [{'field': col('dCalendario', 'MesAno'), 'direction': 'Ascending'}]}},
    'objects': {'dataPoint': dp, 'legend': [{'properties': {'show': lit('true'), 'position': s('Right'), 'fontSize': num(9)}}],
                'valueAxis': [{'properties': {'show': lit('false')}}], 'categoryAxis': [{'properties': {'fontSize': num(9)}}],
                'labels': [{'properties': {'show': lit('false')}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Status das posições lidas em cada snapshot mensal')}, filters=[realizado()])

# Movimentacao mensal (entradas x saidas) com tooltip de estoque
p.add('nxMovimentos', 962, 856, 912, 200, {
    'visualType': 'clusteredColumnChart',
    'query': {'queryState': {'Category': {'projections': [proj(col('dCalendario', 'MesAno'), 'Mês', active=True)]},
                             'Y': {'projections': [proj(meas('Entradas Estoque (un)'), 'Entradas'), proj(meas('Saídas Estoque (un)'), 'Saídas')]}},
              'sortDefinition': {'sort': [{'field': col('dCalendario', 'MesAno'), 'direction': 'Ascending'}]}},
    'objects': {'dataPoint': [{'properties': {'fill': color(COR['teal'])}, 'selector': {'metadata': '_Medidas.Entradas Estoque (un)'}},
                              {'properties': {'fill': color('#3E5C7A')}, 'selector': {'metadata': '_Medidas.Saídas Estoque (un)'}}],
                'legend': [{'properties': {'show': lit('true'), 'position': s('Right'), 'fontSize': num(9)}}],
                'valueAxis': [{'properties': {'show': lit('true'), 'labelDisplayUnits': num(1000)}}], 'categoryAxis': [{'properties': {'fontSize': num(9)}}]},
    'drillFilterOtherVisuals': True},
    container={'title': title('Movimentação de estoque (unidades, amostra)'), 'visualTooltip': tooltip_page(TT)}, filters=[realizado()])
p.write(DEF, overwrite=True)

t = Pagina(TT, 'TT Estoque Mês', fundo=None, tipo='Tooltip', w=320, h=170)
t.html('nxTooltipEstoque', 0, 0, 320, 170, 'UX Tooltip Estoque Mês')
t.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgWarehouse', 'pgFinancial',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora', 'ttMesFinanceiro', 'ttEstoqueMes'])
print('warehouse ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
