# NEXUS 360 - Etapa J: AI Decision Assistant (interface demonstrativa; sem LLM conectado)
# As medidas mostram APENAS resultados de consultas governadas (DAX ao vivo). Nenhum texto e gerado por IA.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert

FD = '08 UX\\Assistente'
CSS = ("<style>.a{font-family:'Segoe UI',sans-serif;color:#FFFFFF;height:100vh;box-sizing:border-box;padding:14px 18px;overflow:hidden}"
       ".h{font-size:13px;font-weight:600;text-align:center;margin-bottom:8px}.sub{font-size:10.5px;color:#A9B9CA;text-align:center;margin-bottom:10px}"
       ".mono{font-family:Consolas,monospace;font-size:11px;color:#7FE6DD}.lb{font-size:9.5px;letter-spacing:.1em;color:#A9B9CA;text-transform:uppercase;margin:10px 0 4px}"
       ".q{background:#12304F;border-radius:10px 10px 10px 2px;padding:9px 12px;font-size:13px;display:inline-block}"
       ".st{border-left:2px solid #173B5C;margin-left:6px;padding:4px 0 4px 12px}"
       ".tb{width:100%;border-collapse:collapse;font-size:11.5px}.tb td{padding:5px 6px;border-bottom:1px solid #12304F;color:#C9D6E3}.tb td.n{text-align:right;color:#FFFFFF}"
       ".pd{border:1px dashed #FFC66D;border-radius:8px;padding:8px 12px;font-size:11px;color:#FFC66D;margin-top:10px}"
       ".in{border:1px solid #173B5C;border-radius:8px;padding:8px 12px;font-size:11.5px;color:#6F86A0;margin-top:10px}"
       ".ok{color:#45D5A1}.ch{display:inline-block;border:1px solid #173B5C;border-radius:12px;padding:3px 10px;margin:0 6px 6px 0;font-size:10.5px;color:#C9D6E3}</style>")

STATUS = r'''
VAR _chip = "<span class='ch' style='border-color:@C'><b style='color:@C'>@S</b> · @T</span>"
RETURN
    "@CSS<div class='a' style='padding:10px 18px;display:flex;align-items:center;gap:18px'>"
        & "<div style='min-width:310px'><div style='font-size:15px;font-weight:600'>Interface demonstrativa</div><div style='font-size:10.5px;color:#FFC66D'>Nenhum modelo de linguagem está conectado. Os números vêm de consultas DAX governadas, não de IA.</div></div><div>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#45D5A1" ), "@S", "Implementado" ), "@T", "catálogo de 8 ferramentas tipadas (JSON Schema)" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#45D5A1" ), "@S", "Testado" ), "@T", "8 consultas DAX executadas no modelo em 02/11/2026" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#FFC66D" ), "@S", "Pendente" ), "@T", "orquestrador LLM e linguagem natural" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _chip, "@C", "#FFC66D" ), "@S", "Pendente" ), "@T", "autenticação Entra ID, RLS e endpoint executeQueries" )
        & "</div></div>"
'''.replace('@CSS', CSS.replace('"', '""'))

