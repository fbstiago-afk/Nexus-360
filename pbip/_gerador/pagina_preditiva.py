# NEXUS 360 - Etapa G: Predictive Intelligence (PBIR)
# Pergunta: para onde a receita caminha, com que incerteza, e onde a meta fica em risco?
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_pbir import (Pagina, register_page, s, lit, num, color, meas, col, proj, title, cat_filter, COR, deneb)

RAIZ = sys.argv[1]
DEF = os.path.join(RAIZ, 'pbip', 'NEXUS360.Report', 'definition')
PG = 'pgPredictive'
# sem slicers de periodo: a pagina sempre mostra o historico completo e o horizonte futuro
SL = [('nxSlRegiao', 'dFilial', 'Regiao', 'Região', 'Basic', False, None, 120, False),
      ('nxSlFilial', 'dFilial', 'Filial', 'Filial', 'Basic', False, None, 300, False),
      ('nxSlCategoria', 'dProduto', 'Categoria', 'Categoria (projeção e sazonalidade)', 'Dropdown', False, None, 90, False)]

p = Pagina(PG, 'Predictive Intelligence')
p.chrome(slicers=SL)
p.html('nxPredResumo', 46, 212, 1828, 112, 'UX Preditiva Resumo')

# Linha do tempo: realizado, meta, projecao com faixa de 90% e previsao da fonte
TL = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"calculate": "toDate(datum['InicioMes'])", "as": "dt"}],
    "encoding": {"x": {"field": "dt", "type": "temporal", "title": None,
                       "axis": {"format": "%b/%y", "labelAngle": 0, "tickCount": {"interval": "month", "step": 3}, "grid": False}}},
    "layer": [
        {"mark": {"type": "area", "color": "#10D4C4", "opacity": 0.16},
         "encoding": {"y": {"field": "Projeção Limite Inferior 90%", "type": "quantitative"}, "y2": {"field": "Projeção Limite Superior 90%"}}},
        {"transform": [{"fold": ["Receita Líquida", "Meta Faturamento", "Projeção Sazonal Receita", "Receita Prevista"], "as": ["serie", "valor"]},
                       {"filter": "isValid(datum.valor) && datum.valor > 0"},
                       {"calculate": "{'Receita Líquida': 'Realizado', 'Meta Faturamento': 'Meta', 'Projeção Sazonal Receita': 'Projeção sazonal (90%)', 'Receita Prevista': 'Previsão da fonte'}[datum.serie]", "as": "Série"}],
         "mark": {"type": "line", "strokeWidth": 2, "point": {"size": 18, "filled": True}},
         "encoding": {
             "y": {"field": "valor", "type": "quantitative", "title": None, "scale": {"zero": False},
                   "axis": {"labelExpr": "pbiFormat(datum.value / 1000000, '#,0') + ' mi'", "grid": True, "tickCount": 5}},
             "color": {"field": "Série", "type": "nominal",
                       "scale": {"domain": ["Realizado", "Meta", "Projeção sazonal (90%)", "Previsão da fonte"], "range": ["#10D4C4", "#FFC66D", "#7FE6DD", "#5FA8E6"]}},
             "strokeDash": {"field": "Série", "type": "nominal",
                            "scale": {"domain": ["Realizado", "Meta", "Projeção sazonal (90%)", "Previsão da fonte"], "range": [[1, 0], [5, 4], [2, 3], [7, 3]]}},
             "tooltip": [{"field": "dt", "type": "temporal", "title": "Mês", "format": "%m/%Y"}, {"field": "Série"},
                         {"field": "valor", "title": "R$", "formatType": "pbiFormat", "format": "R$ #,0"}]}},
        {"mark": {"type": "rule", "color": "#A9B9CA", "strokeDash": [2, 2]},
         "encoding": {"x": {"aggregate": "max", "field": "dt", "type": "temporal"}},
         "transform": [{"filter": "isValid(datum['Receita Líquida']) && datum['Receita Líquida'] > 0"}]}]}
deneb(p, 'nxLinhaTempo', 46, 340, 1270, 430,
      [col('dCalendario', 'InicioMes'), meas('Receita Líquida'), meas('Meta Faturamento'), meas('Projeção Sazonal Receita'),
       meas('Projeção Limite Inferior 90%'), meas('Projeção Limite Superior 90%'), meas('Receita Prevista')],
      TL, 'Receita mensal: realizado, meta, projeção sazonal com faixa de 90% e previsão da fonte (linha vertical = corte)')

# Sazonalidade (indice mensal por ano)
SZ = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Receita Líquida'] > 0"},
                  {"joinaggregate": [{"op": "mean", "field": "Receita Líquida", "as": "media"}], "groupby": ["Ano"]},
                  {"calculate": "100 * datum['Receita Líquida'] / datum.media", "as": "ix"}],
    "encoding": {"x": {"field": "MesAbrev", "type": "ordinal", "sort": {"field": "Mes"}, "title": None, "axis": {"labelAngle": 0, "orient": "top"}},
                 "y": {"field": "Ano", "type": "ordinal", "title": None}},
    "layer": [
        {"mark": {"type": "rect", "cornerRadius": 3, "stroke": "#071528", "strokeWidth": 2},
         "encoding": {"color": {"field": "ix", "type": "quantitative", "title": "Índice",
                                "scale": {"domainMid": 100, "range": ["#FF7285", "#12304F", "#10D4C4"], "domain": [88, 112]},
                                "legend": {"orient": "bottom", "direction": "horizontal", "format": ".0f", "gradientLength": 180}},
                      "tooltip": [{"field": "Ano"}, {"field": "MesAbrev", "title": "Mês"},
                                  {"field": "ix", "title": "Índice (100 = média do ano)", "formatType": "pbiFormat", "format": "0"},
                                  {"field": "Receita Líquida", "title": "Receita", "formatType": "pbiFormat", "format": "R$ #,0"}]}},
        {"mark": {"type": "text", "fontSize": 10, "color": "#FFFFFF"},
         "encoding": {"text": {"field": "ix", "formatType": "pbiFormat", "format": "0"}}}]}
