# NEXUS 360 - Etapa E: medidas do Warehouse Digital Twin (2D no Power BI)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

PARADOS = r'''
VAR _d = [Data Último Snapshot Estoque]
RETURN CALCULATE ( COUNTROWS ( fEstoqueMensal ), KEEPFILTERS ( fEstoqueMensal[DataReferencia] = _d ), KEEPFILTERS ( fEstoqueMensal[DiasSemMovimento] >= 90 ) )
'''
POSCAD = "CALCULATE ( COUNTROWS ( dPosicaoArmazem ), TREATAS ( VALUES ( dFilial[FilialID] ), dPosicaoArmazem[FilialID] ) )"

KPIS = r'''
VAR _t = "<div class='nx-k'><div class='nx-kl'>@L</div><div class='nx-kv'>@V</div><div class='nx-ks'>@S</div></div>"
VAR _d = [Data Último Snapshot WMS]
VAR _css = "<style>.nx-w{font-family:'Segoe UI',sans-serif;display:grid;grid-template-columns:repeat(8,1fr);gap:10px;height:100vh;box-sizing:border-box}.nx-k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-radius:12px;padding:11px 14px;box-sizing:border-box;animation:nxUp .6s ease-out both}.nx-kl{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:22px;font-weight:600;color:#FFFFFF;margin-top:3px;line-height:1.1}.nx-ks{font-size:10px;color:#A9B9CA;margin-top:3px}@keyframes nxUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
RETURN
    _css & "<div class='nx-w'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Posições cadastradas" ), "@V", FORMAT ( [Posições Cadastradas], "#,0", "pt-BR" ) ), "@S", "corredor × coluna × nível" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Posições lidas" ), "@V", FORMAT ( [Posições Amostradas], "#,0", "pt-BR" ) ), "@S", "snapshot de " & FORMAT ( _d, "dd/mm/yyyy" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Ocupadas (amostra)" ), "@V", "<span style='color:#10D4C4'>" & FORMAT ( [Registros Ocupada %], "0%", "pt-BR" ) & "</span>" ), "@S", FORMAT ( [Paletes (amostra)], "#,0", "pt-BR" ) & " paletes lidos" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Bloqueadas (amostra)" ), "@V", "<span style='color:#FF7285'>" & FORMAT ( [Registros Bloqueada %], "0%", "pt-BR" ) & "</span>" ), "@S", "posições indisponíveis" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Estoque (amostra)" ), "@V", "R$ " & FORMAT ( [Valor Estoque Amostra] / 1e6, "#,0.0", "pt-BR" ) & " mi" ), "@S", FORMAT ( [SKU-Filial Amostrados], "#,0", "pt-BR" ) & " SKU-filial" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Ruptura" ), "@V", FORMAT ( COALESCE ( [Ruptura % (amostra)], 0 ), "0.0%", "pt-BR" ) ), "@S", FORMAT ( COALESCE ( [SKUs em Ruptura (amostra)], 0 ), "#,0", "pt-BR" ) & " SKU-filial sem saldo" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Abaixo do mínimo" ), "@V", FORMAT ( [Abaixo do Mínimo % (amostra)], "0.0%", "pt-BR" ) ), "@S", FORMAT ( [SKUs Abaixo do Mínimo (amostra)], "#,0", "pt-BR" ) & " SKU-filial" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _t, "@L", "Parados 90+ dias" ), "@V", FORMAT ( [Produtos Parados 90+ (amostra)], "#,0", "pt-BR" ) ), "@S", "sem movimento (baixo giro)" )
        & "</div>"
'''

