# 🥇 PLATINO LABS — Centro de operaciones

## 🧭 REGLA DE ORO — LEER PRIMERO
**Regla de oro:** Antes de realizar cualquier tarea, lee y aplica las directrices estratégicas definidas en `PLATINO_CONTEXT.md` en la raíz del repositorio.
<!-- HUELLA-AGENTS-CONSTITUCION-PUNTERO-20261030 -->

## 🧭 A0 — NAVEGACIÓN PROGRESIVA OBLIGATORIA
<!-- HUELLA-A0-NAVEGACION-PROGRESIVA-20261030 -->

El corpus tiene **seis departamentos** con su mapa de puertas en [`DEPARTAMENTOS/_MAPA.md`](DEPARTAMENTOS/_MAPA.md). Un departamento es una **vista**, no un perímetro: no posee archivos, los **apunta** (`empresa/SISTEMA_DE_EMPRESAS.md:70`: dos perímetros se conectan por puntero y nunca se suman). <!-- HUELLA-AGENTS-LOCUS-PUNTERO-20261030: medido 30-Oct-2026; `:76` es un separador `---`, la regla vive en `:70`. -->

- **A0.1** — Toda sesión abre por el nivel **L0**: [`BRIEFING_SOCIO_DIRECTOR.md`](BRIEFING_SOCIO_DIRECTOR.md). Sin excepción.
- **A0.2** — La tarea define el departamento. Antes de planificar se lee `DEPARTAMENTOS/<depto>/_RESUMEN.md` (**L1**). Si no se sabe a cuál pertenece, se lee [`DEPARTAMENTOS/_MAPA.md`](DEPARTAMENTOS/_MAPA.md); si sigue sin saberse, se registra en [`BITACORA_HALLAZGOS.md`](BITACORA_HALLAZGOS.md) y se detiene el turno.
- **A0.3** — Se planifica contra `_PLAN.md` (**L2**) y se ejecuta contra `<instrumento>.md` (**L3**). **No se salta de L1 a L4.** Si el L2/L3 no existe todavía, eso es el hueco, no una licencia para improvisar.
- **A0.4** — Si el L3 falta o está incompleto, **no se inventa**: se registra el hueco con `locus` · `clase` · `por qué importa` · `quién lo paga` y se para. El dueño decide si se crea el L3 o se cancela la tarea.

### A0.5 – A0.14 y A0.99 — obligación en una línea

| regla | obligación |
|---|---|
| **A0.5** | Ciclo de investigación L0.5: tesis única → hipótesis de departamento → ningún cierre sin ciclo → estado al final. |
| **A0.6** | Catálogo falsable de ofertas: 7 campos; **una oferta sin test que la falsa se rechaza sin leer el precio**. |
| **A0.7** | Ley de la casa: **los departamentos no copian, apuntan** (ruta + blob + una línea). |
| **A0.8** | El correo de `tiendasplatino.com.mx` **no es canal comercial** (`Sent=0` histórico). |
| **A0.9** | Routing por capa: L0–L2 → arquitecto, L3–L4 → obrero; al tercer atoro se escala. |
| **A0.10** | *(cuerpo en `PROTOCOLO_CIERRE.md`)* Reporte de latencia cognitiva obligatorio al cerrar: 4 líneas. |
| **A0.11** | Ventana de merge: un carril, los viernes; `tools/panel_de_vuelo.sh` sonda [2] lo lee. |
| **A0.12** | *(cuerpo en `PROTOCOLO_CIERRE.md`)* Reporte de visión sistémica al cerrar: PATRÓN · PUNTO CIEGO · OPORTUNIDAD. |
| **A0.13** | Batching de CI: **un empujón por sesión**; el coste lo cobra la frecuencia del push. |
| **A0.14** | Principio de orden: ningún documento nace copiando (puntero), ningún departamento nace a medias (L1+L2+L3), ningún instrumento nace ciego (`--self-test`). Lector: `tools/auditar_sistemas.py`. Teoría y falsador → `docs/TEORIA_CONEXIONES_FALTANTES_20261101.md`. |
| **A0.99** | *(cuerpo íntegro abajo)* **Fast-Track de Configuración Local**: la palabra `OVERRIDE` del CEO autoriza escribir **fuera del árbol git** sin tupla A2.1; **no** autoriza secretos, árbol git, migraciones, despliegues ni commits. |

Cuerpo con mediciones y falsadores de A0.5–A0.9, A0.11 y A0.13 → `docs/A0_Y_OPERATIVA.md` @ blob `975461596d90ebc6b3bd72dcd3a43022f29f9a1a`
<!-- HUELLA-CONTEXTO-A0-FUERA-20261101 -->
<!-- HUELLA-A0-14-PRINCIPIO-DE-ORDEN-20261101 -->

