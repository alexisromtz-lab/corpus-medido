# MINIMAL_CORPUS — la ley, y las 5 reglas que no se derivan de ella

<!-- HUELLA-MINIMAL-CORPUS-LEY-EFECTO-20261101 -->

**Este archivo no es la constitución.** La constitución es [`AGENTS.md`](AGENTS.md): 58 reglas, 7 familias. Este archivo es un **filtro**, no un reemplazo: nombra la ley de la que las 58 son casos y conserva sólo las reglas que **no** se deducen de ella. No copia ninguna: las apunta por ruta.

## Ley 1 — se mide el efecto, no el registro

> El sistema mide el **efecto** —el bundle en producción, la fila en la base, el dinero cobrado, el archivo que el lector puede abrir— y no el **registro** —la rama, el nombre de la migración, el commit, la huella—. Todo test corre contra el efecto.

## Criterio de supervivencia

Una regla sobrevive a la Ley 1 sólo si **no** puede deducirse de ella. Las que se deducen *son* la ley aplicada y no se repiten aquí: repetirlas crea una segunda fuente de verdad que en el siguiente refresco contradice a la primera — el defecto que le costó a `CLAUDE.md` sus 7 038 bytes duplicados.

Corolarios que se retiran de este filtro, no del corpus: las 9 reglas de la familia *Medición y procedencia* son la Ley 1 vista por caso.

## Las 5 que sobreviven

| # | regla | por qué no se deriva de la Ley 1 | texto completo |
|---|---|---|---|
| 1 | **Predicción pre-registrada** | La ley dice qué medir; no impide mover la portería después de medir. | [`docs/doctrina/02_prediccion.md`](docs/doctrina/02_prediccion.md) |
| 2 | **Universo declarado y con lector** | La ley dice qué se mide; no dice sobre qué población, ni que alguien deba leerlo. | [`docs/doctrina/06_universo_y_lector.md`](docs/doctrina/06_universo_y_lector.md) |
| 3 | **Ventana temporal declarada** | Un efecto sin fecha no es un efecto: no se puede refutar ni repetir. | [`docs/doctrina/07_auditoria_y_negocio.md`](docs/doctrina/07_auditoria_y_negocio.md) |
| 4 | **Alcance del instrumento declarado** | La ley mide el efecto; no dice qué dejó de mirar el instrumento que lo mide. | [`docs/doctrina/03_instrumento.md`](docs/doctrina/03_instrumento.md) |
| 5 | **Adjudicación por ruta, nunca por índice compartido** | La ley mide el efecto, no protege el registro mientras se escribe: es higiene del registro. | [`INVESTIGACION/REGLA_CONCURRENCIA_BITACORA.md`](INVESTIGACION/REGLA_CONCURRENCIA_BITACORA.md) |

Las otras **51** no se derogan: siguen vigentes en [`AGENTS.md`](AGENTS.md) y se consultan cuando la tarea las toca.

## Falsador

Si en **n ≥ 10** tareas cerradas leyendo sólo este archivo aparece **≥ 1** caso en que una de las 51 reglas restantes habría cambiado la decisión, el filtro está mal calibrado y esa regla sube a la tabla. Hoy ese panel **no existe**: es el hueco que este archivo publica.

## Lo que este archivo no es

No es una segunda constitución, no deroga nada, y no se lee *en lugar* de [`AGENTS.md`](AGENTS.md) cuando la tarea toca las 51 restantes. Es la puerta barata para arrancar una tarea que la Ley 1 ya cubre.
