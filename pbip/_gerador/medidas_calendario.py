# NEXUS 360 - Etapa I: Operations Calendar (medidas)
# Regras (doc 05 C09 / BRD RF11): semana de segunda a domingo; campanha e intervalo Inicio-Fim (nao evento diario);
# visitas por DataVisita; interacoes por DataInteracao; entregas por DataEntrega; meta e mensal.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

F = '12 Operações'
INT = '#,0'
PCT = '0.0%;-0.0%;0.0%'

CAMP_ATIVAS = r'''
VAR _i = MIN ( dCalendario[Data] )
VAR _f = MAX ( dCalendario[Data] )
RETURN COUNTROWS ( FILTER ( dCampanha, dCampanha[Inicio] <= _f && dCampanha[Fim] >= _i ) )
'''
CAMP_FLAG = r'''
VAR _i = CALCULATE ( MIN ( dCalendario[Data] ), ALLSELECTED ( dCampanha ) )
VAR _f = CALCULATE ( MAX ( dCalendario[Data] ), ALLSELECTED ( dCampanha ) )
RETURN IF ( HASONEVALUE ( dCampanha[CampanhaID] ) && SELECTEDVALUE ( dCampanha[Inicio] ) <= _f && SELECTEDVALUE ( dCampanha[Fim] ) >= _i, 1 )
'''

DIA = r'''
VAR _n = COUNTROWS ( VALUES ( dCalendario[Data] ) )
VAR _d = MAX ( dCalendario[Data] )
VAR _corte = [Data Corte]
VAR _fds = WEEKDAY ( _d, 2 ) >= 6
VAR _vis = [Visitas]
VAR _ped = [Visitas com Pedido]
VAR _ent = [Entregas]
VAR _otif = [OTIF %]
VAR _am = MAX ( dCalendario[AnoMes] )
VAR _meta = CALCULATE ( [Meta OTIF % (média simples)], REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] = _am )
VAR _camp = CALCULATE ( COUNTROWS ( FILTER ( dCampanha, dCampanha[Inicio] <= _d && dCampanha[Fim] >= _d ) ) )
VAR _nome = IF ( _camp = 1, CALCULATE ( MAXX ( FILTER ( dCampanha, dCampanha[Inicio] <= _d && dCampanha[Fim] >= _d ), dCampanha[Campanha] ) ) )
VAR _nomeC = IF ( LEN ( _nome ) > 22, LEFT ( _nome, 21 ) & "...", _nome )
VAR _futuro = _d > _corte
VAR _media = CALCULATE ( [OTIF %], REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] = _am, dCalendario[Data] <= _corte )
VAR _abaixo = NOT ISBLANK ( _otif ) && NOT ISBLANK ( _meta ) && _otif < _meta
VAR _pior = NOT ISBLANK ( _otif ) && _otif < _media - 0.05
VAR _stroke = IF ( _pior, "%23FF7285", "%23173B5C" )
VAR _bg = IF ( _fds, "%23081A2E", "%230C223D" )
VAR _txt = IF ( _fds, "%23A9B9CA", "%23FFFFFF" )
VAR _svgCamp =
    IF (
        _camp > 0,
        "<rect x='8' y='30' width='164' height='16' rx='3' fill='%2310D4C4' fill-opacity='0.22'/><text x='14' y='42' font-size='11' fill='%237FE6DD'>"
            & IF ( _camp = 1, SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _nomeC, "&", "e" ), "<", "" ), "'", "" ), "%", "%25" ), "#", "%23" ), _camp & " campanhas ativas" ) & "</text>"
    )
VAR _svgVis =
    IF ( NOT ISBLANK ( _vis ),
        "<circle cx='13' cy='64' r='3.5' fill='%235FA8E6'/><text x='22' y='68' font-size='12' fill='%23C9D6E3'>" & _vis & " visitas %C2%B7 " & ( _ped + 0 ) & " pedidos</text>" )
VAR _svgEnt =
    IF ( NOT ISBLANK ( _ent ),
        "<circle cx='13' cy='86' r='3.5' fill='" & IF ( _pior, "%23FF7285", IF ( _abaixo, "%23FFC66D", "%2345D5A1" ) ) & "'/><text x='22' y='90' font-size='12' fill='%23C9D6E3'>" & _ent & " entregas %C2%B7 OTIF "
            & FORMAT ( _otif * 100, "0" ) & "%25</text>" )
RETURN
    IF (
        _n = 1,
        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='100' viewBox='0 0 180 100' font-family='Segoe UI'>"
            & "<rect x='1' y='1' width='178' height='98' rx='7' fill='" & _bg & "' stroke='" & _stroke & "' stroke-width='" & IF ( _pior, "1.8", "1" ) & "'"
            & IF ( _futuro, " stroke-dasharray='3 3' fill-opacity='0.4'", "" ) & "/>"
            & "<text x='10' y='22' font-size='17' font-weight='600' fill='" & _txt & "'>" & DAY ( _d ) & "</text>"
            & IF ( _futuro, "<text x='170' y='20' font-size='10' text-anchor='end' fill='%236F86A0'>sem dados</text>", "" )
            & _svgCamp & _svgVis & _svgEnt & "</svg>"
    )
'''

