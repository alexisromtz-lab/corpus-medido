# Visión Open Source — el embudo, medido antes de sembrar

<!-- HUELLA-VISION-OPEN-SOURCE-20261103 -->

**Fecha de la medición:** 2026-11-04T03:15Z.
**Sujeto:** el patrimonio público de `alexisromtz-lab` en cuatro superficies (GitHub propio,
Zenodo, Dev.to) y en una superficie ajena (un PR upstream). No es una opinión sobre open
source: es el estado del embudo el día en que se decidió sembrar en él.
**Dueño único de la **Política de los 3 filtros** (§3). Ningún otro archivo la copia: los
demás la apuntan con ruta y blob.

## 1 · La medición de partida

| superficie | artefactos | señal externa medida | comando |
|---|---:|---|---|
| GitHub propio | **22** repos públicos | **0** estrellas · **0** forks · **0** seguidores | `gh repo list alexisromtz-lab --limit 100 --json name,visibility,stargazerCount,forkCount` |
| Zenodo | **4** registros | **0** citas (OpenAlex) · **19** vistas / **8** descargas sumadas: `23329941` 4/1 · `23329943` 6/1 · `23363121` 9/6 · `23955654` 0/0 · medido 2026-11-04T16:24Z | `.venv/bin/python tools/medir_adopcion.py --solo zenodo` (leen `stats` de `https://zenodo.org/api/records/<id>`, los cuatro ids) |
| Dev.to | **11** artículos | **0** reacciones · **1** comentario (histórico completo) | `curl -s "https://dev.to/api/articles?username=alexisromtz7&per_page=30"` |
| **Upstream `BerriAI/litellm#46222`** | **1** PR | **32** comentarios, **21** escritos por el mantenedor `mateo-berri` | `gh api "repos/BerriAI/litellm/issues/46222/comments?per_page=100" --jq '[.[].user.login]\|group_by(.)\|map({u:.[0],n:length})'` |

**Lectura.** Un solo PR en un repositorio ajeno produjo más atención humana (21 intervenciones
de un mantenedor) que seis meses de publicaciones propias en las tres superficies que
controlamos (0 estrellas, 0 citas, 1 comentario). El activo del corpus no es credibilidad —
22 artefactos con falsadores y DOIs son credibilidad— es **audiencia**.

## 2 · La ley que se sigue de eso

**No tenemos un problema de autoridad; tenemos un problema de distribución.** Publicar un
artefacto número 23 no mueve el embudo: lo alarga por abajo. El cuello está arriba, donde no
hay nadie leyendo.

Corolario que ordena todo lo demás: **se pide prestada la audiencia, no se construye desde
cero.** Un repositorio con 40 000 ojos presta sus ojos a un parche; un repositorio propio con
0 estrellas no presta nada, por bueno que sea el contenido.

Esto valida la intuición del CEO, pero por una razón distinta de la que se dijo. GitHub no es
"el nuevo SEO": nadie encuentra un repo de 0 estrellas buscando. GitHub es **arbitraje de
atención**: el lector ya está ahí, en el issue de otro, con el problema en la mano.

## 3 · Política de los 3 filtros (dueño único de la regla)

Comentar en un repositorio ajeno es un **acto público irreversible** y el único gasto del
corpus que no se puede pagar dos veces: una afirmación falsa quema la cuenta, no el comentario.
Por eso la regla **falla cerrada**: sin los tres filtros no se publica.

| # | filtro | qué se mide | RC si no se cumple |
|---|---|---|---|
| **F1** | **Uso.** Ejecutamos ese componente, o lo vamos a adoptar, en algo que corre | ¿hay un despliegue, un `pyproject` o un servicio que lo importe? | `RC 30 SIN_USO` |
| **F2** | **Frescura.** El locus se releyó **en el mismo turno** del acto | `gh api` del archivo, no memoria de una sesión anterior | `RC 31 LOCUS_CADUCO` |
| **F3** | **Duplicado.** Se buscó antes de escribir | `gh issue list --search`, `gh pr list --search` con la causa, no con el síntoma | `RC 32 DUPLICADO` |

- **F2 es el filtro que más veces ha fallado.** Medido en este mismo frente: dos turnos de
  ejecución, dos mediciones heredadas caducadas — el `:54` heredado del CEO y el `:19` propio
  seis horas después, ya inexistente en `main` porque el upstream lo movió a `:67` dentro de
  `if TYPE_CHECKING:`. Un locus recordado no es un locus.
