# NEXUS 360 - A03: valores esperados (SQL) para validar o modelo semantico. Uso: python3 -I a03_esperados_modelo.py <db> <saida.json>
import sqlite3, sys, json
c = sqlite3.connect(sys.argv[1]); q = lambda s: c.execute(s).fetchone()
C = '2026-10-31'
E = {}
E['receita'], E['cmv'], E['impostos'] = q("select round(sum(ReceitaLiquida),2), round(sum(CMV),2), round(sum(Impostos),2) from fFaturamento")
E['faturas'] = q("select count(*) from fFaturamento")[0]
E['pedidos'], E['pedidos_faturados'], E['pedidos_cancelados'], E['pedidos_pendentes'] = q("select count(*), sum(StatusPedido='Faturado'), sum(StatusPedido='Cancelado'), sum(StatusPedido='Pendente') from fPedido")
E['valor_itens_todos'], E['valor_itens_faturados'], E['qtd_itens_faturados'] = q("select round(sum(i.ValorLiquido),2), round(sum(case when p.StatusPedido='Faturado' then i.ValorLiquido end),2), sum(case when p.StatusPedido='Faturado' then i.Quantidade end) from fItemPedido i join fPedido p using(PedidoID)")
E['valor_devolvido'], E['devolucoes'] = q("select round(sum(ValorDevolvido),2), count(*) from fDevolucao")
E['despesas_elegiveis'] = q(f"select round(sum(Valor),2) from fDespesa where DataReferencia<='{C}'")[0]
E['desconto_ponderado'] = q("select sum(f.ReceitaLiquida*p.DescontoPercentual)/sum(f.ReceitaLiquida) from fFaturamento f join fPedido p using(PedidoID)")[0]
E['clientes_positivados'] = q("select count(distinct p.ClienteID) from fFaturamento f join fPedido p using(PedidoID)")[0]
E['entregas'], E['otif'], E['no_prazo'], E['in_full'], E['ocorrencia'], E['frete'] = q("select count(*), sum(NoPrazo=1 and InFull=1), sum(NoPrazo=1), sum(InFull=1), sum(StatusEntrega='Ocorrência'), round(sum(CustoFrete),2) from fEntrega")
E['atraso_medio'] = q("select avg(julianday(DataEntrega)-julianday(DataPrometida)) from fEntrega where NoPrazo=0")[0]
E['lead_time_medio'] = q("select avg(julianday(e.DataEntrega)-julianday(p.DataPedido)) from fEntrega e join fPedido p using(PedidoID)")[0]
# recebimento D1
r = c.execute("""select case when cr.ValorPago>0 and cr.DataPagamento is not null and cr.DataPagamento>=f.DataFaturamento then 'Recebido'
  when cr.ValorPago=0 and cr.DataPagamento is null then 'Em aberto' else 'Inconsistente' end s, count(*), round(sum(cr.ValorTitulo),2), round(sum(cr.ValorPago),2)
  from fContasReceber cr join fFaturamento f using(PedidoID) group by 1""").fetchall()
E['recebimento'] = {x[0]: {'qtd': x[1], 'valor_titulo': x[2], 'valor_pago': x[3]} for x in r}
E['motivos'] = dict(c.execute("""select case when cr.ValorPago=0 then 'Data de pagamento sem valor pago' when cr.DataPagamento is null then 'Valor pago sem data de pagamento' else 'Pagamento anterior ao faturamento' end, count(*)
  from fContasReceber cr join fFaturamento f using(PedidoID) where not ((cr.ValorPago>0 and cr.DataPagamento is not null and cr.DataPagamento>=f.DataFaturamento) or (cr.ValorPago=0 and cr.DataPagamento is null)) group by 1""").fetchall())
base = f"""from fContasReceber cr join fFaturamento f using(PedidoID) where f.DataFaturamento<='{C}' and cr.Vencimento %s '{C}'
  and ((cr.ValorPago=0 and cr.DataPagamento is null) or (cr.ValorPago>0 and cr.DataPagamento is not null and cr.DataPagamento>=f.DataFaturamento and cr.DataPagamento>'{C}'))"""
E['saldo_vencido_aberto_corte'] = q("select round(sum(cr.ValorTitulo),2) " + base % '<')[0]
E['saldo_a_vencer_aberto_corte'] = q("select round(sum(cr.ValorTitulo),2) " + base % '>=')[0]
E['base_vencido_corte'] = q(f"""select round(sum(cr.ValorTitulo),2) from fContasReceber cr join fFaturamento f using(PedidoID) where f.DataFaturamento<='{C}' and cr.Vencimento<'{C}'
  and not (not ((cr.ValorPago>0 and cr.DataPagamento is not null and cr.DataPagamento>=f.DataFaturamento) or (cr.ValorPago=0 and cr.DataPagamento is null)))""")[0]
# saldo vencido em 2025-12-31 (teste as-of historico)
D2 = '2025-12-31'
E['saldo_vencido_aberto_20251231'] = q(f"""select round(sum(cr.ValorTitulo),2) from fContasReceber cr join fFaturamento f using(PedidoID) where f.DataFaturamento<='{D2}' and cr.Vencimento<'{D2}'
  and ((cr.ValorPago=0 and cr.DataPagamento is null) or (cr.ValorPago>0 and cr.DataPagamento is not null and cr.DataPagamento>=f.DataFaturamento and cr.DataPagamento>'{D2}'))""")[0]
