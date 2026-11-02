# QA — Decision Simulator

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Se eu mexer em preço, desconto, volume, custo, frete ou despesas, o que acontece com o resultado operacional?

## Componentes
- 6 sliders de valor único (tabelas desconectadas Sim *), padrão 0
- Botão Zerar cenário (favorito só dos sliders; mantém período e filiais)
- Resumo HTML base × simulado, margem operacional, volume de equilíbrio, premissas
- Deneb: ponte base → simulado (base e total em azul)
- Deneb: sensibilidade preço × volume (−10% a +10%)

## Medidas criadas/usadas
- `Sim Valor Etapa`
- `Sim Δ Resultado (grade)`
- `UX Simulador Resumo`
- `UX Simulador Aviso`

## Interações e validações
- Cenário +3% preço, +1 p.p. desconto, −5% volume, +2% custo, +10% frete, −5% despesas: DAX = Python (resultado 10.705.062,76 → 10.115.641,29; efeitos fecham; volume de equilíbrio −3,25%; célula da grade +4%/−6% = 477.912,64)
- Zerar cenário: OK
- Simulação indisponível com filtro de produto (frete e despesas sem produto)

## Performance (Performance Analyzer)
Máximo 215 ms.

## Problemas e correções
- Variáveis _d0 e _D0 colidem (DAX não diferencia maiúsculas) → renomeado
- Slider exibia o mínimo → numericStart 0
- Cascata nativa pintava a base de verde → Deneb

## Pendências
- Sem elasticidade preço × volume (premissa declarada)

## Rodada 2 (02/11/2026 17:30) — sliders
- Causa: ao arrastar, o slider de valor único gerava um valor que não existe na série (a coluna não era um parâmetro What-if); o filtro não casava com nenhuma linha e `SELECTEDVALUE` devolvia o padrão 0. Digitar o valor exato funcionava, arrastar não.
- Correção: `extendedProperty ParameterMetadata` nas 6 colunas `Sim *`; desconto em passos de 1 p.p.; sliders com 114 px de altura (com fontes maiores o controle sumia em 104 px).
- Teste por arraste no Desktop: preço +5% e volume −4% → resultado 10.705 mil → 16.605 mil (preço +7.554 mil = 5% de 151.079 mil; volume −1.654 mil = −4% × 41.344 mil); desconto +1 p.p. → −1.729 mil. "Zerar cenário" volta tudo a 0.