KPIS = r'''
VAR _i = MIN ( dCalendario[Data] )
VAR _f = MIN ( MAX ( dCalendario[Data] ), [Data Corte] )
VAR _um = _i = MAX ( dCalendario[Data] )
VAR _rotulo = IF ( _um, FORMAT ( _i, "dd/mm/yyyy (dddd)", "pt-BR" ), FORMAT ( _i, "dd/mm" ) & " a " & FORMAT ( _f, "dd/mm/yyyy" ) )
VAR _vis = [Visitas]
VAR _conv = [Conversão de Visitas %]
VAR _int = [Interações de Campanha]
VAR _cvc = [Conversões de Campanha]
VAR _camp = [Campanhas Ativas (período)]
VAR _ent = [Entregas]
VAR _otif = [OTIF %]
VAR _am = MAX ( dCalendario[AnoMes] )
VAR _metaOtif = CALCULATE ( [Meta OTIF % (média simples)], REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] = _am )
VAR _rec = [Receita (até corte)]
VAR _meta = IF ( NOT _um && HASONEVALUE ( dCalendario[AnoMes] ), [Meta Faturamento (até corte)] )
VAR _ating = DIVIDE ( _rec, _meta )
VAR _card = "<div class='k' style='border-color:@C'><div class='l'>@L</div><div class='v'>@V</div><div class='s'>@S</div></div>"
VAR _css = "<style>.w{font-family:'Segoe UI',sans-serif;color:#FFFFFF;display:grid;grid-template-columns:1.25fr repeat(5,1fr);gap:12px;height:100vh;box-sizing:border-box;padding:4px 0}.k{background:rgba(10,28,51,.92);border:1px solid #173B5C;border-left:3px solid;border-radius:10px;padding:10px 14px;animation:a .5s ease-out both}.l{font-size:10px;letter-spacing:.08em;color:#A9B9CA;text-transform:uppercase}.v{font-size:22px;font-weight:600;margin-top:2px}.s{font-size:10.5px;color:#A9B9CA;margin-top:2px}.p{font-size:15px;font-weight:600;line-height:1.25}@keyframes a{from{opacity:0;transform:translateY(4px)}to{opacity:1}}@media (prefers-reduced-motion:reduce){.k{animation:none}}</style>"
RETURN
    IF (
        ISBLANK ( _vis ) && ISBLANK ( _ent ),
        _css & "<div class='w'><div class='k' style='border-color:#6F86A0;grid-column:1 / span 6'><div class='l'>Sem atividade registrada</div><div class='v' style='font-size:15px'>" & _rotulo & "</div><div class='s'>Datas após o corte (31/10/2026) não têm dados.</div></div></div>",
        _css & "<div class='w'>"
            & "<div class='k' style='border-color:#10D4C4'><div class='l'>" & IF ( _um, "Dia selecionado", "Período" ) & "</div><div class='p'>" & _rotulo & "</div><div class='s'>clique em um dia para detalhar; clique de novo para voltar ao mês</div></div>"
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", "#5FA8E6" ), "@L", "Visitas comerciais" ), "@V", FORMAT ( _vis, "#,0", "pt-BR" ) ), "@S", FORMAT ( _conv, "0.0%", "pt-BR" ) & " viraram pedido" )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", "#10D4C4" ), "@L", "Campanhas ativas" ), "@V", FORMAT ( _camp + 0, "0" ) ), "@S", FORMAT ( _int + 0, "#,0", "pt-BR" ) & " interações · " & FORMAT ( _cvc + 0, "#,0", "pt-BR" ) & " conversões" )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", IF ( _otif < _metaOtif, "#FF7285", "#45D5A1" ) ), "@L", "Entregas" ), "@V", FORMAT ( _ent, "#,0", "pt-BR" ) ), "@S", "OTIF " & FORMAT ( _otif, "0.0%", "pt-BR" ) & " · meta " & FORMAT ( _metaOtif, "0%", "pt-BR" ) )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", IF ( ISBLANK ( _meta ), "#6F86A0", IF ( _ating >= 1, "#45D5A1", "#FFC66D" ) ) ), "@L", "Receita líquida" ), "@V", "R$ " & FORMAT ( _rec / 1e6, "#,0.0", "pt-BR" ) & " mi" ),
                "@S", IF ( ISBLANK ( _meta ), "meta é mensal: selecione o mês inteiro", FORMAT ( _ating, "0.0%", "pt-BR" ) & " da meta do mês" ) )
            & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _card, "@C", "#A9B9CA" ), "@L", "Dias com atividade" ), "@V", FORMAT ( COUNTROWS ( FILTER ( VALUES ( dCalendario[Data] ), NOT ISBLANK ( [Visitas] ) || NOT ISBLANK ( [Entregas] ) ) ), "0" ) ),
                "@S", "de " & COUNTROWS ( VALUES ( dCalendario[Data] ) ) & " dias no período" )
            & "</div>"
    )
'''

