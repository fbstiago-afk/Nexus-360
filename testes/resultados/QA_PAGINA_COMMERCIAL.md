# QA — Commercial Intelligence

Ambiente: Power BI Desktop 2.159 (out/2026), PBIP TMDL+PBIR, canvas 1920×1080, filtro padrão 2026 (jan–out). Testes executados em 02/11/2026.

**Pergunta de negócio:** Quem vende mais, com qual mix e a que custo de desconto?

## Componentes
- KPIs HTML (receita, margem, desconto, positivados vs LY)
- Top 12 vendedores (barras, cor = margem vs média) com tooltip ttVendedor
- Deneb: dispersão desconto × margem com quadrantes (Q3 / mediana)
- Deneb: dumbbell de marcas vs ano anterior
- Matriz de mix Categoria>Subcategoria com barra SVG de participação
- Card de oportunidades (diagnóstico)

## Medidas criadas/usadas
- `UX Comercial KPIs`
- `UX Cor Margem vs Média`
- `UX Barra Participação`
- `UX Comercial Oportunidades`
- `UX Tooltip Vendedor`

## Interações e validações
- Tooltip de vendedor: OK
- Filtros sincronizados com a Executive: OK

## Performance (Performance Analyzer)
Máximo 274 ms por visual.

## Problemas e correções
- Receita por fornecedor não atribuível (registrado como limitação)

## Pendências
- Meta por vendedor/produto inexistente na fonte
