# QA — AI Decision Assistant

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Como responder perguntas de negócio em linguagem natural sem perder a rastreabilidade?

## Componentes
- Faixa de status (implementado / testado / pendente)
- Fluxo pergunta → ferramentas → resultados DAX ao vivo (sem resposta de IA)
- Catálogo de 8 ferramentas tipadas com resultado atual
- Arquitetura e controles de segurança

## Medidas criadas/usadas
- `UX Assistente Status`
- `UX Assistente Fluxo`
- `UX Assistente Ferramentas`
- `UX Assistente Arquitetura`

## Interações e validações
- 8 consultas de apps/ai_assistant executadas no modelo (EXEMPLOS_RENDERIZADOS.dax)
- Valores coerentes com as demais páginas: receita 151,1 mi, meta 152,6 mi, BH 93,4%

## Performance (Performance Analyzer)
Máximo 138 ms.

## Problemas e correções
- IF não retorna tabela → expressão de filiais montada pelo orquestrador
- VAR antes de EVALUATE exige DEFINE

## Pendências
- Orquestrador LLM, Entra ID/RLS e endpoint executeQueries não implementados: funcionalidade NÃO concluída
