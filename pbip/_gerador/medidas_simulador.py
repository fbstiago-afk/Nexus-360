# NEXUS 360 - Etapa H: Decision Simulator (parametros What-if e medidas de cenario)
# Premissas (documentadas na pagina):
#  - Base: periodo selecionado, limitado ao corte. Resultado operacional = Receita - CMV - Frete - Despesas operacionais.
#  - Preco (%) e desconto (p.p.) alteram a receita liquida: fator do desconto = (1 - (d0 + delta)) / (1 - d0), d0 = desconto medio ponderado.
#  - Volume (%) escala receita, CMV e frete. Custo (%) altera o custo unitario. Frete (%) altera a tarifa. Despesas (%) nao escalam com volume.
#  - Sem elasticidade: preco e volume sao independentes (o usuario define os dois). Nao e previsao.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert
from nx_tabelas import tabela

PCT = '+0%;-0%;0%'
PP = '+0.0" p.p.";-0.0" p.p.";0.0" p.p."'
FMT = 'R$ #,0.00;-R$ #,0.00;R$ #,0.00'
PARAMS = [('Sim Preço', 'Preço %', -20, 20, 1, PCT, 'Variacao de preco sobre a receita liquida.'),
          ('Sim Desconto', 'Desconto p.p.', -5, 5, 1, PP, 'Variacao do desconto medio em pontos percentuais.'),
          ('Sim Volume', 'Volume %', -20, 20, 1, PCT, 'Variacao de volume (escala receita, CMV e frete).'),
          ('Sim Custo', 'Custo %', -10, 10, 1, PCT, 'Variacao do custo unitario da mercadoria.'),
          ('Sim Frete', 'Frete %', -20, 20, 1, PCT, 'Variacao da tarifa de frete.'),
          ('Sim Despesas', 'Despesas %', -20, 20, 1, PCT, 'Variacao das despesas operacionais (nao escalam com volume).')]


def criar_tabelas(definition):
    for (t, c, a, b, st, fmt, d) in PARAMS:
        div = 1 if t == 'Sim Desconto' else 100   # desconto: coluna em p.p.; demais em fracao
        dax = 'SELECTCOLUMNS ( GENERATESERIES ( %d, %d, %d ), "%s", [Value] / %d )' % (a, b, st, c, div)
        tabela(definition, t, [(c, 'double', fmt)], dax, 'Parametro de simulacao: ' + d, param=True)
    tabela(definition, 'Sim Etapa', [('Ordem', 'int64', '0'), ('Etapa', 'string', None, 'Ordem')],
           'DATATABLE ( "Ordem", INTEGER, "Etapa", STRING, { { 1, "Resultado base" }, { 2, "Preço" }, { 3, "Desconto" }, { 4, "Volume" }, { 5, "Custo da mercadoria" }, { 6, "Frete" }, { 7, "Despesas" } } )',
           'Etapas da ponte do resultado simulado (cascata).')
    tabela(definition, 'Sim Grade Preço', [('Preço grade %', 'double', PCT)], 'SELECTCOLUMNS ( GENERATESERIES ( -10, 10, 2 ), "Preço grade %", [Value] / 100 )',
           'Eixo de preco da grade de sensibilidade.')
    tabela(definition, 'Sim Grade Volume', [('Volume grade %', 'double', PCT)], 'SELECTCOLUMNS ( GENERATESERIES ( -10, 10, 2 ), "Volume grade %", [Value] / 100 )',
           'Eixo de volume da grade de sensibilidade.')


BASEVARS = r'''
VAR _c = [Data Corte]
VAR _R0 = [Receita (até corte)]
VAR _C0 = CALCULATE ( [CMV], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _F0 = CALCULATE ( [Custo Frete], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _D0 = CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _dsc0 = CALCULATE ( [Desconto Médio Ponderado %], KEEPFILTERS ( dCalendario[Data] <= _c ) )
VAR _p = SELECTEDVALUE ( 'Sim Preço'[Preço %], 0 )
VAR _dd = SELECTEDVALUE ( 'Sim Desconto'[Desconto p.p.], 0 ) / 100
VAR _v = SELECTEDVALUE ( 'Sim Volume'[Volume %], 0 )
VAR _cc = SELECTEDVALUE ( 'Sim Custo'[Custo %], 0 )
VAR _f = SELECTEDVALUE ( 'Sim Frete'[Frete %], 0 )
VAR _e = SELECTEDVALUE ( 'Sim Despesas'[Despesas %], 0 )
VAR _k = DIVIDE ( 1 - ( _dsc0 + _dd ), 1 - _dsc0 )
VAR _R1 = _R0 * ( 1 + _p ) * _k * ( 1 + _v )
VAR _C1 = _C0 * ( 1 + _v ) * ( 1 + _cc )
VAR _F1 = _F0 * ( 1 + _v ) * ( 1 + _f )
VAR _D1 = _D0 * ( 1 + _e )
VAR _Res0 = _R0 - _C0 - _F0 - _D0
VAR _Res1 = _R1 - _C1 - _F1 - _D1
'''