- **F3 no busca el síntoma, busca la causa.** La búsqueda que salvó el frente no fue
  `"prisma check_mcp_sdk_install"` (0 resultados), fue rastrear el archivo hasta su último
  commit: `BerriAI/litellm#49771` ya lo había arreglado, y abrir un issue habría sido ruido a
  nombre de la empresa.
- **Declaración de excepción, hoy abierta.** `BerriAI/litellm#46222` **no cumple F1 como
  está escrita**: no hay medición de que ejecutemos litellm en producción. Se mantiene porque
  el artefacto es un parche que necesitaríamos igual y porque el mantenedor ya está en la
  conversación; pero el filtro se declara incumplido, no se reescribe para que pase.
- **El volumen no es una estrategia.** Comentar N issues para "estar presente" es la vía más
  rápida al ban de un mantenedor. Esta política no tiene cuota diaria: tiene tres puertas.

**Falsador de §3.** Si de los comentarios publicados bajo esta política **≥ 3 de 10** resultan
refutados por el mantenedor (dato falso, locus caducado, duplicado), la política no estaba
midiendo lo que dice y se retira. Hoy el panel es **n = 2** (ambos comentarios publicados en
`#46222`, ambos con F2 y F3 verdes): **no alcanza para sostener ni para retirar la regla**.

## 4 · El embudo

> El open source es el embudo. Los desarrolladores usan nuestras herramientas, las empresas
> las adoptan, y nosotros les vendemos las SaaS (Barber, Dental) para que automaticen su
> negocio. La auditoría es la puerta de entrada.

Las tres etapas del embudo, y lo que cada una **exige medido**:

1. **Uso** — alguien instala y corre. Sin README de 30 segundos (instalar, un comando, una
   salida) no hay uso, hay archivo. Hoy esta etapa mide **0**: hay 8 descargas en Zenodo
   (2026-11-04T03:40Z) y ninguna está verificada como instalación.
2. **Adopción** — alguien lo mete en su CI o en su `pyproject` y depende de él. Es la única
   etapa que paga: un fork cuenta, una estrella no.
3. **Venta** — la auditoría entra por una puerta que el uso abrió. **La auditoría se ofrece,
   no se impone**: una auditoría no pedida en el issue de otro es spam con bibliografía.

**Lo que la auditoría NO es.** No es el diagnóstico que ya hizo el mantenedor, ni el defecto
que el autor del PR no pidió revisar. Un defecto ajeno entra solo si cambia el veredicto del
acto; si no, va a la bitácora y no al comentario.

## 5 · DOI: para qué sirve y para qué no

- **Sirve para** fijar anterioridad sobre un método (que la idea existía y cuándo), y para que
  un comprador enterprise pueda citar el artefacto en un expediente de compra. Coste ≈ 0
  (Zenodo + DataCite). Ya tenemos práctica: 4 registros, 0 citas.
