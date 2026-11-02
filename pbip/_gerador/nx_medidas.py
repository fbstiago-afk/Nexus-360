# NEXUS 360 - Insere ou substitui medidas no _Medidas.tmdl salvo pelo Desktop (idempotente por nome).
# Uso como biblioteca: from nx_medidas import upsert; upsert(tmdl_path, [dict(name=..., expr=..., folder=..., fmt=..., desc=...)])
import re, uuid, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nx_estilo


def _block(m):
    lines = []
    if m.get('desc'):
        lines.append('\t/// ' + m['desc'])
    expr = nx_estilo.dax(m['expr'].strip('\n'))
    if '\n' in expr:
        lines.append("\tmeasure '%s' =" % m['name'])
        lines += ['\t\t\t' + l if l.strip() else '' for l in expr.split('\n')]
    else:
        lines.append("\tmeasure '%s' = %s" % (m['name'], expr))
    if m.get('fmt'):
        lines.append('\t\tformatString: ' + nx_estilo.fmt(m['fmt']))
    if m.get('cat'):
        lines.append('\t\tdataCategory: ' + m['cat'])
    if m.get('hidden'):
        lines.append('\t\tisHidden')
    lines.append('\t\tdisplayFolder: ' + m['folder'])
    lines.append('\t\tlineageTag: ' + m.get('tag', str(uuid.uuid4())))
    return '\n'.join(lines) + '\n\n'


def upsert(path, measures):
    raw = open(path, encoding='utf-8-sig').read()
    crlf = '\r\n' in raw
    t = raw.replace('\r\n', '\n')
    for m in measures:
        # localiza bloco existente (com descricao opcional) ate o proximo item de nivel 1
        pat = re.compile(r"(?:\t///[^\n]*\n)*\tmeasure '%s' =.*?(?=\n\t(?:///|measure |column |partition |hierarchy )|\Z)" % re.escape(m['name']), re.S)
        old = pat.search(t)
        if old:
            tag = re.search(r'lineageTag: (\S+)', old.group(0))
            if tag:
                m = dict(m, tag=tag.group(1))
            t = t[:old.start()] + _block(m).rstrip('\n') + t[old.end():]
        else:
            anchor = t.find('\n\tpartition ')
            ins = _block(m)
            t = t[:anchor + 1] + ins + t[anchor + 1:] if anchor >= 0 else t.rstrip('\n') + '\n\n' + ins
    if crlf:
        t = t.replace('\n', '\r\n')
    open(path, 'w', encoding='utf-8').write(t)
