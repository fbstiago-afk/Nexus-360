# NEXUS 360 - Medidas de apresentacao da Home (mapa SVG das filiais reais e faixa de indicadores)
# Contorno: Natural Earth (world-atlas 2.0.2, ISC), equiretangular com cos(-14 graus) = 0.970296, K = 12, origem (-74.2, 5.6).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nx_medidas import upsert
BR = "M85 53 L91 58 L99 55 L102 59 L106 54 L116 49 L119 44 L125 41 L126 38 L118 37 L116 24 L110 16 L112 18 L117 18 L119 20 L126 20 L132 24 L134 19 L137 18 L140 18 L147 16 L150 13 L154 13 L158 8 L157 5 L158 5 L164 4 L165 6 L164 13 L169 15 L168 16 L171 20 L167 24 L165 35 L168 40 L169 46 L179 53 L183 52 L185 48 L188 49 L189 47 L193 47 L199 43 L202 45 L212 45 L213 43 L210 40 L212 37 L215 38 L224 36 L228 39 L234 42 L238 39 L241 40 L243 39 L244 41 L247 41 L251 38 L255 29 L265 15 L268 18 L273 42 L276 45 L282 47 L283 53 L273 65 L267 68 L259 84 L251 86 L259 86 L271 78 L274 88 L277 91 L282 89 L285 90 L290 88 L286 99 L288 97 L291 90 L294 89 L297 85 L300 87 L301 85 L300 84 L300 81 L304 76 L310 75 L312 76 L312 75 L314 75 L335 83 L336 88 L339 85 L343 88 L343 89 L344 88 L345 92 L343 94 L344 96 L347 93 L347 96 L345 98 L343 106 L347 103 L349 97 L350 97 L349 101 L352 98 L358 97 L359 96 L372 101 L376 100 L381 102 L393 101 L399 102 L416 112 L421 118 L426 122 L430 124 L431 126 L438 128 L450 129 L454 134 L459 155 L457 168 L455 174 L449 182 L446 183 L446 185 L440 193 L434 197 L429 204 L429 202 L425 212 L419 221 L416 223 L413 219 L412 221 L413 222 L409 230 L410 231 L409 236 L411 236 L409 243 L411 258 L407 273 L408 280 L402 286 L401 302 L398 304 L394 314 L389 318 L387 322 L387 331 L378 335 L375 338 L374 343 L364 343 L361 340 L361 343 L353 344 L355 343 L353 342 L344 344 L344 346 L345 346 L336 350 L335 353 L329 353 L318 358 L305 368 L306 369 L303 372 L303 371 L300 370 L300 373 L297 372 L297 373 L300 374 L297 377 L298 381 L296 382 L299 394 L298 404 L296 410 L285 420 L278 432 L271 442 L258 453 L258 449 L262 449 L267 445 L268 441 L270 440 L271 438 L274 436 L273 432 L275 432 L275 430 L270 432 L267 428 L268 432 L267 436 L266 435 L264 440 L259 444 L256 450 L257 453 L251 465 L243 472 L241 471 L241 465 L245 460 L240 456 L238 452 L233 449 L228 445 L222 443 L217 437 L212 440 L211 437 L202 428 L199 429 L198 431 L193 429 L203 420 L213 408 L216 408 L215 406 L222 402 L226 398 L231 396 L237 393 L239 383 L236 375 L233 373 L228 374 L232 356 L228 353 L223 355 L219 355 L216 339 L214 335 L209 334 L207 332 L205 334 L201 334 L189 333 L191 319 L187 309 L190 307 L187 304 L192 296 L191 294 L195 286 L191 277 L184 274 L183 268 L185 263 L163 262 L163 253 L159 248 L162 248 L159 233 L153 229 L145 230 L141 225 L133 223 L130 219 L126 219 L122 217 L114 216 L113 214 L107 211 L103 202 L103 199 L102 193 L104 189 L103 184 L89 186 L75 195 L71 196 L65 201 L58 199 L41 199 L43 180 L34 187 L23 187 L21 181 L12 180 L14 175 L8 167 L5 162 L6 161 L2 158 L3 156 L6 155 L5 150 L12 145 L11 140 L14 135 L15 129 L27 121 L38 119 L40 117 L44 117 L46 119 L49 119 L56 82 L53 73 L48 69 L48 60 L55 58 L59 59 L57 55 L51 54 L51 47 L70 47 L70 43 L73 46 L79 42 L83 48 L83 53 L85 53Z M286 70 L292 69 L300 71 L295 84 L293 85 L291 84 L291 86 L288 85 L287 88 L284 89 L281 88 L276 89 L273 82 L275 80 L273 78 L274 70 L279 69 L286 70Z M350 345 L347 345 L349 344 L350 345Z M298 384 L297 383 L299 381 L298 384Z M337 354 L335 354 L336 352 L337 354Z M346 102 L345 104 L346 100 L346 102Z M413 224 L414 222 L414 223 L413 224Z M341 83 L340 84 L340 82 L341 83Z M285 64 L283 67 L278 67 L279 64 L285 64Z M278 44 L276 44 L276 42 L278 42 L278 44Z M274 69 L271 71 L270 70 L272 68 L274 69Z M288 69 L284 68 L288 66 L289 67 L288 69Z M277 66 L277 67 L274 67 L275 65 L277 60 L278 64 L277 66Z M280 62 L279 63 L279 61 L281 60 L280 62Z M260 84 L259 85 L264 75 L267 74 L268 75 L267 79 L260 84Z M299 400 L299 401 L299 398 L300 396 L299 400Z"
MAPA = r'''
VAR _corte = [Data Corte]
VAR _t =
    ADDCOLUMNS (
        VALUES ( dFilial[FilialID] ),
        "@cid", CALCULATE ( SELECTEDVALUE ( dFilial[Cidade] ) ),
        "@uf", CALCULATE ( SELECTEDVALUE ( dFilial[UF] ) ),
        "@reg", CALCULATE ( SELECTEDVALUE ( dFilial[Regiao] ) ),
        "@x", CALCULATE ( ( SELECTEDVALUE ( dFilial[Longitude] ) + 74.2 ) * 12 * 0.970296 ),
        "@y", CALCULATE ( ( 5.6 - SELECTEDVALUE ( dFilial[Latitude] ) ) * 12 ),
        "@rec", [Receita Líquida],
        "@at", [Atingimento Meta Faturamento %]
    )
VAR _max = MAXX ( _t, [@rec] )
VAR _tot = SUMX ( _t, [@rec] )
VAR _pts =
    CONCATENATEX (
        _t,
        VAR _r = 3 + 6 * SQRT ( DIVIDE ( [@rec], _max ) )
        VAR _c = SWITCH ( [@reg], "Sudeste", "#10D4C4", "Sul", "#5FA8E6", "#FFC66D" )
        VAR _cx = FORMAT ( [@x], "0.0", "en-US" )
        VAR _cy = FORMAT ( [@y], "0.0", "en-US" )
        RETURN
            "<g><circle class='nx-hl' cx='" & _cx & "' cy='" & _cy & "' r='" & FORMAT ( _r * 1.9, "0.0", "en-US" ) & "' fill='" & _c & "' style='animation-delay:" & FORMAT ( MOD ( [FilialID] * 0.37, 3 ), "0.00", "en-US" ) & "s'/>"
                & "<circle cx='" & _cx & "' cy='" & _cy & "' r='" & FORMAT ( _r, "0.0", "en-US" ) & "' fill='" & _c & "' stroke='#071528' stroke-width='1.2'/></g>",
        "",
        [@rec], ASC
    )
VAR _lista =
    CONCATENATEX (
        TOPN ( 12, _t, [@rec], DESC ),
        VAR _c = SWITCH ( [@reg], "Sudeste", "#10D4C4", "Sul", "#5FA8E6", "#FFC66D" )
        RETURN
            "<div class='nx-li'><span class='nx-dt' style='background:" & _c & "'></span><span class='nx-ci'>" & [@cid] & "</span><span class='nx-bw'><span class='nx-b' style='width:" & FORMAT ( 100 * DIVIDE ( [@rec], _max ), "0", "en-US" ) & "%;background:" & _c & "'></span></span><span class='nx-v'>" & FORMAT ( [@rec] / 1e6, "#,0" ) & "</span></div>",
        "",
        [@rec], DESC
    )
VAR _leg =
    CONCATENATEX (
        DISTINCT ( SELECTCOLUMNS ( _t, "@rg", [@reg] ) ),
        VAR _rr = [@rg]
        VAR _n = COUNTROWS ( FILTER ( _t, [@reg] = _rr ) )
        VAR _c = SWITCH ( _rr, "Sudeste", "#10D4C4", "Sul", "#5FA8E6", "#FFC66D" )
        RETURN "<span class='nx-lg'><span class='nx-dt' style='background:" & _c & "'></span>" & _rr & " · " & _n & "</span>",
        "", [@rg], ASC
    )
VAR _css = "<style>.nx-m{font-family:'Segoe UI',sans-serif;color:#FFFFFF;box-sizing:border-box;height:100vh;padding:18px 22px;background:rgba(7,21,40,.95);border:1px solid #173B5C;border-radius:16px;animation:nxIn .8s ease-out both}.nx-t{font-size:16px;font-weight:600}.nx-s{font-size:11px;color:#A9B9CA;margin:2px 0 8px}.nx-g{display:flex;gap:14px;align-items:flex-start}.nx-l{flex:1;padding-top:4px}.nx-li{display:flex;align-items:center;gap:7px;font-size:11.5px;height:24px}.nx-ci{width:92px;color:#C9D6E3;white-space:nowrap;overflow:hidden}.nx-bw{flex:1;height:5px;background:#12304F;border-radius:3px}.nx-b{display:block;height:5px;border-radius:3px;opacity:.85}.nx-v{width:26px;text-align:right;color:#FFFFFF;font-weight:600}.nx-dt{display:inline-block;width:7px;height:7px;border-radius:50%}.nx-lgs{display:flex;gap:14px;font-size:10px;color:#A9B9CA;margin-top:8px}.nx-lg{display:flex;align-items:center;gap:5px}.nx-u{font-size:9px;color:#6F86A0;text-align:right;margin-top:2px}.nx-hl{opacity:.0;transform-box:fill-box;transform-origin:center;animation:nxP 3.2s ease-out infinite}@keyframes nxP{0%{opacity:.45;transform:scale(.45)}70%{opacity:0;transform:scale(1.35)}100%{opacity:0}}@keyframes nxIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-hl{animation:none}.nx-m{animation:none}}</style>"
RETURN
    _css & "<div class='nx-m'><div class='nx-t'>Rede de filiais</div><div class='nx-s'>" & COUNTROWS ( _t ) & " unidades · receita líquida de " & FORMAT ( CALCULATE ( MIN ( dCalendario[Data] ), dCalendario[Data] <= _corte ), "mmm/yyyy", "pt-BR" ) & " a " & FORMAT ( _corte, "mmm/yyyy", "pt-BR" ) & "</div>"
        & "<div class='nx-g'><svg width='318' height='328' viewBox='0 0 465 480' role='img' aria-label='Mapa do Brasil com as filiais'><path d='" & "@@BR@@" & "' fill='#0A2540' stroke='#10D4C4' stroke-opacity='.55' stroke-width='1.4'/>" & _pts & "</svg>"
        & "<div class='nx-l'>" & _lista & "<div class='nx-u'>R$ milhões</div></div></div><div class='nx-lgs'>" & _leg & "</div></div>"
'''.replace('@@BR@@', BR)
KPIS = r'''
VAR _corte = [Data Corte]
VAR _ini = CALCULATE ( MIN ( dCalendario[Data] ), dCalendario[Data] <= _corte )
VAR _filiais = COUNTROWS ( FILTER ( VALUES ( dFilial[FilialID] ), [Receita Líquida] > 0 ) )
VAR _item = "<div class='nx-k' style='animation-delay:@@ds'><div class='nx-kl'>@@L</div><div class='nx-kv'>@@V</div><div class='nx-ks'>@@S</div></div>"
VAR _css = "<style>.nx-ks-w{font-family:'Segoe UI',sans-serif;display:flex;height:100%;box-sizing:border-box;align-items:stretch;background:rgba(7,21,40,.78);border:1px solid #173B5C;border-radius:14px;padding:14px 8px}.nx-k{flex:1;padding:0 20px;border-left:1px solid #173B5C;animation:nxUp .7s ease-out both}.nx-k:first-child{border-left:none}.nx-kl{font-size:10px;letter-spacing:.12em;color:#A9B9CA;text-transform:uppercase}.nx-kv{font-size:26px;font-weight:600;color:#FFFFFF;margin-top:4px;line-height:1.1}.nx-ks{font-size:10px;color:#6F86A0;margin-top:4px}@keyframes nxUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}@media (prefers-reduced-motion:reduce){.nx-k{animation:none}}</style>"
VAR _per = FORMAT ( _ini, "mmm/yy", "pt-BR" ) & " – " & FORMAT ( _corte, "mmm/yy", "pt-BR" )
RETURN
    _css & "<div class='nx-ks-w'>"
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0" ), "@@L", "Receita líquida" ), "@@V", "R$ " & FORMAT ( [Receita Líquida] / 1e6, "#,0.0" ) & " mi" ), "@@S", _per )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.08" ), "@@L", "Margem bruta" ), "@@V", FORMAT ( [Margem Bruta %], "0.0%" ) ), "@@S", _per )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.16" ), "@@L", "Clientes ativos" ), "@@V", FORMAT ( [Clientes Ativos (total)], "#,0" ) ), "@@S", "compra há menos de " & [Limite Ativo (dias)] & " dias em " & FORMAT ( _corte, "dd/mm/yy" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.24" ), "@@L", "Entregas" ), "@@V", FORMAT ( [Entregas], "#,0" ) ), "@@S", "OTIF " & FORMAT ( [OTIF %], "0.0%" ) )
        & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( _item, "@@d", "0.32" ), "@@L", "Filiais" ), "@@V", _filiais ), "@@S", "Sudeste, Sul e Centro-Oeste" )
        & "</div>"
'''
upsert(sys.argv[1], [
    dict(name='UX Home Mapa', expr=MAPA, folder='08 UX\\Home',
         desc='Mapa SVG independente: contorno do Brasil (Natural Earth) e as filiais de dFilial posicionadas por latitude/longitude; tamanho pela receita; lista ordenada por receita.'),
    dict(name='UX Home KPIs', expr=KPIS, folder='08 UX\\Home',
         desc='Faixa de indicadores da Home com medidas reais: receita, margem, clientes ativos, entregas (com OTIF) e filiais com receita.'),
])
print('ok')
