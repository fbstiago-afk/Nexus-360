# 06 — Storytelling e matriz de insights

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## Princípio
Cada tela deve encadear **sinal → investigação → decisão → acompanhamento**. Correlação não prova causalidade; recomendações são hipóteses até validação operacional.

| Tela | Pergunta executiva | Fonte comprovada | Insight e ação possível | Ressalva |
|---|---|---|---|---|
| Home | Onde investigar primeiro? | `fFaturamento`, `fEntrega`, `fMeta` | Destacar anomalias e abrir tela de origem | Não pontuar risco sem regra |
| Executiva | Quais filiais crescem com margem? | `fFaturamento`, `fDespesa` | Comparar crescimento e margem por filial | Despesa não auditável |
| Comercial | Quem vende mais, com qual mix? | `fPedido`, `fItemPedido` | Identificar concentração e descontos | Receita item ≠ fatura |
| Clientes | Quem deixou de comprar? | `fPedido`, `dCliente` | Priorizar contato e reativação | Janela churn proposta |
| Logística | Quais transportadoras falham? | `fEntrega` | Investigar OTIF e custo frete | Elegibilidade necessária |
| WMS | Onde há gargalo de ocupação? | `fOcupacaoArmazem`, `dPosicaoArmazem` | Revisar zonas amostradas | Amostra não é total |
| Financeira | Onde a margem se perde? | `fFaturamento`, `fDespesa` | Priorizar custo e inadimplência | DRE simplificada |
| Previsão | Onde a demanda pode subir? | `fPrevisao`, `fFaturamento` | Planejar capacidade e estoque | Não há validação de forecast real |
| Simulador | Qual impacto de preço e frete? | `fFaturamento`, `fEntrega` | Comparar cenários sob premissas | Não é recomendação automática |
| Calendário | Quando ocorrem ações e visitas? | `fVisitaComercial`, `fInteracaoCampanha` | Planejar cadência comercial | Campanha é intervalo |
| Assistente | Por que o KPI mudou? | `Medidas semânticas` | Responder com evidência e navegação | Agente não implementado |

## Cenários narrativos transversais
1. **Margem cai apesar de receita crescer:** confirmar margem por mês, investigar descontos em itens, frete e despesas; não atribuir causalidade sem teste.
2. **Clientes de alto potencial ficam inativos:** usar `ClassePotencial`, frequência histórica e `DataVisita` para priorizar abordagem; classificar reativados separadamente.
3. **OTIF piora em uma filial:** comparar transportadoras, custo frete e `NoPrazo`/`InFull`; não extrapolar para rotas sem dados geográficos de entregas.
4. **Ruptura em produtos amostrados:** relacionar snapshot `fEstoqueMensal` com `fCompra` e lead time de `dProduto`; não inferir estoque total.
5. **Meta e previsão divergem:** comparar somente filial, período e indicador compatíveis; identificar cenários e incerteza.

## Regras de insight
- Cada insight exibe fonte, janela temporal, unidade, denominador, variação e contexto do filtro.
- Não narrar um valor que não esteja calculado por medida.
- Usar alertas para exceções verificáveis; usar texto explicativo curto.
- Limitar a 1-2 insights acionáveis por tela; permitir drillthrough para investigação.
