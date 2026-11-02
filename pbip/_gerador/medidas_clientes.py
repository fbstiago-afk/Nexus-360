# NEXUS 360 - Etapa C: medidas da Customer Intelligence
# Reaproveita as medidas de churn validadas (Clientes por Status e derivadas). Novas medidas de negocio: so de detalhe por cliente.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

DIAS = r'''
VAR _ref = [Data Referência]
VAR _ult = CALCULATE ( MAX ( fFaturamento[DataFaturamento] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
RETURN IF ( NOT ISBLANK ( _ult ) && HASONEVALUE ( dCliente[ClienteID] ), DATEDIFF ( _ult, _ref, DAY ) )
'''
REC12 = r'''
VAR _ref = [Data Referência]
RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] > EDATE ( _ref, -12 ), dCalendario[Data] <= _ref )
'''
PRIOR = r'''
VAR _d = [Dias sem Compra (Data Ref.)]
RETURN IF ( _d >= [Limite Ativo (dias)] && _d < [Limite Churn (dias)], [Receita 12M (Data Ref.)] )
'''

STATUS = r'''
VAR _ref = [Data Referência]
VAR _hist = [Clientes com Histórico]
VAR _st =
    ADDCOLUMNS (
        ALL ( dStatusCliente[Status], dStatusCliente[Ordem] ),
        "@n", CALCULATE ( [Clientes por Status] ),
        "@c", SWITCH ( dStatusCliente[Status], "Novo", "#7FE6DD", "Ativo", "#45D5A1", "Reativado", "#5FA8E6", "Em risco", "#FFC66D", "#FF7285" )
    )
VAR _seg = CONCATENATEX ( _st, "<span style='flex:" & FORMAT ( [@n], "0", "en-US" ) & ";background:" & [@c] & "'></span>", "", dStatusCliente[Ordem], ASC )
VAR _rows =
    CONCATENATEX (
        _st,
        "<div class='nx-sr'><span class='nx-sd' style='background:" & [@c] & "'></span><span class='nx-sn'>" & dStatusCliente[Status] & "</span><b>" & FORMAT ( [@n], "#,0", "pt-BR" ) & "</b><span class='nx-sp'>" & FORMAT ( DIVIDE ( [@n], _hist ), "0.0%", "pt-BR" ) & "</span></div>",
        "", dStatusCliente[Ordem], ASC
    )
VAR _css = "<style>.nx-s{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:16px 20px;display:flex;flex-direction:column;gap:12px;animation:nxIn .6s ease-out both}.nx-st{font-size:13px;font-weight:600;text-align:center}.nx-sh{font-size:10px;letter-spacing:.12em;color:#A9B9CA;text-transform:uppercase}.nx-sk{font-size:30px;font-weight:600;line-height:1.05}.nx-sk small{font-size:12px;color:#A9B9CA;font-weight:400;margin-left:6px}.nx-bar{display:flex;height:10px;border-radius:5px;overflow:hidden;gap:2px;margin:6px 0 4px}.nx-sr{display:flex;align-items:center;gap:8px;font-size:12px;padding:4px 0;border-bottom:1px solid #12304F}.nx-sd{width:9px;height:9px;border-radius:50%}.nx-sn{flex:1;color:#C9D6E3}.nx-sr b{font-weight:600;width:60px;text-align:right}.nx-sp{width:46px;text-align:right;color:#A9B9CA}.nx-g2{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}.nx-g2 .nx-sk{font-size:20px}.nx-blk{border-left:3px solid #173B5C;padding-left:10px}.nx-blk.r{border-color:#FF7285}.nx-blk.a{border-color:#FFC66D}.nx-blk.g{border-color:#45D5A1}.nx-blk.b{border-color:#5FA8E6}.nx-nt{font-size:10px;color:#6F86A0}@keyframes nxIn{from{opacity:0}to{opacity:1}}@media (prefers-reduced-motion:reduce){.nx-s{animation:none}}</style>"
RETURN
    IF (
        NOT ISBLANK ( _ref ),
        _css & "<div class='nx-s'><div class='nx-st'>Base de clientes em " & FORMAT ( _ref, "dd/mm/yyyy" ) & "</div>"
            & "<div><div class='nx-sh'>Clientes com histórico</div><div class='nx-sk'>" & FORMAT ( _hist, "#,0", "pt-BR" ) & "</div><div class='nx-bar'>" & _seg & "</div>" & _rows & "</div>"
            & "<div class='nx-g2'><div class='nx-blk r'><div class='nx-sh'>Taxa de churn</div><div class='nx-sk'>" & FORMAT ( [Taxa de Churn %], "0.0%", "pt-BR" ) & "</div><div class='nx-nt'>sem compra há " & [Limite Churn (dias)] & "+ dias</div></div>"
            & "<div class='nx-blk a'><div class='nx-sh'>Em risco</div><div class='nx-sk'>" & FORMAT ( [Clientes em Risco %], "0.0%", "pt-BR" ) & "</div><div class='nx-nt'>" & [Limite Ativo (dias)] & " a " & ( [Limite Churn (dias)] - 1 ) & " dias</div></div></div>"
            & "<div class='nx-g2'><div class='nx-blk b'><div class='nx-sh'>Reativações no período</div><div class='nx-sk'>" & FORMAT ( [Reativações no Período], "#,0", "pt-BR" ) & "</div><div class='nx-nt'>retorno após " & [Limite Churn (dias)] & "+ dias sem compra</div></div>"
            & "<div class='nx-blk b'><div class='nx-sh'>Receita recuperada</div><div class='nx-sk'>R$ " & FORMAT ( [Receita Recuperada] / 1e6, "#,0.0", "pt-BR" ) & " mi</div><div class='nx-nt'>faturas de reativados no período</div></div></div>"
            & "<div class='nx-g2'><div class='nx-blk g'><div class='nx-sh'>Taxa de recompra</div><div class='nx-sk'>" & FORMAT ( [Taxa de Recompra %], "0.0%", "pt-BR" ) & "</div><div class='nx-nt'>clientes com 2+ faturas no período</div></div>"
            & "<div class='nx-blk g'><div class='nx-sh'>Intervalo entre compras</div><div class='nx-sk'>" & FORMAT ( [Intervalo Médio entre Compras (dias)], "#,0", "pt-BR" ) & " <small>dias (mediana " & FORMAT ( [Intervalo Mediano entre Compras (dias)], "#,0", "pt-BR" ) & ")</small></div><div class='nx-nt'>" & FORMAT ( [Compras por Cliente], "0.00", "pt-BR" ) & " compras por cliente</div></div></div>"
            & "</div>"
    )
'''

