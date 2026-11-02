# NEXUS 360 - Etapa D: medidas de apresentacao da Logistics Control Tower (medidas de negocio de 03 Logistica ja validadas)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert
from nx_geo import BR

KPIS = r'''
VAR _corte = [Data Corte]
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _otif = [OTIF %]
VAR _meta = CALCULATE ( [Meta OTIF % (média simples)], KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _otifLY = CALCULATE ( CALCULATE ( [OTIF %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _fe = [Frete por Entrega]
VAR _feLY = CALCULATE ( CALCULATE ( [Frete por Entrega], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _atr = DIVIDE ( [Entregas] - [Entregas No Prazo], [Entregas] )
VAR _w = FORMAT ( 100 * MIN ( _otif, 1 ), "0.0", "en-US" )
VAR _wm = FORMAT ( 100 * MIN ( _meta, 1 ), "0.0", "en-US" )
VAR _cO = IF ( _otif >= _meta, "#45D5A1", IF ( _otif >= _meta - 0.05, "#FFC66D", "#FF7285" ) )
VAR _t = "<div class='nx-k'><div class='nx-kl'>@L</div><div class='nx-kv'>@V</div><div class='nx-ks'>@S</div></div>"
VAR _css = "<style>.nx-l{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:1.6fr repeat(6,1fr);gap:12px;height:100vh;box-sizing:border-box}.nx-k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:12px 16px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-kl{font-size:10px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:24px;font-weight:600;color:#FFFFFF;margin-top:3px;line-height:1.1}.nx-ks{font-size:10.5px;color:#A9B9CA;margin-top:3px}.nx-bl{position:relative;height:10px;background:#12304F;border-radius:5px;margin-top:9px}.nx-bf{position:absolute;left:0;top:0;bottom:0;border-radius:5px}.nx-bm{position:absolute;top:-4px;width:2px;height:18px;background:#FFFFFF}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
RETURN
    _css & "<div class='nx-l'>"
        & "<div class='nx-k' style='border-left:4px solid " & _cO & "'><div class='nx-kl'>OTIF (no prazo e completo)</div><div class='nx-kv' style='color:" & _cO & "'>" & FORMAT ( _otif, "0.0%", "pt-BR" ) & " <span style='font-size:12px;color:#A9B9CA;font-weight:400'>meta " & FORMAT ( _meta, "0.0%", "pt-BR" ) & "</span></div>"
        & "<div class='nx-bl'><div class='nx-bf' style='width:" & _w & "%;background:" & _cO & "'></div><div class='nx-bm' style='left:" & _wm & "%'></div></div>"
        & "<div class='nx-ks'>" & IF ( _umAno && NOT ISBLANK ( _otifLY ), FORMAT ( ( _otif - _otifLY ) * 100, "▲ 0.0;▼ 0.0", "pt-BR" ) & " p.p. vs ano anterior", "Selecione um único ano para comparar" ) & "</div></div>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "No prazo" ), "@V", FORMAT ( [No Prazo %], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [Entregas No Prazo], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Completas (in full)" ), "@V", FORMAT ( [In Full %], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [Entregas In Full], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Com ocorrência" ), "@V", FORMAT ( [Ocorrência %], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [Entregas com Ocorrência], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Atraso médio" ), "@V", FORMAT ( [Atraso Médio (dias)], "0.0", "pt-BR" ) & " dias" ), "@S", FORMAT ( _atr, "0.0%", "pt-BR" ) & " das entregas fora do prazo" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Lead time pedido→entrega" ), "@V", FORMAT ( [Lead Time Médio (dias)], "0.0", "pt-BR" ) & " dias" ), "@S", FORMAT ( [Entregas], "#,0", "pt-BR" ) & " entregas" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Frete por entrega" ), "@V", "R$ " & FORMAT ( _fe, "#,0", "pt-BR" ) ), "@S", IF ( _umAno && NOT ISBLANK ( _feLY ), FORMAT ( DIVIDE ( _fe - _feLY, _feLY ), "▲ 0.0%;▼ 0.0%", "pt-BR" ) & " vs ano ant. · ", "" ) & FORMAT ( [Frete % Receita], "0.0%", "pt-BR" ) & " da receita" )
        & "</div>"
'''

