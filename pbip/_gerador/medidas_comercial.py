# NEXUS 360 - Etapa B: medidas de apresentacao da Commercial Intelligence
# So medidas de UX (HTML/SVG/cores). As medidas de negocio reaproveitadas ja estao validadas no QA do modelo.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

CP, CN, CNEU = '#45D5A1', '#FF7285', '#A9B9CA'


def kpi(i, rotulo, valor, delta, cor, cur, ly, nota):
    """Bloco da faixa de KPIs: valor, variacao vs ano anterior e barras atual x ano anterior (SVG)."""
    return f'''"<div class='nx-c' style='animation-delay:{i * 0.07:.2f}s'><div class='nx-cl'>{rotulo}</div><div class='nx-cv'>" & {valor} & "</div>"
        & IF ( _umAno && NOT ISBLANK ( {ly} ),
            "<div class='nx-cd' style='color:" & {cor} & "'>" & {delta} & " <span>vs ano anterior</span></div>"
                & "<svg class='nx-cb' viewBox='0 0 200 22' preserveAspectRatio='none'><rect x='0' y='2' height='7' rx='2' fill='#10D4C4' width='" & FORMAT ( 200 * DIVIDE ( {cur}, MAX ( {cur}, {ly} ) ), "0", "en-US" ) & "'/><rect x='0' y='13' height='7' rx='2' fill='#3E5C7A' width='" & FORMAT ( 200 * DIVIDE ( {ly}, MAX ( {cur}, {ly} ) ), "0", "en-US" ) & "'/></svg>",
            "<div class='nx-cd' style='color:#A9B9CA'>{nota}</div>" )
        & "</div>"'''


KPIS = r'''
VAR _corte = [Data Corte]
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _rec = [Receita (até corte)]
VAR _recLY = [Receita LY]
VAR _mg = [Margem Bruta %]
VAR _mgLY = [Margem Bruta % LY]
VAR _ds = [Desconto Médio Ponderado %]
VAR _dsLY = CALCULATE ( CALCULATE ( [Desconto Médio Ponderado %], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _cl = [Clientes Positivados]
VAR _clLY = CALCULATE ( CALCULATE ( [Clientes Positivados], SAMEPERIODLASTYEAR ( dCalendario[Data] ) ), KEEPFILTERS ( dCalendario[Data] <= _corte ) )
VAR _css = "<style>.nx-r{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(4,1fr);height:100vh;box-sizing:border-box;gap:16px}.nx-c{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:12px 18px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-cl{font-size:10px;letter-spacing:.12em;color:#A9B9CA;text-transform:uppercase}.nx-cv{font-size:26px;font-weight:600;color:#FFFFFF;line-height:1.15;margin-top:3px}.nx-cd{font-size:11px;font-weight:600;margin-top:2px}.nx-cd span{color:#6F86A0;font-weight:400}.nx-cb{width:100%;height:20px;margin-top:6px}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-c{animation:none}}</style>"
RETURN
    _css & "<div class='nx-r'>"
''' + '        & ' + kpi(0, 'Receita líquida', '"R$ " & FORMAT ( [Receita Líquida] / 1e6, "#,0.0", "pt-BR" ) & " mi"',
                     'FORMAT ( DIVIDE ( _rec - _recLY, _recLY ), "▲ 0.0%;▼ 0.0%", "pt-BR" )', 'IF ( _rec >= _recLY, "' + CP + '", "' + CN + '" )',
                     '_rec', '_recLY', 'Selecione um único ano para comparar') + '\n' \
  + '        & ' + kpi(1, 'Margem bruta', 'FORMAT ( _mg, "0.0%", "pt-BR" )',
                     'FORMAT ( ( _mg - _mgLY ) * 100, "▲ 0.0;▼ 0.0", "pt-BR" ) & " p.p."', 'IF ( _mg >= _mgLY, "' + CP + '", "' + CN + '" )',
                     '_mg', '_mgLY', 'Selecione um único ano para comparar') + '\n' \
  + '        & ' + kpi(2, 'Desconto médio ponderado', 'FORMAT ( _ds, "0.0%", "pt-BR" )',
                     'FORMAT ( ( _ds - _dsLY ) * 100, "▲ 0.0;▼ 0.0", "pt-BR" ) & " p.p."', 'IF ( _ds <= _dsLY, "' + CP + '", "' + CN + '" )',
                     '_ds', '_dsLY', 'Selecione um único ano para comparar') + '\n' \
  + '        & ' + kpi(3, 'Clientes positivados', 'FORMAT ( _cl, "#,0", "pt-BR" )',
                     'FORMAT ( DIVIDE ( _cl - _clLY, _clLY ), "▲ 0.0%;▼ 0.0%", "pt-BR" )', 'IF ( _cl >= _clLY, "' + CP + '", "' + CN + '" )',
                     '_cl', '_clLY', 'Selecione um único ano para comparar') + '\n        & "</div>"\n'

