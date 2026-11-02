# NEXUS 360 - A04: esperados (Python/SQL) da classificacao de clientes. Uso: python3 -I a04_esperados_churn.py <db> <saida.json>
import sqlite3, sys, json, datetime as dt, collections, statistics
c = sqlite3.connect(sys.argv[1])
rows = c.execute("select p.ClienteID, f.DataFaturamento, f.FaturaID, f.ReceitaLiquida from fFaturamento f join fPedido p using(PedidoID) order by p.ClienteID, f.DataFaturamento, f.FaturaID").fetchall()
D = lambda s: dt.date.fromisoformat(s)
inv = collections.defaultdict(list)  # cliente -> [(data, gap, receita)]
gaps = []
for cid, d, fid, rec in rows:
    lst = inv[cid]; d = D(d)
    gap = (d - lst[-1][0]).days if lst else None
    lst.append((d, gap, rec))
    if gap is not None: gaps.append(gap)
E = {'intervalo_medio': sum(gaps)/len(gaps), 'intervalo_mediano': statistics.median(gaps), 'intervalos': len(gaps)}
def status(R, La, Lc, filial=None):
    cnt = collections.Counter()
    for cid, lst in inv.items():
        h = [x for x in lst if x[0] <= R]
        if not h: continue
        U = h[-1][0]; P = h[0][0]
        Cs = [x[0] for x in h if x[1] is not None and x[1] >= Lc]
        C = max(Cs) if Cs else None
        d = (R - U).days
        if d >= Lc: s = 'Churn'
        elif d >= La: s = 'Em risco'
        elif (R - P).days < La: s = 'Novo'
        elif C and (R - C).days < La: s = 'Reativado'
        else: s = 'Ativo'
        cnt[s] += 1
    return dict(cnt)
R = dt.date(2026, 10, 31)
E['status_20261031_180_365'] = status(R, 180, 365)
E['status_20251231_180_365'] = status(dt.date(2025, 12, 31), 180, 365)
E['status_20261031_90_180'] = status(R, 90, 180)
# eventos de reativacao no periodo (gap >= 365) e receita recuperada (receita no periodo a partir da 1a compra de retorno no periodo)
def reat(ini, fim, Lc=365):
    n = 0; rec = 0.0
    for cid, lst in inv.items():
        ret = [x[0] for x in lst if ini <= x[0] <= fim and x[1] is not None and x[1] >= Lc]
        if not ret: continue
        n += 1; r0 = min(ret)
        rec += sum(x[2] for x in lst if r0 <= x[0] <= fim)
    return n, round(rec, 2)
E['reativados_2026'], E['receita_recuperada_2026'] = reat(dt.date(2026,1,1), R)
E['reativados_2025'], E['receita_recuperada_2025'] = reat(dt.date(2025,1,1), dt.date(2025,12,31))
# churn por janela comparativa em R: clientes com historico - clientes com compra nos ultimos L dias
hist = sum(1 for l in inv.values() if l[0][0] <= R)
E['churn_janelas_20261031'] = {L: round((hist - sum(1 for l in inv.values() if any(R - dt.timedelta(days=L-1) <= x[0] <= R for x in l)))/hist, 6) for L in (90,180,270,365,540,730)}
# frequencia
f26 = [(cid, x) for cid, l in inv.items() for x in l if dt.date(2026,1,1) <= x[0] <= R]
cli26 = collections.Counter(cid for cid, _ in f26)
E['compras_por_cliente_2026'] = len(f26)/len(cli26)
E['taxa_recompra_2026'] = sum(1 for v in cli26.values() if v > 1)/len(cli26)
# cohort: primeira compra jan/2025, retidos no mes +3 (abr/2025) e +12 (jan/2026)
coh = [cid for cid, l in inv.items() if l[0][0].strftime('%Y-%m') == '2025-01']
def ret(m): return sum(1 for cid in coh if any(x[0].strftime('%Y-%m') == m for x in inv[cid]))
E['cohort_2025_01'] = {'tamanho': len(coh), 'm0': ret('2025-01'), 'm3': ret('2025-04'), 'm12': ret('2026-01')}
json.dump(E, open(sys.argv[2], 'w'), indent=1, default=str)
print(json.dumps(E, default=str))
