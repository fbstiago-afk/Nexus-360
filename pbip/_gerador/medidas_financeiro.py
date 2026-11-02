# NEXUS 360 - Etapa F: medidas da Financial & Profitability
# Novas medidas de negocio: caixa por data de pagamento (relacoes inativas ja existentes) e DRE do ano anterior. Validar contra SQL.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

RECEB = "CALCULATE ( [Valor Recebido Confirmado], USERELATIONSHIP ( fContasReceber[DataPagamento], dCalendario[Data] ) )"
PAG = "CALCULATE ( [Valor Pago (CP)], USERELATIONSHIP ( fContasPagar[DataPagamento], dCalendario[Data] ) )"
SALDO = "[Recebimentos (Data Pagamento)] - [Pagamentos (Data Pagamento)]"
DRE_LY = r'''
VAR _corte = [Data Corte]
RETURN
    CALCULATE (
        CALCULATE ( [Valor DRE Gerencial], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ),
        KEEPFILTERS ( dCalendario[Data] <= _corte )
    )
'''


def linha(rot, cur, ly, orc=None, cls='', inverso=False, pct=True):
    """Linha da DRE HTML: realizado, % receita, ano anterior, variacao, orcado e desvio (quando houver)."""
    bom = '<=' if inverso else '>='
    o = ('IF ( NOT ISBLANK ( %(o)s ), "<td>" & FORMAT ( %(o)s / 1e6, "#,0.0", "pt-BR" ) & "</td><td style=\'color:" & IF ( ABS ( %(c)s ) %(b)s ABS ( %(o)s ), "#45D5A1", "#FF7285" ) & "\'>" & FORMAT ( DIVIDE ( ABS ( %(c)s ) - ABS ( %(o)s ), ABS ( %(o)s ) ), "+0.0%%;-0.0%%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" )'
         % {'o': orc, 'c': cur, 'b': bom}) if orc else '"<td>—</td><td></td>"'
    return ('"<tr class=\'%(cls)s\'><td>%(rot)s</td><td>" & FORMAT ( %(cur)s / 1e6, "#,0.0", "pt-BR" ) & "</td><td>" & %(pc)s & "</td>"'
            ' & IF ( _umAno && NOT ISBLANK ( %(ly)s ), "<td>" & FORMAT ( %(ly)s / 1e6, "#,0.0", "pt-BR" ) & "</td><td style=\'color:" & IF ( ABS ( %(cur)s ) %(b)s ABS ( %(ly)s ), "#45D5A1", "#FF7285" ) & "\'>" & FORMAT ( DIVIDE ( ABS ( %(cur)s ) - ABS ( %(ly)s ), ABS ( %(ly)s ) ), "+0.0%%;-0.0%%", "pt-BR" ) & "</td>", "<td>—</td><td></td>" )'
            ' & %(o)s & "</tr>"') % {'cls': cls, 'rot': rot, 'cur': cur, 'ly': ly, 'b': bom, 'o': o,
                                   'pc': 'FORMAT ( DIVIDE ( %s, _rec ), "0.0%%", "pt-BR" )' % cur if pct else '""'}


DESP = ['Pessoal', 'Aluguel', 'Energia', 'Marketing', 'TI', 'Administrativo']
vars_desp = '\n'.join('VAR _d%d = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "%s" ) )\nVAR _d%dly = - CALCULATE ( CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( fDespesa[Conta] = "%s" ), SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )'
                      % (i, c, i, c) for i, c in enumerate(DESP))
