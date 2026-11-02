# 00 — Auditoria de dados NEXUS 360

**Data:** 01/11/2026 · **Fonte auditada:** 26 CSV de `dados/NEXUS360/csv` (SQLite original ausente) · **Reprodução:** `python3 -I testes/scripts/a01_carga_perfil.py <raiz>` e `a02_integridade.py <raiz> <db>` · **Evidência bruta:** `testes/resultados/a01_perfil.json`, `a02_integridade.json`.

Legenda: **CRÍTICO** = afeta indicador ou modelo se ignorado · **MODERADO** = exige regra explícita · **INFO** = registrar.

## 1. Inventário verificado
**26 tabelas · 849.620 registros**, 0 linhas malformadas, todos UTF-8 com BOM, vírgula, ponto decimal, datas ISO válidas.  
Contagens, nomes de colunas, ordem, tipos e nulos **batem 100%** com `DICIONARIO_DADOS.json` e com `02_DICIONARIO_DADOS.md` (26/26 tabelas sem divergência).

| Tabela | Linhas | Período | Tabela | Linhas | Período |
|---|---:|---|---|---:|---|
| dCalendario | 1.216 | 2024-01-01→2027-04-30 | fEntrega | 88.979 | 2024-01→2026-10-31 |
| dCampanha | 72 | 2024-01→2026-10 | fEstoqueMensal | 86.400 | 2024-01→**2026-12** |
| dCliente | 35.000 | — | fFaturamento | 88.979 | 2024-01-01→2026-10-31 |
| dFilial | 12 | — | fInteracaoCampanha | 6.724 | 2024-01→2026-10 |
| dFornecedor | 150 | — | fItemPedido | 249.976 | (via pedido) |
| dPosicaoArmazem | 4.800 | — | fMeta | 1.296 | 2024-01→2026-12 |
| dProduto | 15.000 | — | fMovimentoEstoque | 30.240 | 2024-01→**2026-12** |
| dTransportadora | 30 | — | fOcupacaoArmazem | 15.120 | 2024-01→**2026-12** |
| dVendedor | 180 | — | fOrcamento | 864 | 2024-01→2026-12 |
| fCompra | 8.640 | 2024-01→**2026-12** | fPedido | 100.000 | 2024-01-01→2026-10-30 |
| fContasPagar | 8.640 | venc. ≤2026-10-31 | fPrevisao | 72 | **2027-01→2027-06** |
| fContasReceber | 88.979 | ≤2026-10-31 | fVisitaComercial | 12.500 | 2024-01→2026-10 |
| fDespesa | 2.592 | 2024-01→**2026-12** | fDevolucao | 3.159 | 2024-01→2026-10 |

## 2. Chaves e integridade referencial
- **PK:** 26/26 únicas e não nulas.
- **FK candidatas (`RELACIONAMENTOS.csv`):** 45 testadas, 44 sem órfãos. Única falha: `fPrevisao[DataReferencia] → dCalendario[Data]` = **24 órfãos** (2027-05-31 e 2027-06-30) — reproduz o REVIEW do doc 08.
- `fPedido[CampanhaID]` nulo em 84.903 linhas (pedido sem campanha — esperado).
- Cardinalidades confirmadas: `fFaturamento`, `fEntrega`, `fContasReceber` = exatamente 1 linha por pedido **Faturado** (88.979); 0 para Cancelado (3.457) e Pendente (7.564). `FaturaID = PedidoID` em 100% das linhas. 1–4 itens por pedido.

