# 📚 Índice de doctrina bajo demanda

<!-- HUELLA-INDICE-DOCTRINA-FUERA-20261103 -->

Vivía en `AGENTS.md` hasta el 3-Nov-2026. Se separó por una razón medida: el núcleo
se inyecta en **cada** turno, y esta tabla —siete filas con todos los nombres de regla
y el blob HEAD de cada familia— se pagaba entera para no leerse. Aquí cuesta cero
hasta que se abre; `AGENTS.md` conserva el puntero.

- **Compuerta:** `tools/refrescar_indice_doctrina.py --check` (RC 0 = índice == sujeto).
- **Escritor único:** `tools/refrescar_indice_doctrina.py --aplicar`.
- **Controles:** `tests/test_preregistro_crudo.py::test_13`…`test_18` y
  `tests/test_indice_doctrina_refrescable.py::test_b1`…`test_b6`.


<!-- HUELLA-AGENTS-NUCLEO-Y-DOCTRINA-20261024 -->

El 24-Oct-2026 el archivo se partió en **núcleo** (esto) y **doctrina bajo demanda** (7 familias en `docs/doctrina/`). Nada se retiró: las **58** reglas acumuladas siguen vigentes y se consultan cuando la tarea las toca. Un hueco que la regla resuelve no se cierra sin haberla leído. <!-- HUELLA-AGENTS-REGLAS-40-20261025 --> <!-- HUELLA-AGENTS-REGLAS-43-20261025 --> <!-- HUELLA-AGENTS-REGLAS-44-20261025 --> <!-- HUELLA-AGENTS-REGLAS-45-20261025 -->

**La ley que contiene a las demás** —«se mide el efecto, no el registro»— vive en [`MINIMAL_CORPUS.md`](MINIMAL_CORPUS.md) con las **cinco** reglas que no se derivan de ella y la cláusula de no derogación de las otras 51. Empieza por ahí: la tabla de abajo es el detalle, no la puerta. <!-- HUELLA-AGENTS-PUNTERO-MINIMAL-CORPUS-20261101 -->