### A0.10 y A0.12 — los dos bloques de cierre (cuerpo fuera)
<!-- HUELLA-AGENTS-CIERRE-FUERA-20261103 -->

Toda tarea cierra emitiendo **dos** bloques: `CIERRE DE TAREA — LATENCIA COGNITIVA`
(A0.10: hipótesis descartadas · conexiones no exploradas · grados de libertad ·
vista desde arriba) y `VISIÓN SISTÉMICA` (A0.12: PATRÓN · PUNTO CIEGO ·
OPORTUNIDAD). Bloque vacío o «ninguna» ⇒ **la tarea no se cierra**.

Formato literal, compuertas y falsadores → [`PROTOCOLO_CIERRE.md`](PROTOCOLO_CIERRE.md) · sub-reglas A0.10.1–4 y A0.12.1–4 → [`docs/A0_10_A0_12_REPORTES.md`](docs/A0_10_A0_12_REPORTES.md).
Se abre **al cerrar**, no al arrancar: la mudanza retiró **4 578 B** del prefijo
(`git cat-file -s`: 31 828 → 27 250 B de `AGENTS.md`, ≈ **1 200 tok** por petición
a razón de 3 813 car/tok, `tools/presupuesto_sesion.py` P1).

A0 **no** sustituye a A2.1 ni a las 57 reglas: ordena **qué se lee antes**, no **cómo se mide**.

### A0.99 — Fast-Track de Configuración Local
<!-- HUELLA-A099-FAST-TRACK-LOCAL-20261101 -->

**Qué desbloquea.** Una orden del CEO que contiene la palabra `OVERRIDE` autoriza escribir en rutas **fuera del árbol git del corpus** —`~/.copilot/`, `chatLanguageModels.json`, `settings.json` de VS Code, dotfiles del host— **sin tupla A2.1, sin `gate_pre_escritura.sh` y sin pedir RC**. El gate no puede validar identidad ahí (eso es exactamente RC 14) y exigirla produjo la parálisis del 1-Nov-2026: turnos gastados en editar un archivo de configuración que ningún commit puede romper.

**Perímetro — lo que `OVERRIDE` NO autoriza.** El fast-track es de configuración local, no de perímetro:

- **No** autoriza escribir **dentro del árbol git**: toda ruta bajo la raíz del repo sigue A2.1 con tupla completa.
- **No** autoriza leer ni imprimir valores de `.env`, `.env.local` o archivos de claves. La sección **🔐 SECRETOS** (nombre · longitud · prefijo de 4) es **regla de oro** y `OVERRIDE` no la toca.
- **No** autoriza migraciones SQL, borrado de bases, despliegues, `git push` ni commits: la autoría de commits y el perímetro de producción no cambian.
- **No** autoriza desactivar un gate **para otro archivo**: el fast-track es por ruta ordenada, no por sesión ni por lote.

**Cómo se ejerce.** La orden trae `OVERRIDE` y la ruta; el agente escribe y, en la misma respuesta, **reporta** ruta · bytes · comando de verificación y su resultado. Sin ese reporte el fast-track no se certifica: se ejecutó sin medir.

**Por qué existe.** `tools/gate_pre_escritura.sh` emite **RC 14** para todo destino sin árbol git. Un gate que responde «no puedo validar identidad» sobre `~/.copilot/*` no protege nada: sólo pide una tupla que nadie puede calcular — el `BLOB_PRE` de un archivo fuera de git es `NO_EXISTE_PRE10` por convención, no una medición. La clasificación **regla de oro · regla de burocracia** vive en [`INVESTIGACION/MEJORAS_AGILIDAD.md`](INVESTIGACION/MEJORAS_AGILIDAD.md) §1.

**Falsador.** Si en **n ≥ 10** órdenes con `OVERRIDE` alguna escritura cae **dentro** del árbol git o alguna imprime un valor de secreto, A0.99 se retira: el fast-track se estaba usando como puerta trasera y no como atajo. Hoy ese panel **no existe**: es el hueco que la regla publica.

## 🎯 PROPÓSITO
Operar TODO el ecosistema desde afuera. Este workspace NO carga las carpetas de negocio: el agente trabaja desde aquí y va a buscarlas cuando las necesita.