MAPA = r'''
VAR _corte = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        VALUES ( dFilial[FilialID] ),
        "@cid", CALCULATE ( SELECTEDVALUE ( dFilial[Cidade] ) ),
        "@x", CALCULATE ( ( SELECTEDVALUE ( dFilial[Longitude] ) + 74.2 ) * 12 * 0.970296 ),
        "@y", CALCULATE ( ( 5.6 - SELECTEDVALUE ( dFilial[Latitude] ) ) * 12 ),
        "@e", [Entregas],
        "@o", [OTIF %],
        "@d", [Desvio OTIF vs Meta (p.p.)]
    )
VAR _ok = FILTER ( _t, [@e] > 0 )
VAR _max = MAXX ( _ok, [@e] )
VAR _pts =
    CONCATENATEX (
        _ok,
        VAR _r = 4 + 6 * SQRT ( DIVIDE ( [@e], _max ) )
        VAR _c = SWITCH ( TRUE (), ISBLANK ( [@d] ), "#A9B9CA", [@d] >= 0, "#45D5A1", [@d] >= -5, "#FFC66D", "#FF7285" )
        RETURN "<circle cx='" & FORMAT ( [@x], "0.0", "en-US" ) & "' cy='" & FORMAT ( [@y], "0.0", "en-US" ) & "' r='" & FORMAT ( _r, "0.0", "en-US" ) & "' fill='" & _c & "' fill-opacity='.9' stroke='#071528' stroke-width='1.2'/>",
        "", [@e], DESC
    )
VAR _lista =
    CONCATENATEX (
        _ok,
        VAR _c = SWITCH ( TRUE (), ISBLANK ( [@d] ), "#A9B9CA", [@d] >= 0, "#45D5A1", [@d] >= -5, "#FFC66D", "#FF7285" )
        RETURN "<div class='nx-li'><span class='nx-ci'>" & [@cid] & "</span><b style='color:" & _c & "'>" & FORMAT ( [@o], "0.0%", "pt-BR" ) & "</b><span class='nx-dv'>" & FORMAT ( [@d], "+0.0;-0.0", "pt-BR" ) & "</span></div>",
        "", [@o], ASC
    )
VAR _css = "<style>.nx-m{font-family:'Segoe UI',sans-serif;color:#FFFFFF;box-sizing:border-box;height:100vh;padding:12px 16px;display:flex;flex-direction:column}.nx-t{font-size:13px;font-weight:600;text-align:center}.nx-s{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 6px}.nx-g{display:flex;gap:10px;flex:1;align-items:center}.nx-l{flex:1}.nx-li{display:flex;align-items:center;font-size:11px;height:20px;border-bottom:1px solid #12304F}.nx-ci{flex:1;color:#C9D6E3}.nx-li b{width:46px;text-align:right}.nx-dv{width:40px;text-align:right;color:#6F86A0;font-size:10px}.nx-lg{display:flex;gap:12px;justify-content:center;font-size:10px;color:#A9B9CA;margin-top:6px}.nx-lg i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}</style>"
RETURN
    IF (
        NOT ISEMPTY ( _ok ),
        _css & "<div class='nx-m'><div class='nx-t'>OTIF por filial de origem</div><div class='nx-s'>tamanho = entregas · Δ em p.p. vs meta da filial</div>"
            & "<div class='nx-g'><svg width='230' height='238' viewBox='120 160 340 330' role='img' aria-label='Mapa das filiais com OTIF'><path d='" & "@@BR@@" & "' fill='#0A2540' stroke='#10D4C4' stroke-opacity='.45' stroke-width='1.6'/>" & _pts & "</svg>"
            & "<div class='nx-l'>" & _lista & "</div></div>"
            & "<div class='nx-lg'><span><i style='background:#45D5A1'></i>na meta</span><span><i style='background:#FFC66D'></i>até 5 p.p. abaixo</span><span><i style='background:#FF7285'></i>mais de 5 p.p. abaixo</span></div></div>"
    )
'''.replace('@@BR@@', BR)