FLUXO = r'''
VAR _rank = TOPN ( 3, FILTER ( ADDCOLUMNS ( VALUES ( dFilial[Cidade] ), "@a", [Atingimento Meta Faturamento %], "@g", [Gap Meta Faturamento] ), NOT ISBLANK ( [@a] ) ), [@a], ASC )
VAR _linhas = CONCATENATEX ( _rank, "<tr><td>" & dFilial[Cidade] & "</td><td class='n'>" & FORMAT ( [@a], "0.0%", "pt-BR" ) & "</td><td class='n'>R$ " & FORMAT ( [@g] / 1e3, "#,0", "pt-BR" ) & " mil</td></tr>", "", [@a], ASC )
VAR _ini = MIN ( dCalendario[Data] )
VAR _fim = MIN ( MAX ( dCalendario[Data] ), [Data Corte] )
RETURN
    "@CSS<div class='a'><div class='h'>Fluxo de uma pergunta (demonstração com dados reais, sem IA)</div>"
        & "<div class='lb'>1 · Pergunta do usuário (exemplo fixo)</div><div class='q'>Onde a meta de faturamento está mais em risco neste período?</div>"
        & "<div class='lb'>2 · Plano de ferramentas que o orquestrador chamaria</div><div class='st'><div class='mono'>resumo_executivo(periodo={" & FORMAT ( _ini, "yyyy-mm-dd" ) & ".." & FORMAT ( _fim, "yyyy-mm-dd" ) & "}, filiais=contexto)</div>"
        & "<div class='mono'>ranking_filiais(metrica=""Atingimento Meta Faturamento %"", ordem=""asc"", top_n=3)</div></div>"
        & "<div class='lb'>3 · Resultado das ferramentas (DAX ao vivo, filtros da página)</div>"
        & "<table class='tb'><tr><td>Receita líquida</td><td class='n'>R$ " & FORMAT ( [Receita (até corte)] / 1e6, "#,0.0", "pt-BR" ) & " mi</td><td class='n'>meta R$ " & FORMAT ( [Meta Faturamento (até corte)] / 1e6, "#,0.0", "pt-BR" ) & " mi</td></tr>"
        & "<tr><td>Atingimento da meta</td><td class='n'>" & FORMAT ( [Atingimento Meta Faturamento %], "0.0%", "pt-BR" ) & "</td><td class='n'>margem bruta " & FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" ) & "</td></tr></table>"
        & "<div class='lb' style='margin-top:8px'>Filiais com menor atingimento (atingimento · gap)</div><table class='tb'>" & _linhas & "</table>"
        & "<div class='pd'>4 · Resposta em linguagem natural: <b>pendente</b>. Quando integrado, o LLM redigirá a resposta somente a partir das linhas acima e citará a ferramenta de origem de cada número.</div>"
        & "<div class='in'>Digite uma pergunta…  <span style='float:right'>entrada desativada: integração pendente</span></div></div>"
'''.replace('@CSS', CSS.replace('"', '""'))

FERR = r'''
VAR _r = "<tr><td class='mono'>@N</td><td>@D</td><td class='n'>@V</td></tr>"
VAR _fw = TOPN ( 1, FILTER ( VALUES ( dFilial[Cidade] ), NOT ISBLANK ( [Atingimento Meta Faturamento %] ) ), [Atingimento Meta Faturamento %], ASC )
VAR _vd = TOPN ( 1, VALUES ( dVendedor[Vendedor] ), [Receita Líquida], DESC )
VAR _tr = TOPN ( 1, FILTER ( VALUES ( dTransportadora[Transportadora] ), [Entregas] >= 50 ), [OTIF %], ASC )
VAR _proj = CALCULATE ( SUMX ( VALUES ( dCalendario[AnoMes] ), [Projeção Sazonal Receita] ), REMOVEFILTERS ( dCalendario ), dCalendario[AnoMes] IN { 202611, 202612 } )
VAR _sim = CALCULATE ( [Sim Valor Etapa], 'Sim Etapa'[Ordem] = 1 )
RETURN
    "@CSS<div class='a'><div class='h'>Ferramentas tipadas e o que retornam agora</div><div class='sub'>Somente leitura · parâmetros validados por JSON Schema · consultas em apps/ai_assistant/CONSULTAS_DAX.dax</div><table class='tb'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "resumo_executivo" ), "@D", "receita, margem, meta, churn, OTIF" ), "@V", "R$ " & FORMAT ( [Receita (até corte)] / 1e6, "#,0.0", "pt-BR" ) & " mi · " & FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "ranking_filiais" ), "@D", "ranking por métrica permitida" ), "@V", "menor atingimento: " & MAXX ( _fw, dFilial[Cidade] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "clientes_em_risco" ), "@D", "180–364 dias sem compra, por receita 12M" ), "@V", FORMAT ( [Clientes em Risco], "#,0", "pt-BR" ) & " clientes" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "desempenho_vendedores" ), "@D", "receita, margem e desconto" ), "@V", "maior receita: " & MAXX ( _vd, dVendedor[Vendedor] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "otif_transportadoras" ), "@D", "OTIF, atraso e frete (mín. 50 entregas)" ), "@V", "menor OTIF: " & MAXX ( _tr, dTransportadora[Transportadora] ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "dre_gerencial" ), "@D", "DRE por linha vs ano anterior" ), "@V", "resultado R$ " & FORMAT ( [Resultado Gerencial Simplificado] / 1e6, "#,0.0", "pt-BR" ) & " mi" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "projecao_receita" ), "@D", "projeção sazonal com faixa de 90%" ), "@V", "nov–dez/26 R$ " & FORMAT ( _proj / 1e6, "#,0.0", "pt-BR" ) & " mi" )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _r, "@N", "simular_cenario" ), "@D", "resultado sob premissas (não é previsão)" ), "@V", "base R$ " & FORMAT ( _sim / 1e6, "#,0.0", "pt-BR" ) & " mi" )
        & "</table></div>"
'''.replace('@CSS', CSS.replace('"', '""'))

