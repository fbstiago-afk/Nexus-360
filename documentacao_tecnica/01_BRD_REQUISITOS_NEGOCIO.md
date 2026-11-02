# 01 — BRD | Requisitos de negócio

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## 1. Visão e limites
NEXUS 360 é um ambiente de decisão para distribuidora B2B fictícia com **12 filiais**, **35,000 clientes**, **15,000 produtos** e 849,620 linhas distribuídas em 26 tabelas. Os números são sintéticos e não representam empresa real.

**Objetivo:** permitir decisões integradas entre diretoria, comercial, crédito/financeiro, suprimentos, logística e operações. Não se trata de ERP operacional nem de demonstrativo contábil auditado.

## 2. Personas e decisões
| Persona | Decisão | Dados efetivos | Critério de aceite |
|---|---|---|---|
| Diretoria | Priorizar filial e margem | `fFaturamento`, `fDespesa`, `fMeta` | Receita e margem conciliam com soma da fato |
| Gerente comercial | Rebalancear carteira e descontos | `fPedido`, `fItemPedido`, `dVendedor` | Filtros por vendedor não duplicam pedidos |
| Gestão de clientes | Identificar inatividade e reativação | `fPedido`, `dCliente`, `fVisitaComercial` | Janela de churn explícita, sem antecipar futuro |
| Logística | Identificar falhas de entrega | `fEntrega`, `dTransportadora` | Denominador OTIF documentado |
| WMS | Identificar ocupação da amostra | `dPosicaoArmazem`, `fOcupacaoArmazem` | Não inferir ocupação total da filial |
| Financeiro | Avaliar vencidos e liquidação | `fContasReceber`, `fContasPagar` | Data de corte aplicada ao status |
| Suprimentos | Monitorar rupturas amostrais | `fEstoqueMensal`, `fCompra` | Ruptura restrita aos SKUs amostrados |
| Planejamento | Comparar metas e cenários | `fMeta`, `fPrevisao`, `fOrcamento` | Realizado não mistura período futuro |

## 3. Requisitos funcionais (RF)
| ID | Requisito | Prioridade | Aceite |
|---|---|---|---|
| RF01 | Home com navegação e filtros recolhíveis | Alta | Navegação acessível por teclado e mouse |
| RF02 | KPIs executivos por período/filial | Alta | Total consistente com SQLite |
| RF03 | Diagnóstico de preço, volume e mix | Alta | Medidas respeitam grão de item versus fatura |
| RF04 | Análise de churn com parâmetro 90 dias (PROPOSTA) | Alta | Reativação não apaga churn histórico |
| RF05 | OTIF, atrasos e transportadoras | Alta | Apenas entregas elegíveis entram no denominador |
| RF06 | Mapa de filiais com latitude/longitude reais do banco | Média | Nenhuma coordenada criada artificialmente |
| RF07 | WMS 3D para posições amostradas | Média | Renderização 3D em camada compatível; fallback 2D |
| RF08 | DRE gerencial simplificada | Alta | Rotulada não contábil; despesas não reconciliadas |
| RF09 | Forecast comparativo com dados históricos | Média | Projeção identificada como sintética |
| RF10 | Simulador What-if sem persistir transações | Média | Premissas e resultados reproduzíveis |
| RF11 | Calendário de visitas e campanhas | Média | Sem confundir `Inicio/Fim` com evento diário |
| RF12 | Assistente conversacional | Opcional | Respostas com DAX parametrizado e controles de acesso |

## 4. Requisitos não funcionais
- **Performance (meta proposta):** abertura de página em até 5 s e interação simples até 2 s em máquina de referência documentada; não são resultados medidos.
- **Acessibilidade:** contraste adequado, teclado, não depender só de cor e respeito a redução de movimento.
- **Governança:** camada de medidas centralizada, documentação TMDL, versão do tema e logs de validação.
- **Segurança:** sem credenciais embutidas; RLS apenas se houver cenário de acesso por filial, a ser testado.

## 5. Regras empresariais fundamentadas
- Receita = soma de `fFaturamento[ReceitaLiquida]`; CMV = soma de `fFaturamento[CMV]`; margem bruta = receita menos CMV.
- `fItemPedido[ValorLiquido]` já contém efeito de desconto: não descontar novamente.
- Devoluções são eventos separados: receita ajustada precisa declarar a dedução.
- OTIF = entregas `NoPrazo=1` **e** `InFull=1` / entregas elegíveis.
- Inadimplência depende de vencimento, pagamento e data de corte, não apenas de status atual.
- Estoque, ocupação e despesas têm limitações explícitas no README; não produzir afirmações de cobertura integral ou auditoria.

## 6. Exclusões e riscos
Excluídos: rastreamento GPS real, picking em tempo real, IA conectada sem infraestrutura, previsão validada em produção, reconciliação contábil, inventário integral, otimização real de rotas. Riscos: caminhos de filtro ambíguos, datas futuras, falsa causalidade e indicadores agregados com grãos distintos.

## 7. Definition of Done
Dados e esquema verificados; medidas com reconciliação SQL; 11 telas com hierarquia clara; testes de filtros; ausência de erros visuais; documentação de limitações; pacote PBIP reproduzível e sem credenciais.