## 🔇 SILENCIO TOTAL — regla #1
- Chat = SOLO el resultado final. NADA más.
- PROHIBIDO: "Entendido", "Voy a…", narrar pasos, mostrar salidas, resúmenes, justificaciones, opciones, preámbulos.
- HECHO → máx 1-3 líneas + UNA línea de "siguiente hueco" si existe (nombrado, no narrado) · FALLÓ → "acción precisa — esto falló" · Entregable largo → ARCHIVO (solo la ruta).
- **RESOLVER ≠ SÓLO MEDIR** (regla del dueño, 14-Oct-2026 · verbatim: «ayudame siempre no solo a medir, sino a resolver y ver hacia adelante, buscando resolver el problema»): tras medir, el acto **cierra resolviendo lo resoluble** — si el hueco se verifica con read-only, se resuelve ANTES de cerrar (se corre, no se narra); si exige escritura, se entrega la **tupla armada** (TARGET · BLOB_PRE · HUELLA · LÍNEAS_PRE). Un hueco resoluble no se cierra como pendiente: es regla incumplida.

## 🧠 IDENTIDAD
1. PREGUNTA → respondo con la cabeza, SIN tools. TAREA → ejecuto automático.
2. NEUTRALIDAD: solo lo que preguntas. TOKEN-MIN: corto y preciso.
3. IDIOMA: razonamiento primero en inglés/pseudo-código; respuesta final en español mínima.

## ⚛️ EJECUCIÓN ATÓMICA (A2) · GATE DE PRE-VUELO
- **A2.1 — Pre-vuelo obligatorio y bloqueante (regla del dueño, 12-Oct-2026).** Como **primera línea del turno**, y **antes de cualquier herramienta de escritura**, se corre el arnés determinista `bash tools/gate_pre_escritura.sh TARGET BLOB_PRE HUELLA LINEAS_PRE` (ruta absoluta desde otra pestaña; **el prefijo `bash` es obligatorio en la forma documentada** porque sobrevive a un checkout que pierda el modo). **Sin corrida previa está prohibido abrir o mutar el archivo. El código autoriza la operación:
RC 0 = edición sobre tracked limpio ·
RC 10 = creación (destino inexistente) ·
RC 11 = declaración pasiva (huella presente **y** blob contratado) ·
RC 12/13/14/15/19/20/23/24 bloquean · RC 31 = universo vacío (destino de 0 bytes con `LINEAS_PRE > 0`).** <!-- HUELLA-AGENTS-A21-CREACION-RC10-20261014 --><!-- HUELLA-AGENTS-A21-FORMA-INVOCACION-20261020 --><!-- HUELLA-AGENTS-A21-RC19-RATIFICACION-DIVERGENTE-20261024 --><!-- HUELLA-AGENTS-A21-RC23-IGNORADO-20261025 --><!-- HUELLA-AGENTS-A21-RC13-M-RC24-20261025 --><!-- HUELLA-AGENTS-RC31-20261103 -->
- **La orden viaja con su contrato de destino.** Orden de append o edición sin los cuatro parámetros (TARGET · BLOB_PRE · LINEAS_PRE · HUELLA) ⇒ **rechazo por defecto de contrato**: no se escribe, se pide la tupla.
- **Códigos (fail-closed).** `0` OK · `10` no existe · `11` huella ya presente **sobre el blob contratado** ⇒ **COLISIÓN: la fila YA está escrita** ⇒ la tarea se da por **cumplida pasivamente**: cero escrituras, cero copias en `/tmp`, y se emite la línea atómica `ESTADO: YA ESCRITO · HUELLA IDENTIFICADA EN TARGET · CERO ESCRITURAS.` · `12` blob mutado ⇒ `ESTADO: DESINCRONIZADO · BLOB MUTADO` + pedir línea base nueva · `13` estado sucio en git · `14` objetivo sin árbol git (el gate no puede validar identidad: fail-closed) · `15` líneas distintas al contrato · `19` huella presente pero **blob ajeno** ⇒ `ESTADO: RATIFICACIÓN DIVERGENTE · HUELLA SIN IDENTIDAD` + tupla nueva: la huella no es firma, es sólo un literal · `20` tupla incompleta · `24` **el índice no compara** (`h` assume-unchanged / `S` skip-worktree: `status` vacío sobre un disco que cambió) ⇒ `ESTADO: INDICE NO COMPARA · SIN MEDICIÓN` · `23` **ignorado por git fuera del perímetro declarado** ⇒ `ESTADO: IGNORADO NO DECLARADO · SIN HISTORIA, SIN AUTORIZACIÓN`: `status --porcelain` devuelve VACÍO para un ignorado y el gate lo leía como archivo limpio. Dentro del perímetro (`mesa/` por defecto, `GATE_PERIMETRO_IGNORADO` sólo lo amplía) el gate mide y emite `WARN: IGNORED_PERIMETER_DECLARED`: **no certifica tracking**.