deneb(p, 'nxSazonal', 1332, 340, 542, 430,
      [col('dCalendario', 'Ano'), col('dCalendario', 'MesAbrev'), col('dCalendario', 'Mes'), meas('Receita Líquida')],
      SZ, 'Sazonalidade (100 = média do ano)')
p.vis['nxSazonal']['filterConfig'] = {'filters': [cat_filter('fRealizado', 'dCalendario', 'FlagRealizado', ['1L'])]}

# Risco: projecao nov-dez vs meta por filial (bullet, Deneb)
RK = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Meta Faturamento'] > 0 && isValid(datum['Projeção Sazonal Receita'])"},
                  {"calculate": "datum['Projeção Sazonal Receita'] / datum['Meta Faturamento'] - 1", "as": "gap"},
                  {"calculate": "datum.gap >= 0 ? 'Projeção atinge a meta' : 'Projeção abaixo da meta'", "as": "sit"}],
    "encoding": {"y": {"field": "Cidade", "type": "nominal", "sort": {"field": "gap", "op": "max", "order": "ascending"}, "title": None,
                       "axis": {"labelFontSize": 10, "labelColor": "#C9D6E3"}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadiusEnd": 2, "height": {"band": 0.6}},
         "encoding": {"x": {"field": "gap", "type": "quantitative", "title": None, "axis": {"format": "+.0%", "grid": True, "tickCount": 5}},
                      "color": {"field": "sit", "type": "nominal", "scale": {"domain": ["Projeção atinge a meta", "Projeção abaixo da meta"], "range": ["#45D5A1", "#FF7285"]}},
                      "tooltip": [{"field": "Cidade", "title": "Filial"}, {"field": "Projeção Sazonal Receita", "title": "Projeção", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "Meta Faturamento", "title": "Meta", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "gap", "title": "Diferença", "formatType": "pbiFormat", "format": "+0.0%;-0.0%"}]}},
        {"mark": {"type": "rule", "color": "#A9B9CA"}, "encoding": {"x": {"datum": 0}}}]}
deneb(p, 'nxRiscoMeta', 46, 786, 900, 270,
      [col('dFilial', 'Cidade'), meas('Projeção Sazonal Receita'), meas('Meta Faturamento')], RK,
      'Risco à meta de nov–dez/2026: projeção sazonal vs meta por filial')
p.vis['nxRiscoMeta']['filterConfig'] = {'filters': [cat_filter('fNovDez', 'dCalendario', 'AnoMes', ['202611L', '202612L'])]}

# Previsao da fonte 1o sem/2027 vs mesmo periodo de 2026, por filial
PV = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json", "data": {"name": "dataset"}, "width": "container", "height": "container",
    "transform": [{"filter": "datum['Receita Base Ano Anterior'] > 0 && isValid(datum['Receita Prevista'])"},
                  {"calculate": "datum['Receita Prevista'] / datum['Receita Base Ano Anterior'] - 1", "as": "cres"},
                  {"calculate": "datum.cres >= 0 ? 'Crescimento' : 'Queda'", "as": "sit"}],
    "encoding": {"y": {"field": "Cidade", "type": "nominal", "sort": {"field": "cres", "op": "max", "order": "descending"}, "title": None,
                       "axis": {"labelFontSize": 10, "labelColor": "#C9D6E3"}}},
    "layer": [
        {"mark": {"type": "bar", "cornerRadiusEnd": 2, "height": {"band": 0.6}},
         "encoding": {"x": {"field": "cres", "type": "quantitative", "title": None, "axis": {"format": "+.0%", "grid": True, "tickCount": 5}},
                      "color": {"field": "sit", "type": "nominal", "scale": {"domain": ["Crescimento", "Queda"], "range": ["#5FA8E6", "#FFC66D"]}},
                      "tooltip": [{"field": "Cidade", "title": "Filial"}, {"field": "Receita Prevista", "title": "Previsão 1º sem/27", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "Receita Base Ano Anterior", "title": "Realizado 1º sem/26", "formatType": "pbiFormat", "format": "R$ #,0"},
                                  {"field": "cres", "title": "Variação", "formatType": "pbiFormat", "format": "+0.0%;-0.0%"}]}},
        {"mark": {"type": "rule", "color": "#A9B9CA"}, "encoding": {"x": {"datum": 0}}}]}
deneb(p, 'nxPrevFilial', 962, 786, 912, 270,
      [col('dFilial', 'Cidade'), meas('Receita Prevista'), meas('Receita Base Ano Anterior')], PV,
      'Previsão da fonte para o 1º sem/2027 vs realizado do 1º sem/2026, por filial')
p.vis['nxPrevFilial']['filterConfig'] = {'filters': [cat_filter('f2027', 'dCalendario', 'Ano', ['2027L'])]}
p.write(DEF, overwrite=True)
register_page(DEF, PG, ['pgHome', 'pgExecutive', 'pgCommercial', 'pgCustomer', 'pgLogistics', 'pgWarehouse', 'pgFinancial', 'pgPredictive',
                        '2a6aff4ae45b2ec75c15', 'ttVendedor', 'ttCliente', 'ttTransportadora', 'ttMesFinanceiro', 'ttEstoqueMes'])
print('predictive ok', len(p.vis), 'visuais;', len(p.bookmarks), 'favoritos')
