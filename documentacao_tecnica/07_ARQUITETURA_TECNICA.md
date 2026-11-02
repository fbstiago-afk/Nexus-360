# 07 — Arquitetura técnica e integrações

**Projeto:** NEXUS 360 | **Fonte verificada:** `NEXUS360.db`, `RELACIONAMENTOS.csv`, `README.md` | **Corte da extração:** 01/11/2026 | **Estado:** especificação para implementação, não PBIP implementado.

> **Regra de evidência:** nomes de tabelas/colunas são os encontrados no SQLite. Propostas novas são marcadas `PROPOSTA`, e relações do CSV são `CANDIDATAS`, não comprovadas como relacionamentos ativos.

## Camadas
```text
SQLite NEXUS360.db / CSVs
    -> Power Query (tipagem, validação, enriquecimento controlado)
    -> Modelo semântico PBIP / TMDL (dimensões, fatos, medidas)
    -> Power BI Report (11 telas, HTML Content, Deneb, Azure Maps)
    -> OPCIONAL: Fabric App / Three.js e agente BI com DAX tipado
```

## Fontes confirmadas
- `NEXUS360.db`: 26 tabelas, esquema auditável por SQLite.
- `csv/`: uma exportação por tabela, UTF-8 BOM e vírgula.
- `RELACIONAMENTOS.csv`: 45 relações **candidatas**; não são relações já aplicadas.
- `DICIONARIO_DADOS.json`: referência suplementar, mas schema real prevalece.
- `README.md`: limitações de grão, integridade e datas.
- `SKILL_NEXUS360_POWERBI.md` e manual visual: padrões de projeto.

## Estrutura proposta de projeto
```text
NEXUS360/
  dados/                    # db, csv, contrato de fontes
  documentacao/             # os 8 MDs e resultados QA
  assets/                   # logo, fundos, ícones licenciados
  tema/NEXUS360_THEME.json  # PROPOSTA, ainda não criado
  specs_deneb/              # specs versionadas
  componentes_html/         # modelos CSS/SVG
  pbip/                     # arquivos gerados pelo Power BI Desktop
  testes/                   # SQL, DAX, screenshots e benchmarks
```

## Power Query
1. Parametrizar raiz do projeto e caminho de `NEXUS360.db`; evitar caminhos absolutos hardcoded.
2. Importar por SQLite ou CSV; padronizar tipos explicitamente (datas ISO, inteiros e decimais).
3. Separar staging de dimensões/fatos, desabilitar carregamento de consultas intermediárias.
4. Criar `dPedido` apenas se a arquitetura selecionada exigir; verificar unicidade de `PedidoID`.
5. Tratar nulos e datas posteriores ao corte sem apagar registros; manter colunas brutas para auditoria.
6. Não presumir query folding em CSV/SQLite; medir tempo real de refresh.

## Modelo e segurança
- Uma única direção de filtro de dimensão para fato; evitar relações fato-fato e caminhos duplicados.
- Datas de papéis alternativos via relações inativas ou dimensões role-playing.
- Sem PII real: base sintética. Mesmo assim, configurar RLS por filial apenas se houver requisito explícito, com testes de não vazamento.
- Versionar TMDL, specs e medidas; nunca armazenar tokens no PBIP.

## Integrações avançadas
- **HTML Content:** componentes de apresentação; sem JavaScript arbitrário ou chamadas externas presumidas.
- **Deneb:** Vega-Lite dentro do visual certificado/permitido no ambiente.
- **WMS 3D:** aplicação separada (Three.js/Fabric Apps) com filtros e integração autenticada; fallback 2D no relatório.
- **Agentic BI:** serviço separado, catálogo de ferramentas tipadas, allowlist de medidas e dimensões, autenticação, limites de consulta e trilha de auditoria. Não afirmar MCP ou agente nativamente disponíveis sem validação do ambiente.
- **Mapas:** `dFilial[Latitude]`, `dFilial[Longitude]`; não inventar coordenadas de clientes/entregas.

## Entregáveis de engenharia
PBIP que abre no Power BI Desktop; tema; catálogo DAX; parâmetros de fontes; specs visuais; evidências QA; roteiro de publicação; lista de dependências de visuais; documento de limitações.