TT_TRANSP = r'''
VAR _tr = SELECTEDVALUE ( dTransportadora[Transportadora] )
VAR _ref = [Data Referência]
VAR _otif = [OTIF %]
VAR _otifRef = CALCULATE ( [OTIF %], REMOVEFILTERS ( dTransportadora ) )
VAR _fe = [Frete por Entrega]
VAR _feRef = CALCULATE ( [Frete por Entrega], REMOVEFILTERS ( dTransportadora ) )
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( [OTIF %], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _ok = FILTER ( _serie, NOT ISBLANK ( [@V] ) )
VAR _min = MINX ( _ok, [@V] ) - 0.02
VAR _max = MAXX ( _ok, [@V] ) + 0.02
VAR _pts = CONCATENATEX ( _ok, FORMAT ( ( 11 - [Value] ) * 23 + 4, "0", "en-US" ) & "," & FORMAT ( 30 - ( [@V] - _min ) / ( _max - _min ) * 26, "0.0", "en-US" ), " ", [Value], DESC )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600}.nx-ts{font-size:10px;color:#A9B9CA;margin-bottom:4px}.nx-tg{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px 12px;margin-top:6px}.nx-tk{font-size:9.5px;color:#A9B9CA}.nx-tv{font-size:13px;font-weight:600}</style>"
RETURN
    IF (
        NOT ISBLANK ( _tr ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _tr & "</div><div class='nx-ts'>" & SELECTEDVALUE ( dTransportadora[Modal] ) & " · " & FORMAT ( [Entregas], "#,0", "pt-BR" ) & " entregas · OTIF 12 meses</div>"
            & "<svg width='264' height='32' viewBox='0 0 264 32'><polyline points='" & _pts & "' fill='none' stroke='#10D4C4' stroke-width='2'/></svg>"
            & "<div class='nx-tg'>"
            & "<div><div class='nx-tk'>OTIF (geral " & FORMAT ( _otifRef, "0.0%", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _otif >= _otifRef, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _otif, "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>No prazo</div><div class='nx-tv'>" & FORMAT ( [No Prazo %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Completas</div><div class='nx-tv'>" & FORMAT ( [In Full %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Atraso médio</div><div class='nx-tv'>" & FORMAT ( [Atraso Médio (dias)], "0.0", "pt-BR" ) & " d</div></div>"
            & "<div><div class='nx-tk'>Ocorrência</div><div class='nx-tv'>" & FORMAT ( [Ocorrência %], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Frete/entrega (geral R$ " & FORMAT ( _feRef, "#,0", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _fe <= _feRef, "#45D5A1", "#FF7285" ) & "'>R$ " & FORMAT ( _fe, "#,0", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
'''
COR_OTIF_REL = r'''
VAR _o = [OTIF %]
VAR _ref = CALCULATE ( [OTIF %], ALLSELECTED ( dTransportadora ) )
RETURN SWITCH ( TRUE (), ISBLANK ( _o ), "#A9B9CA", _o - _ref >= 0.01, "#45D5A1", _o - _ref <= -0.01, "#FF7285", "#FFFFFF" )
'''
if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='UX Logística KPIs', expr=KPIS, folder='08 UX\\Logística',
             desc='Faixa de KPIs logisticos: OTIF com bullet vs meta (media simples das metas filial-mes ate o corte), no prazo, in full, ocorrencia, atraso medio, lead time e frete por entrega.'),
        dict(name='UX Logística Mapa', expr=MAPA, folder='08 UX\\Logística',
             desc='Mapa SVG das filiais (lat/long de dFilial) com OTIF e desvio vs meta; tamanho pelas entregas. Sem rotas: a fonte nao tem destino geografico.'),
        dict(name='UX Tooltip Transportadora', expr=TT_TRANSP, folder='08 UX\\Componentes',
             desc='Tooltip de transportadora: modal, entregas, OTIF 12 meses, OTIF e frete por entrega vs total geral, no prazo, in full, atraso e ocorrencia.'),
        dict(name='UX Cor OTIF Relativo', expr=COR_OTIF_REL, folder='08 UX\\Cores',
             desc='Verde/vermelho quando o OTIF difere 1 p.p. ou mais do OTIF da selecao de transportadoras; branco na faixa neutra.'),
    ])
    print('ok')