## 3. Reconciliações-base (referência para validar DAX)
| Medida | Valor SQL |
|---|---:|
| Receita Líquida (`fFaturamento`) | **515.283.958,96** |
| CMV | 376.561.791,51 |
| Margem Bruta / % | 138.722.167,45 / **26,9215%** |
| Impostos | 38.646.291,11 |
| Receita por ano 2024 / 2025 / 2026 (jan–out) | 178.963.796,55 / 185.241.143,72 / 151.079.018,69 |
| Pedidos / Faturas | 100.000 / 88.979 |
| Itens: valor líquido (todos os status) | 579.865.662,52 |
| Entregas / OTIF | 88.979 / 56.768 = **63,7993%** |
| Custo de frete | 23.043.925,05 |
| Devoluções | 3.159 / 4.984.803,21 |
| Despesas até 31/10/2026 / total arquivo | 71.028.404,16 / 74.791.924,78 |
| Clientes com pedido / com faturamento | 32.915 / 32.225 |
| Saldo a receber (`ValorTitulo − ValorPago`) | 45.969.639,32 (ver C4) |

Receita por filial em `a02_integridade.json`. **Soma dos itens do pedido = receita da fatura e CMV item = CMV fatura (diferença máx. 3,6e-12)** → `fItemPedido` pode explicar a receita faturada quando filtrada por pedidos faturados.

## 4. Problemas encontrados

### CRÍTICOS
| ID | Problema | Evidência | Impacto | Tratamento proposto |
|---|---|---|---|---|
| C1 | SQLite original ausente | partes `.bin` não estão na pasta | Fonte primária e SHA não verificáveis | Usar CSV; CSV reproduz contagens e órfãos do doc 08. Se as partes chegarem, comparar |
| C2 | **Fatos "realizados" com datas após o corte 31/10/2026** | fDespesa 144 (R$ 3,76 mi), fCompra 480 (227 com status *Recebido*), fEstoqueMensal 4.800, fMovimentoEstoque 1.680, fOcupacaoArmazem 840 linhas em nov–dez/2026 | Viola QA04; YTD 2026 e despesas inflados | Parâmetro `pDataCorte = 2026-10-31`; filtrar fatos realizados no Power Query com contagem de excluídos em medida `99_QA`. fMeta/fOrcamento nov–dez são planos → manter |
| C3 | **Previsão desalinhada** | fPrevisao = jan–jun/2027; calendário termina 30/04/2027; não há previsão para nov–dez/2026 | 24 órfãos; lacuna de 2 meses entre realizado e previsão; contradiz SKILL/README | Calendário gerado no PQ até 30/06/2027 (dimensão de datas determinística, não dado novo); lacuna nov–dez/2026 exibida como lacuna, nunca interpolada |
| C4 | **Contas a receber incoerentes** | Só 73.530 títulos coerentes. 7.283 com `DataPagamento` e `ValorPago = 0`; 7.451 com `ValorPago` integral e sem `DataPagamento`; 715 sem ambos; 38 pagos antes do faturamento | Inadimplência, aging e "saldo em aberto" mudam conforme a regra escolhida (diferença de ~15% dos títulos) | **Decisão necessária** (ver Plano §5). Até lá, indicadores de inadimplência ficam **BLOQUEADOS** |
| C5 | Truncamento de datas no fim da série | 31/10/2026: 397 entregas (média diária ≈ 90), 3.229 vencimentos, 3.018 pagamentos | Out/2026 distorcido em OTIF, aging e recebimento | Sinalizar mês de corte; comparar períodos fechados por padrão |
| C6 | Datas logicamente impossíveis | 8.076 entregas antes do faturamento; 7 antes do pedido; 31.784 pedidos (18.822 clientes) antes de `DataCadastro`; 14.994 pedidos e 1.894 visitas antes da admissão do vendedor; contas a pagar de compras nov–dez com vencimento (480) e pagamento (446) **antes** da compra | "Cliente novo" por `DataCadastro` é inválido; lead time de entrega por faturamento gera negativos | Cliente novo = **1ª compra**, não cadastro; lead time de entrega medido de `DataPedido`; não corrigir datas na fonte |
| C7 | Atribuição de campanha não confiável | 14.678 de 15.097 pedidos com campanha (97%) fora da vigência `Inicio–Fim`; 6.550 de 6.724 interações (97%) fora da vigência | ROI/efeito de campanha seria fictício | Campanha só como atributo do pedido; não calcular ROI nem "receita da campanha durante a vigência" sem aprovação |
| C8 | Metas não aditivas | `fMeta`: Faturamento (R$), **Margem Bruta (0,23–0,34) e OTIF (0,91–0,97) são razões** | Somar meta de margem/OTIF entre filiais ou meses é errado | Meta de razão consolidada ponderada (margem por meta de faturamento; OTIF por entregas) ou exibida só no grão filial-mês |
| C9 | Ocupação WMS com grão quebrado | 616 pares (mês, posição) duplicados com produtos e status diferentes; `StatusPosicao` independe de `Paletes` (Disponível/Bloqueada com 1–4 paletes); sem capacidade por posição; 35 de 400 posições por filial/mês | "% ocupação" sem denominador confiável | Grão = posição×produto×mês; KPI = distribuição de status na amostra; nunca ocupação da filial |

