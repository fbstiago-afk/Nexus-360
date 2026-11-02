# NEXUS 360 - Etapa G: Predictive Intelligence
# Metodo de projecao (documentado e testavel): sazonal ingenuo ajustado pela tendencia de 12 meses.
#   Projecao(m) = Receita(m - 12 meses) x G, G = receita dos 12 meses ate o corte / receita dos 12 meses anteriores.
#   Faixa de 90%: Projecao x (1 +/- t(0,95; 9 gl) x sigma), sigma = desvio-padrao dos erros relativos do mesmo metodo
#   aplicado aos meses do ano do corte (backtest de 10 meses, cada um com G calculado ate o mes anterior).
# A previsao da fonte (fPrevisao, jan-jun/2027) e exibida separada; sua "margem de erro" nao tem semantica validada.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

FMT = 'R$ #,0.00;-R$ #,0.00;R$ #,0.00'
G = r'''
VAR _s = EOMONTH ( [Data Corte], 0 ) + 1
VAR _a = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _s, -12 ), dCalendario[Data] < _s )
VAR _b = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _s, -24 ), dCalendario[Data] < EDATE ( _s, -12 ) )
RETURN DIVIDE ( _a, _b )
'''
PROJ = r'''
VAR _c = [Data Corte]
VAR _g = [Fator Tendência 12M]
VAR _meses = FILTER ( VALUES ( dCalendario[InicioMes] ), dCalendario[InicioMes] > _c )
RETURN
    IF (
        NOT ISEMPTY ( _meses ),
        SUMX (
            _meses,
            VAR _m = dCalendario[InicioMes]
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] <= EOMONTH ( _m, -12 ) )
        ) * _g
    )
'''
BACKTEST = r'''
VAR _c = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        CALCULATETABLE ( VALUES ( dCalendario[InicioMes] ), REMOVEFILTERS ( dCalendario ), dCalendario[InicioMes] >= DATE ( YEAR ( _c ), 1, 1 ), dCalendario[InicioMes] <= _c ),
        "@r",
            VAR _m = dCalendario[InicioMes]
            RETURN CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= _m, dCalendario[Data] <= EOMONTH ( _m, 0 ) ),
        "@p",
            VAR _m = dCalendario[InicioMes]
            VAR _ly = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] <= EOMONTH ( _m, -12 ) )
            VAR _g = DIVIDE (
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -12 ), dCalendario[Data] < _m ),
                CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= EDATE ( _m, -24 ), dCalendario[Data] < EDATE ( _m, -12 ) )
            )
            RETURN _ly * _g
    )
VAR _e = FILTER ( ADDCOLUMNS ( _t, "@err", DIVIDE ( [@r], [@p] ) - 1 ), NOT ISBLANK ( [@r] ) && NOT ISBLANK ( [@p] ) )
RETURN @@AGG
'''
SIGMA = BACKTEST.replace('@@AGG', 'STDEVX.S ( _e, [@err] )')
MAPE = BACKTEST.replace('@@AGG', 'AVERAGEX ( _e, ABS ( [@err] ) )')
NBT = BACKTEST.replace('@@AGG', 'COUNTROWS ( _e )')
LOW = "VAR _p = [Projeção Sazonal Receita] RETURN IF ( NOT ISBLANK ( _p ), _p * ( 1 - 1.833 * [Projeção Erro σ (backtest)] ) )"
HIGH = "VAR _p = [Projeção Sazonal Receita] RETURN IF ( NOT ISBLANK ( _p ), _p * ( 1 + 1.833 * [Projeção Erro σ (backtest)] ) )"
BASE_LY = "CALCULATE ( [Receita Líquida], SAMEPERIODLASTYEAR ( dCalendario[Data] ) )"