TT = r'''
VAR _d = MAX ( dCalendario[Data] )
VAR _one = HASONEVALUE ( dCalendario[Data] )
VAR _r = "<tr><td>@L</td><td>@V</td></tr>"
VAR _vis = [Visitas]
RETURN
    IF (
        _one,
        "<style>.t{font-family:'Segoe UI',sans-serif;color:#FFFFFF;padding:10px 12px;height:100vh;box-sizing:border-box;background:#0A1C33;border:1px solid #173B5C;border-radius:8px}.h{font-size:12px;font-weight:600;margin-bottom:6px}.t table{width:100%;font-size:11px;border-collapse:collapse}.t td{padding:2px 0;color:#C9D6E3}.t td+td{text-align:right;color:#FFFFFF}</style><div class='t'><div class='h'>"
            & FORMAT ( _d, "dddd, dd/mm/yyyy", "pt-BR" ) & "</div><table>"
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Visitas" ), "@V", FORMAT ( _vis + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Pedidos nas visitas" ), "@V", FORMAT ( [Visitas com Pedido] + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Propostas / follow-up" ), "@V", FORMAT ( CALCULATE ( [Visitas], fVisitaComercial[Resultado] IN { "Proposta", "Follow-up" } ) + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Interações de campanha" ), "@V", FORMAT ( [Interações de Campanha] + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Entregas" ), "@V", FORMAT ( [Entregas] + 0, "0" ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "OTIF" ), "@V", IF ( ISBLANK ( [OTIF %] ), "—", FORMAT ( [OTIF %], "0.0%", "pt-BR" ) ) )
            & SUBSTITUTE ( SUBSTITUTE ( _r, "@L", "Receita faturada" ), "@V", "R$ " & FORMAT ( [Receita Líquida] / 1e3, "#,0", "pt-BR" ) & " mil" )
            & "</table></div>"
    )
'''

