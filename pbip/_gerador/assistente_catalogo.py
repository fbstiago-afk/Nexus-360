# NEXUS 360 - Etapa J: catalogo de ferramentas tipadas do AI Decision Assistant
# Cada ferramenta = schema JSON (entrada validada) + consulta DAX parametrizada somente leitura.
# Gera: apps/ai_assistant/CATALOGO_FERRAMENTAS.json e CONSULTAS_DAX.dax; exemplos usados na validacao.
import json, os, sys

PERIODO = {"type": "object", "description": "Intervalo de datas (inclusive), limitado a 01/01/2024..31/10/2026 (corte).",
           "properties": {"inicio": {"type": "string", "format": "date"}, "fim": {"type": "string", "format": "date"}},
           "required": ["inicio", "fim"], "additionalProperties": False}
FILIAL = {"type": "array", "items": {"type": "string", "enum": ["Belo Horizonte", "Brasília", "Campinas", "Curitiba", "Goiânia", "Joinville", "Maringá",
                                                              "Porto Alegre", "Ribeirão Preto", "Rio de Janeiro", "Sorocaba", "São Paulo"]},
          "description": "Filiais (dFilial[Cidade]). Vazio = todas."}
TOPN = {"type": "integer", "minimum": 1, "maximum": 20, "default": 5}

# filtro comum: periodo + filiais
FILT = '''VAR _ini = DATEVALUE ( "{inicio}" )
VAR _fim = DATEVALUE ( "{fim}" )
VAR _per = DATESBETWEEN ( dCalendario[Data], _ini, _fim )
VAR _fil = {fil_expr}'''

