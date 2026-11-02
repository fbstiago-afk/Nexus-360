# NEXUS 360 - Padrao tipografico e numerico (pedido de 02/11/2026):
#  fontes +20% em tudo, +30% em tabelas e matrizes; colunas de tabelas/matrizes centralizadas;
#  valores sem casas decimais (numeros inteiros).
# Aplicado na escrita pelos geradores (nx_pbir.Pagina.write, nx_medidas.upsert, nx_tabelas) e uma unica vez
# sobre os arquivos existentes (aplicar_estilo_existente.py).
import re, json

F_GERAL, F_TABELA = 1.2, 1.3
TABELAS = ('tableEx', 'pivotTable')
FONT_KEYS = ('fontSize', 'textSize', 'labelFontSize', 'titleFontSize', 'headerSize', 'titleSize', 'searchTextSize')


def _r(v, f):
    x = round(float(v) * f, 1)
    return ('%g' % x)


# ---------- formatos numericos
_FMT_LIT = re.compile(r'"([#0,.%+\-;R$ ▲▼]*0\.0+[#0,.%+\-;R$ ▲▼]*)"')


def fmt(s):
    """Formato do Power BI/Excel sem casas decimais."""
    return re.sub(r'0\.0+', '0', s) if s else s


def dax(expr):
    """Expressao DAX (HTML/SVG): fontes x1,2 e FORMAT sem decimais."""
    expr = re.sub(r'font-size:\s*([0-9.]+)px', lambda m: 'font-size:%spx' % _r(m.group(1), F_GERAL), expr)
    expr = re.sub(r"font-size=('|\"\")([0-9.]+)", lambda m: 'font-size=%s%s' % (m.group(1), _r(m.group(2), F_GERAL)), expr)
    expr = _FMT_LIT.sub(lambda m: '"%s"' % fmt(m.group(1)), expr)
    return expr


# ---------- Vega-Lite (Deneb)
def _d3(s):
    s = re.sub(r'\.([1-9])f', '.0f', s)
    s = re.sub(r'\.([1-9])%', '.0%', s)
    return s


def _expr(v):
    """Expressoes Vega (calculate, labelExpr, filter): formatos sem decimais."""
    v = re.sub(r"'([#0,.%+\-;R$ ▲▼]*0\.0+[#0,.%+\-;R$ ▲▼]*)'", lambda m: "'%s'" % fmt(m.group(1)), v)
    v = re.sub(r"'([+,]*)\.([1-9])([f%])'", lambda m: "'%s.0%s'" % (m.group(1), m.group(3)), v)
    return v


def vega(o):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if k in FONT_KEYS and isinstance(v, (int, float)):
                out[k] = float(_r(v, F_GERAL)) if '.' in _r(v, F_GERAL) else int(_r(v, F_GERAL))
            elif k == 'format' and isinstance(v, str):
                out[k] = fmt(_d3(v)) if any(c in v for c in '#') or v.startswith(('0', '+0', 'R$')) else _d3(v)
            elif isinstance(v, str) and k not in ('field', 'as', 'title', 'name'):
                out[k] = _expr(v)
            else:
                out[k] = vega(v)
        return out
    if isinstance(o, list):
        return [vega(x) for x in o]
    return o


# ---------- PBIR visual.json
def _lit_scale(d, f):
    v = d.get('expr', {}).get('Literal', {}).get('Value') if isinstance(d, dict) else None
    if not v:
        return d
    m = re.match(r'^([0-9.]+)([DL]?)$', v)
    if not m:
        return d
    return {'expr': {'Literal': {'Value': _r(m.group(1), f) + 'D'}}}


def _walk(o, f):
    if isinstance(o, dict):
        for k in list(o):
            v = o[k]
            if k in FONT_KEYS and isinstance(v, dict) and 'expr' in v:
                o[k] = _lit_scale(v, f)
            elif k == 'textStyle' and isinstance(v, dict) and isinstance(v.get('fontSize'), str) and v['fontSize'].endswith('pt'):
                v['fontSize'] = _r(v['fontSize'][:-2], f) + 'pt'
            elif k in ('jsonSpec', 'jsonConfig') and isinstance(v, dict):
                lv = v.get('expr', {}).get('Literal', {}).get('Value')
                if lv and lv.startswith("'"):
                    spec = json.loads(lv[1:-1].replace("''", "'"))
                    spec = vega(spec)
                    if k == 'jsonConfig':
                        spec.setdefault('text', {}).setdefault('fontSize', 13)
                        spec.setdefault('title', {}).setdefault('fontSize', 14)
                    o[k] = {'expr': {'Literal': {'Value': "'" + json.dumps(spec, ensure_ascii=False).replace("'", "''") + "'"}}}
            else:
                _walk(v, f)
    elif isinstance(o, list):
        for x in o:
            _walk(x, f)


def visual(v):
    """Aplica o padrao a um visual.json (dict) e devolve o mesmo dict."""
    vis = v.get('visual')
    if not vis:
        return v
    vt = vis.get('visualType', '')
    f = F_TABELA if vt in TABELAS else F_GERAL
    _walk(vis, f)
    objs = vis.setdefault('objects', {}) if vis.get('query') or vt in TABELAS else vis.get('objects', {})
    # rotulos de dados sem casas decimais
    for lab in objs.get('labels', []):
        lab.setdefault('properties', {})['labelPrecision'] = {'expr': {'Literal': {'Value': '0L'}}}
    if vt in TABELAS:
        ali = {'expr': {'Literal': {'Value': "'Center'"}}}
        for ch in objs.setdefault('columnHeaders', [{'properties': {}}]):
            ch.setdefault('properties', {})['alignment'] = ali
        if vt == 'pivotTable':
            rh = objs.setdefault('rowHeaders', [{'properties': {}}])
            rh[0].setdefault('properties', {})['alignment'] = ali
        refs = []
        for role in vis.get('query', {}).get('queryState', {}).values():
            for p in role.get('projections', []):
                if p.get('queryRef'):
                    refs.append(p['queryRef'])
        cf = [c for c in objs.get('columnFormatting', []) if 'alignment' not in c.get('properties', {})]
        for r in refs:
            cf.append({'properties': {'alignment': ali}, 'selector': {'metadata': r}})
        objs['columnFormatting'] = cf
    return v


# ---------- tema
def tema(t):
    for k, v in t.get('textClasses', {}).items():
        if 'fontSize' in v:
            v['fontSize'] = float(_r(v['fontSize'], F_GERAL))
    for vt, cfg in t.get('visualStyles', {}).items():
        f = F_TABELA if vt in TABELAS else F_GERAL

        def w(o):
            if isinstance(o, dict):
                for k in list(o):
                    if k in FONT_KEYS and isinstance(o[k], (int, float)):
                        o[k] = float(_r(o[k], f))
                    else:
                        w(o[k])
            elif isinstance(o, list):
                for x in o:
                    w(x)
        w(cfg)
    return t
