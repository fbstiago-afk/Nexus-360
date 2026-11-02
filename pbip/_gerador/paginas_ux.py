# NEXUS 360 - Linhas de dPaginaUX (cabecalho e painel de informacoes de cada pagina). Upsert por nome da pagina.
import re, sys

PAGINAS = {
 'Commercial Intelligence': dict(ordem=2, sub='Quem vende mais, com qual mix e a que custo de desconto?',
   obj='Identificar vendedores, categorias e marcas que sustentam ou corroem receita e margem, e onde o desconto não se converte em resultado.',
   kpis='Receita Líquida: itens de pedidos faturados, pela data da fatura.|Margem Bruta %: (Receita − CMV) ÷ Receita, no nível do item.|Desconto Médio Ponderado %: desconto dos itens ponderado pelo valor líquido.|Clientes Positivados: clientes distintos com item faturado no período.|Participação: receita do item ÷ receita da seleção.',
   fonte='fItemPedido, dVendedor, dProduto, dFilial. Base sintética, histórico de 01/01/2024 a 31/10/2026.',
   regras='Comparações com o ano anterior limitadas à data de corte.|Cores de margem comparam o item com a margem da seleção (±0,5 p.p.).|Desconto alto: acima do 3º quartil dos vendedores da seleção; margem baixa: abaixo da mediana.',
   lim='Não há meta por vendedor nem por produto na fonte: o atingimento comercial é apresentado por filial na página executiva.|Receita por fornecedor não é atribuível (produtos vendidos sem compra e com mais de um fornecedor).|Metas, frete, impostos e devoluções não têm grão de produto.'),
 'Customer Intelligence': dict(ordem=3, sub='Quem deixou de comprar, quem está em risco e quem vale recuperar?',
   obj='Acompanhar a saúde da base de clientes, priorizar o contato com clientes em risco de maior valor e medir reativação e recompra.',
   kpis='Status (exclusivos, na data de referência): Novo (1ª compra há menos de 180 dias), Ativo, Reativado (voltou após 365+ dias), Em risco (180 a 364 dias sem compra), Churn (365+ dias).|Taxa de Churn: clientes em churn ÷ clientes com histórico.|Reativações e Receita Recuperada: retornos no período e faturas desses retornos.|Taxa de Recompra: clientes com 2+ faturas no período.|Retenção de cohort: clientes do mês de 1ª compra que voltam a comprar N meses depois.',
   fonte='fFaturamento, fItemPedido, dCliente. Base sintética, histórico de 01/01/2024 a 31/10/2026.',
   regras='A data de referência é o fim do período selecionado (limitada ao corte).|Limites de ativo (180) e churn (365) são parâmetros do painel de filtros.|Frequência × valor: faturas no período (1, 2, 3–4, 5+) × quartis de receita do período; são faixas de exibição, não uma pontuação RFM.|O cohort usa o histórico completo: os filtros de ano e mês não se aplicam a ele.',
   lim='A documentação não define regra de RFM/RFQ; a página usa a grade frequência × valor.|DataCadastro do cliente não é usada como aquisição (auditoria C6): a 1ª fatura define o cohort.|Os status não respondem a filtro de produto (são calculados por fatura).'),
 'Logistics Control Tower': dict(ordem=4, sub='Onde e por que a entrega falha, e quanto custa?',
   obj='Monitorar o nível de serviço (OTIF) contra a meta, localizar filiais e transportadoras que falham e relacionar falha e custo de frete.',
   kpis='OTIF %: entregas no prazo e completas ÷ entregas.|No prazo %: entrega até a data prometida.|In full %: entrega completa.|Ocorrência %: entregas com ocorrência registrada.|Atraso médio: dias de atraso das entregas fora do prazo.|Frete por entrega: custo de frete ÷ entregas.',
   fonte='fEntrega, dTransportadora, dFilial, fMeta. Base sintética, histórico de 01/01/2024 a 31/10/2026.',
   regras='Data ativa: data da entrega (a data prometida está disponível como relação inativa).|Meta OTIF: média simples das metas filial-mês até o corte.|Destaque de transportadora: OTIF abaixo da mediana e frete acima da mediana da seleção.',
   lim='A fonte não tem destino geográfico das entregas: o mapa mostra a filial de origem, sem rotas.|Out/2026 tem datas truncadas em 31/10 (auditoria C5): OTIF do último mês pode estar distorcido.|Frete % da receita não responde a filtro de produto.'),
 'Financial & Profitability': dict(ordem=6, sub='Onde a margem se perde e como o caixa acompanha o resultado?',
   obj='Ler a DRE gerencial contra o ano anterior e o orçamento, explicar a variação do resultado por linha, acompanhar recebimentos e pagamentos e localizar desvios de despesa.',
   kpis='Receita, CMV e margem bruta: itens faturados, por competência (data da fatura).|Despesas operacionais: fDespesa elegível, por conta.|Resultado gerencial: margem bruta − despesas operacionais (não contábil).|Recebido: títulos recebidos (regra D1), pela data do pagamento.|Pago a fornecedores: contas a pagar elegíveis pagas, pela data do pagamento.|Inadimplência: vencido em aberto ÷ vencido até a data de referência.',
   fonte='fItemPedido, fFaturamento, fDespesa, fOrcamento, fContasReceber, fContasPagar. Base sintética, histórico de 01/01/2024 a 31/10/2026.',
   regras='DRE e ponte comparam com o mesmo período do ano anterior, limitado ao corte.|Orçamento existe só para receita e despesa operacional total (não por conta).|Ponte do resultado: efeito de cada linha = valor atual − valor do ano anterior.|Pareto: margem bruta por subcategoria, linha = participação acumulada.',
   lim='Caixa parcial: despesas operacionais não têm registro de pagamento; o saldo mostrado é recebido de clientes − pago a fornecedores.|Impostos não entram na DRE gerencial (sem regra de alocação).|DRE não auditada; títulos inconsistentes ficam fora do recebido.'),
 'Warehouse Digital Twin': dict(ordem=5, sub='Onde há gargalo de ocupação e estoque parado?',
   obj='Visualizar as posições do armazém de cada filial (corredor × coluna × nível) com o status lido no snapshot, acompanhar a ocupação ao longo do tempo e o estoque sem giro.',
   kpis='Posições cadastradas: dPosicaoArmazem (400 por filial).|Posições lidas: posições com leitura no último snapshot do período.|Ocupada / Bloqueada / Disponível: participação das leituras do snapshot.|Ruptura e abaixo do mínimo: SKU-filial do snapshot de estoque.|Parados 90+: SKU-filial com 90 ou mais dias sem movimento.',
   fonte='dPosicaoArmazem, fOcupacaoArmazem, fEstoqueMensal, fMovimentoEstoque. Base sintética, snapshots mensais até 31/10/2026.',
   regras='O mapa usa o último snapshot do período e exige uma única filial.|Posições sem leitura aparecem vazias: não são tratadas como disponíveis.|A grade mostra a vista de cima de cada nível (Y de 10 a 1, X de 1 a 10).',
   lim='Ocupação e estoque são amostras (auditoria C9): cerca de 35 posições lidas por filial por mês, não a capacidade real.|A fonte registra posições Disponível com paletes; o dado é exibido como está.|O gêmeo 3D é uma aplicação complementar, fora do Power BI.'),
 'Predictive Intelligence': dict(ordem=7, sub='Para onde a receita caminha, com que incerteza, e onde a meta fica em risco?',
   obj='Separar histórico, projeção e previsão; estimar os próximos meses com um método explícito e medir seu erro; identificar filiais com risco de não atingir a meta.',
   kpis='Projeção sazonal: receita do mesmo mês do ano anterior × fator de tendência de 12 meses.|Faixa de 90%: projeção × (1 ± 1,833 × σ), σ dos erros do backtest (t de Student, 9 gl).|MAPE: erro percentual absoluto médio do método nos meses do ano do corte.|Previsão da fonte: fPrevisao (jan–jun/2027), exibida separada da projeção.|Sazonalidade: receita do mês ÷ média mensal do ano.',
   fonte='fItemPedido (realizado), fMeta, fPrevisao. Base sintética, histórico de 01/01/2024 a 31/10/2026.',
   regras='A página não tem filtro de período: mostra todo o histórico e o horizonte futuro.|A projeção começa no mês seguinte ao corte; o backtest usa 10 meses (jan–out do ano do corte), cada um com a tendência calculada até o mês anterior.|Risco à meta: projeção de nov–dez comparada à meta da filial.',
   lim='Backtest curto (10 meses): a faixa de 90% é indicativa.|A margem de erro de fPrevisao não tem semântica validada e não é usada como intervalo.|A previsão da fonte é sintética; não há validação contra um realizado futuro.|Meta disponível até dez/2026; não há meta para 2027.'),
   'Decision Simulator': dict(ordem=8, sub='Se eu mexer em preço, desconto, volume, custo, frete ou despesas, o que acontece com o resultado?',
   obj='Testar cenários sobre a base real do período e medir o efeito de cada premissa no resultado operacional, antes de decidir.',
   kpis='Resultado operacional (simulador): receita líquida − CMV − frete − despesas operacionais.|Margem bruta: (receita − CMV) ÷ receita.|Margem operacional: resultado ÷ receita.|Volume para manter o resultado: variação de volume que iguala o resultado simulado ao base, com as demais premissas.|Sensibilidade: Δ resultado para cada par preço × volume da grade (−10% a +10%).',
   fonte='fItemPedido (receita, CMV, desconto), fEntrega (frete), fDespesa (despesas). Base: período e filiais selecionados, limitado ao corte (31/10/2026).',
   regras='Preço: receita × (1 + Δpreço).|Desconto: receita × (1 − (d₀ + Δ)) ÷ (1 − d₀), d₀ = desconto médio ponderado da base.|Volume: escala receita, CMV e frete.|Custo e frete: alteram o custo unitário e a tarifa.|Despesas: variação direta, não escalam com volume.|Ponte: efeitos sequenciais (preço → desconto → volume → custo → frete → despesas); a soma fecha no resultado simulado.',
   lim='Não há elasticidade preço × volume: o usuário define os dois de forma independente.|O resultado do simulador inclui o frete e difere do resultado gerencial da DRE.|A simulação não responde a filtro de produto (frete e despesas não têm produto).|Não é previsão nem recomendação: o cenário vale apenas sob as premissas escolhidas.'),
   'Operations Calendar': dict(ordem=9, sub='Quando acontecem campanhas, visitas e entregas, e em que dias a operação falha?',
   obj='Ler o mês dia a dia: campanhas em vigor, cadência de visitas comerciais e volume e nível de serviço das entregas, para planejar a agenda e localizar dias críticos.',
   kpis='Visitas: registros de fVisitaComercial pela data da visita.|Conversão de visitas: visitas com resultado Pedido ÷ visitas.|Campanhas ativas: campanhas cujo intervalo início–fim cruza o período.|Interações e conversões: fInteracaoCampanha pela data da interação.|Entregas e OTIF: fEntrega pela data da entrega; meta OTIF do mês (fMeta).|Receita vs meta: só com o mês inteiro (a meta é mensal).',
   fonte='fVisitaComercial, fInteracaoCampanha, dCampanha, fEntrega, fMeta, fItemPedido. Base sintética, histórico até 31/10/2026.',
   regras='Semana de segunda a domingo; dias de outros meses ficam vazios.|Campanha é intervalo: aparece em todos os dias entre início e fim, sem ser tratada como evento diário.|Ponto das entregas: verde quando o OTIF do dia atinge a meta do mês, âmbar abaixo da meta, vermelho (com borda) quando fica 5 p.p. abaixo da média do mês; como o OTIF está abaixo da meta em quase todos os dias, a borda destaca os piores dias.|A tabela de vendedores mostra só os 10 com mais visitas e não tem total (o total do mês está no indicador).|Clique em um dia filtra o cronograma, a tabela e os indicadores; o mês é escolhido no seletor visível.',
   lim='Campanhas não têm filial: o filtro de filial não as afeta.|31/10/2026 concentra entregas com data truncada (auditoria C5).|Datas após o corte aparecem tracejadas e sem dados.|Não há agenda futura de visitas na fonte: o calendário é histórico.'),
   'AI Decision Assistant': dict(ordem=10, sub='Como responder perguntas de negócio em linguagem natural sem perder a rastreabilidade dos números?',
   obj='Apresentar a arquitetura de análise conversacional sobre o modelo semântico: ferramentas tipadas, consultas DAX governadas e controles de segurança. A página mostra os resultados reais das consultas; não há IA conectada.',
   kpis='Ferramentas: 8 funções somente leitura com entrada validada por JSON Schema.|Consultas: modelos DAX fixos, parametrizados pelo orquestrador.|Status: implementado (catálogo e consultas), testado (8 consultas executadas no modelo), pendente (LLM, autenticação, endpoint).',
   fonte='Modelo semântico NEXUS360 (medidas existentes). Especificação em apps/ai_assistant.',
   regras='O LLM nunca escreve DAX: escolhe a ferramenta e os parâmetros.|Cada número da resposta deve citar a ferramenta e os filtros de origem.|Sem dado retornado, sem resposta.',
   lim='Interface demonstrativa: a pergunta é um exemplo fixo e a entrada de texto está desativada.|Integração com LLM, Entra ID, RLS e API executeQueries não implementadas.|Os resultados exibidos seguem os filtros da página, não uma pergunta digitada.'),
}


