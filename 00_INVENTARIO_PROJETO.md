# 00 — Inventário do projeto NEXUS 360

**Data da inspeção:** 01/11/2026 · **Raiz:** `E:\Projetos BI\18 - Nexus 360` · **Método:** shell Linux montado sobre a pasta (via app Claude Desktop) + MCP `powerbi-modeling-mcp`.

## 1. Estrutura encontrada (estado original, preservado)

| Arquivo | Tamanho | Observação |
|---|---:|---|
| `SKILL_NEXUS360_POWERBI(1).md` | 16 KB | Skill mestra. Nome com sufixo `(1)` — prompts referenciam `SKILL_NEXUS360_POWERBI.md` |
| `documentacao_tecnica/01..08_*.md` + `INDICE.md` | 73 KB | Os 8 documentos técnicos — **presentes** |
| `NEXUS360_DOCUMENTACAO_TECNICA_01_A_08.zip` | 21 KB | Cópia compactada dos mesmos 9 MDs |
| `NEXUS360_CSV_PARTE_01..04.zip` | 14,4 MB | 26 CSV + `DICIONARIO_DADOS.json` + `RELACIONAMENTOS.csv` + `README.md` |
| `NEXUS360_DESIGN_SYSTEM_COMPLETO.pdf` | 7,7 MB | 11 págs, 960×540 — tokens, tipografia, layout, componentes, QA |
| `NEXUS360_Manual_Identidade_Visual.pdf` | 3,3 MB | 6 págs A4 — marca, paleta base, tipografia |
| `Inteligência de Dados em Movimento.png` | 1672×941 | **Fundo da Home** (logo, headline, botão INICIAR e mapa do Brasil desenhados na imagem) |
| `Dashboard NEXUS 360 em Neon fundo.png` | 1672×941 | **Fundo analítico comum** (slot de título, barra de filtros, botões Filtro/Info/Home desenhados) |
| `Logo.png` | 2172×724 | Logo raster oficial |
| `RECONSTRUIR_BANCO_WINDOWS.bat` | 116 B | Concatena `NEXUS360_DB_PARTE_*.bin` → `NEXUS360.db` |

### Ausentes
| Item | Impacto |
|---|---|
| `NEXUS360_DB_PARTE_*.bin` (partes do SQLite) | **Banco `NEXUS360.db` não pode ser reconstruído.** SHA256 original (`fab35e95…10c0a`) não verificável. Fonte adotada: CSV (Opção 2 da descrição do projeto) |
| Wireframes em imagem | Só existem wireframes ASCII genéricos no doc 04 (mesmo template repetido nas 11 telas) |
| Imagens de fundo por página | Existe **um** fundo analítico para as 10 páginas, não um por página |
| PBIP / PBIX | Nenhum existente — projeto parte do zero |
| Tema JSON, specs Deneb, componentes HTML | Nenhum existente (o doc 07 marca como PROPOSTA) |

## 2. Estrutura criada nesta etapa (sem mover nem alterar originais)

```text
18 - Nexus 360/
  00_INVENTARIO_PROJETO.md · 00_AUDITORIA_DADOS.md · 00_PLANO_IMPLEMENTACAO.md · 00_STATUS_DESENVOLVIMENTO.md
  dados/NEXUS360/                  # extração dos 4 ZIPs (csv/, DICIONARIO_DADOS.json, RELACIONAMENTOS.csv, README.md)
  dados/sqlite_auditoria/NEXUS360_auditoria_csv.db   # SQLite reconstruído A PARTIR DOS CSV (não é o .db original)
  assets/img/                      # cópias com nomes ASCII: bg_home_1672x941.png, bg_analitico_1672x941.png, logo_nexus360_2172x724.png
  assets/icones/ · tema/ · specs_deneb/ · componentes_html/ · pbip/
  testes/scripts/                  # a01_carga_perfil.py, a02_integridade.py (reprodutíveis)
  testes/resultados/               # a01_perfil.json, a02_integridade.json
  testes/sql/ · testes/screenshots/ · logs/ · apps/wms3d/ · apps/agente_bi/ · backups/
  _to_delete/                      # 2 arquivos de uma tentativa falha de SQLite direto no disco montado (lock I/O) — pode apagar
```
SHA256 do SQLite de auditoria: `2c43abff3bd529e21ad011c6528655b55d58168fe5e5f46b8e8ee68e3e772a92`. SHA256 de cada CSV em `testes/resultados/a01_perfil.json`.

## 3. Ferramentas

| Ferramenta | Status | Evidência |
|---|---|---|
| Power BI Desktop | **Não verificado** | Não visível pelo shell; `ListLocalInstances` = 0 instâncias abertas. Versão e preview features PBIR/TMDL a confirmar |
| `powerbi-modeling-mcp` (local) | **Disponível** | Servidor anunciado; responde. Permite criar tabelas/medidas/relações e executar DAX contra o Desktop aberto |
| DAX Studio / Tabular Editor / Measure Killer / PBI Helper | **Não verificado** | Sem acesso a `Program Files` pelo shell |
| Python 3.10 + sqlite3 | Disponível | Na VM Linux do shell (não no Windows) |
| `pdftotext` / `unzip` | Disponível | VM Linux |
| Node.js / npx no Windows | **Ausente do PATH** | Playwright MCP falha com "npx não é reconhecido" → `pbiviz` (visual custom 3D) indisponível sem instalar Node |
| VS Code | Indício (`.vscode` no perfil) | Não verificado |
| Visuais custom (HTML Content, Deneb) | **Não verificado** | Precisam estar no relatório; confirmar no Desktop |

## 4. Identidade visual consolidada (fonte: PDFs)
Base (manual = design system): navy `#071528`, deep blue `#0A1C33`, teal `#10D4C4`, blue `#0878C9`, white `#FFFFFF`, muted `#A9B9CA`.  
Semânticas: **Design System** `#45D5A1` / `#FF7285` / `#FFC66D` **≠** SKILL `#22B89A` / `#E76F75` / `#F2B84B`. Adotar Design System (fonte visual mais específica); validar contraste. Tipografia Inter/Segoe UI; títulos de página 28–34 px, componentes 18–22 px, texto ≥ 11 px; grid 8 px; raio 8–12 px (SKILL diz 14 px).

## 5. Conflitos entre documentos (registrados, não resolvidos silenciosamente)
| Tema | Fonte A | Fonte B | Proposta |
|---|---|---|---|
| Canvas | Master prompt: 1920×1080 | Doc 04: 1600×900 · imagens: 1672×941 | 1920×1080 com fundo escalado 1,148× (perda leve de nitidez) — confirmar |
| Navegação | Doc 04: sidebar 76 px | Fundo analítico não tem área de menu | Navegador de páginas em painel recolhível (bookmark), não sidebar fixa |
| Cores semânticas | SKILL | Design System | Design System |
| Raio | SKILL 14 px | Design System 8–12 px | 12 px |
| Horizonte da previsão | SKILL/README: até 30/04/2027, “6 meses” | Dados: jan–jun/2027 | Ver auditoria (C3) |