GRADE = r'''
VAR _nf = COUNTROWS ( VALUES ( dFilial[FilialID] ) )
VAR _d = [Data Último Snapshot WMS]
VAR _pos =
    ADDCOLUMNS (
        CALCULATETABLE (
            SUMMARIZE ( dPosicaoArmazem, dPosicaoArmazem[PosicaoID], dPosicaoArmazem[EixoX], dPosicaoArmazem[EixoY], dPosicaoArmazem[EixoZ], dPosicaoArmazem[Zona] ),
            TREATAS ( VALUES ( dFilial[FilialID] ), dPosicaoArmazem[FilialID] )
        ),
        "@st", CALCULATE ( MAX ( fOcupacaoArmazem[StatusPosicao] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) ),
        "@pl", CALCULATE ( SUM ( fOcupacaoArmazem[Paletes] ), KEEPFILTERS ( fOcupacaoArmazem[DataReferencia] = _d ) )
    )
VAR _niv =
    CONCATENATEX (
        { 1, 2, 3, 4 },
        VAR _z = [Value]
        RETURN
            "<div class='nx-n'><div class='nx-nt'>Nível " & _z & IF ( _z = 1, " (térreo)", "" ) & "</div><div class='nx-gr'>"
                & CONCATENATEX (
                    FILTER ( _pos, dPosicaoArmazem[EixoZ] = _z ),
                    VAR _cls = SWITCH ( [@st], "Ocupada", "o", "Bloqueada", "b", "Disponível", "d", "s" )
                    VAR _zc = SWITCH ( dPosicaoArmazem[Zona], "Expedição", "ze", "Picking", "zp", "zu" )
                    RETURN "<i class='" & _cls & " " & _zc & "'>" & IF ( [@pl] > 0, [@pl], "" ) & "</i>",
                    "", dPosicaoArmazem[EixoY], DESC, dPosicaoArmazem[EixoX], ASC
                )
                & "</div></div>",
        "", [Value], ASC
    )
VAR _css = "<style>.nx-a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:12px 18px;display:flex;flex-direction:column}.nx-at{font-size:13px;font-weight:600;text-align:center}.nx-as{font-size:10.5px;color:#A9B9CA;text-align:center;margin:2px 0 10px}.nx-ns{display:flex;gap:22px;justify-content:center;flex:1}.nx-n{display:flex;flex-direction:column;align-items:center}.nx-nt{font-size:11px;color:#C9D6E3;margin-bottom:6px}.nx-gr{display:grid;grid-template-columns:repeat(10,24px);grid-auto-rows:24px;gap:3px}.nx-gr i{font-style:normal;font-size:9px;font-weight:600;display:flex;align-items:center;justify-content:center;border-radius:4px;background:#12304F;color:#071528;border-bottom:3px solid transparent;animation:nxIn .5s ease-out both}.nx-gr i.o{background:#10D4C4}.nx-gr i.b{background:#FF7285}.nx-gr i.d{background:#5FA8E6}.nx-gr i.s{background:#12304F;opacity:.75}.nx-gr i.ze{border-bottom-color:#FFC66D}.nx-gr i.zp{border-bottom-color:#7FE6DD}.nx-gr i.zu{border-bottom-color:#6F86A0}.nx-ax{font-size:9.5px;color:#6F86A0;margin-top:4px}.nx-lg{display:flex;gap:16px;justify-content:center;font-size:10.5px;color:#A9B9CA;margin-top:10px;flex-wrap:wrap}.nx-lg span{display:flex;align-items:center;gap:5px}.nx-lg b{display:inline-block;width:12px;height:12px;border-radius:3px}.nx-lg u{display:inline-block;width:14px;height:3px;text-decoration:none}@keyframes nxIn{from{opacity:0}to{opacity:1}}@media (prefers-reduced-motion:reduce){.nx-gr i{animation:none}}</style>"
VAR _leg = "<div class='nx-lg'><span><b style='background:#10D4C4'></b>Ocupada</span><span><b style='background:#FF7285'></b>Bloqueada</span><span><b style='background:#5FA8E6'></b>Disponível</span><span><b style='background:#12304F;border:1px solid #3E5C7A'></b>Sem leitura no snapshot</span><span><u style='background:#FFC66D'></u>Expedição</span><span><u style='background:#7FE6DD'></u>Picking</span><span><u style='background:#6F86A0'></u>Pulmão</span><span>número = paletes lidos</span></div>"
RETURN
    IF (
        _nf <> 1,
        _css & "<div class='nx-a'><div class='nx-at'>Mapa de posições</div><div class='nx-as'>Selecione uma única filial para ver o armazém.</div></div>",
        _css & "<div class='nx-a'><div class='nx-at'>Mapa de posições · " & SELECTEDVALUE ( dFilial[Cidade] ) & "</div><div class='nx-as'>vista de cima por nível · linhas = coluna (Y 10→1) · colunas = corredor (X 1→10) · snapshot de " & FORMAT ( _d, "dd/mm/yyyy" ) & " · " & COUNTROWS ( FILTER ( _pos, NOT ISBLANK ( [@st] ) ) ) & " de " & COUNTROWS ( _pos ) & " posições com leitura</div>"
            & "<div class='nx-ns'>" & _niv & "</div>" & _leg & "</div>"
    )
'''

