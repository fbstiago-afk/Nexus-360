# NEXUS 360 — Lições da página-modelo para as demais páginas

Fonte: testes da Executive Command Center em 01/11/2026 (`testes/resultados/QA_PAGINA_EXECUTIVE.md`).

## Padrões validados (reaproveitar)
1. **Gerador por script.** Cada página sai de um script Python que escreve o PBIR (`pbip/_gerador/gerar_pagina_executive.py` + `finalizar_pagina_executive.py` + `ajustes_pos_teste_1.py`). Antes da próxima página, consolidar os três num módulo único de componentes (cabeçalho, barra, card, painel, botão, slicer).
2. **Posições de filhos de grupo são relativas ao grupo.**
3. **Favoritos de painel:** só exibição (`suppressData: true`), sem `preserveNewVisualVisibility`, com `visualContainers` vazio. Um favorito "Padrão" fecha todos os painéis da página.
4. **Botões com texto:** além da entrada do estado `default`, incluir `text` com `show: true` sem seletor.
5. **Slicers de período:** filtro de visual `FlagRealizado = 1`.
6. **Componentes HTML** custam 200–390 ms cada. Limite prático: **até 7 visuais HTML por página**. A matriz com cor condicional ficou em 404 ms; cor baseada em medida de churn custaria cerca de 8 s e foi descartada.
7. **Transparência do tema em 8%** mantém o fundo visível nas margens sem vazar a imagem sob os dados.
8. **Ctrl+clique** é necessário para testar botões no modo de edição do Desktop.

## Corrigir antes de replicar
| Prioridade | Item | Ação proposta |
|---|---|---|
| P1 | Tooltip de página não aciona | Criar uma página de tooltip pelo Desktop, salvar e comparar o JSON gerado com o atual (mesma técnica que resolveu o botão). Se o HTML Content não renderizar dentro de tooltip, usar cards nativos na página de tooltip |
| P1 | Home sem destino | A Home é a próxima página a construir. Depois, ligar `nxBtnHome` (ação Navegação de página) |
| P2 | Matriz com rolagem | Ajustar a altura da faixa inferior ou reduzir `rowPadding` para caber as 12 filiais |
| P2 | Rótulos da cascata inclinados | Agrupar despesas menores em "Outras despesas" (é preciso medida/linha nova em `dLinhaDRE`, mudança de modelo que exige aprovação) ou aumentar a largura |
| P2 | Menu lateral fixo do wireframe | Decidir se vale manter o painel recolhível (escolha atual) ou o menu fixo do doc 04 |
| P3 | Linhas do combo suavizadas | Definir interpolação linear no visual |
| P3 | Traço de 4 px nos títulos dos painéis | Trocar a caixa de texto do título por HTML ou ajustar o tamanho |

## Por página (o que a página-modelo antecipa)
- **Commercial / Customer:** a receita agora reage a produto, categoria e marca. Medidas sem produto (frete, impostos, metas, devolução) ficam em branco com filtro de produto e a barra de filtros mostra o aviso. Não colocar essas medidas ao lado de recortes por produto.
- **Customer:** a evolução mensal dos 5 status leva 2,8 s. Limitar a 12–24 meses ou materializar a última compra por cliente-mês antes de usar com segmentações.
- **Logistics:** OTIF de out/2026 está distorcido pelas datas truncadas (C5). Mostrar a ressalva no painel de informações.
- **Warehouse:** estoque e WMS são amostrais (C9). A ocupação não é a capacidade real.
- **Decision Simulator / AI Assistant:** seguem a decisão de não simular integrações (sem Fabric verificado).
