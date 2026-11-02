# AI Decision Assistant — especificação de integração

**Estado em 02/11/2026:** interface demonstrativa no PBIP (página `AI Decision Assistant`). **Nenhum modelo de linguagem está conectado.**

| Componente | Estado | Evidência |
|---|---|---|
| Catálogo de 8 ferramentas tipadas (JSON Schema) | Implementado | `CATALOGO_FERRAMENTAS.json` |
| Consultas DAX parametrizadas, somente leitura | Implementado e testado | `CONSULTAS_DAX.dax`; os 8 exemplos de `EXEMPLOS_RENDERIZADOS.dax` foram executados no modelo aberto no Desktop |
| Página com resultados ao vivo das ferramentas | Implementado e testado | `testes/resultados/QA_PAGINA_ASSISTANT.md` |
| Orquestrador LLM (tool use) | Pendente | — |
| Autenticação Entra ID + RLS | Pendente | — |
| Endpoint de consulta (Power BI REST `executeQueries` ou XMLA) | Pendente | exige publicação no Service/Fabric |

Gerado por `pbip/_gerador/assistente_catalogo.py` (fonte única dos schemas e das consultas).

## Fluxo
1. Usuário pergunta em linguagem natural.
2. O orquestrador envia ao LLM a pergunta e o `CATALOGO_FERRAMENTAS.json` como ferramentas.
3. O LLM devolve chamadas de ferramenta com parâmetros. **Nunca DAX.**
4. O servidor valida os parâmetros contra o schema (enum de filiais e métricas, faixas de datas, `top_n ≤ 20`), preenche o modelo de `CONSULTAS_DAX.dax` e executa com a identidade do usuário.
5. Linhas retornadas voltam ao LLM, que redige a resposta citando ferramenta e filtros de cada número. Sem linhas, a resposta é "sem dados".

## Ferramentas
`resumo_executivo`, `ranking_filiais`, `clientes_em_risco`, `desempenho_vendedores`, `otif_transportadoras`, `dre_gerencial`, `projecao_receita`, `simular_cenario`.

## Controles de segurança
- Sem DAX livre; modelos fixos com placeholders preenchidos somente após validação de schema.
- Allowlist de medidas (`ranking_filiais.metrica` é enum) e de colunas.
- Período limitado a 01/01/2024–31/10/2026; `top_n` ≤ 20; tempo máximo de consulta e limite de linhas no endpoint.
- Identidade do usuário propagada (Entra ID) para aplicar RLS (ainda não há papéis RLS no modelo: criar antes de publicar).
- Credencial somente leitura; trilha de auditoria por chamada (usuário, ferramenta, parâmetros, duração, linhas).
- Texto vindo do usuário nunca é concatenado ao DAX; nomes de filial só entram via enum.

## Dependências para concluir
1. Publicar o modelo em workspace com XMLA ou habilitar `executeQueries` (tenant setting "Dataset Execute Queries REST API").
2. Registrar app no Entra ID com permissão `Dataset.Read.All` e fluxo on-behalf-of.
3. Backend (ex.: Azure Function) com validador de JSON Schema, renderizador de consultas e chamada ao LLM com tool use.
4. Definir papéis RLS (por filial/região) e testar com "Exibir como".
5. Incorporar o chat ao relatório (visual de terceiros ou app incorporado) — não há execução de JavaScript no HTML Content.