TOOLS = [
    dict(name='resumo_executivo', desc='Receita, margem, atingimento da meta, resultado gerencial e churn do periodo.',
         params={"periodo": PERIODO, "filiais": FILIAL}, required=["periodo"],
         dax=FILT + '''
EVALUATE
CALCULATETABLE (
    ROW (
        "Receita", [Receita Líquida], "Margem Bruta %", [Margem Bruta %], "Meta", [Meta Faturamento],
        "Atingimento %", [Atingimento Meta Faturamento %], "Resultado Gerencial", [Resultado Gerencial Simplificado],
        "Taxa de Churn %", [Taxa de Churn %], "OTIF %", [OTIF %]
    ),
    _per, _fil
)''', exemplo=dict(inicio='2026-01-01', fim='2026-10-31', filiais=[])),
    dict(name='ranking_filiais', desc='Ranking de filiais por uma metrica permitida (allowlist).',
         params={"periodo": PERIODO, "metrica": {"type": "string", "enum": ["Receita Líquida", "Margem Bruta %", "Atingimento Meta Faturamento %", "OTIF %", "Taxa de Churn %"]},
                 "ordem": {"type": "string", "enum": ["asc", "desc"], "default": "desc"}, "top_n": TOPN},
         required=["periodo", "metrica"],
         dax='''VAR _ini = DATEVALUE ( "{inicio}" )
VAR _fim = DATEVALUE ( "{fim}" )
EVALUATE
TOPN (
    {top_n},
    CALCULATETABLE ( ADDCOLUMNS ( VALUES ( dFilial[Cidade] ), "Valor", [{metrica}] ), DATESBETWEEN ( dCalendario[Data], _ini, _fim ) ),
    [Valor], {ordem_dax}
)
ORDER BY [Valor] {ordem_dax}''', exemplo=dict(inicio='2026-01-01', fim='2026-10-31', metrica='Atingimento Meta Faturamento %', ordem='asc', top_n=3)),
    dict(name='clientes_em_risco', desc='Clientes em risco (180 a 364 dias sem compra) ordenados pela receita dos ultimos 12 meses.',
         params={"data_referencia": {"type": "string", "format": "date"}, "filiais": FILIAL, "top_n": TOPN}, required=["data_referencia"],
         dax='''VAR _ref = DATEVALUE ( "{data_referencia}" )
VAR _fil = {fil_expr}
VAR _t =
    CALCULATETABLE (
        FILTER (
            ADDCOLUMNS ( VALUES ( dCliente[ClienteID] ), "Dias sem compra", [Dias sem Compra (Data Ref.)], "Receita 12M", [Receita 12M (Data Ref.)] ),
            [Dias sem compra] >= 180 && [Dias sem compra] < 365
        ),
        dCalendario[Data] <= _ref, _fil
    )
EVALUATE TOPN ( {top_n}, _t, [Receita 12M], DESC )
ORDER BY [Receita 12M] DESC''', exemplo=dict(data_referencia='2026-10-31', filiais=[], top_n=5)),
    dict(name='desempenho_vendedores', desc='Receita, margem e desconto por vendedor.',
         params={"periodo": PERIODO, "filiais": FILIAL, "top_n": TOPN}, required=["periodo"],
         dax=FILT + '''
EVALUATE
TOPN (
    {top_n},
    CALCULATETABLE (
        ADDCOLUMNS ( VALUES ( dVendedor[Vendedor] ), "Receita", [Receita Líquida], "Margem %", [Margem Bruta %], "Desconto %", [Desconto Médio Ponderado %] ),
        _per, _fil
    ),
    [Receita], DESC
)
ORDER BY [Receita] DESC''', exemplo=dict(inicio='2026-01-01', fim='2026-10-31', filiais=['Campinas'], top_n=5)),
    dict(name='otif_transportadoras', desc='OTIF, atraso medio e frete por transportadora (minimo de entregas para entrar no ranking).',
         params={"periodo": PERIODO, "min_entregas": {"type": "integer", "minimum": 1, "default": 50}, "top_n": TOPN}, required=["periodo"],
         dax='''VAR _ini = DATEVALUE ( "{inicio}" )
VAR _fim = DATEVALUE ( "{fim}" )
EVALUATE
TOPN (
    {top_n},
    FILTER (
        CALCULATETABLE (
            ADDCOLUMNS ( VALUES ( dTransportadora[Transportadora] ), "Entregas", [Entregas], "OTIF %", [OTIF %], "Atraso médio", [Atraso Médio (dias)], "Frete/entrega", [Frete por Entrega] ),
            DATESBETWEEN ( dCalendario[Data], _ini, _fim )
        ),
        [Entregas] >= {min_entregas}
    ),
    [OTIF %], ASC
)
ORDER BY [OTIF %] ASC''', exemplo=dict(inicio='2026-01-01', fim='2026-10-31', min_entregas=50, top_n=5)),
    dict(name='dre_gerencial', desc='DRE gerencial por linha, com ano anterior.',
         params={"periodo": PERIODO, "filiais": FILIAL}, required=["periodo"],
         dax=FILT + '''
EVALUATE
CALCULATETABLE (
    ADDCOLUMNS ( VALUES ( dLinhaDRE[Linha] ), "Valor", [Valor DRE Gerencial], "Ano anterior", [Valor DRE Gerencial LY] ),
    _per, _fil
)''', exemplo=dict(inicio='2026-01-01', fim='2026-10-31', filiais=[])),
    dict(name='projecao_receita', desc='Projecao sazonal mensal apos o corte, com faixa de 90% (metodo documentado na pagina Predictive).',
         params={"filiais": FILIAL}, required=[],
         dax='''VAR _fil = {fil_expr}
EVALUATE
CALCULATETABLE (
    FILTER (
        ADDCOLUMNS ( VALUES ( dCalendario[AnoMes] ), "Projeção", [Projeção Sazonal Receita], "Inferior 90%", [Projeção Limite Inferior 90%], "Superior 90%", [Projeção Limite Superior 90%] ),
        NOT ISBLANK ( [Projeção] )
    ),
    _fil
)
ORDER BY dCalendario[AnoMes]''', exemplo=dict(filiais=[])),
    dict(name='simular_cenario', desc='Resultado operacional sob premissas (preco, desconto, volume, custo, frete, despesas). Nao e previsao.',
         params={"periodo": PERIODO, "filiais": FILIAL,
                 "preco": {"type": "number", "minimum": -0.2, "maximum": 0.2, "multipleOf": 0.01, "default": 0},
                 "desconto_pp": {"type": "integer", "minimum": -5, "maximum": 5, "default": 0},
                 "volume": {"type": "number", "minimum": -0.2, "maximum": 0.2, "multipleOf": 0.01, "default": 0},
                 "custo": {"type": "number", "minimum": -0.1, "maximum": 0.1, "multipleOf": 0.01, "default": 0},
                 "frete": {"type": "number", "minimum": -0.2, "maximum": 0.2, "multipleOf": 0.01, "default": 0},
                 "despesas": {"type": "number", "minimum": -0.2, "maximum": 0.2, "multipleOf": 0.01, "default": 0}},
         required=["periodo"],
         dax=FILT + '''
EVALUATE
CALCULATETABLE (
    ADDCOLUMNS ( SUMMARIZE ( 'Sim Etapa', 'Sim Etapa'[Ordem], 'Sim Etapa'[Etapa] ), "Efeito", [Sim Valor Etapa] ),
    _per, _fil,
    'Sim Preço'[Preço %] = {preco}, 'Sim Desconto'[Desconto p.p.] = {desconto_pp}, 'Sim Volume'[Volume %] = {volume},
    'Sim Custo'[Custo %] = {custo}, 'Sim Frete'[Frete %] = {frete}, 'Sim Despesas'[Despesas %] = {despesas}
)
ORDER BY 'Sim Etapa'[Ordem]''', exemplo=dict(inicio='2026-01-01', fim='2026-10-31', filiais=[], preco=0.03, desconto_pp=1, volume=-0.05, custo=0.02, frete=0.1, despesas=-0.05)),
]