FREQVAL = r'''
VAR _t =
    FILTER (
        ADDCOLUMNS (
            SUMMARIZE ( fFaturamento, fFaturamento[ClienteID] ),
            "@f", CALCULATE ( COUNTROWS ( fFaturamento ) ),
            "@v", CALCULATE ( SUM ( fFaturamento[ReceitaLiquida] ) )
        ),
        [@v] > 0
    )
VAR _n = COUNTROWS ( _t )
VAR _tot = SUMX ( _t, [@v] )
VAR _q1 = PERCENTILEX.INC ( _t, [@v], 0.25 )
VAR _q2 = PERCENTILEX.INC ( _t, [@v], 0.5 )
VAR _q3 = PERCENTILEX.INC ( _t, [@v], 0.75 )
VAR _b =
    ADDCOLUMNS (
        _t,
        "@fb", SWITCH ( TRUE (), [@f] = 1, 1, [@f] = 2, 2, [@f] <= 4, 3, 4 ),
        "@vb", SWITCH ( TRUE (), [@v] > _q3, 4, [@v] > _q2, 3, [@v] > _q1, 2, 1 )
    )
VAR _g = GROUPBY ( _b, [@vb], [@fb], "@cn", COUNTX ( CURRENTGROUP (), 1 ), "@rv", SUMX ( CURRENTGROUP (), [@v] ) )
VAR _max = MAXX ( _g, [@cn] )
VAR _hdr = "<div></div><div class='nx-fh'>1 compra</div><div class='nx-fh'>2</div><div class='nx-fh'>3–4</div><div class='nx-fh'>5+</div>"
VAR _lbl = SELECTCOLUMNS ( { ( 4, "Valor Q4 (maior)" ), ( 3, "Valor Q3" ), ( 2, "Valor Q2" ), ( 1, "Valor Q1 (menor)" ) }, "vb", [Value1], "lb", [Value2] )
VAR _grid =
    CONCATENATEX (
        _lbl,
        VAR _vb = [vb]
        RETURN
            "<div class='nx-fl'>" & [lb] & "</div>"
                & CONCATENATEX (
                    { 1, 2, 3, 4 },
                    VAR _fb = [Value]
                    VAR _c = MAXX ( FILTER ( _g, [@vb] = _vb && [@fb] = _fb ), [@cn] )
                    VAR _r = MAXX ( FILTER ( _g, [@vb] = _vb && [@fb] = _fb ), [@rv] )
                    VAR _a = FORMAT ( 0.12 + 0.78 * DIVIDE ( _c, _max ), "0.00", "en-US" )
                    VAR _hl = IF ( _vb = 4 && _fb = 1, " nx-hl", "" )
                    RETURN "<div class='nx-fc" & _hl & "' style='background:rgba(16,212,196," & _a & ")'><b>" & FORMAT ( _c, "#,0", "pt-BR" ) & "</b><span>" & FORMAT ( DIVIDE ( _r, _tot ), "0%", "pt-BR" ) & " rec.</span></div>",
                    "", [Value], ASC
                ),
        "", [vb], DESC
    )
VAR _hv = MAXX ( FILTER ( _g, [@vb] = 4 && [@fb] = 1 ), [@cn] )
VAR _hr = MAXX ( FILTER ( _g, [@vb] = 4 && [@fb] = 1 ), [@rv] )
VAR _css = "<style>.nx-f{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:12px 16px;display:flex;flex-direction:column}.nx-ft{font-size:13px;font-weight:600;text-align:center}.nx-fs{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 8px}.nx-fg{display:grid;grid-template-columns:92px repeat(4,1fr);gap:4px;flex:1}.nx-fh{font-size:10px;color:#A9B9CA;text-align:center;align-self:end}.nx-fl{font-size:10px;color:#A9B9CA;display:flex;align-items:center}.nx-fc{border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px}.nx-fc b{font-weight:600}.nx-fc span{font-size:9.5px;color:#E8F7F5}.nx-hl{outline:2px solid #FFC66D}.nx-fn{font-size:10.5px;color:#C9D6E3;margin-top:8px}.nx-fn b{color:#FFC66D}</style>"
RETURN
    IF (
        _n > 0,
        _css & "<div class='nx-f'><div class='nx-ft'>Frequência × valor dos clientes no período</div><div class='nx-fs'>" & FORMAT ( _n, "#,0", "pt-BR" ) & " clientes com fatura · valor em quartis · célula = clientes e % da receita</div>"
            & "<div class='nx-fg'>" & _hdr & _grid & "</div>"
            & "<div class='nx-fn'><b>" & FORMAT ( _hv, "#,0", "pt-BR" ) & "</b> clientes de maior valor compraram uma única vez (" & FORMAT ( DIVIDE ( _hr, _tot ), "0.0%", "pt-BR" ) & " da receita): candidatos a recompra.</div></div>"
    )
'''