# pos-corte
E['pos_corte'] = {
 'despesas_qtd_valor': q(f"select count(*), round(sum(Valor),2) from fDespesa where DataReferencia>'{C}'"),
 'compras_qtd_valor': q(f"select count(*), round(sum(ValorCompra),2) from fCompra where DataCompra>'{C}'"),
 'cp_qtd_valor': q(f"select count(*), round(sum(cp.ValorTitulo),2) from fContasPagar cp join fCompra co using(CompraID) where co.DataCompra>'{C}'"),
 'estoque_qtd': q(f"select count(*) from fEstoqueMensal where DataReferencia>'{C}'")[0],
 'mov_qtd': q(f"select count(*) from fMovimentoEstoque where DataMovimento>'{C}'")[0],
 'ocup_qtd': q(f"select count(*) from fOcupacaoArmazem where DataReferencia>'{C}'")[0],
 'data_max': q("select max(d) from (select max(DataReferencia) d from fDespesa union all select max(DataCompra) from fCompra union all select max(DataReferencia) from fEstoqueMensal union all select max(DataMovimento) from fMovimentoEstoque union all select max(DataReferencia) from fOcupacaoArmazem)")[0]}
# clientes (janela 90d na data de corte) - compra = fatura
E['clientes_historico_corte'] = q(f"select count(distinct p.ClienteID) from fFaturamento f join fPedido p using(PedidoID) where f.DataFaturamento<='{C}'")[0]
E['clientes_ativos_90d_corte'] = q(f"select count(distinct p.ClienteID) from fFaturamento f join fPedido p using(PedidoID) where f.DataFaturamento between date('{C}','-89 day') and '{C}'")[0]
E['clientes_novos_2026'] = q("select count(*) from (select p.ClienteID, min(f.DataFaturamento) m from fFaturamento f join fPedido p using(PedidoID) group by 1) where m between '2026-01-01' and '2026-10-31'")[0]
E['clientes_novos_2025'] = q("select count(*) from (select p.ClienteID, min(f.DataFaturamento) m from fFaturamento f join fPedido p using(PedidoID) group by 1) where m between '2025-01-01' and '2025-12-31'")[0]
E['clientes_reativados_2026'] = q("""select count(*) from (select distinct p.ClienteID cid from fFaturamento f join fPedido p using(PedidoID) where f.DataFaturamento between '2026-01-01' and '2026-10-31') a
  join (select p.ClienteID cid, max(f.DataFaturamento) ult from fFaturamento f join fPedido p using(PedidoID) where f.DataFaturamento<'2026-01-01' group by 1) b using(cid)
  where julianday('2026-01-01')-julianday(b.ult) > 90""")[0]
# estoque/wms no ultimo snapshot elegivel
E['estoque_snapshot_out26'] = q("select sum(SaldoUnidades), round(sum(ValorEstoque),2), count(*), sum(Ruptura), sum(SaldoUnidades<EstoqueMinimo) from fEstoqueMensal where DataReferencia='2026-10-31'")
E['wms_snapshot_out26'] = q("select count(*), count(distinct o.PosicaoID), sum(Paletes), sum(StatusPosicao='Ocupada') from fOcupacaoArmazem o where DataReferencia='2026-10-31'")
E['compras_elegiveis'] = q(f"select count(*), round(sum(ValorCompra),2) from fCompra where DataCompra<='{C}'")
E['cp_elegivel'] = q(f"select round(sum(cp.ValorTitulo),2), round(sum(case when cp.DataPagamento is not null then cp.ValorTitulo end),2), round(sum(case when cp.DataPagamento is null then cp.ValorTitulo end),2) from fContasPagar cp join fCompra co using(CompraID) where co.DataCompra<='{C}'")
# metas e tempo
E['meta_fat_total'], E['meta_fat_ate_corte'] = q(f"select round(sum(ValorMeta),2), round(sum(case when DataReferencia<='{C}' then ValorMeta end),2) from fMeta where Indicador='Faturamento'")
E['meta_margem_ponderada_ate_corte'] = q(f"""select sum(a.ValorMeta*b.ValorMeta)/sum(a.ValorMeta) from fMeta a join fMeta b on a.DataReferencia=b.DataReferencia and a.FilialID=b.FilialID
  where a.Indicador='Faturamento' and b.Indicador='Margem Bruta' and a.DataReferencia<='{C}'""")[0]
E['meta_otif_media'] = q("select avg(ValorMeta) from fMeta where Indicador='OTIF'")[0]
E['receita_2025'], E['receita_2026'] = q("select round(sum(case when DataFaturamento like '2025%' then ReceitaLiquida end),2), round(sum(case when DataFaturamento like '2026%' then ReceitaLiquida end),2) from fFaturamento")
E['receita_2025_jan_out'] = q("select round(sum(ReceitaLiquida),2) from fFaturamento where DataFaturamento between '2025-01-01' and '2025-10-31'")[0]
E['receita_set26'], E['receita_out26'] = q("select round(sum(case when DataFaturamento like '2026-09%' then ReceitaLiquida end),2), round(sum(case when DataFaturamento like '2026-10%' then ReceitaLiquida end),2) from fFaturamento")
E['receita_filial1'] = q("select round(sum(f.ReceitaLiquida),2) from fFaturamento f join fPedido p using(PedidoID) where p.FilialID=1")[0]
E['receita_categoria_alimentos_itens'] = q("select round(sum(i.ValorLiquido),2) from fItemPedido i join fPedido p using(PedidoID) join dProduto d using(ProdutoID) where p.StatusPedido='Faturado' and d.Categoria='Alimentos'")[0]
E['previsao_total'] = q("select round(sum(ReceitaPrevista),2) from fPrevisao")[0]
json.dump(E, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1, default=str)
print(json.dumps(E, ensure_ascii=False, default=str))
