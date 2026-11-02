# NEXUS 360 - Cria/atualiza tabelas calculadas desconectadas (parametros) no TMDL e registra em model.tmdl. Idempotente.
import os, uuid, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nx_estilo


def tabela(definition, nome, colunas, dax, desc=None, param=False):
    """colunas: lista de (nome, dataType, formatString ou None)."""
    tdir = os.path.join(definition, 'tables')
    path = os.path.join(tdir, nome + '.tmdl')
    q = "'%s'" % nome if re.search(r'[^A-Za-z0-9_]', nome) else nome
    tags = {}
    if os.path.exists(path):  # preserva lineageTags
        old = open(path, encoding='utf-8-sig').read()
        m = re.search(r'^table .*?\n\tlineageTag: (\S+)', old, re.M)
        if m:
            tags['__t'] = m.group(1)
        for c in re.finditer(r"\tcolumn (?:'(.+?)'|(\S+))\n(?:\t\t.*\n)*?\t\tlineageTag: (\S+)", old):
            tags[c.group(1) or c.group(2)] = c.group(3)
    L = []
    if desc:
        L.append('/// ' + desc)
    L += ['table ' + q, '\tlineageTag: ' + tags.get('__t', str(uuid.uuid4())), '']
    for c in colunas:
        cn, dt, fmt = c[:3]
        sb = c[3] if len(c) > 3 else None
        cq = "'%s'" % cn if re.search(r'[^A-Za-z0-9_]', cn) else cn
        L.append('\tcolumn ' + cq)
        L.append('\t\tdataType: ' + dt)
        if fmt:
            L.append('\t\tformatString: ' + nx_estilo.fmt(fmt))
        L.append('\t\tlineageTag: ' + tags.get(cn, str(uuid.uuid4())))
        L.append('\t\tsummarizeBy: none')
        if sb:
            L.append('\t\tsortByColumn: ' + sb)
        L.append('\t\tisNameInferred')
        L.append('\t\tsourceColumn: [%s]' % cn)
        L.append('')
        if param:  # parametro What-if: o slider de valor unico encaixa nos valores da serie
            L += ['\t\textendedProperty ParameterMetadata =', '\t\t\t\t{', '\t\t\t\t  "version": 0', '\t\t\t\t}', '']
    L += ['\tpartition %s = calculated' % q, '\t\tmode: import', '\t\tsource = ' + dax, '']
    open(path, 'w', encoding='utf-8').write('\r\n'.join(L) + '\r\n')
    mp = os.path.join(definition, 'model.tmdl')
    model = open(mp, encoding='utf-8-sig').read()
    ref = 'ref table ' + q
    if ref not in model:
        crlf = '\r\n' in model
        lines = model.replace('\r\n', '\n').split('\n')
        last = max(i for i, l in enumerate(lines) if l.startswith('ref table '))
        lines.insert(last + 1, ref)
        model = '\n'.join(lines)
        if crlf:
            model = model.replace('\n', '\r\n')
        open(mp, 'w', encoding='utf-8').write(model)