- **El cuarto DOI, depositado y publicado por API el 2026-11-04** (no a mano):
  [`10.5281/zenodo.23955654`](https://doi.org/10.5281/zenodo.23955654) — *Coherencia no es
  completitud: el punto ciego de `uv pip check` frente a dependencias extra*, preprint, 4
  págs, 194 320 B, `sha256 c41e3dbe…b9f650`, CC-BY-4.0, ORCID `0009-0001-9116-075X`. El
  depósito se reproduce con `tools/depositar_zenodo.py --metadata docs/zenodo_deposito_nota_coherencia_20261103.json`;
  el instrumento comprueba el `sha256` del artefacto antes de subirlo y **se niega a depositar
  si ya existe un registro con ese título** (RC 11, cero escrituras).
- **Lo que el depósito deja ver y no se arregla cambiando el DOI:** el `PUT` de metadatos
  devuelve RC 200 con 10 `keywords` y `language: spa` en la representación legacy
  (`/api/deposit/depositions/23955654`), y el registro publicado expone **0 `subjects` y sin
  `languages`** (`/api/records/23955654`). Mismo resultado en el registro `23514239`: 8
  keywords legacy, 0 subjects. El verde de la escritura no es el verde del artefacto, y es
  preexistente a este depósito.
- **No sirve para** un comentario de PR o de issue. Nadie cita un issue, y un DOI colgado en
  una conversación técnica se lee como disfraz: convierte un argumento en un folleto.
- **La prueba de merecimiento:** una nota merece DOI si trae **locus, contraejemplo y
  falsador** — si un lector puede ejecutar algo que la tumbe. Si solo trae una opinión con
  aparato, engorda el catálogo y no el conocimiento.
- **El KPI del DOI no es el DOI.** Es `cited_by_count` y descargas. Hoy: **0 citas, 8
  descargas totales** — de las cuales 0 pertenecen al cuarto DOI, que lleva minutos publicado.
  El cuarto DOI existía como predicción en la versión anterior de este documento; ya existe
  como objeto y mide **0 vistas / 0 descargas**, que es exactamente lo que la predicción decía
  que no cambiaría nada. El instrumento que lo dice es `tools/medir_adopcion.py`.

## 6 · El KPI: adoptado ≠ visto

`tools/medir_adopcion.py` es el medidor. Lee cuatro fuentes y publica, por métrica, `estado`
(`MEDIDO` · `NO_MEDIDO`), `fuente`, la sonda y su `RC`. **Un `0` es un dato; un `NO_MEDIDO` es
un hueco** y nunca se suman: la línea base de este documento tiene ceros reales (0 estrellas,
4 registros Zenodo con 19 vistas y 8 descargas) y un hueco real declarado (`cited_by_count`
de los cuatro DOIs, que OpenAlex indexa con retraso).

Lo que el medidor **no** puede afirmar: que una descarga sea un ingeniero, que una estrella sea
un usuario, que una cita sea una adopción. Mide el canal, no la intención. Se declara.

## 7 · Falsadores de este documento

- **§2 (distribución, no autoridad).** Se falsa si un artefacto propio, publicado sin
  participación en ningún repo ajeno, alcanza ≥ 10 estrellas o ≥ 10 descargas Zenodo en 30
  días. Entonces sí había demanda latente y el problema era el formato, no la audiencia.
- **§5 (el DOI no mueve nada).** Se falsa si `medir_adopcion.py` mide ≥ 1 cita de OpenAlex
  sobre cualquier registro del corpus en los 90 días siguientes al depósito. Entonces el DOI
  sí era canal y esta sección está equivocada.
- **§1 (la línea base).** Toda cifra de §1 se re-deriva con el comando de su fila. Si la
  corrida no reproduce el número, manda la corrida y este documento se corrige con fecha, no
  se reescribe en silencio.

## 8 · Lo que este documento no autoriza

No autoriza abrir issues, comentar en repos ajenos, depositar en Zenodo ni publicar artículos:
cada acto público conserva su propia autorización del CEO y su propia medición. No sustituye a
`PROTOCOLO_DELEGACION.md` (modos `MAP`/`AUDIT`/`FIX`) ni a A2.1 (tupla de pre-escritura). No
crea cuota de comentarios. Es una tesis con denominador, no un permiso.

### Estado del frente al 2026-11-04: CONGELADO
<!-- HUELLA-VISION-OSS-CONGELAMIENTO-DEL-FRENTE-20261104 -->

El cuarto DOI quedó publicado por API —`10.5281/zenodo.23955654`, medido `2026-11-04`:
`https://doi.org/10.5281/zenodo.23955654` → **HTTP 302** y `/api/records/23955654` → **HTTP
200** con `publication_date` `2026-11-04`— y la deuda de metadatos que lo acompaña queda
**declarada, no reparada**: `keywords` y `language` viajan en la vista legacy del depósito y
**no** llegan al registro publicado (`subjects: []`, `languages: null`), en **4 de 4** registros
(Bitácora, Bloque 168). La reparación vive en la API RDM y se difiere: editar un DOI recién
nacido abre versión y produce un v2 que nadie pidió. De ahí el congelamiento — desde este
frente no se abre issue, no se comenta en repo ajeno y no se deposita artefacto nuevo.

**Descongela con cualquiera de estas tres sondas, y no antes:** (a) el mantenedor responde en
`BerriAI/litellm#46222`; (b) `tools/medir_adopcion.py` deja de reportar `NO_MEDIDO` para
`10.5281/zenodo.23955654` en OpenAlex — hoy es el único de sus 21 renglones en ese estado—, lo
que vuelve testeable el falsador de §5; (c) el CEO levanta el congelamiento por escrito.
Ninguna de las tres es una fecha: son sondas.

### 2026-11-04 · la sonda (c) disparó: de CONGELADO a COLOCACIÓN
<!-- HUELLA-VISION-OSS-COLOCACION-UV13963-20261104 -->

El CEO levantó el congelamiento **por escrito** y asignó a esta pestaña la misma tarea, no una
nueva: *atraer miradas*. La fábrica sigue cerrada —cero instrumentos, cero papers—; lo que
reabre es la **colocación** de lo ya medido donde ya hay audiencia.

**Acto:** `astral-sh/uv#13963` —abierto, *enhancement* del `2025-06-11`, 6 comentarios, último
del `2025-06-12`— pregunta literalmente si un extra pedido y no cumplido haría fallar la
instalación. La respuesta medida se publicó el `2026-11-04T16:55:19Z` en
`https://github.com/astral-sh/uv/issues/13963#issuecomment-6636640016`; el hilo pasa de 6 a 7
comentarios.

**Los tres filtros, con su número:** (a) `uv` en producción — `uv 0.11.21`, `uv.lock` de
340 808 B, `.venv` creado por `uv`; (b) loci releídos **en este mismo turno** sobre el sha
inmutable `9b94134`, con la cadena completa hasta `proxy_setting_endpoints.py:19`; (c)
duplicado: los 6 comentarios previos discuten diseño y ninguno aporta caso medido.

**Lo que el acto corrigió del propio corpus:** esta sección describía el fallo como un import
de módulo en `check_mcp_sdk_install.py:29`. La traza real falla en `:54`, al **llamar**
`unsupported_protocol_version`, y el módulo perdido se alcanza por un import diferido en
`mcp_server/capabilities.py:76`. La afirmación de §5 no cambia —verde sobre 117 paquetes y
`ModuleNotFoundError` 12,06 s después—; el mecanismo queda medido a nivel de línea.

**Siguiente sonda:** ¿responde una persona en `astral-sh/uv#13963`? Una reacción no es
respuesta; una respuesta sí. Sin ella, el frente vuelve a congelarse con el acto ya registrado.

### Operar el frente en cuatro comandos <!-- HUELLA-VISION-OSS-OPERAR-FRENTE-20261104 -->

Cada sonda del frente es un número comparable, no una impresión. Las cuatro se corrieron tal
cual el `2026-11-04` y esto devolvieron:

| sonda | comando | medido | se abre cuando |
|---|---|---|---|
| colocación | `gh api repos/astral-sh/uv/issues/13963/comments --jq '[.[]\|select(.user.login!="alexisromtz-lab")\|length'` | `6` | `≥ 7`: una **persona** respondió |
| aprobación | `gh pr view 46222 --repo BerriAI/litellm --json state,reviewDecision --jq '.state+" "+.reviewDecision'` | `OPEN REVIEW_REQUIRED` | `MERGED`, o `reviewDecision` distinto de `REVIEW_REQUIRED` |
| adopción | `.venv/bin/python tools/medir_adopcion.py --json` | `NO_MEDIDO` en OpenAlex para `10.5281/zenodo.23955654` | ese renglón deja de decir `NO_MEDIDO` |
| superficie | `gh repo view alexisromtz-lab/platino-labs --json isPrivate,stargazerCount --jq '"private=\(.isPrivate) stars=\(.stargazerCount)"'` | `private=true stars=0` | `private=false` **y** `stars≥1` |

**Regla de lectura:** la sonda de colocación cuenta personas, no reacciones. Un `+1` de reacción
deja el contador en `6`; por eso una reacción no es una respuesta y no descongela nada.

**El Motor no está conectado, y eso está medido.** `~/Library/Application Support/Code/User/mcp.json`
pesa **0 B** y `~/.copilot/config.json` no expone ninguna clave `mcp*`: las cuatro lecturas de
A2.1-R —`obtener_estado`, `obtener_veredicto_gate`, `obtener_impacto`, `obtener_delta`— **no están
registradas en esta sesión**, así que toda lectura cae al fallback de `bash`. El Motor existe
—`~/primer/ast-channel-router`, seis módulos—; lo que falta es el registro, que es escritura
fuera del árbol git y exige `OVERRIDE` (A0.99). Con el Motor apagado, «escanear» se hace con
`gh` y con `grep`, y cada lectura cuesta lo que cuesta un `git status` sin acotar.

Este bloque es lo único que hace falta para reabrir el frente sin releer el documento: cuatro
comandos, cuatro números, y un umbral por número.

### 2026-11-04 · el escaparate no listaba el activo que se estaba colocando <!-- HUELLA-VISION-OSS-ESCAPARATE-20261104 -->

Barrido de los **22** README públicos de `alexisromtz-lab` buscando `10.5281/zenodo.23955654`: **0
coincidencias**. El DOI llevaba un día publicado y colocado en `astral-sh/uv#13963`, y el perfil al
que aterriza cualquiera que hace clic en el autor —`alexisromtz-lab/alexisromtz-lab`, README de
17 266 B, último commit `a1b6be31` del `2026-11-01`— no lo mencionaba. Peor: su propio badge decía
`Zenodo — 3 DOIs` mientras los DOIs que el perfil lista **hoy**, verificados uno por uno ese día, son
**6** —cinco previos más el nuevo— (los seis responden `302` en `doi.org`, y `zenodo.org/api/records/<id>` devuelve el título de
cada uno).

Ese es el eslabón que faltaba del embudo: el comentario trae al lector y el escaparate decide si se
queda. Se cerró con dos commits quirúrgicos sobre `alexisromtz-lab/alexisromtz-lab` — `bf8b85e5`
(añade *§4. `uv pip check` is green and the import still fails*, con el DOI y el hilo) y `917c13dc`
(corrige una palabra)— y el README pasa de **17 266 a 18 290 B**. El badge queda en `6 DOIs`, que es
el número medido y no el que se recordaba.

**Lo que esto no es:** no es un instrumento nuevo ni un paper nuevo; es el activo de ayer llegando a
la única superficie que el lector sí abre.

### Línea base medida · 2026-11-04T17:04Z <!-- HUELLA-VISION-BASELINE-EMBUDO-20261104 -->

`.venv/bin/python tools/medir_adopcion.py` ⇒ **20 MEDIDO · 1 NO_MEDIDO**, RC 0. Es la primera
corrida con el DOI nuevo ya colocado; sirve para diferenciar contra ella, no para felicitarse.

| eslabón | sonda | medido | umbral que lo abre |
|---|---|---|---|
| escaparate | README de perfil `alexisromtz-lab/alexisromtz-lab` | **18 290 B**, 6 DOIs, cita el DOI y `uv#13963` | ya en verde: el lector que llega encuentra el activo |
| colocación | `gh api repos/astral-sh/uv/issues/13963/comments` menos `alexisromtz-lab` | **6** personas · última humana 2025-06-12 | **≥ 7** = alguien además de nosotros responde |
| adopción · Zenodo | `zenodo.org/api/records/23955654` → `stats` | **0 vistas · 0 descargas** | **≥ 1** descarga real |
| adopción · Zenodo (previos) | ídem `23329941` / `23329943` / `23363121` | **4/1 · 6/1 · 9/6** | inventario del techo actual: **9** vistas es el máximo histórico |
| adopción · OpenAlex | `citas::10.5281/zenodo.23955654` | `NO_MEDIDO` (sin obra recuperable) | indexación; no se lee como 0 |
| adopción · dev.to | `gh`-equivalente sobre 11 artículos | **0 reacciones · 1 comentario** | **≥ 1** reacción por artículo |

**Dos cifras que no se reprodujeron.** El reporte previo hablaba de *17 vistas / 8 descargas* en la
nota depositada. Ninguno de los cuatro registros alcanza eso por API: el máximo es **9 vistas / 6
descargas** (`23363121`) y el DOI de hoy está en **0 / 0**. La cifra no se hereda: se re-mide o no se
publica. Si el número venía de una pantalla de la interfaz, esa pantalla no es la sonda.

**Lo que la línea base dice del embudo, sin adornos.** El activo está colocado donde se hacía la
pregunta y el escaparate ya lo lista, y aun así el registro nuevo lleva **0 lecturas**. Colocar no es
distribuir: el hilo de `uv` lo leyeron las mismas 6 personas de siempre. El siguiente movimiento no es
publicar más fuerte en ese hilo — es otro hilo, con los mismos 3 filtros, o el canal que sí mueve
lectores (dev.to tiene 11 artículos y 0 reacciones: es superficie, no distribución).

**Dos decisiones que no son mías.** (a) `platino-labs` sigue **privado** (`isPrivate: true`, 0
estrellas): el corpus de 58 reglas, gates y RC **no es citable** y todo comentario colocado aterriza
en el perfil, no en el material. (b) El motor `platino-engine` **no está registrado**
(`~/Library/Application Support/Code/User/mcp.json` = 0 B): las cuatro lecturas de A2.1-R no pueden
dispararse y cada consulta paga el fallback `bash`. Registrarlo es escritura fuera del árbol git ⇒
requiere `OVERRIDE`.