TT_CLI = r'''
VAR _cli = SELECTEDVALUE ( dCliente[RazaoSocial] )
VAR _ref = [Data Referência]
VAR _ult = CALCULATE ( MAX ( fFaturamento[DataFaturamento] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
VAR _dias = [Dias sem Compra (Data Ref.)]
VAR _st = CALCULATE ( MAXX ( FILTER ( VALUES ( dStatusCliente[Status] ), [Clientes por Status] = 1 ), dStatusCliente[Status] ), ALL ( dStatusCliente ) )
VAR _rec12 = [Receita 12M (Data Ref.)]
VAR _fat12 = CALCULATE ( COUNTROWS ( fFaturamento ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] > EDATE ( _ref, -12 ), dCalendario[Data] <= _ref )
VAR _int = CALCULATE ( [Intervalo Médio entre Compras (dias)], REMOVEFILTERS ( dCalendario ), dCalendario[Data] <= _ref )
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( SUM ( fFaturamento[ReceitaLiquida] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _max = MAXX ( _serie, [@V] )
VAR _bars = CONCATENATEX ( _serie, VAR _h = IF ( ISBLANK ( [@V] ), 1, 3 + DIVIDE ( [@V], _max ) * 25 ) RETURN "<rect x='" & ( 11 - [Value] ) * 22 & "' y='" & FORMAT ( 30 - _h, "0.0", "en-US" ) & "' width='16' height='" & FORMAT ( _h, "0.0", "en-US" ) & "' rx='2' fill='" & IF ( ISBLANK ( [@V] ), "#173B5C", "#0878C9" ) & "'/>", "" )
VAR _cst = SWITCH ( _st, "Novo", "#7FE6DD", "Ativo", "#45D5A1", "Reativado", "#5FA8E6", "Em risco", "#FFC66D", "Churn", "#FF7285", "#A9B9CA" )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nx-ts{font-size:10px;color:#A9B9CA;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin-top:8px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}.nx-pill{display:inline-block;padding:1px 8px;border-radius:9px;font-size:10px;font-weight:600;color:#071528}</style>"
RETURN
    IF (
        NOT ISBLANK ( _cli ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _cli & "</div><div class='nx-ts'>" & SELECTEDVALUE ( dCliente[Segmento] ) & " · potencial " & SELECTEDVALUE ( dCliente[ClassePotencial] ) & " · <span class='nx-pill' style='background:" & _cst & "'>" & _st & "</span></div>"
            & "<svg width='260' height='30' viewBox='0 0 260 30' aria-hidden='true'>" & _bars & "</svg>"
            & "<div class='nx-tg'>"
            & "<div><div class='nx-tk'>Última compra</div><div class='nx-tv'>" & FORMAT ( _ult, "dd/mm/yyyy" ) & "</div></div>"
            & "<div><div class='nx-tk'>Dias sem compra</div><div class='nx-tv' style='color:" & _cst & "'>" & FORMAT ( _dias, "#,0", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Receita 12 meses</div><div class='nx-tv'>R$ " & FORMAT ( _rec12 / 1e3, "#,0", "pt-BR" ) & " mil · " & _fat12 & " fat.</div></div>"
            & "<div><div class='nx-tk'>Intervalo médio</div><div class='nx-tv'>" & IF ( ISBLANK ( _int ), "1ª compra", FORMAT ( _int, "#,0", "pt-BR" ) & " dias" ) & "</div></div>"
            & "</div></div>"
    )
'''

