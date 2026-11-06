# Corpus de metrología de sistemas

[![doctrina](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Falexisromtz-lab%2Fcorpus-medido%2Fmain%2Fbadges%2Freglas.json&query=%24.message&label=doctrina&color=111111&style=flat-square)](docs/DOCTRINA_MANIFIESTO.json)

Este repositorio es la **capa citable** del corpus con el que Platino Labs mide sistemas. No es un
framework ni una librería: es un conjunto de reglas de medición, compuertas de código de retorno y
notas técnicas depositadas con DOI.

La ley que contiene a las demás es una sola: **se mide el efecto, no el registro**. Todo lo demás
—57 reglas en 7 familias— se deriva de ella o la acota. Cinco no se derivan: están en
[`MINIMAL_CORPUS.md`](MINIMAL_CORPUS.md) y el detalle está en [`INDICE_DOCTRINA.md`](INDICE_DOCTRINA.md).

## Qué puedes verificar aquí

## La cifra de arriba no está escrita a mano

**57 reglas · 7 familias** no es texto: es lo que mide
[`tools/medir_reglas.py`](tools/medir_reglas.py) contra el manifiesto
[`docs/DOCTRINA_MANIFIESTO.json`](docs/DOCTRINA_MANIFIESTO.json), que trae cada nombre de regla y el
blob de la familia que lo produce. Cualquiera puede reproducirlo y contradecirlo:

```bash
python3 tools/medir_reglas.py --check      # RC 0 alineado · RC 1 deriva nombrada · RC 2 NO_MEDIDO
python3 tools/medir_reglas.py --self-test  # 23 controles, incluidos los negativos
```

El badge de este repositorio lee [`badges/reglas.json`](badges/reglas.json), y ese archivo sólo lo
reescribe el medidor. Una cifra que no puede contradecirse no es una medición.

## Qué puedes verificar aquí

El PDF y el Markdown de la nota depositada son los mismos bytes que se publicaron con el DOI. Se
comprueban sin confiar en este repositorio:

```bash
shasum -a 256 NOTA_COHERENCIA_VS_COMPLETITUD_20261103.pdf
# c41e3dbec089a6777febbd62f93d323ccc2669406e7c52a85063bfcce5b9f650
shasum -a 256 NOTA_COHERENCIA_VS_COMPLETITUD_20261103.md
# ab787da7df098403c44f5291e76dc253f4a285c134e34af2abb5980a050f67ea
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