# NEXUS 360 - Etapa J: AI Decision Assistant (PBIR) - interface demonstrativa, sem LLM conectado
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, lit, num, color, COR)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG = 'pgAssistant'
CARD = {'background': [{'properties': {'show': lit('true'), 'color': color(COR['card']), 'transparency': num(8)}}],
        'border': [{'properties': {'show': lit('true'), 'color': color(COR['borda']), 'radius': num(12)}}]}
SL = [('nxSlAno', 'dCalendario', 'Ano', 'Ano', 'Basic', True, ['2026L'], 76, True),
      ('nxSlMes', 'dCalendario', 'MesAno', 'Mês', 'Dropdown', False, None, 70, True),
      ('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Basic', False, None, 300, False)]

p = Pagina(PG, 'AI Decision Assistant')
p.chrome(slicers=SL)
p.html('nxAsstStatus', 46, 212, 1828, 84, 'UX Assistente Status')
p.vis['nxAsstStatus']['visual']['visualContainerObjects'] = dict(CARD)
p.html('nxAsstFluxo', 46, 312, 900, 744, 'UX Assistente Fluxo')
p.vis['nxAsstFluxo']['visual']['visualContainerObjects'] = dict(CARD)
p.html('nxAsstFerramentas', 962, 312, 912, 404, 'UX Assistente Ferramentas')
p.vis['nxAsstFerramentas']['visual']['visualContainerObjects'] = dict(CARD)
p.html('nxAsstArquitetura', 962, 732, 912, 324, 'UX Assistente Arquitetura')
p.vis['nxAsstArquitetura']['visual']['visualContainerObjects'] = dict(CARD)
p.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgWarehouse', 'pgFinancial', 'pgPredictive', 'pgSimulator', 'pgCalendar', 'pgAssistant',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora', 'ttMesFinanceiro', 'ttEstoqueMes', 'ttDia'])
print('assistant ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