ARQ = r'''
"@CSS<div class='a'><div class='h'>Arquitetura proposta e controles de segurança</div>"
    & "<svg viewBox='0 0 880 120' width='100%' height='118' font-family='Segoe UI' font-size='11'>"
    & "<defs><marker id='m' viewBox='0 0 8 8' refX='7' refY='4' markerWidth='7' markerHeight='7' orient='auto'><path d='M0,0 L8,4 L0,8 z' fill='#5FA8E6'/></marker></defs>"
    & "<g fill='#0C223D' stroke='#173B5C'><rect x='2' y='30' width='130' height='56' rx='8'/><rect x='178' y='30' width='160' height='56' rx='8' stroke='#FFC66D' stroke-dasharray='4 3'/><rect x='384' y='30' width='150' height='56' rx='8'/><rect x='580' y='30' width='140' height='56' rx='8' stroke='#FFC66D' stroke-dasharray='4 3'/><rect x='766' y='30' width='110' height='56' rx='8'/></g>"
    & "<g fill='#FFFFFF' text-anchor='middle' font-weight='600'><text x='67' y='54'>Usuário</text><text x='258' y='54'>Orquestrador LLM</text><text x='459' y='54'>Ferramentas tipadas</text><text x='650' y='54'>API executeQueries</text><text x='821' y='54'>Modelo NEXUS360</text></g>"
    & "<g fill='#A9B9CA' text-anchor='middle' font-size='9.5'><text x='67' y='72'>pergunta</text><text x='258' y='72'>pendente</text><text x='459' y='72'>8 · validadas</text><text x='650' y='72'>pendente</text><text x='821' y='72'>RLS · leitura</text></g>"
    & "<g stroke='#5FA8E6' stroke-width='1.5' marker-end='url(#m)'><line x1='134' y1='58' x2='174' y2='58'/><line x1='340' y1='58' x2='380' y2='58'/><line x1='536' y1='58' x2='576' y2='58'/><line x1='722' y1='58' x2='762' y2='58'/></g>"
    & "<text x='440' y='110' fill='#6F86A0' font-size='9.5' text-anchor='middle'>tracejado = componente não implementado</text></svg>"
    & "<table class='tb' style='margin-top:6px'>"
    & "<tr><td>Sem DAX livre: o LLM escolhe ferramenta e parâmetros; o servidor valida o schema e monta a consulta a partir de modelo fixo.</td></tr>"
    & "<tr><td>Allowlist de medidas e colunas; limites de top_n (≤ 20), de período (até o corte) e de tempo de consulta.</td></tr>"
    & "<tr><td>Identidade do usuário propagada (Entra ID) para aplicar RLS; credencial só de leitura; trilha de auditoria por chamada.</td></tr>"
    & "<tr><td>Resposta obrigatoriamente citada: cada número traz a ferramenta e os filtros de origem; sem dado, sem resposta.</td></tr>"
    & "</table></div>"
'''.replace('@CSS', CSS.replace('"', '""'))

if __name__ == '__main__':
    upsert(sys.argv[1], [
        dict(name='UX Assistente Status', expr=STATUS, folder=FD, desc='Faixa de status da integracao (implementado/testado/pendente).'),
        dict(name='UX Assistente Fluxo', expr=FLUXO, folder=FD, desc='Demonstracao do fluxo pergunta -> ferramentas -> resultados DAX; sem resposta gerada por IA.'),
        dict(name='UX Assistente Ferramentas', expr=FERR, folder=FD, desc='Catalogo de ferramentas tipadas com o resultado atual de cada uma.'),
        dict(name='UX Assistente Arquitetura', expr=ARQ, folder=FD, desc='Diagrama da arquitetura proposta e controles de seguranca.'),
    ])
    print('ok')