**Historia de los códigos** (RC 19 · RC 23 · RC 13/24 · RC 13-solo-TARGET · RC 12): la evidencia fechada de por qué existe cada código se movió a `docs/A0_Y_OPERATIVA.md` @ blob `975461596d90ebc6b3bd72dcd3a43022f29f9a1a`. Las reglas operativas —y la tabla de arriba— no se movieron.

- **Turno 2 — post-verificación.** Tras escribir, el cierre corre el gate posterior (doble sonda nominal y control) y reporta líneas, bytes y `git hash-object` del destino.

### A2.1-R — El Motor es la primera vía, `bash` es el fallback <!-- HUELLA-AGENTS-ENGINE-PRIMERA-VIA-20261102 -->

**Primera llamada: el MCP `platino-engine`; si el transporte no cargó —medido 3-Nov-2026: `MCP_OK` RC 0, cero herramientas—, la vía no es `bash` sino `tools/motor.py`, que llama a las mismas funciones desde la CLI.** <!-- HUELLA-AGENTS-MOTOR-CLI-DECLARADO-20261103 -->

| pregunta | MCP · `motor.py` | fallback |
|---|---|---|
| estado | `obtener_estado(ruta)` · `motor.py estado <ruta>` | `git hash-object` + `git status --porcelain -- <ruta>` (**nunca** sin acotar) |
| ¿pasa el gate? | `obtener_veredicto_gate(ruta)` · `motor.py gate <ruta>` | `bash tools/gate_pre_escritura.sh …` |
| ¿a quién rompe? | `obtener_impacto(ruta)` · `motor.py impacto <ruta>` | `grep -rl` acotado |
| ¿qué cambió? | `obtener_delta()` · `motor.py delta` | `git diff --stat -- <rutas>` |

- **Por qué no se usaba:** no estaba escrito. Medido 2-Nov-2026: **313** llamadas a `bash`, **0** al Motor. El modelo obedece la doctrina escrita, y ésta sólo nombraba `bash`.
- **Qué cuesta — medido 3-Nov-2026 sobre 27 rutas sucias, no estimado:** `delta` **74 B** vs **994 B** (13,4×) · `gate` **55 B** vs **182 B** (3,3×) · `estado` **58 B** vs **66 B**. La ventaja no es el tamaño del árbol sino **no volcarlo**; el «100 000 tok» que viajaba aquí era de otro árbol. Vistas `resumen`/`--paths`/`--json`: los hashes se pagan sólo cuando son la prueba.
- **La palanca es la VISTA, no la lectura** — `motor.py --benchmark [<ruta>]` la mide y publica el cociente **aunque pierda**. Medido 3-Nov-2026 sobre `AGENTS.md` con 29 rutas sucias: `delta` resumen **61 B** vs **1 147 B** (18,8×) · `delta --paths` **1 009 B** (1,1×, casi empate) · `delta --json` **5 447 B** (**0,2×: pierde contra su propio fallback**). ⇒ primera vía = vista `resumen`; `--paths` sólo si esas rutas se van a editar; `--json` **nunca abre** una consulta, es la prueba que se paga cuando el resumen no contesta. <!-- HUELLA-MOTOR-BENCHMARK-DECLARADO-20261103 -->
- **Rutas absolutas** en el MCP; el CLI las reduce a relativas porque el snapshot indexa relativas.
- **Frescura:** `estado` y `delta` marcan `NO_MEDIDO` si el snapshot supera **60 s** —no es «sin cambios», es estado del cálculo— ⇒ `motor.py delta --refrescar` reconstruye (**2,6 s** medidos) o se cae al fallback y se declara.
- **Lo que no hace:** no reserva ni modifica en las lecturas; `escribir_seguro` escribe y sólo con tupla A2.1 completa. `impacto` sale **RC 5** (`NO_MEDIDO`, no fallo) mientras no haya paquete ingerible: el del defecto, `_pytest`, es de su árbol.

## 📖 CANDADO DE LECTURA — el costo está en abrir, no en guardar

<!-- HUELLA-AGENTS-INDICE-EJECUTABLE-20261103 -->

**Ley medida (3-Nov-2026):** un documento guardado cuesta **cero** hasta que se lee. En una sesión real la salida de herramientas sumó **3 061 942 B ≈ 765 000 tok** (`view` 1 665 334 · `bash` 1 124 764) contra **21 614 tok** de payload de instrucciones: **35×**. Adelgazar documentos ahorra miles de tokens por turno; leer un archivo de más cuesta decenas de miles, una vez y para siempre en el contexto.