if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='Visitas', expr='COUNTROWS ( fVisitaComercial )', folder=F, fmt=INT, desc='Visitas comerciais registradas (fVisitaComercial), pela DataVisita.'),
        dict(name='Visitas com Pedido', expr='IF ( NOT ISBLANK ( [Visitas] ), CALCULATE ( [Visitas], KEEPFILTERS ( fVisitaComercial[Resultado] = "Pedido" ) ) + 0 )', folder=F, fmt=INT,
             desc='Visitas com Resultado = Pedido.'),
        dict(name='Conversão de Visitas %', expr='DIVIDE ( [Visitas com Pedido], [Visitas] )', folder=F, fmt=PCT, desc='Visitas com pedido / visitas.'),
        dict(name='Interações de Campanha', expr='COUNTROWS ( fInteracaoCampanha )', folder=F, fmt=INT, desc='Interacoes de clientes com campanhas, pela DataInteracao.'),
        dict(name='Conversões de Campanha', expr='CALCULATE ( [Interações de Campanha], KEEPFILTERS ( fInteracaoCampanha[TipoInteracao] = "Conversão" ) )',
             folder=F, fmt=INT, desc='Interacoes do tipo Conversao.'),
        dict(name='Campanhas Ativas (período)', expr=CAMP_ATIVAS, folder=F, fmt=INT,
             desc='Campanhas cujo intervalo Inicio-Fim cruza o periodo do contexto (campanha e intervalo, nao evento diario).'),
        dict(name='Campanha no Período', expr=CAMP_FLAG, folder=F, fmt='0', hidden=True,
             desc='1 quando a campanha da linha cruza o periodo selecionado (usado pelo cronograma).'),
        dict(name='Período Início', expr='CALCULATE ( MIN ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario[Data], dCalendario[SemanaDoMes], dCalendario[DiaSemanaAbrev], dCalendario[DiaSemana] ), ALLSELECTED ( dCampanha ) )', folder=F, fmt='dd/mm/yyyy', hidden=True,
             desc='Primeiro dia do mes do calendario (ignora o dia clicado na matriz).'),
        dict(name='Período Fim', expr='CALCULATE ( MAX ( dCalendario[Data] ), REMOVEFILTERS ( dCalendario[Data], dCalendario[SemanaDoMes], dCalendario[DiaSemanaAbrev], dCalendario[DiaSemana] ), ALLSELECTED ( dCampanha ) )', folder=F, fmt='dd/mm/yyyy', hidden=True,
             desc='Ultimo dia do mes do calendario (ignora o dia clicado na matriz).'),
        dict(name='Dia Selecionado', expr='IF ( COUNTROWS ( VALUES ( dCalendario[Data] ) ) = 1, MAX ( dCalendario[Data] ) )', folder=F, fmt='dd/mm/yyyy', hidden=True,
             desc='Data quando um unico dia esta no contexto (marcador do cronograma).'),
        dict(name='UX Calendário Dia', expr=DIA, folder='08 UX\\Calendário', cat='ImageUrl',
             desc='Celula SVG do calendario: dia, campanha ativa, visitas/pedidos e entregas/OTIF. Ponto: verde >= meta, ambar < meta, vermelho = OTIF 5 p.p. abaixo da media do mes (tambem borda). Tracejado apos o corte.'),
        dict(name='UX Calendário KPIs', expr=KPIS, folder='08 UX\\Calendário',
             desc='Faixa de indicadores do periodo ou do dia selecionado.'),
        dict(name='UX Tooltip Dia', expr=TT, folder='08 UX\\Calendário', desc='Tooltip do dia no calendario.'),
    ])
    print('ok')