def m(body):
    return BASEVARS + body


ETAPA = m(r'''VAR _o = SELECTEDVALUE ( 'Sim Etapa'[Ordem] )
RETURN
    IF (
        NOT [Filtro de Produto Ativo] && NOT ISBLANK ( _R0 ),
        SWITCH (
            _o,
            1, _Res0,
            2, _R0 * _p,
            3, _R0 * ( 1 + _p ) * ( _k - 1 ),
            4, _v * ( _R0 * ( 1 + _p ) * _k - _C0 - _F0 ),
            5, - _C0 * ( 1 + _v ) * _cc,
            6, - _F0 * ( 1 + _v ) * _f,
            7, - _D0 * _e
        )
    )
''')
GRADE = m(r'''VAR _gp = SELECTEDVALUE ( 'Sim Grade Preço'[Preço grade %] )
VAR _gv = SELECTEDVALUE ( 'Sim Grade Volume'[Volume grade %] )
VAR _Rg = _R0 * ( 1 + _gp ) * _k * ( 1 + _gv )
VAR _Resg = _Rg - _C0 * ( 1 + _gv ) * ( 1 + _cc ) - _F0 * ( 1 + _gv ) * ( 1 + _f ) - _D1
RETURN IF ( NOT [Filtro de Produto Ativo] && NOT ISBLANK ( _gp ) && NOT ISBLANK ( _gv ), _Resg - _Res0 )
''')
RESUMO = m(r'''VAR _veq = DIVIDE ( _Res0 + _D1, _R0 * ( 1 + _p ) * _k - _C0 * ( 1 + _cc ) - _F0 * ( 1 + _f ) ) - 1
VAR _mg0 = DIVIDE ( _R0 - _C0, _R0 )
VAR _mg1 = DIVIDE ( _R1 - _C1, _R1 )
VAR _css = "<style>.nx-s{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 20px;display:flex;flex-direction:column;gap:10px}.nx-st{font-size:13px;font-weight:600;text-align:center}.nx-ss{font-size:10.5px;color:#FFC66D;text-align:center}.nx-s table{width:100%;border-collapse:collapse;font-size:12.5px}.nx-s th{font-size:10px;color:#A9B9CA;font-weight:600;text-align:right;padding:5px 6px;border-bottom:1px solid #173B5C}.nx-s th:first-child,.nx-s td:first-child{text-align:left}.nx-s td{text-align:right;padding:7px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.nx-s tr.r td{color:#FFFFFF;font-weight:600;font-size:14px;background:rgba(18,48,79,.6)}.nx-eq{display:grid;grid-template-columns:1fr 1fr;gap:12px}.nx-b{border-left:3px solid #5FA8E6;padding-left:10px}.nx-bl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-bv{font-size:20px;font-weight:600}.nx-bs{font-size:10px;color:#A9B9CA}.nx-pr{font-size:10px;color:#6F86A0;line-height:1.5}</style>"
VAR _d = _Res1 - _Res0
RETURN
    IF (
        [Filtro de Produto Ativo] || ISBLANK ( _R0 ),
        _css & "<div class='nx-s'><div class='nx-st'>Simulação indisponível</div><div class='nx-ss'>Remova o filtro de produto: frete e despesas não têm produto.</div></div>",
        _css & "<div class='nx-s'><div class='nx-st'>Cenário simulado vs base do período</div><div class='nx-ss'>Simulação sob premissas declaradas. Não é previsão nem recomendação.</div>"
            & "<table><tr><th></th><th>Base</th><th>Simulado</th><th>Variação</th></tr>"
            & "<tr><td>Receita líquida</td><td>R$ " & FORMAT ( _R0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _R1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _R1 >= _R0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _R1, _R0 ) - 1, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</td></tr>"
            & "<tr><td>Margem bruta</td><td>" & FORMAT ( _mg0, "0.0%", "pt-BR" ) & "</td><td>" & FORMAT ( _mg1, "0.0%", "pt-BR" ) & "</td><td style='color:" & IF ( _mg1 >= _mg0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( ( _mg1 - _mg0 ) * 100, "+0.0;-0.0;0.0", "pt-BR" ) & " p.p.</td></tr>"
            & "<tr><td>Frete</td><td>R$ " & FORMAT ( _F0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _F1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _F1 <= _F0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _F1, _F0 ) - 1, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</td></tr>"
            & "<tr><td>Despesas operacionais</td><td>R$ " & FORMAT ( _D0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _D1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _D1 <= _D0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _D1, _D0 ) - 1, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</td></tr>"
            & "<tr class='r'><td>Resultado operacional</td><td>R$ " & FORMAT ( _Res0 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td>R$ " & FORMAT ( _Res1 / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td style='color:" & IF ( _d >= 0, "#45D5A1", "#FF7285" ) & "'>" & IF ( _d >= 0, "+", "−" ) & "R$ " & FORMAT ( ABS ( _d ) / 1e6, "#,0.0", "pt-BR" ) & " mi</td></tr></table>"
            & "<div class='nx-eq'><div class='nx-b'><div class='nx-bl'>Margem operacional</div><div class='nx-bv'>" & FORMAT ( DIVIDE ( _Res0, _R0 ), "0.0%", "pt-BR" ) & " → " & FORMAT ( DIVIDE ( _Res1, _R1 ), "0.0%", "pt-BR" ) & "</div><div class='nx-bs'>resultado ÷ receita</div></div>"
            & "<div class='nx-b' style='border-color:#FFC66D'><div class='nx-bl'>Volume para manter o resultado</div><div class='nx-bv'>" & FORMAT ( _veq, "+0.0%;-0.0%;0.0%", "pt-BR" ) & "</div><div class='nx-bs'>com os demais parâmetros escolhidos</div></div></div>"
            & "<div class='nx-pr'>Premissas: preço e desconto alteram a receita; volume escala receita, custo e frete; despesas não escalam com volume; sem elasticidade preço × volume. Resultado operacional = receita − CMV − frete − despesas (difere da DRE gerencial, que não subtrai frete).</div></div>"
    )
''')