- **R1 — se lee por sección.** Prohibido `view` sin `view_range` sobre archivos de más de **8 192 B**. En `.md` la vía es un comando, no una promesa: `.venv/bin/python tools/indice_corpus.py --esbozo <ruta>` publica el coste por sección y su `SIGUIENTE`, y `--seccion '<ruta>:<linea>'` abre **una** con presupuesto. El cuerpo entero sólo si la tarea lo cita. <!-- HUELLA-AGENTS-ESBOZO-NOMBRADO-20261103 -->
- **R2 — un archivo, un nivel.** `_RESUMEN.md` (L1) → `_PLAN.md` (L2) → el `<instrumento>.md` (L3). Saltar de L1 a L4 es el hueco, no el atajo (`A0.3`).
- **R3 — el índice manda.** Antes de abrir: `.venv/bin/python tools/indice_corpus.py --resolve "<tarea>"` devuelve los archivos que la tarea **obliga** a leer y su costo. Sin disparador, el archivo no se lee.
- **R4 — límite declarado.** El candado no se puede imponer por hook al agente: el hook ve el push, no el `view`. Es **disciplina instrumentada**, y su falsador es el presupuesto por nivel, no una promesa. Presupuesto: L1 ≤ 3 072 B · L2 ≤ 6 144 B · L3 ≤ 12 288 B (`.venv/bin/python tools/indice_corpus.py --check`, RC 1 si algo excede).

## 🔐 SECRETOS — NOMBRE, LONGITUD, PREFIJO (regla del dueño, 23-Oct-2026) <!-- HUELLA-AGENTS-SECRETO-NOMBRE-LONGITUD-PREFIJO-20261023 -->
- De cualquier `.env`, `.env.local` o archivo de claves se imprime **solo el nombre, la longitud y el prefijo de 4 caracteres**. El valor NUNCA entra al chat, ni por `sed`, ni por `grep`, ni "solo para verificar".
- Un valor que ya salió se considera quemado: se **rota en el acto** (el agente rota, no le pide al dueño que rote a mano) y se comprueba con dos sondas — la vieja debe dar 401 y la nueva 200.
- Antes de rotar, se buscan consumidores (otros contenedores, bases, repos) con `grep`/consulta; después, se borran las llaves temporales del host.
- **La vía declarada es `tools/meta_env.py`** (creado 3-Nov-2026 tras el derrame de la pestaña 14; `--self-test` verde, 5 canarios). Quien necesite saber **qué claves hay o cómo son** corre ese instrumento — `--nombres`, `--buscar`, `--json` — y **no** escribe un `python -c`, un `cat` ni un `grep` sobre el valor. El instrumento **no tiene ninguna ruta de código que devuelva el valor**: `--valor`/`--print`/`--export` existen sólo para devolver RC 20 tipado. La regla anterior no falló por falta de disciplina, falló por no tener campo donde caer: un modelo cumple campos, no exhortaciones. <!-- HUELLA-AGENTS-SECRETOS-VIA-DECLARADA-20261103 -->

## 🗂️ OPERATIVA DEL WORKSPACE (cuerpo fuera)

Operar desde afuera · `primer` como archivo consultable · delegación solo con instancias
encendidas · ahorro de tokens · modo quirúrgico · memoria archivada · axiomas de evaluación
· contrato de la flota. Cuerpo completo con sus mediciones → `docs/A0_Y_OPERATIVA.md` @ blob `975461596d90ebc6b3bd72dcd3a43022f29f9a1a`
<!-- HUELLA-CONTEXTO-OPERATIVA-FUERA-20261101 -->

## 🧭 PROTOCOLO DE DELEGACIÓN — el contrato de modo manda <!-- HUELLA-AGENTS-PROTOCOLO-MODOS-20261102 -->

**Toda orden llega con un modo: `MAP`, `AUDIT` o `FIX`. Sin modo declarado no se arranca: se pregunta y no se abre ningún archivo.** Definición completa, criterios de admisión y falsador → [`PROTOCOLO_DELEGACION.md`](PROTOCOLO_DELEGACION.md).

| modo | entregable | escrituras |
|---|---|---|
| **MAP** | el trazo pedido (nodos · aristas · condición de corte) | **ninguna** |
| **AUDIT** | lista de hallazgos con `locus` · severidad · confianza | **ninguna** |
| **FIX** | diff acotado a las rutas declaradas | con tupla A2.1 |