TT_EST = r'''
VAR _mes = SELECTEDVALUE ( dCalendario[MesAno] )
VAR _css = "<style>.nx-t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:12px 16px;box-sizing:border-box;background:#0A1C33;height:100vh;border:1px solid #173B5C;border-radius:10px}.nx-tn{font-size:14px;font-weight:600;margin-bottom:6px}.nx-tg{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}.nx-tk{font-size:10px;color:#A9B9CA}.nx-tv{font-size:14px;font-weight:600}</style>"
RETURN
    IF (
        NOT ISBLANK ( _mes ),
        _css & "<div class='nx-t'><div class='nx-tn'>" & _mes & " · estoque (amostra)</div><div class='nx-tg'>"
            & "<div><div class='nx-tk'>Entradas</div><div class='nx-tv' style='color:#10D4C4'>" & FORMAT ( [Entradas Estoque (un)], "#,0", "pt-BR" ) & " un</div></div>"
            & "<div><div class='nx-tk'>Saídas</div><div class='nx-tv'>" & FORMAT ( [Saídas Estoque (un)], "#,0", "pt-BR" ) & " un</div></div>"
            & "<div><div class='nx-tk'>Saldo no fim do mês</div><div class='nx-tv'>" & FORMAT ( [Saldo Estoque Amostra (un)], "#,0", "pt-BR" ) & " un</div></div>"
            & "<div><div class='nx-tk'>Valor em estoque</div><div class='nx-tv'>R$ " & FORMAT ( [Valor Estoque Amostra] / 1e6, "#,0.0", "pt-BR" ) & " mi</div></div>"
            & "<div><div class='nx-tk'>Ruptura</div><div class='nx-tv' style='color:#FF7285'>" & FORMAT ( [Ruptura % (amostra)], "0.0%", "pt-BR" ) & "</div></div>"
            & "<div><div class='nx-tk'>Parados 90+ dias</div><div class='nx-tv' style='color:#FFC66D'>" & FORMAT ( [Produtos Parados 90+ (amostra)], "#,0", "pt-BR" ) & "</div></div>"
            & "</div></div>"
    )
'''

if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='Produtos Parados 90+ (amostra)', expr=PARADOS, folder='04 Estoque e WMS\\Estoque', fmt='#,0',
             desc='SKU-filial do ultimo snapshot de estoque do contexto com 90 ou mais dias sem movimento (DiasSemMovimento da fonte).'),
        dict(name='Posições Cadastradas', expr=POSCAD, folder='04 Estoque e WMS\\WMS', fmt='#,0',
             desc='Posicoes de dPosicaoArmazem das filiais no contexto (dPosicaoArmazem nao se relaciona com dFilial; filtro por TREATAS).'),
        dict(name='UX Armazém KPIs', expr=KPIS, folder='08 UX\\Armazém', desc='Faixa de KPIs de armazem e estoque (amostras C9).'),
        dict(name='UX Armazém Grade', expr=GRADE, folder='08 UX\\Armazém',
             desc='Gemeo digital 2D: grade 10x10 por nivel com o status de cada posicao no ultimo snapshot do contexto; posicoes sem leitura aparecem vazias.'),
        dict(name='UX Tooltip Estoque Mês', expr=TT_EST, folder='08 UX\\Componentes', desc='Tooltip mensal de estoque: entradas, saidas, saldo, valor, ruptura e parados.'),
    ])
    print('ok')