AVISO = r'''
VAR _ini = CALCULATE ( MIN ( dCalendario[Data] ), FILTER ( VALUES ( dCalendario[Data] ), NOT ISBLANK ( [Receita Líquida] ) ) )
VAR _fim = MIN ( MAX ( dCalendario[Data] ), [Data Corte] )
RETURN
    "<div style='font-family:Segoe UI,sans-serif;font-size:10px;line-height:1.45;color:#A9B9CA;padding:2px 2px'>Base: "
        & FORMAT ( _ini, "dd/mm/yyyy" ) & " a " & FORMAT ( _fim, "dd/mm/yyyy" )
        & " (período e filiais do painel de filtros).<br><span style='color:#FFC66D'>Cálculo sob premissas, sem elasticidade. Não é previsão.</span></div>"
'''

if __name__ == '__main__':
    defn = sys.argv[1]
    criar_tabelas(defn)
    upsert(os.path.join(defn, 'tables', '_Medidas.tmdl'), [
        dict(name='Sim Valor Etapa', expr=ETAPA, folder='11 Simulador', fmt=FMT,
             desc='Ponte do resultado operacional: base e efeito sequencial de preco, desconto, volume, custo, frete e despesas (soma = simulado).'),
        dict(name='Sim Δ Resultado (grade)', expr=GRADE, folder='11 Simulador', fmt=FMT,
             desc='Variacao do resultado operacional para cada par preco x volume da grade, com os demais parametros dos controles.'),
        dict(name='UX Simulador Aviso', expr=AVISO, folder='08 UX\\Simulador',
             desc='Rodape dos controles: base do cenario e aviso de que a simulacao nao e previsao.'),
        dict(name='UX Simulador Resumo', expr=RESUMO, folder='08 UX\\Simulador',
             desc='Comparacao base x simulado, margem operacional, volume de equilibrio e premissas.'),
    ])
    print('ok')