COR_JANELA = r'''IF ( SELECTEDVALUE ( 'Param Janela Comparativa'[Janela (dias)] ) = [Limite Churn (dias)], "#10D4C4", "#3E5C7A" )'''

if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='Dias sem Compra (Data Ref.)', expr=DIAS, folder='02 Clientes\\Detalhe', fmt='#,0',
             desc='Dias entre a ultima fatura do cliente e a Data Referencia. So no grao de um cliente.'),
        dict(name='Receita 12M (Data Ref.)', expr=REC12, folder='02 Clientes\\Detalhe', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00',
             desc='Receita liquida dos 12 meses encerrados na Data Referencia.'),
        dict(name='Prioridade Risco (Receita 12M)', expr=PRIOR, folder='02 Clientes\\Detalhe', fmt='R$ #,0.00;-R$ #,0.00;R$ #,0.00', hidden=True,
             desc='Receita 12M apenas para clientes Em risco (mesma regra de dias do status); ordena a lista de prioridade de contato.'),
        dict(name='UX Clientes Status', expr=STATUS, folder='08 UX\\Clientes',
             desc='Painel da base de clientes na Data Referencia: 5 status exclusivos, churn, risco, reativacao, receita recuperada e recompra (medidas validadas).'),
        dict(name='UX Clientes Freq Valor', expr=FREQVAL, folder='08 UX\\Clientes',
             desc='Grade frequencia (faturas no periodo: 1, 2, 3-4, 5+) x valor (quartis da receita do periodo). Faixas de exibicao, nao pontuacao RFM.'),
        dict(name='UX Tooltip Cliente', expr=TT_CLI, folder='08 UX\\Componentes',
             desc='Tooltip de cliente: segmento, potencial, status, ultima compra, dias sem compra, receita e faturas 12 meses, intervalo medio, barras mensais.'),
        dict(name='UX Cor Janela Churn', expr=COR_JANELA, folder='08 UX\\Cores', desc='Destaca a janela igual ao limite de churn vigente.'),
    ])
    print('ok')