### MODERADOS
| ID | Problema | Tratamento |
|---|---|---|
| M1 | OTIF real 63,8% vs metas 91–97% | Indicador correto pela regra documentada; exibir denominador. `StatusEntrega` independe de OTIF (14.282 "Ocorrência" contam como OTIF) — não usar Status como elegibilidade. `DataEntrega` não tem nulos → "Entregas Elegíveis" = todas |
| M2 | 91% dos pedidos com `FilialID` ≠ filial do vendedor; 91% das visitas com filial cliente ≠ filial vendedor | Filial analítica = `fPedido[FilialID]` (= filial do cliente em 100%). `dVendedor[FilialID]` = "filial de lotação", só atributo |
| M3 | `PrecoUnitario` ≠ `PrecoTabela × (1 − DescontoPercentual)` em 98,9% dos itens | Desconto analisado como atributo do pedido; não reconstruir "valor de desconto" em R$ |
| M4 | `dCliente[CondicaoPagamento]` não explica vencimento (prazo médio ≈ 35 d para todas, inclusive "À vista") | Não usar condição para prazo/aging |
| M5 | `dCliente[Inativo]=1` com pedidos até 30/10/2026 (4.727) | Status cadastral ≠ comportamento; churn calculado por compras |
| M6 | `dCalendario[NomeMes]` em inglês; `DiaUtil` só exclui fins de semana (sem feriados) | Colunas PT-BR no PQ; declarar ausência de feriados |
| M7 | 375 faturas com margem negativa | Manter; exceção legítima para diagnóstico |
| M8 | `fOrcamento[Receita]` = `fMeta[Faturamento]` em 432/432 linhas | Orçamento de receita e meta são o mesmo número — não exibir como duas referências independentes |
| M9 | Ruptura = saldo zero (188 casos); 12.272 abaixo do mínimo não são ruptura | Dois KPIs distintos: Ruptura e Abaixo do Mínimo |
| M10 | 4.768 itens de produtos `Descontinuado=1` | Registrar; flag é atual, não histórica |

### INFO
`DiaSemana` 1 = segunda (ISO). `dPosicaoArmazem` = grade completa 10×10×4 por filial (X,Y,Z inteiros) — suficiente para planta 2D/3D. `dFilial` tem lat/long reais para 12 cidades, todas em Sul, Sudeste e Centro-Oeste (lat −15,8 a −30,0). Impostos ≈ 7,5% constante da receita. 13 gaps de interpretação ainda sem semântica de fonte: `MargemErroEstimada` (fração? IC?), `IndiceServico`, `Confiabilidade`, `DiasSemMovimento`, `CapacidadePaletes` vs posições (400/filial) → **pendente de validação**, sem significado atribuído.

## 5. Conformidade com a documentação
- Doc 02 e JSON: conformes.
- Doc 08 (auditoria anterior no SQLite): resultados reproduzidos nos CSV (44 PASS + 1 REVIEW).
- Doc 03, medida `Entregas Elegíveis`: inócua (sem `DataEntrega` nula).
- Doc 03, `Saldo Títulos Atual`: depende de C4.
- SKILL §6 "Executive: fDespesa" e "Calendário: fInteracaoCampanha": viáveis com C2/C7 aplicados.