def _esc(t):
    return t.replace('"', '""')


def upsert(path):
    raw = open(path, encoding='utf-8-sig').read()
    crlf = '\r\n' in raw
    t = raw.replace('\r\n', '\n')
    for nome, d in PAGINAS.items():
        row = ('\t\t\t\t        { %d, "%s", "%s",\n\t\t\t\t          "%s",\n\t\t\t\t          "%s",\n\t\t\t\t          "%s",\n\t\t\t\t          "%s",\n\t\t\t\t          "%s" }'
               % (d['ordem'], _esc(nome), _esc(d['sub']), _esc(d['obj']), _esc(d['kpis']), _esc(d['fonte']), _esc(d['regras']), _esc(d['lim'])))
        pat = re.compile(r'\t\t\t\t        \{ \d+, "%s",.*?" \}' % re.escape(nome), re.S)
        if pat.search(t):
            t = pat.sub(lambda m: row, t)
        else:
            i = t.index('\n\t\t\t\t    }\n')  # fechamento da lista de linhas
            t = t[:i] + ',\n' + row + t[i:]
    if crlf:
        t = t.replace('\n', '\r\n')
    open(path, 'w', encoding='utf-8').write(t)


if __name__ == '__main__':
    upsert(sys.argv[1])
    print('ok')