| familia | reglas | archivo | blob HEAD |
|---|---|---|---|
| Medición y procedencia | MEDICIÓN CON BLOB · MEDICIÓN CON UNIDAD · RC CON CAUSA DECLARADA · VERIFICADOR CON RE-VERIFICACIÓN · AUDITORÍA CON BLOB · CAMPO COPIADO · ESTADO TRANSITORIO NO ES ESTADO DEL OBJETO · CLAVE VECINA NO REFUTA · UN RELOJ DE PARED NO ES UN RELOJ DE DURACIÓN | [`docs/doctrina/01_medicion.md`](docs/doctrina/01_medicion.md) | `225a61abb195492e2161ef26d8ff82c91848079f` |
| Predicción | PREDICCIÓN PRE-REGISTRADA · PREDICCIÓN CON cota_error · PREDICCIÓN CON TERRENO DECLARADO · PREDICCIÓN NO EJERCITADA · ESTADOS Y MECANISMO DE PREDICCIÓN · PREDICCIÓN BIFURCADA | [`docs/doctrina/02_prediccion.md`](docs/doctrina/02_prediccion.md) | `ffb83f9d9654184860c17c21fea867fca00dd933` |
| Instrumento | FALSO VERDE EN LA DIRECCIÓN PELIGROSA · EL DIFF QUE NO MIRA EL COMMIT · INSTRUMENTO VS PREDICCIÓN · FALSO ROJO · INSTRUMENTO CON SCOPE DECLARADO · NOMBRE EQUIVOCADO EN LA LITERATURA · AST O NADA · DESFASE DE VENTANA · PROTOCOLO DE SOLUCIÓN AUTOAUDITABLE · LA LÍNEA BASE NO ES UN DISCRIMINADOR DE AUTORÍA · UN AVISO ES NOMBRE, JUICIO Y STREAM · PLAZO MENOR QUE EL COSTE DEL SUJETO · UNA REGLA DECLARADA VENCE AL DEFAULT non_code | [`docs/doctrina/03_instrumento.md`](docs/doctrina/03_instrumento.md) | `43519eb1444da605deb751598ff050f6c9ff901f` |
| Commit y estado | TURNO ATÓMICO · DRIFT DE HEAD ≠ COMMIT EN RAMA EQUIVOCADA · PROPIEDAD DE ARCHIVO SUCIO · COMMIT SIN ARRASTRE · ÍNDICE PRIVADO POR PESTAÑA · MECANISMO ADOPTADO A MEDIAS · COMMIT SIN ARRASTRE INSTRUMENTADO · MENSAJE DE COMMIT Y CERROJO POR GITDIR · LEY DE LA RANURA AUSENTE · EL GUARDIÁN NO PUEDE GUARDARSE A SÍ MISMO · Regla 51 | [`docs/doctrina/04_commit_y_estado.md`](docs/doctrina/04_commit_y_estado.md) | `7f6c713aa8250e554468d4efe22f2be24e3c215a` |
| Contrato y taxonomía RC | TAXONOMÍA DE RANGOS RC · TAXONOMÍA CON REGISTRO · CORRECCIÓN CON CADENA · MECANISMO SIN CONTRATO · NIVEL DE VERIFICACIÓN Y SU EVIDENCIA · AUTORREFERENCIA FALSABLE · TOMBSTONE SOLO PARA CLAIMS VIGENTES · EL TÉRMINO MEDIO · SQLite del despachador: quiescencia acotada de WAL vacío · Adenda 30-Oct-2026 · A2.3 | [`docs/doctrina/05_contrato_y_rc.md`](docs/doctrina/05_contrato_y_rc.md) | `e4757fc1be25d3eee5e75d66a1b71fbb49ca8d42` |
| Universo, lector y controles | CONVENCIÓN CON LECTOR · DEFAULT NO_MEDIDO · SECCIÓN QUE APAGA EL CONTROL | [`docs/doctrina/06_universo_y_lector.md`](docs/doctrina/06_universo_y_lector.md) | `da94db52a80138acccdf6e67804db5a394d79749` |
| Auditoría y negocio | BLOQUEO CON PLAZO · AUDITORÍA CON CAMINO · TIPO DE CAMINO · VENTANA TEMPORAL DECLARADA · ACTO PÚBLICO CON CHEQUEO DE EXISTENCIA PREVIA | [`docs/doctrina/07_auditoria_y_negocio.md`](docs/doctrina/07_auditoria_y_negocio.md) | `c1140548000d775f4fe6dd96219e3c24f0d358bb` |
<!-- HUELLA-AGENTS-INDICE-BLOB-FULL-20261025 --> <!-- HUELLA-AGENTS-REFRESH-BLOB-20261025 --> <!-- HUELLA-AGENTS-BLOB-05-REFRESH-20261025 --> <!-- HUELLA-AGENTS-HEAD05-20261025 --> <!-- HUELLA-AGENTS-BLOB05-ADJUDICADO-20261025 --> <!-- HUELLA-AGENTS-BLOB05-MARCA-FUERA-DE-FILA-20261025 --> <!-- HUELLA-AGENTS-ESCALERA-L1L2L3-20261025 --> <!-- HUELLA-AGENTS-BLOB05-RESURRECCION-20261026 --> <!-- HUELLA-AGENTS-INDICE-BLOB-05-20261026 --> <!-- HUELLA-AGENTS-REFRESCO-BLOB05-20261030 --> <!-- HUELLA-AGENTS-BLOB04-ADENDA-RC103-20261030 --> <!-- HUELLA-AGENTS-REFRESCO-CONTRATO-ROJOS-20261030 --> <!-- HUELLA-AGENTS-INDICE-BLOB-REFRESCO-030-20261031 --> <!-- HUELLA-REFRESCO-INDICE-05-TRASPASO-CONTEXTO-20261031 -->

<!-- HUELLA-CONTEXTO-ADDENDAS-FUERA-20261101: la evidencia del índice se mueve, la regla no. -->

Las adendas que sostienen esta tabla —el historial de `chars` de cada fila, el caso
del `sha16` que no era un blob, el primer y el segundo bump, §EL TÉRMINO MEDIO y sus
tres proyecciones— **ya no viajan en el núcleo**: se leen cuando se toca el índice
doctrinal o se cita cualquiera de sus cifras →
[`docs/DOCTRINA_ADDENDAS_INDICE.md`](docs/DOCTRINA_ADDENDAS_INDICE.md).
Si esta tabla y ese archivo discrepan, manda la tabla: la fija
`tests/test_preregistro_crudo.py::test_13`.