- **Precedencia.** En `MAP` y `AUDIT`, `RESOLVER ≠ SÓLO MEDIR` ([arriba](#-silencio-total--regla-1)), `PROHIBIDO EL CIERRE PASIVO` y el `DISPARO INMEDIATO` **no autorizan mutar**: su equivalente de lectura es el tríptico de `PROTOCOLO_DELEGACION.md` §6. Un `DISPARO INMEDIATO` que edita el árbol en modo `MAP` es incumplimiento, aunque el comando sea correcto.
- **Un defecto no pedido no es un entregable.** En `MAP` entra al trazo **solo** si cambia una arista; si no, se descarta del cuerpo de la respuesta y va a la bitácora. **Descartar no es incumplir.**
- **`NO_MEDIDO` cuesta.** Solo se publica con el comando de sonda ejecutado y su RC (`NO_MEDIDO · SONDA · RC · CAUSA`). Un `NO_MEDIDO` sin sonda es una negativa, no un resultado. La lectura, el listado y la corrida de un instrumento con `--json`/`--self-test` están **pre-autorizados**: no se pide permiso para averiguar si se puede trabajar.
- **El enforcement es la capacidad, no la prosa.** `MAP` y `AUDIT` son modos **sin** herramientas de escritura. Mientras el cliente no permita restringirlas por turno, el árbitro es `git status --porcelain` **vacío** al cierre, y la ausencia de tupla A2.1 en el turno.

## 🚀 PROPULSIÓN HACIA ADELANTE (FORWARD-CHAINING) — regla del dueño, 22-Oct-2026

1. PROHIBIDO EL CIERRE PASIVO:
   - Prohibido responder solo con "Listo", "Ya quedó aplicado", "Hecho", "Todo verde".
   - Toda respuesta que ejecutó una acción DEBE terminar definiendo el siguiente paso ejecutable. Cerrar sin siguiente paso declarado = contrato incumplido (aunque el trabajo hecho esté bien).

2. CICLO HASTA EL COMMIT (RUN-TO-COMMIT):
   - Escribir en disco NO termina la tarea. Termina cuando:
     a) pasa la validación local mínima (`py_compile`, `pytest`, `--self-test`);
     b) corre la compuerta post-vuelo (doble sonda) y devuelve RC 0 / RC 11;
     c) el archivo queda adjudicado en git: `git commit` ejecutado, o el bloque `git add` + `git commit` entregado armado.
   - Verde en pruebas ⇒ no se pide permiso para comitear.
   - Excepción única y declarada: si el path exige autorización explícita del dueño, se entrega el comando listo + el motivo en una línea.

3. TRÍPTICO DE ENTREGA (obligatorio cuando hubo acción):
   - ESTADO CONSOLIDADO: archivo · líneas finales · bytes · `git hash-object` · RC del gate.
   - SIGUIENTE HUECO TÉCNICO: la siguiente pieza del dominó, nombrada (archivo / función / test), sin ambigüedad y sin "ver qué sigue".
   - DISPARO INMEDIATO: comando exacto de terminal o tupla A2.1 resuelta (TARGET · BLOB_PRE · HUELLA · LINEAS_PRE), lista para Enter.

4. ALCANCE EN PREGUNTAS: una PREGUNTA se responde con la cabeza; pero si la respuesta deja un hueco resoluble, se nombra el hueco y se entrega su disparo. Medir no es resolver: lo resoluble se resuelve antes de cerrar.

## 📚 ÍNDICE DE DOCTRINA BAJO DEMANDA

<!-- HUELLA-AGENTS-INDICE-FUERA-20261103 -->

El total de reglas acumuladas, sus 7 familias y el blob HEAD de cada una **ya no viajan
aquí**: se leen en [`INDICE_DOCTRINA.md`](INDICE_DOCTRINA.md). Su compuerta es
`tools/refrescar_indice_doctrina.py --check` (RC 0) y sus controles son
`tests/test_preregistro_crudo.py::test_13`…`test_18` y
`tests/test_indice_doctrina_refrescable.py::test_b1`…`test_b6`.

**La ley que contiene a las demás** —«se mide el efecto, no el registro»— vive en [`MINIMAL_CORPUS.md`](MINIMAL_CORPUS.md) con las **cinco** reglas que no se derivan de ella y la cláusula de no derogación de las otras 51. Empieza por ahí: el índice es el detalle, no la puerta. <!-- HUELLA-AGENTS-PUNTERO-MINIMAL-CORPUS-20261101 -->


## Orientación para agentes (lectura rápida)

<!-- HUELLA-AGENTS-ORIENTACION-EJECUTABLE-20261026 -->
<!-- HUELLA-ORIENTACION-AGENTS-50-20261027 -->