COR_MARGEM = r'''
VAR _m = [Margem Bruta %]
VAR _ref = CALCULATE ( [Margem Bruta %], ALLSELECTED () )
RETURN SWITCH ( TRUE (), ISBLANK ( _m ), "#A9B9CA", _m - _ref >= 0.005, "#45D5A1", _m - _ref <= -0.005, "#FF7285", "#5FA8E6" )
'''
COR_YOY = r'''
VAR _v = [Receita YoY %]
RETURN SWITCH ( TRUE (), ISBLANK ( _v ), "#A9B9CA", _v >= 0, "#45D5A1", "#FF7285" )
'''
BARRA_PART = r'''
VAR _p = [Participação Receita %]
VAR _max =
    SWITCH (
        TRUE (),
        ISINSCOPE ( dProduto[Subcategoria] ), MAXX ( ALLSELECTED ( dProduto[Subcategoria] ), [Participação Receita %] ),
        ISINSCOPE ( dProduto[Categoria] ), MAXX ( ALLSELECTED ( dProduto[Categoria] ), [Participação Receita %] ),
        _p
    )
VAR _w = FORMAT ( 110 * DIVIDE ( _p, _max ), "0", "en-US" )
RETURN
    IF (
        NOT ISBLANK ( _p ) && ( ISINSCOPE ( dProduto[Categoria] ) || ISINSCOPE ( dProduto[Subcategoria] ) ),
        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='16'><rect x='0' y='4' width='110' height='8' rx='3' fill='%2312304F'/><rect x='0' y='4' width='" & _w & "' height='8' rx='3' fill='%2310D4C4'/></svg>"
    )
'''
OPORT = r'''
VAR _umAno = HASONEVALUE ( dCalendario[Ano] )
VAR _v =
    FILTER (
        ADDCOLUMNS (
            VALUES ( dVendedor[Vendedor] ),
            "@r", [Receita Líquida],
            "@d", [Desconto Médio Ponderado %],
            "@m", [Margem Bruta %]
        ),
        [@r] > 0
    )
VAR _n = COUNTROWS ( _v )
VAR _p75 = PERCENTILEX.INC ( _v, [@d], 0.75 )
VAR _med = MEDIANX ( _v, [@m] )
VAR _crit = FILTER ( _v, [@d] > _p75 && [@m] < _med )
VAR _tot = SUMX ( _v, [@r] )
VAR _top = TOPN ( ROUNDUP ( _n * 0.2, 0 ), _v, [@r], DESC )
VAR _conc = DIVIDE ( SUMX ( _top, [@r] ), _tot )
VAR _sub =
    FILTER (
        ADDCOLUMNS ( VALUES ( dProduto[Subcategoria] ), "@dy", [Receita YoY Δ], "@py", [Receita YoY %] ),
        NOT ISBLANK ( [@dy] ) && [@dy] < 0
    )
VAR _subTxt =
    IF (
        NOT _umAno, "<div class='nx-o-e'>Selecione um único ano para comparar com o anterior.</div>",
        IF (
            ISEMPTY ( _sub ), "<div class='nx-o-e'>Nenhuma subcategoria abaixo do ano anterior.</div>",
            CONCATENATEX (
                TOPN ( 3, _sub, [@dy], ASC ),
                "<div class='nx-o-l'><span>" & dProduto[Subcategoria] & "</span><b style='color:#FF7285'>" & FORMAT ( [@dy] / 1e6, "#,0.0", "pt-BR" ) & " mi · " & FORMAT ( [@py], "0.0%", "pt-BR" ) & "</b></div>",
                "", [@dy], ASC
            )
        )
    )
VAR _vendTxt =
    CONCATENATEX (
        TOPN ( 3, _crit, [@r], DESC ),
        "<div class='nx-o-l'><span>" & dVendedor[Vendedor] & "</span><b>" & FORMAT ( [@d], "0.0%", "pt-BR" ) & " desc. · " & FORMAT ( [@m], "0.0%", "pt-BR" ) & " marg.</b></div>",
        "", [@r], DESC
    )
VAR _css = "<style>.nx-o{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 20px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr;gap:10px 22px}.nx-o-t{grid-column:1/3;font-size:13px;font-weight:600;text-align:center}.nx-o-b{border-left:3px solid #FFC66D;padding-left:12px}.nx-o-b.n{border-color:#FF7285}.nx-o-b.i{border-color:#5FA8E6}.nx-o-h{font-size:10px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin-bottom:6px}.nx-o-k{font-size:24px;font-weight:600}.nx-o-s{font-size:11px;color:#A9B9CA;margin-bottom:6px}.nx-o-l{display:flex;justify-content:space-between;font-size:11.5px;padding:3px 0;border-bottom:1px solid #12304F;color:#C9D6E3}.nx-o-l b{font-weight:600;color:#FFFFFF}.nx-o-e{font-size:11px;color:#6F86A0}</style>"
RETURN
    _css & "<div class='nx-o'><div class='nx-o-t'>Oportunidades e exceções comerciais</div>"
        & "<div class='nx-o-b n'><div class='nx-o-h'>Subcategorias em queda</div>" & _subTxt & "</div>"
        & "<div><div class='nx-o-b'><div class='nx-o-h'>Desconto alto e margem baixa</div><div class='nx-o-k'>" & COUNTROWS ( _crit ) & " <span style='font-size:13px;color:#A9B9CA'>de " & _n & " vendedores</span></div>"
        & "<div class='nx-o-s'>desconto acima do 3º quartil (" & FORMAT ( _p75, "0.0%", "pt-BR" ) & ") e margem abaixo da mediana (" & FORMAT ( _med, "0.0%", "pt-BR" ) & ")</div>" & _vendTxt & "</div>"
        & "<div class='nx-o-b i' style='margin-top:12px'><div class='nx-o-h'>Concentração</div><div class='nx-o-s' style='margin:0'><b style='color:#FFFFFF;font-size:15px'>" & FORMAT ( _conc, "0.0%", "pt-BR" ) & "</b> da receita vem dos 20% maiores vendedores (" & ROUNDUP ( _n * 0.2, 0 ) & ")</div></div></div></div>"
'''
TT_VEND = r'''
VAR _vend = SELECTEDVALUE ( dVendedor[Vendedor] )
VAR _eq = SELECTEDVALUE ( dVendedor[Equipe] )
VAR _fil = CALCULATE ( SELECTEDVALUE ( dFilial[Cidade] ), TREATAS ( VALUES ( dVendedor[FilialID] ), dFilial[FilialID] ) )
VAR _ref = [Data Referência]
VAR _rec = [Receita Líquida]
VAR _yoy = IF ( HASONEVALUE ( dCalendario[Ano] ), [Receita YoY %] )
VAR _mg = [Margem Bruta %]
VAR _mgRef = CALCULATE ( [Margem Bruta %], REMOVEFILTERS ( dVendedor ) )
VAR _ds = [Desconto Médio Ponderado %]
VAR _dsRef = CALCULATE ( [Desconto Médio Ponderado %], REMOVEFILTERS ( dVendedor ) )
VAR _cl = [Clientes Positivados]
VAR _rk = IF ( NOT ISBLANK ( _vend ), RANKX ( FILTER ( ALL ( dVendedor[Vendedor] ), [Receita Líquida] > 0 ), [Receita Líquida], , DESC ) )
VAR _nv = COUNTROWS ( FILTER ( ALL ( dVendedor[Vendedor] ), [Receita Líquida] > 0 ) )
VAR _serie =
    ADDCOLUMNS (
        GENERATESERIES ( 0, 11, 1 ),
        "@V",
            VAR _f = EOMONTH ( _ref, - [Value] )
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EOMONTH ( _f, -1 ) + 1, dCalendario[Data] <= _f )
    )
VAR _ok = FILTER ( _serie, NOT ISBLANK ( [@V] ) )
VAR _min = MINX ( _ok, [@V] )
VAR _max = MAXX ( _ok, [@V] )
VAR _rng = IF ( _max = _min, 1, _max - _min )
VAR _bars = CONCATENATEX ( _ok, VAR _h = 4 + ( [@V] - _min ) / _rng * 26 RETURN "<rect x='" & ( 11 - [Value] ) * 22 & "' y='" & FORMAT ( 32 - _h, "0.0", "en-US" ) & "' width='16' height='" & FORMAT ( _h, "0.0", "en-US" ) & "' rx='2' fill='" & IF ( [Value] = 0, "#10D4C4", "#0878C9" ) & "'/>", "" )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600}.nx-ts{font-size:10px;color:#A9B9CA;letter-spacing:.06em;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin-top:8px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}.nx-tv small{font-size:10.5px;font-weight:600;margin-left:4px}</style>"
RETURN
    IF (
        NOT ISBLANK ( _vend ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _vend & "</div><div class='nx-ts'>" & UPPER ( _eq ) & " · " & UPPER ( _fil ) & " · " & _rk & "º DE " & _nv & " EM RECEITA</div>"
            & "<svg width='260' height='34' viewBox='0 0 260 34' aria-hidden='true'>" & _bars & "</svg>"
            & "<div class='nx-tg'>"
            & "<div><div class='nx-tk'>Receita</div><div class='nx-tv'>R$ " & FORMAT ( _rec / 1e6, "#,0.00", "pt-BR" ) & " mi" & IF ( NOT ISBLANK ( _yoy ), "<small style='color:" & IF ( _yoy >= 0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _yoy, "+0.0%;-0.0%", "pt-BR" ) & "</small>" ) & "</div></div>"
            & "<div><div class='nx-tk'>Clientes positivados</div><div class='nx-tv'>" & FORMAT ( _cl, "#,0", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Margem bruta (média " & FORMAT ( _mgRef, "0.0%", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _mg >= _mgRef, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _mg, "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Desconto (média " & FORMAT ( _dsRef, "0.0%", "pt-BR" ) & ")</div><div class='nx-tv' style='color:" & IF ( _ds <= _dsRef, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _ds, "0.0%", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
'''
if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='UX Comercial KPIs', expr=KPIS, folder='08 UX\\Comercial',
             desc='Faixa de 4 KPIs comerciais com variacao vs ano anterior (ate o corte) e barras atual x anterior. Desconto maior e desfavoravel.'),
        dict(name='UX Cor Margem vs Média', expr=COR_MARGEM, folder='08 UX\\Cores',
             desc='Verde/vermelho quando a margem do item difere em 0,5 p.p. ou mais da margem da selecao (ALLSELECTED); azul na faixa neutra.'),
        dict(name='UX Cor Receita YoY', expr=COR_YOY, folder='08 UX\\Cores', desc='Verde para crescimento, vermelho para queda vs ano anterior.'),
        dict(name='UX Barra Participação', expr=BARRA_PART, folder='08 UX\\Comercial', cat='ImageUrl',
             desc='Barra SVG da participacao na receita, escalada pelo maior item do mesmo nivel (categoria ou subcategoria).'),
        dict(name='UX Comercial Oportunidades', expr=OPORT, folder='08 UX\\Comercial',
             desc='Diagnostico: subcategorias em queda vs ano anterior, vendedores com desconto acima do 3o quartil e margem abaixo da mediana, concentracao da receita nos 20% maiores vendedores.'),
        dict(name='UX Tooltip Vendedor', expr=TT_VEND, folder='08 UX\\Componentes',
             desc='Tooltip de vendedor: equipe, filial, ranking, receita 12 meses, margem e desconto vs media.'),
    ])
    print('ok')
