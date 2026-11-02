# NEXUS 360 - Gera DICIONARIO_MEDIDAS.md e RELACIONAMENTOS_MODELO.md a partir do TMDL salvo pelo Power BI Desktop
# Uso: python3 -I gerar_docs_modelo.py <pasta_definition> <pasta_saida_docs>
import sys, os, re, collections

D, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# ---------- medidas
txt = open(os.path.join(D, 'tables', '_Medidas.tmdl'), encoding='utf-8-sig').read().replace('\r\n', '\n')
lines = txt.split('\n')
meas = []
i = 0
desc = []
while i < len(lines):
    l = lines[i]
    if l.startswith('\t///'):
        desc.append(l.strip()[3:].strip())
        i += 1
        continue
    m = re.match(r"^\tmeasure (?:'(.+?)'|(\S+))\s*=\s*(.*)$", l)
    if m:
        name = m.group(1) or m.group(2)
        expr = [m.group(3)] if m.group(3).strip() else []
        props = {}
        i += 1
        while i < len(lines) and (lines[i].startswith('\t\t') or lines[i].strip() == ''):
            s = lines[i]
            if s.startswith('\t\t\t') or (s.strip() == '' and not props):
                expr.append(s[3:] if s.startswith('\t\t\t') else '')
            elif s.startswith('\t\t') and ':' in s and not s.startswith('\t\t\t'):
                k, v = s.strip().split(':', 1)
                props[k.strip()] = v.strip()
            i += 1
        while expr and not expr[-1].strip():
            expr.pop()
        meas.append((props.get('displayFolder', ''), name, props.get('formatString', ''), ' '.join(desc), '\n'.join(expr).strip()))
        desc = []
        continue
    if not l.startswith('\t///'):
        desc = [] if l.strip() else desc
    i += 1

byf = collections.OrderedDict()
for f, n, fmt, de, ex in sorted(meas, key=lambda x: x[0]):
    byf.setdefault(f, []).append((n, fmt, de, ex))
md = ['# NEXUS 360 — Dicionário de medidas', '',
      '**Fonte:** `pbip/NEXUS360.SemanticModel/definition/tables/_Medidas.tmdl` (gerado automaticamente por `pbip/_gerador/gerar_docs_modelo.py`).', '',
      '**Total:** %d medidas em %d pastas. Validação SQL × DAX em `testes/resultados/QA_MODELO_SEMANTICO.md`.' % (len(meas), len(byf)), '']
md += ['| Pasta | Medidas |', '|---|---:|'] + ['| %s | %d |' % (f, len(v)) for f, v in byf.items()] + ['']
for f, v in byf.items():
    md += ['## %s' % f, '']
    for n, fmt, de, ex in v:
        md += ['### %s' % n, '']
        if de:
            md += [de, '']
        md += ['Formato: `%s`' % fmt, '', '```dax', ex, '```', '']
open(os.path.join(OUT, 'DICIONARIO_MEDIDAS.md'), 'w', encoding='utf-8').write('\n'.join(md))

# ---------- relacionamentos
rt = open(os.path.join(D, 'relationships.tmdl'), encoding='utf-8-sig').read().replace('\r\n', '\n')
rels = []
for blk in rt.split('\nrelationship ')[0:]:
    b = blk if blk.startswith('relationship') else 'relationship ' + blk
    fc = re.search(r'fromColumn:\s*(\S+)\.(\S+)', b)
    tc = re.search(r'toColumn:\s*(\S+)\.(\S+)', b)
    if not fc:
        continue
    act = 'isActive: false' not in b
    cf = 'Ambas' if 'crossFilteringBehavior: bothDirections' in b else 'Única'
    rels.append((fc.group(1), fc.group(2), tc.group(1), tc.group(2), act, cf))
rels.sort(key=lambda r: (r[0], not r[4], r[2]))
mr = ['# NEXUS 360 — Relacionamentos do modelo', '',
      '**Fonte:** `relationships.tmdl` salvo pelo Power BI Desktop. **Total:** %d (%d ativos, %d inativos). Cardinalidade N:1 em todos (fato → dimensão); %d com filtro bidirecional.' % (
          len(rels), sum(r[4] for r in rels), sum(not r[4] for r in rels), sum(r[5] == 'Ambas' for r in rels)), '',
      '| Fato | Coluna | Dimensão | Coluna | Ativo | Filtro |', '|---|---|---|---|:---:|:---:|']
mr += ['| %s | %s | %s | %s | %s | %s |' % (a, b, c, d, 'Sim' if e else 'Não (USERELATIONSHIP)', f) for a, b, c, d, e, f in rels]
open(os.path.join(OUT, 'RELACIONAMENTOS_MODELO.md'), 'w', encoding='utf-8').write('\n'.join(mr) + '\n')
print('medidas', len(meas), 'pastas', len(byf), 'relacoes', len(rels), 'bidirecionais', sum(r[5] == 'Ambas' for r in rels))