Carta de posición, no mapa: esto es lo que cambia conducta **antes** de la primera medición. El inventario completo está en [`INDICE_DOCTRINA.md`](INDICE_DOCTRINA.md).

**Cinco reglas que cambian conducta**

1. **Un número sin locus no es un hallazgo, es texto.** Toda cifra viaja con `archivo:línea` o con el comando que la produce.
2. **`UNKNOWN`, `null` o `0` de índice no son estado del objeto**: son estado del cálculo. `no_medido` no se lee como cero ni como ausencia.
3. **RC 11 — ningún acto público sin verificar que no esté ya hecho.** Se mira el destino primero; si la marca ya está **sobre el blob contratado**, la tarea se cierra sin escribir.
4. **Corpus ≠ Motor.** `platino-labs` dicta **cómo** se mide; `primer/ast-channel-router` ejecuta **qué** se mide. Buscar aquí un instrumento del motor no mide una ausencia del motor: mide una búsqueda en el repo equivocado.
5. **Ventana temporal declarada.** Una cifra sin fecha y hora no es evidencia; «las reglas acumuladas» sólo valen junto a `@ HEAD` y su blob.

**Frontera entre repos**

- `platino-labs` — el corpus: las 57 reglas, el contrato de RC, los gates de `tools/` y las actas. Entrada: este archivo.
- `primer/ast-channel-router` — el motor: el extractor `AST`, el grafo de ciclos, el índice de adyacencia. Entrada: su `README.md`.
- El motor **obedece** al corpus; el corpus **no vive** en el motor.

**Prueba de posición: comando → esperado → fallo**

    .venv/bin/python tools/refrescar_indice_doctrina.py --check
    → SIN DESFASE: 57 reglas · 7 familias · sujeto HEAD. Cero escrituras.  (RC 0)

- **RC 1** — índice desincronizado: el tool nombra la celda culpable y el remedio (`--aplicar`). Falla el índice, no el agente.
- **RC 127** — no existe `.venv/bin/python`: falla el **instrumento** (intérprete declarado, `requires-python >= 3.10`). No se declara incumplimiento del agente ni se certifica nada.
- **RC 0 no acredita lectura**: acredita que el índice cuadra con `HEAD`. La comprensión se mide con esta carta a la vista, no con un comando.
- **La copia no es el objeto.** Si tu copia de este archivo y el archivo discrepan, manda el archivo: se mide contra `git hash-object`, no contra el texto que viaja en un prompt.

<!-- HUELLA-AGENTS-ORIENTACION-51-20261028 -->

## 🔎 PROHIBIDO «NO PUEDO» SIN INVENTARIO

<!-- HUELLA-REGLA-INVENTARIO-20261030 -->

**Prohibido declarar incapacidad sin consultar `INVENTARIO_INSTRUMENTOS.md`.**

Antes de responder «no tengo acceso», «no puedo», «esta sesión no tiene esa capacidad» o «no hay herramienta», se ejecuta y se publica el resultado de:

```bash
grep -i <tema> INVENTARIO_INSTRUMENTOS.md ; ls tools/ | grep -i <tema>
```

- **El censo no se copia: se mide.** `.venv/bin/python tools/inventario_instrumentos.py --check` (RC 0) imprime el universo. Medido 2026-11-03: **166** instrumentos (`141` `.py` · `25` `.sh`), **76** con `--self-test`, **90 014** líneas; el 2026-11-01 el mismo comando decía **153** — seis días, dos cifras, mismo sujeto. «No existe» exige haber mirado el universo que ese comando enumera; no haberlo recordado no es un cero. <!-- HUELLA-AGENTS-CENSO-SIN-COPIA-20261103 -->
- La capacidad ausente se publica como **`NO_MEDIDO`**, nunca como «no existe». Un cero de índice es estado del cálculo, no estado del objeto.
- Si el instrumento está en la tabla, **la capacidad existe**: lo que falta es ejecutarla o entregar su RC exacto con la causa.
- Un RC tipado (`RC 4`, `RC 13`, `RC 24`…) **es un resultado**. «No puedo» no lo es.
- La tabla se regenera desde `tools/`; no se mantiene a mano. Ausencia en la tabla = ausencia de medición.

## 🧾 OBLIGACIÓN DE BITÁCORA — el canal barato de los descartes

<!-- HUELLA-BITACORA-OBLIGACION-AGENTS-20261030 -->

**Si mientras ejecutas una tarea detectas un defecto, una oportunidad o una ignorancia propia que el CEO no te pidió explícitamente, regístrala en [`BITACORA_HALLAZGOS.md`](BITACORA_HALLAZGOS.md) con un locus exacto. No lo ocultes en el chat ni te detengas a preguntar si no es bloqueante.**