DRE = r'''
VAR _corte = [Data Corte]
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _rec = [Receita (até corte)]
VAR _recLY = [Receita LY]
VAR _recO = CALCULATE ( [Orçamento Receita], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _cmv = - CALCULATE ( [CMV], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _cmvLY = - CALCULATE ( CALCULATE ( [CMV], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _mb = _rec + _cmv
VAR _mbLY = _recLY + _cmvLY
''' + vars_desp + r'''
VAR _dt = - CALCULATE ( [Despesas Operacionais], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _dtLY = - CALCULATE ( CALCULATE ( [Despesas Operacionais], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _dtO = - CALCULATE ( [Orçamento Despesa Operacional], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _rs = _mb + _dt
VAR _rsLY = _mbLY + _dtLY
VAR _css = "<style>.nx-d{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;display:flex;flex-direction:column}.nx-dt{font-size:13px;font-weight:600;text-align:center}.nx-ds{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 10px}.nx-d table{width:100%;border-collapse:collapse;font-size:11.5px}.nx-d th{font-size:9.5px;font-weight:600;color:#A9B9CA;text-align:right;padding:4px 4px;border-bottom:1px solid #173B5C;letter-spacing:.04em}.nx-d th:first-child,.nx-d td:first-child{text-align:left}.nx-d td{text-align:right;padding:5px 4px;border-bottom:1px solid #12304F;color:#C9D6E3}.nx-d tr.s td{color:#FFFFFF;font-weight:600;background:rgba(18,48,79,.55)}.nx-d tr.r td{color:#10D4C4;font-weight:600;background:rgba(18,48,79,.85);border-bottom:none}.nx-d tr.i td:first-child{padding-left:16px}.nx-k{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:auto}.nx-kb{border-left:3px solid #173B5C;padding-left:10px}.nx-kl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:20px;font-weight:600}</style>"
VAR _hd = "<tr><th>R$ mi</th><th>Realizado</th><th>% rec.</th><th>Ano ant.</th><th>Var.</th><th>Orçado</th><th>Desvio</th></tr>"
RETURN
    IF (
        [Filtro de Produto Ativo],
        _css & "<div class='nx-d'><div class='nx-dt'>DRE gerencial</div><div class='nx-ds'>Indisponível com filtro de produto: despesas e impostos não têm produto.</div></div>",
        _css & "<div class='nx-d'><div class='nx-dt'>DRE gerencial (não contábil)</div><div class='nx-ds'>competência até " & FORMAT ( MIN ( _corte, MAX ( dCalendario[Data] ) ), "dd/mm/yyyy" ) & " · variação e desvio favoráveis em verde</div><table>" & _hd
            & ''' + linha('Receita líquida', '_rec', '_recLY', '_recO', 's') + r'''
            & ''' + linha('(−) CMV', '_cmv', '_cmvLY', None, 'i', True) + r'''
            & ''' + linha('Margem bruta', '_mb', '_mbLY', None, 's') + '\n' + '\n'.join(
                '            & ' + linha('(−) %s' % c, '_d%d' % i, '_d%dly' % i, None, 'i', True) for i, c in enumerate(DESP)) + r'''
            & ''' + linha('Despesas operacionais', '_dt', '_dtLY', '_dtO', 's', True) + r'''
            & ''' + linha('Resultado gerencial', '_rs', '_rsLY', None, 'r') + r'''
            & "</table><div class='nx-k'>"
            & "<div class='nx-kb' style='border-color:#10D4C4'><div class='nx-kl'>Margem bruta</div><div class='nx-kv'>" & FORMAT ( DIVIDE ( _mb, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "<div class='nx-kb' style='border-color:#5FA8E6'><div class='nx-kl'>Despesas / receita</div><div class='nx-kv'>" & FORMAT ( DIVIDE ( - _dt, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "<div class='nx-kb' style='border-color:" & IF ( _rs >= 0, "#45D5A1", "#FF7285" ) & "'><div class='nx-kl'>Resultado / receita</div><div class='nx-kv'>" & FORMAT ( DIVIDE ( _rs, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
'''

RECEBIVEIS = r'''
VAR _ref = [Data Referência]
VAR _venc = [Saldo Vencido em Aberto (Data Ref.)]
VAR _av = [Saldo a Vencer em Aberto (Data Ref.)]
VAR _ab = _venc + _av
VAR _wv = FORMAT ( 100 * DIVIDE ( _venc, _ab ), "0.0", "en-US" )
VAR _css = "<style>.nx-r{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:12px 16px;display:flex;flex-direction:column;gap:9px}.nx-rt{font-size:13px;font-weight:600;text-align:center}.nx-rg{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px}.nx-rl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-rv{font-size:19px;font-weight:600}.nx-rs{font-size:10px;color:#A9B9CA}.nx-bar{display:flex;height:9px;border-radius:5px;overflow:hidden;background:#12304F;margin-top:4px}.nx-dq{font-size:10px;color:#C9D6E3;border-left:3px solid #FFC66D;padding-left:8px}</style>"
RETURN
    _css & "<div class='nx-r'><div class='nx-rt'>Recebíveis e pagamentos em " & FORMAT ( _ref, "dd/mm/yyyy" ) & "</div>"
        & "<div><div class='nx-rl'>Saldo a receber em aberto</div><div class='nx-rv'>R$ " & FORMAT ( _ab / 1e6, "#,0.00", "pt-BR" ) & " mi</div>"
        & "<div class='nx-bar'><span style='width:" & _wv & "%;background:#FF7285'></span><span style='flex:1;background:#5FA8E6'></span></div>"
        & "<div class='nx-rs'><span style='color:#FF7285'>vencido R$ " & FORMAT ( _venc / 1e6, "#,0.00", "pt-BR" ) & " mi</span> · a vencer R$ " & FORMAT ( _av / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
        & "<div class='nx-rg'>"
        & "<div><div class='nx-rl'>Inadimplência</div><div class='nx-rv'>" & FORMAT ( [Inadimplência % (Data Ref.)], "0.00%", "pt-BR" ) & "</div><div class='nx-rs'>vencido em aberto ÷ vencido até a data</div></div>"
        & "<div><div class='nx-rl'>Prazo médio de recebimento</div><div class='nx-rv'>" & FORMAT ( [Prazo Médio Recebimento (dias)], "0.0", "pt-BR" ) & " dias</div><div class='nx-rs'>da fatura ao pagamento</div></div>"
        & "<div><div class='nx-rl'>Recebido no período</div><div class='nx-rv'>R$ " & FORMAT ( [Recebimentos (Data Pagamento)] / 1e6, "#,0.0", "pt-BR" ) & " mi</div><div class='nx-rs'>pela data do pagamento</div></div>"
        & "<div><div class='nx-rl'>Pago a fornecedores</div><div class='nx-rv'>R$ " & FORMAT ( [Pagamentos (Data Pagamento)] / 1e6, "#,0.0", "pt-BR" ) & " mi</div><div class='nx-rs'>em aberto R$ " & FORMAT ( [Valor em Aberto (CP)] / 1e6, "#,0.0", "pt-BR" ) & " mi</div></div>"
        & "</div><div class='nx-dq'>Qualidade: " & FORMAT ( [Títulos Inconsistentes], "#,0", "pt-BR" ) & " títulos inconsistentes (R$ " & FORMAT ( [Valor Títulos Inconsistentes] / 1e6, "#,0.0", "pt-BR" ) & " mi) ficam fora do recebido.</div></div>"
'''

