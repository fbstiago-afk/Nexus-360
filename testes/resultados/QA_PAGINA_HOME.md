# QA — Home

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Porta de entrada: marca, histórico e acesso às análises.

## Componentes
- Fundo oficial `bg_home_1920x1080.jpg`
- nxHomeMapa: SVG independente com as 12 filiais reais (Natural Earth, projeção documentada), pulsação CSS, legenda por região
- nxHomeKPIs: receita, margem, clientes ativos, entregas, filiais (medidas reais, histórico completo)
- nxIniciar: área transparente sobre o botão desenhado → Executive
- 4 atalhos (Comercial, Clientes, Logística, Financeiro) conforme doc 04

## Medidas criadas/usadas
- `UX Home Mapa`
- `UX Home KPIs`

## Interações e validações
- INICIAR → Executive (Ctrl+clique no Desktop): OK
- Atalho Clientes → Customer Intelligence: OK
- Pontos ilustrativos do fundo cobertos pelo mapa real (D4)

## Performance (Performance Analyzer)
Não medido nesta rodada (2 visuais HTML).

## Problemas e correções
- `<title>` do SVG gerava tooltip vazio → removido; detalhe por filial está na lista lateral do mapa
- Cartão do mapa cortado → altura 566 e 100vh

## Pendências
- Cantos arredondados dos atalhos não aplicados pelo Desktop (botões retangulares); ajuste cosmético