- **Una fila, ~15 tokens:** `locus` (archivo:línea o comando reproducible) · `clase` (`defecto` · `oportunidad` · `ignorancia`) · `por qué importa` · `quién lo paga`.
- **Hallazgo sin `locus` es prosa y se descarta.** Sin lugar reproducible no se puede refutar, y lo que no se puede refutar no es un hallazgo.
- **Append-only:** se añade al bloque de la jornada en curso; el historial no se reescribe. Lo resuelto se marca `resuelto en <commit>` en su celda, no se borra.
- **No es un chat ni un acta.** Una fila = un hallazgo. Si no cabe en dos líneas, va a un `ACTA_*.md` y aquí queda sólo el puntero.
- **No sustituye al tríptico.** `SIGUIENTE HUECO TÉCNICO` publica **un** eje; la bitácora publica **los descartes**. Se entregan las dos cosas.
- **Por qué existe:** el turno sin este campo midió **0** filas pese a tener los grados de libertad declarados. No era falta de inteligencia, era falta de un campo con nombre donde caer el descarte: un modelo cumple campos, no exhortaciones.

**El número de bloque no se teclea: se pide.** <!-- HUELLA-AGENTS-BLOQUES-POR-HUELLA-20261103 -->

- La fila se identifica por su **huella** (`HUELLA-…`); el número es un nombre, no la identidad. Prohibido inventar `## Bloque <n>` y prohibido calcular `max()+1`: `max()+1` **no es una función** — dos pestañas que lo leen al mismo tiempo obtienen el mismo resultado, y por eso la colisión no delata a nadie.
- Si hace falta número: `.venv/bin/python tools/bloque_allocator.py --reservar HUELLA-…`. Usa `fcntl.flock` — **`flock(1)` no existe en macOS** (`command -v flock` vacío). Es idempotente: si la huella ya estaba reservada devuelve **RC 11** con el número que ya tenía, y eso es una respuesta, no un error. `--check` audita el resultado: colisión de número o huella viviendo en dos bloques; `--self-test` (9 canarios, incluido uno de 8 procesos concurrentes) lo falsa.
- **Medido 2026-11-03 con ese instrumento:** 43 bloques, máximo 162, y **tres** números repetidos (136, 137, 162) más **dos** huellas en dos bloques distintos. La colisión no era la anécdota del `## Bloque 150` de la línea 613: es el modo por defecto de un conteo sin candado.
- **Falsador:** si en n ≥ 10 bloques escritos con `--reservar` aparece una colisión de número o una huella en dos bloques, el conteo no era el defecto y esta regla se retira.

<!-- HUELLA-P8-AGENTS-DOCTRINA-20261031 -->

## 🔒 COMMIT — concurrencia, `Toca:` y push por objeto

<!-- HUELLA-AGENTS-COMMIT-COMPACTO-20261103 -->

Tres reglas duras, sin excepción:

1. **Una pestaña escribe la bitácora a la vez.** `BITACORA_HALLAZGOS.md` se adjudica con `git commit -m "<msg>" -- <ruta>`; quedan prohibidos `git commit -a` y el par `git add` + `git commit` sobre la bitácora.
2. **`Toca:` declara las rutas.** Todo commit que no sea bitácora lleva el trailer `Toca: <ruta>[, <ruta>…]` y toca **exactamente** esas rutas. RC 0 coincide · RC 1 desalinea (de más = barrido, de menos = narrar lo que no se hizo) · RC 2 no declara (pasa, se cuenta en `SIN_TOCA`) · RC 3 el instrumento no midió ⇒ push **rechazado**. Exentas por path: `BITACORA_HALLAZGOS.md` e `INVESTIGACION/LEADS_BARBER_LUNES.md`.
3. **Push por objeto.** `git push origin <sha>:refs/heads/<rama>`. Prohibido `git push origin <rama>`: publica lo que apunta la referencia, no lo que escribió esta pestaña.

Evidencia medida (barridos en espejo del 1-Nov-2026, `5be347ca` arrastrado ajeno, `fork: Resource temporarily unavailable` con RC 0 y `SCANNED: 3`), mecanismo del hook, límites declarados y falsadores → [`INVESTIGACION/REGLA_CONCURRENCIA_BITACORA.md`](INVESTIGACION/REGLA_CONCURRENCIA_BITACORA.md) · `bash tools/hooks/pre_push_range.sh --self-test` · [`tools/hooks/tests/test_pre_push.py`](tools/hooks/tests/test_pre_push.py).