TT_MES = r'''
VAR _mes = SELECTEDVALUE ( dCalendario[MesAno] )
VAR _rec = [Receita Líquida]
VAR _rs = [Resultado Gerencial Simplificado]
VAR _in = [Recebimentos (Data Pagamento)]
VAR _out = [Pagamentos (Data Pagamento)]
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}</style>"
RETURN
    IF (
        NOT ISBLANK ( _mes ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _mes & "</div><div class='nx-tg'>"
            & "<div><div class='nx-tk'>Recebido</div><div class='nx-tv' style='color:#10D4C4'>R$ " & FORMAT ( _in / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Pago a fornecedores</div><div class='nx-tv'>R$ " & FORMAT ( _out / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Saldo do mês</div><div class='nx-tv' style='color:" & IF ( _in >= _out, "#45D5A1", "#FF7285" ) & "'>R$ " & FORMAT ( ( _in - _out ) / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Receita (competência)</div><div class='nx-tv'>R$ " & FORMAT ( _rec / 1e6, "#,0.00", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Margem bruta</div><div class='nx-tv'>" & FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Resultado gerencial</div><div class='nx-tv' style='color:" & IF ( _rs >= 0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( DIVIDE ( _rs, _rec ), "0.0%", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
'''

if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='Recebimentos (Data Pagamento)', expr=RECEB, folder='05 Financeiro\\Caixa', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00',
             desc='Recebido confirmado (regra D1) datado pelo pagamento (relacao inativa fContasReceber[DataPagamento]).'),
        dict(name='Pagamentos (Data Pagamento)', expr=PAG, folder='05 Financeiro\\Caixa', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00',
             desc='Contas a pagar elegiveis pagas, datadas pelo pagamento (relacao inativa fContasPagar[DataPagamento]). Despesas operacionais nao tem registro de pagamento.'),
        dict(name='Saldo Recebimentos - Pagamentos', expr=SALDO, folder='05 Financeiro\\Caixa', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00',
             desc='Entradas de clientes menos pagamentos a fornecedores no periodo (nao e o fluxo de caixa completo).'),
        dict(name='Orçamento Despesa Operacional (até corte)', expr="VAR _corte = [Data Corte]\nRETURN CALCULATE ( [Orçamento Despesa Operacional], KEEPFILTERS ( dCalendario[Data] <= _corte ) )",
             folder='06 Planejamento', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00', desc='Orcamento de despesa operacional restrito aos meses com realizado (mesma base do desvio).'),
        dict(name='Valor DRE Gerencial LY', expr=DRE_LY, folder='06 Planejamento', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00',
             desc='Valor DRE Gerencial no mesmo periodo do ano anterior, limitado ao corte.'),
        dict(name='UX Financeiro DRE', expr=DRE, folder='08 UX\\Financeiro',
             desc='DRE gerencial HTML: realizado, % da receita, ano anterior, variacao, orcado e desvio (orcamento so existe para receita e despesa total).'),
        dict(name='UX Financeiro Recebíveis', expr=RECEBIVEIS, folder='08 UX\\Financeiro',
             desc='Saldo a receber (vencido x a vencer) na Data Referencia, inadimplencia, prazo medio, recebido e pago no periodo, titulos inconsistentes.'),
        dict(name='UX Tooltip Mês Financeiro', expr=TT_MES, folder='08 UX\\Componentes',
             desc='Tooltip mensal: recebido, pago, saldo, receita, margem e resultado gerencial.'),
    ])
    print('ok')
