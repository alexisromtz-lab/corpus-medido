# Corpus de metrología de sistemas

Este repositorio es la **capa citable** del corpus con el que Platino Labs mide sistemas. No es un
framework ni una librería: es un conjunto de reglas de medición, compuertas de código de retorno y
notas técnicas depositadas con DOI.

La ley que contiene a las demás es una sola: **se mide el efecto, no el registro**. Todo lo demás
—56 reglas en 7 familias— se deriva de ella o la acota. Cinco no se derivan: están en
[`MINIMAL_CORPUS.md`](MINIMAL_CORPUS.md) y el detalle está en [`INDICE_DOCTRINA.md`](INDICE_DOCTRINA.md).

## Qué puedes verificar aquí

```bash
# el índice de doctrina cuadra con este árbol
python tools/refrescar_indice_doctrina.py --check   # RC 0 = SIN DESFASE
```

Ninguna cifra de este repositorio viaja sin `archivo:línea` o sin el comando que la produce. Un
número sin locus es texto, no un hallazgo.

## Notas depositadas

| DOI | Título | Vistas / descargas* |
|---|---|---|
| [10.5281/zenodo.23955654](https://doi.org/10.5281/zenodo.23955654) | Coherencia no es completitud: el punto ciego de `uv pip check` | 0 / 0 |
| [10.5281/zenodo.23459450](https://doi.org/10.5281/zenodo.23459450) | Adjudicación empírica de andamios y contexto masivo | 18 / 3 |
| [10.5281/zenodo.23363121](https://doi.org/10.5281/zenodo.23363121) | Predicción pre-registrada cumplida (768 s) | 9 / 6 |
| [10.5281/zenodo.23329943](https://doi.org/10.5281/zenodo.23329943) | fotonica-monotile: instrumento FDTD 2D TM | 6 / 1 |
| [10.5281/zenodo.23329941](https://doi.org/10.5281/zenodo.23329941) | acustica-monotile: enlace experimental | 4 / 1 |
| [10.5281/zenodo.23288831](https://doi.org/10.5281/zenodo.23288831) | Protocolo de custodia determinista y reserva de ranuras | 7 / 0 |

\* Medido el 2026-11-04 vía `zenodo.org/api/records/<id>` → `stats`. La cifra envejece: se re-mide o
no se publica.

La más reciente —[*Coherencia no es completitud*](docs/NOTA_COHERENCIA_VS_COMPLETITUD_20261103.md)—
documenta un caso medido en un repositorio ajeno: `uv pip check` respondió
`All installed packages are compatible` sobre 117 paquetes y **12,06 s después el mismo intérprete**
lanzó `ModuleNotFoundError: No module named 'prisma'`. La coherencia es una relación entre
declaraciones; la completitud, entre declaraciones y código.

## Licencias

- Código: [Apache 2.0](LICENSE)
- Documentación: [CC BY 4.0](LICENSE-DOCS.md)

## Alcance

Esta es la capa citable. El árbol de trabajo completo —con datos comerciales, prospectos y
material de clientes— no se publica: contiene datos de terceros que no son nuestros para
distribuir. Lo que está aquí es reproducible sin ellos.