RESUMO = r'''
VAR _c = [Data Corte]
VAR _nd = CALCULATETABLE ( VALUES ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] > _c, dCalendario[Data] <= DATE ( YEAR ( _c ), 12, 31 ) )
VAR _projND = CALCULATE ( [Projeção Sazonal Receita], REMOVEFILTERS ( dCalendario ), _nd )
VAR _metaND = CALCULATE ( [Meta Faturamento], REMOVEFILTERS ( dCalendario ), _nd )
VAR _h1 = CALCULATETABLE ( VALUES ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= DATE ( YEAR ( _c ) + 1, 1, 1 ), dCalendario[Data] <= DATE ( YEAR ( _c ) + 1, 6, 30 ) )
VAR _prev = CALCULATE ( [Receita Prevista], REMOVEFILTERS ( dCalendario ), _h1 )
VAR _projH1 = CALCULATE ( [Projeção Sazonal Receita], REMOVEFILTERS ( dCalendario ), _h1 )
VAR _baseH1 = CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Data] >= DATE ( YEAR ( _c ), 1, 1 ), dCalendario[Data] <= DATE ( YEAR ( _c ), 6, 30 ) )
VAR _g = [Fator Tendência 12M]
VAR _sig = [Projeção Erro σ (backtest)]
VAR _mape = [Projeção MAPE (backtest)]
VAR _n = [Projeção Meses no Backtest]
VAR _saz =
    ADDCOLUMNS (
        FILTER ( CALCULATETABLE ( VALUES ( dCalendario[Mes] ), REMOVEFILTERS ( dCalendario ) ), NOT ISBLANK ( dCalendario[Mes] ) ),
        "@nm", VAR _m1 = dCalendario[Mes] RETURN CALCULATE ( SELECTEDVALUE ( dCalendario[NomeMesPT] ), REMOVEFILTERS ( dCalendario ), dCalendario[Mes] = _m1 ),
        "@ix",
            VAR _mm = dCalendario[Mes]
            RETURN AVERAGEX (
                { YEAR ( _c ) - 2, YEAR ( _c ) - 1 },
                VAR _y = [Value]
                RETURN DIVIDE (
                    CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Ano] = _y, dCalendario[Mes] = _mm ),
                    CALCULATE ( [Receita Líquida], REMOVEFILTERS ( dCalendario ), dCalendario[Ano] = _y ) / 12
                )
            )
    )
VAR _pico = TOPN ( 1, _saz, [@ix], DESC )
VAR _vale = TOPN ( 1, _saz, [@ix], ASC )
VAR _t = "<div class='nx-k'><div class='nx-kl'>@L</div><div class='nx-kv'>@V</div><div class='nx-ks'>@S</div></div>"
VAR _css = "<style>.nx-p{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(5,1fr);gap:12px;height:100vh;box-sizing:border-box}.nx-k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:11px 16px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-kl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:22px;font-weight:600;color:#FFFFFF;margin-top:3px;line-height:1.1}.nx-ks{font-size:10px;color:#A9B9CA;margin-top:3px}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
VAR _gap = DIVIDE ( _projND - _metaND, _metaND )
RETURN
    _css & "<div class='nx-p'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Projeção nov–dez/" & YEAR ( _c ) ), "@V", "R$ " & FORMAT ( _projND / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
            "@S", "<span style='color:" & IF ( _gap >= 0, "#45D5A1", "#FF7285" ) & "'>" & FORMAT ( _gap, "+0.0%;-0.0%", "pt-BR" ) & " vs meta</span> (R$ " & FORMAT ( _metaND / 1e6, "#,0.0", "pt-BR" ) & " mi)" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Previsão da fonte 1º sem/" & ( YEAR ( _c ) + 1 ) ), "@V", "R$ " & FORMAT ( _prev / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
            "@S", FORMAT ( DIVIDE ( _prev, _baseH1 ) - 1, "+0.0%;-0.0%", "pt-BR" ) & " vs 1º sem/" & YEAR ( _c ) & " realizado" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Projeção sazonal 1º sem/" & ( YEAR ( _c ) + 1 ) ), "@V", "R$ " & FORMAT ( _projH1 / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
            "@S", "previsão da fonte " & FORMAT ( DIVIDE ( _prev, _projH1 ) - 1, "+0.0%;-0.0%", "pt-BR" ) & " vs projeção" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Tendência 12 meses" ), "@V", FORMAT ( _g - 1, "+0.0%;-0.0%", "pt-BR" ) ),
            "@S", "pico: " & MAXX ( _pico, [@nm] ) & " · vale: " & MAXX ( _vale, [@nm] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Erro do método (backtest)" ), "@V", FORMAT ( _mape, "0.0%", "pt-BR" ) & " <span style='font-size:12px;color:#A9B9CA;font-weight:400'>MAPE</span>" ),
            "@S", "σ " & FORMAT ( _sig, "0.0%", "pt-BR" ) & " · " & _n & " meses · faixa de 90%" )
        & "</div>"
'''

if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='Fator Tendência 12M', expr=G, folder='10 Previsão', fmt='0.000',
             desc='Receita dos 12 meses ate o corte / receita dos 12 meses anteriores.'),
        dict(name='Projeção Sazonal Receita', expr=PROJ, folder='10 Previsão', fmt=FMT,
             desc='Meses apos o corte: receita do mesmo mes no ano anterior x Fator Tendencia 12M. Nao e a previsao da fonte.'),
        dict(name='Projeção Erro σ (backtest)', expr=SIGMA, folder='10 Previsão', fmt='0.0%',
             desc='Desvio-padrao dos erros relativos do metodo aplicado aos meses do ano do corte (G calculado ate o mes anterior).'),
        dict(name='Projeção MAPE (backtest)', expr=MAPE, folder='10 Previsão', fmt='0.0%', desc='Erro percentual absoluto medio do backtest.'),
        dict(name='Projeção Meses no Backtest', expr=NBT, folder='10 Previsão', fmt='0', desc='Quantidade de meses usados no backtest.'),
        dict(name='Projeção Limite Inferior 90%', expr=LOW, folder='10 Previsão', fmt=FMT, desc='Projecao x (1 - 1,833 x sigma); t de Student com 9 gl.'),
        dict(name='Projeção Limite Superior 90%', expr=HIGH, folder='10 Previsão', fmt=FMT, desc='Projecao x (1 + 1,833 x sigma); t de Student com 9 gl.'),
        dict(name='Receita Base Ano Anterior', expr=BASE_LY, folder='10 Previsão', fmt=FMT,
             desc='Receita do mesmo periodo do ano anterior sem limitar ao corte (base para comparar periodos futuros, ex.: previsao 2027 vs 2026).'),
        dict(name='UX Preditiva Resumo', expr=RESUMO, folder='08 UX\\Preditiva',
             desc='Resumo: projecao nov-dez vs meta, previsao da fonte do 1o semestre seguinte vs realizado, projecao x previsao, tendencia, sazonalidade e erro do metodo.'),
    ])
    print('ok')
