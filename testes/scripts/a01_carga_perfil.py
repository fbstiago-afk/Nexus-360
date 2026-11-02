# NEXUS 360 - Auditoria A01: carga dos CSV em SQLite de auditoria + perfil de colunas
# Uso: python3 -I a01_carga_perfil.py <raiz_projeto>
import sys, os, csv, json, sqlite3, re, hashlib, datetime
raiz = sys.argv[1]
csvdir = os.path.join(raiz, 'dados', 'NEXUS360', 'csv')
meta = os.path.join(raiz, 'dados', 'NEXUS360')
outdb_dir = os.path.join(raiz, 'dados', 'sqlite_auditoria'); os.makedirs(outdb_dir, exist_ok=True)
dbp = os.environ.get('NX_DB', os.path.join(outdb_dir, 'NEXUS360_auditoria_from_csv.db'))
if os.path.exists(dbp):
    print('DB ja existe, reutilizando:', dbp)
con = sqlite3.connect(dbp)
dic = json.load(open(os.path.join(meta, 'DICIONARIO_DADOS.json'), encoding='utf-8-sig'))['tabelas']
INT = re.compile(r'^-?\d+$'); NUM = re.compile(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$'); DT = re.compile(r'^\d{4}-\d{2}-\d{2}$')
perfil = {}; hashes = {}
for fn in sorted(os.listdir(csvdir)):
    if not fn.endswith('.csv'): continue
    t = fn[:-4]; p = os.path.join(csvdir, fn)
    hashes[fn] = hashlib.sha256(open(p,'rb').read()).hexdigest()
    raw = open(p,'rb').read(3); bom = raw == b'\xef\xbb\xbf'
    with open(p, encoding='utf-8-sig', newline='') as f:
        r = csv.reader(f); hdr = next(r); rows = list(r)
    badlen = sum(1 for x in rows if len(x) != len(hdr))
    cols = {}
    for i, c in enumerate(hdr):
        vals = [x[i] for x in rows]
        nonempty = [v for v in vals if v != '']
        kind = 'empty'
        if nonempty:
            if all(INT.match(v) for v in nonempty): kind = 'int'
            elif all(NUM.match(v) for v in nonempty): kind = 'decimal'
            elif all(DT.match(v) for v in nonempty): kind = 'date'
            else: kind = 'text'
        bad_dates = 0
        if kind == 'date':
            for v in nonempty:
                try: datetime.date.fromisoformat(v)
                except Exception: bad_dates += 1
        num = None
        if kind in ('int','decimal'):
            fv = [float(v) for v in nonempty]
            num = {'min': min(fv), 'max': max(fv), 'neg': sum(1 for v in fv if v < 0), 'zero': sum(1 for v in fv if v == 0)}
        d = set(nonempty)
        cols[c] = {'tipo_inferido': kind, 'vazios': len(vals)-len(nonempty), 'distintos': len(d),
                   'min': min(nonempty) if nonempty and kind in ('date','text') else (num['min'] if num else None),
                   'max': max(nonempty) if nonempty and kind in ('date','text') else (num['max'] if num else None),
                   'negativos': num['neg'] if num else None, 'zeros': num['zero'] if num else None,
                   'datas_invalidas': bad_dates,
                   'dominio': sorted(d)[:25] if len(d) <= 25 else None}
    perfil[t] = {'linhas': len(rows), 'colunas': hdr, 'bom': bom, 'linhas_malformadas': badlen, 'perfil': cols,
                 'dic_colunas': dic.get(t, {}).get('colunas'), 'dic_linhas': dic.get(t, {}).get('linhas')}
    # carga sqlite (tipagem conforme inferida)
    tmap = {'int':'INTEGER','decimal':'REAL','date':'TEXT','text':'TEXT','empty':'TEXT'}
    con.execute(f'DROP TABLE IF EXISTS "{t}"')
    con.execute(f'CREATE TABLE "{t}" (' + ','.join(f'"{c}" {tmap[cols[c]["tipo_inferido"]]}' for c in hdr) + ')')
    def conv(v, k):
        if v == '': return None
        if k == 'int': return int(v)
        if k == 'decimal': return float(v)
        return v
    kinds = [cols[c]['tipo_inferido'] for c in hdr]
    con.executemany(f'INSERT INTO "{t}" VALUES (' + ','.join('?'*len(hdr)) + ')', ([conv(v,k) for v,k in zip(x,kinds)] for x in rows))
    con.commit()
    print(f'{t}: {len(rows)} linhas, {len(hdr)} colunas, bom={bom}, malformadas={badlen}')
json.dump({'perfil': perfil, 'sha256_csv': hashes}, open(os.path.join(raiz,'testes','resultados','a01_perfil.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('TOTAL', sum(v['linhas'] for v in perfil.values()), 'tabelas', len(perfil))