for _t in TOOLS:  # VARs de consulta exigem DEFINE
    if _t['dax'].lstrip().startswith('VAR'):
        _t['dax'] = 'DEFINE\n' + _t['dax']


def render(tool, args):
    a = dict(args)
    fil = a.get('filiais', [])
    a['n_filiais'] = len(fil)
    a['fil_expr'] = ('TREATAS ( { %s }, dFilial[Cidade] )' % ', '.join('"%s"' % f.replace('"', '') for f in fil)) if fil else 'ALL ( dFilial[Cidade] )'
    if 'ordem' in a:
        a['ordem_dax'] = 'ASC' if a['ordem'] == 'asc' else 'DESC'
    return tool['dax'].format(**a)


def schema(tool):
    props = {}
    for k, v in tool['params'].items():
        if k == 'periodo':
            props[k] = v
        else:
            props[k] = v
    return {"name": tool['name'], "description": tool['desc'],
            "input_schema": {"type": "object", "properties": props, "required": tool['required'], "additionalProperties": False}}


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    json.dump({"versao": "1.0", "modelo": "NEXUS360 (Power BI semantic model)", "modo": "somente leitura",
               "ferramentas": [schema(t) for t in TOOLS]}, open(os.path.join(out, 'CATALOGO_FERRAMENTAS.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    with open(os.path.join(out, 'CONSULTAS_DAX.dax'), 'w', encoding='utf-8') as f:
        f.write('// NEXUS 360 - Consultas DAX governadas do AI Decision Assistant\n// Placeholders {x} sao preenchidos pelo orquestrador APOS validacao do schema; nunca por texto livre do LLM.\n\n')
        for t in TOOLS:
            f.write('// ===== %s: %s\n%s\n\n' % (t['name'], t['desc'], t['dax']))
    with open(os.path.join(out, 'EXEMPLOS_RENDERIZADOS.dax'), 'w', encoding='utf-8') as f:
        for t in TOOLS:
            f.write('// ===== %s %s\n%s\n\n' % (t['name'], json.dumps(t['exemplo'], ensure_ascii=False), render(t, t['exemplo'])))
    print('ok', len(TOOLS))
