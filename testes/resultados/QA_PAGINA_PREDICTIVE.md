# QA — Predictive Intelligence

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Para onde a receita caminha, com que incerteza, e onde a meta fica em risco?

## Componentes
- Resumo HTML
- Deneb: linha do tempo (realizado, meta, projeção sazonal com faixa 90%, previsão da fonte, corte)
- Deneb: heatmap de sazonalidade
- Deneb: risco à meta nov–dez por filial
- Deneb: previsão 1º sem/27 vs 1º sem/26

## Medidas criadas/usadas
- `Fator Tendência 12M`
- `Projeção Sazonal Receita`
- `Projeção Erro σ (backtest)`
- `Projeção MAPE (backtest)`
- `Projeção Limite Inferior/Superior 90%`
- `Receita Base Ano Anterior`
- `UX Preditiva Resumo`

## Interações e validações
- DAX = Python: σ 0,0382748 (0,038275), MAPE 0,0310038 (0,031004), 10 meses, fator 0,986439, projeção nov/26 15.027.381,54
- Mês de vale = fevereiro após correção
- Legenda da linha do tempo visível

## Performance (Performance Analyzer)
Não remedido após a correção (medição anterior dentro da meta).

## Problemas e correções
- Janelas EDATE de fim de mês erravam em ano bissexto → janelas por início de mês
- Linha em branco do calendário zerava o vale → filtro NOT ISBLANK
- Legenda sumia (strokeDash com legend null mesclado à cor) → legenda única

## Pendências
- Backtest curto (10 meses): faixa indicativa
