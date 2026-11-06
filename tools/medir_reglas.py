#!/usr/bin/env python3
# HUELLA-MEDIDOR-REGLAS-20261106
"""Medidor de reglas del corpus: la cifra del badge, derivada y no tecleada.

Sujeto por defecto: ``docs/DOCTRINA_MANIFIESTO.json`` —7 familias, N reglas—.

El manifiesto **no se escribe a mano**: se emite desde los encabezados ``## `` de
la doctrina con

    python3 tools/medir_reglas.py --sujeto doctrinal --ruta <DIR> \\
        --emitir-manifiesto docs/DOCTRINA_MANIFIESTO.json

Superficies que ``--check`` coteja contra el manifiesto:

* ``INDICE_DOCTRINA.md`` — columna ``reglas`` de las 7 filas de doctrina.
* los documentos que declaran la cifra (``README.md``, ``MINIMAL_CORPUS.md``,
  ``VISION_OPEN_SOURCE.md``, ``AGENTS.md``, ``INDICE_DOCTRINA.md``).
* ``MINIMAL_CORPUS.md`` — encabezados ``## `` contra las reglas no derivadas
  que el mismo archivo declara con número en palabras.

Un número que no puede diferir no es evidencia: si una superficie dice otra
cosa, este instrumento devuelve RC 1 y nombra la superficie culpable.

Códigos de retorno: 0 alineado · 1 deriva medida · 2 NO_MEDIDO · 20 argumentos.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANIFIESTO = RAIZ / "docs" / "DOCTRINA_MANIFIESTO.json"
INDICE = RAIZ / "INDICE_DOCTRINA.md"
ENDPOINT = RAIZ / "badges" / "reglas.json"
MINIMAL = RAIZ / "MINIMAL_CORPUS.md"
DOCUMENTOS = (
    "README.md",
    "MINIMAL_CORPUS.md",
    "VISION_OPEN_SOURCE.md",
    "AGENTS.md",
    "INDICE_DOCTRINA.md",
)

MARCA_ENCABEZADO = "## "
SEPARADOR_NOMBRES = " · "
RE_ENCABEZADO_RUIDO = re.compile(r"^[^\wÁÉÍÓÚÑáéíóúñ§`*]+")
# La cifra puede venir con énfasis en medio (``las **56** reglas``) o sin la
# palabra que la nombra (``las 56 son casos``). Las tres formas son la misma
# afirmación: el total del corpus. Un medidor que sólo vea la primera deja el
# documento diciendo 58 en una cláusula y 56 en la siguiente.
RE_REGLA_EN_PROSA = re.compile(r"(?<![\d.])(\d+)(\*\*)?\s+reglas?\b")
RE_FAMILIA_EN_PROSA = re.compile(r"(?<![\d.])(\d+)(\*\*)?\s+familias?\b")
RE_REGLA_ELIPSIS = re.compile(r"\blas (\d+)\b(?=\s+son casos)")
RE_ENLACE_DOCTRINA = "docs/doctrina/"

CALIFICADORES_ANTES = (
    "otras ", "otras\u00a0", "restantes", "no se derivan", "no se deducen",
    "de la familia", "que no se", "suelen",
)
CALIFICADORES_DESPUES = (
    "restantes", "de la familia", "que no se", "que sobreviven", "no derivadas",
)

NUMERO_EN_PALABRAS = {
    "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
    "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12,
}
RE_NO_DERIVADAS = re.compile(
    r"\b(" + "|".join(NUMERO_EN_PALABRAS) + r")\s+(?:reglas\s+)?(?:que\s+)?no\s+se\s+(?:derivan|deducen)\b",
    re.IGNORECASE,
)


class NoMedido(Exception):
    """El sujeto no se pudo medir. Nunca degrada a cero."""


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def sha_blob(datos):
    """SHA-1 del blob git de ``datos`` (misma identidad que ``git hash-object``)."""
    return hashlib.sha1(b"blob %d\0" % len(datos) + datos).hexdigest()


def nombre_de_encabezado(texto):
    """Nombre canónico de una regla a partir del texto del encabezado.

    ``## 🔬 MEDICIÓN CON BLOB — regla del dueño, 22-Oct-2026`` → ``MEDICIÓN CON BLOB``.
    El corte por ``—`` reproduce los nombres que el índice público ya publica:
    el emoji es adorno y lo que sigue al guion es procedencia, no nombre.
    """
    limpio = texto.strip()
    # Quita el separador de pieza de título que GitHub añade si existe.
    limpio = re.sub(r"\s+#+\s*$", "", limpio)
    limpio = RE_ENCABEZADO_RUIDO.sub("", limpio)
    return limpio.split(" — ")[0].strip()


def encabezados(texto):
    return [l[len(MARCA_ENCABEZADO):] for l in texto.splitlines() if l.startswith(MARCA_ENCABEZADO)]


def medido_ahora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# Lectores
# --------------------------------------------------------------------------
def leer_doctrina(directorio, familias=None):
    """Cuenta las reglas de ``<directorio>/*.md`` por encabezados ``## ``."""
    directorio = Path(directorio)
    if not directorio.is_dir():
        raise NoMedido("no existe el directorio doctrinal: %s" % directorio)
    archivos = sorted(directorio.glob("*.md"))
    if not archivos:
        raise NoMedido("universo vacío: 0 archivos .md en %s" % directorio)
    salida = []
    for i, f in enumerate(archivos):
        crudo = f.read_bytes()
        nombres = [nombre_de_encabezado(h) for h in encabezados(crudo.decode("utf-8"))]
        nombres = [n for n in nombres if n]
        familia = familias[i] if familias and i < len(familias) else f.stem
        salida.append({
            "familia": familia,
            "archivo": f.name,
            "reglas": len(nombres),
            "nombres": nombres,
            "blob": sha_blob(crudo),
        })
    return salida


def leer_familias_del_indice(ruta=INDICE):
    """Orden y nombre de las familias tal como los publica el índice."""
    ruta = Path(ruta)
    if not ruta.is_file():
        return None
    familias = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if not linea.startswith("|") or RE_ENLACE_DOCTRINA not in linea:
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if celdas:
            familias.append(celdas[0])
    return familias or None


def leer_manifiesto(ruta=MANIFIESTO):
    ruta = Path(ruta)
    if not ruta.is_file():
        raise NoMedido("no existe el manifiesto: %s" % ruta)
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise NoMedido("manifiesto ilegible (%s): %s" % (ruta, exc))
    familias = datos.get("familias")
    if not isinstance(familias, list) or not familias:
        raise NoMedido("manifiesto sin familias: %s" % ruta)
    for fila in familias:
        if not isinstance(fila, dict) or not isinstance(fila.get("nombres"), list):
            raise NoMedido("manifiesto con familia malformada en %s" % ruta)
        if fila["nombres"] != [str(n) for n in fila["nombres"]]:
            raise NoMedido("manifiesto con nombres no textuales en %s" % ruta)
    total = sum(len(f["nombres"]) for f in familias)
    declarado = datos.get("total_reglas")
    if declarado is not None and declarado != total:
        raise NoMedido(
            "manifiesto incoherente: total_reglas=%r pero la suma de familias es %d"
            % (declarado, total)
        )
    if total == 0:
        raise NoMedido("universo vacío: el manifiesto no declara ninguna regla")
    return datos, total


def leer_indice(ruta=INDICE):
    """Filas de la tabla doctrinal: familia, nombres y celdas intactas."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise NoMedido("no existe el índice: %s" % ruta)
    filas = []
    for numero, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.startswith("|") or RE_ENLACE_DOCTRINA not in linea:
            continue
        celdas = linea.strip().strip("|").split("|")
        nombres = [n.strip() for n in celdas[1].split(SEPARADOR_NOMBRES.strip()) if n.strip()]
        filas.append({
            "linea": numero,
            "familia": celdas[0].strip(),
            "nombres": nombres,
            "archivo": celdas[2].strip() if len(celdas) > 2 else "",
        })
    if not filas:
        raise NoMedido("índice sin filas de doctrina: %s" % ruta)
    return filas


def _es_total(linea, inicio, fin):
    """Distingue la cifra del corpus de una cifra de subconjunto.

    ``las 51 reglas restantes``, ``las 9 reglas de la familia`` y ``las 5 reglas
    que no se derivan`` no son la cifra del corpus: reescribirlas sería destruir
    significado. El instrumento sólo toca lo que puede probar que es el total.
    """
    antes = linea[max(0, inicio - 40):inicio].lower()
    despues = linea[fin:fin + 30].lower()
    if any(q in antes for q in CALIFICADORES_ANTES):
        return False
    if any(q in despues for q in CALIFICADORES_DESPUES):
        return False
    return True


def _patrones():
    """Pares (clave, patrón) que declaran el total, en sus tres formas."""
    return [
        ("reglas", RE_REGLA_EN_PROSA),
        ("reglas", RE_REGLA_ELIPSIS),
        ("familias", RE_FAMILIA_EN_PROSA),
    ]


def leer_figuras(paths=DOCUMENTOS, raiz=RAIZ, solo_totales=True):
    """Apariciones de la cifra en prosa, con su columna exacta."""
    salida = {"reglas": [], "familias": []}
    for nombre in paths:
        ruta = Path(raiz) / nombre
        if not ruta.is_file():
            continue
        for numero, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            for clave, patron in _patrones():
                for m in patron.finditer(linea):
                    if solo_totales and not _es_total(linea, m.start(1), m.end(1)):
                        continue
                    salida[clave].append({
                        "documento": nombre,
                        "linea": numero,
                        "valor": int(m.group(1)),
                        "col_inicio": m.start(1),
                        "col_fin": m.end(1),
                    })
    return salida


def leer_minimal(ruta=MINIMAL):
    """Encabezados de MINIMAL_CORPUS contra las reglas que declara no derivadas."""
    ruta = Path(ruta)
    if not ruta.is_file():
        return None
    texto = ruta.read_text(encoding="utf-8")
    m = RE_NO_DERIVADAS.search(texto)
    declaradas = NUMERO_EN_PALABRAS[m.group(1).lower()] if m else None
    return {"encabezados": len(encabezados(texto)), "declaradas": declaradas}


# --------------------------------------------------------------------------
# Medición
# --------------------------------------------------------------------------
def medir(manifiesto=MANIFIESTO, indice=INDICE, documentos=DOCUMENTOS, minimal=MINIMAL,
          raiz=RAIZ):
    """Coteja todas las superficies contra el manifiesto. RC 0/1/2."""
    manifiesto = Path(manifiesto)
    try:
        datos, total = leer_manifiesto(manifiesto)
        filas = leer_indice(indice)
    except NoMedido as exc:
        return {
            "veredicto": "NO_MEDIDO",
            "causa": str(exc),
            "medido_en": medido_ahora(),
        }, 2

    n_familias = len(datos["familias"])
    deriva = []

    # Superficie 1 — índice: una fila por familia y los mismos nombres.
    if len(filas) != n_familias:
        deriva.append({
            "superficie": "INDICE_DOCTRINA.md",
            "clase": "FAMILIAS_DESALINEADAS",
            "detalle": "índice %d filas · manifiesto %d familias" % (len(filas), n_familias),
        })
    for fila, ref in zip(filas, datos["familias"]):
        faltan = [n for n in ref["nombres"] if n not in fila["nombres"]]
        sobran = [n for n in fila["nombres"] if n not in ref["nombres"]]
        if faltan or sobran:
            deriva.append({
                "superficie": "INDICE_DOCTRINA.md:%d" % fila["linea"],
                "clase": "NOMBRES_DESALINEADOS",
                "detalle": "%s · faltan=%s sobran=%s" % (fila["familia"], faltan, sobran),
            })

    # Superficie 2 — documentos que declaran la cifra.
    figuras = leer_figuras(documentos, raiz)
    for aparicion in figuras["reglas"]:
        if aparicion["valor"] != total:
            deriva.append({
                "superficie": "%s:%d" % (aparicion["documento"], aparicion["linea"]),
                "clase": "CIFRA_DESALINEADA",
                "detalle": "declara %d reglas · manifiesto %d" % (aparicion["valor"], total),
            })
    for aparicion in figuras["familias"]:
        if aparicion["valor"] != n_familias:
            deriva.append({
                "superficie": "%s:%d" % (aparicion["documento"], aparicion["linea"]),
                "clase": "CIFRA_DESALINEADA",
                "detalle": "declara %d familias · manifiesto %d" % (aparicion["valor"], n_familias),
            })
    if not figuras["reglas"]:
        deriva.append({
            "superficie": "documentos",
            "clase": "CIFRA_SIN_LECTOR",
            "detalle": "ningún documento declara la cifra: no hay nada que pueda diferir",
        })

    # Superficie 3 — MINIMAL_CORPUS: encabezados contra lo que el archivo declara.
    mini = leer_minimal(minimal)
    if mini and mini["declaradas"] is not None and mini["encabezados"] != mini["declaradas"]:
        deriva.append({
            "superficie": "MINIMAL_CORPUS.md",
            "clase": "NO_DERIVADAS_DESALINEADAS",
            "detalle": "%d encabezados · declara %d" % (mini["encabezados"], mini["declaradas"]),
        })

    informe = {
        "sujeto": "docs/DOCTRINA_MANIFIESTO.json :: reglas por familia",
        "origen": datos.get("origen", {}),
        "medido_en": medido_ahora(),
        "total_reglas": total,
        "familias": [
            {"familia": f["familia"], "archivo": f.get("archivo", ""), "reglas": len(f["nombres"])}
            for f in datos["familias"]
        ],
        "superficies": {
            "indice_filas": len(filas),
            "indice_reglas": sum(len(f["nombres"]) for f in filas),
            "documentos_medidos": sorted({a["documento"] for a in figuras["reglas"]}),
            "minimal": mini,
        },
        "deriva": deriva,
        "veredicto": "ALINEADO" if not deriva else "DERIVA",
    }
    return informe, (0 if not deriva else 1)


# --------------------------------------------------------------------------
# Endpoint y aplicación
# --------------------------------------------------------------------------
def endpoint(total, n_familias, etiqueta="doctrina", color="111111"):
    return {
        "schemaVersion": 1,
        "label": etiqueta,
        "message": "%d rules · %d families" % (total, n_familias),
        "color": color,
        "cacheSeconds": 3600,
    }


def aplicar(manifiesto=MANIFIESTO, indice=INDICE, documentos=DOCUMENTOS, destino=ENDPOINT,
            raiz=RAIZ):
    """Reescribe índice, documentos y endpoint desde el manifiesto. Un solo escritor."""
    datos, total = leer_manifiesto(manifiesto)
    n_familias = len(datos["familias"])
    escritos = []

    # 1. Endpoint shields.io
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(endpoint(total, n_familias), indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8")
    escritos.append(str(destino))

    # 2. Columna `reglas` del índice (solo la celda 2; el resto de la fila no se toca).
    indice = Path(indice)
    lineas = indice.read_text(encoding="utf-8").splitlines(keepends=True)
    tocado = False
    for i, linea in enumerate(lineas):
        if not linea.startswith("|") or RE_ENLACE_DOCTRINA not in linea:
            continue
        celdas = linea.rstrip("\n").strip().strip("|").split("|")
        familia = celdas[0].strip()
        ref = next((f for f in datos["familias"] if f["familia"] == familia), None)
        if ref is None:
            continue
        celdas[1] = " " + SEPARADOR_NOMBRES.join(ref["nombres"]) + " "
        lineas[i] = "|" + "|".join(celdas) + "|\n"
        tocado = True
    if tocado:
        indice.write_text("".join(lineas), encoding="utf-8")
        escritos.append(str(indice))

    # 3. Cifras en prosa: sólo los tramos que el medidor probó que son el total.
    figuras = leer_figuras(documentos, raiz)
    por_documento = {}
    for clave, valor in (("reglas", total), ("familias", n_familias)):
        for aparicion in figuras[clave]:
            por_documento.setdefault(aparicion["documento"], {}).setdefault(
                aparicion["linea"], []).append((aparicion, valor))
    for nombre, lineas in por_documento.items():
        ruta = Path(raiz) / nombre
        contenido = ruta.read_text(encoding="utf-8").splitlines(keepends=True)
        for numero, tramos in lineas.items():
            linea = contenido[numero - 1]
            for aparicion, valor in sorted(tramos, key=lambda x: -x[0]["col_inicio"]):
                linea = linea[:aparicion["col_inicio"]] + str(valor) + linea[aparicion["col_fin"]:]
            contenido[numero - 1] = linea
        ruta.write_text("".join(contenido), encoding="utf-8")
        escritos.append(str(ruta))
    return escritos


# --------------------------------------------------------------------------
# Autocontroles
# --------------------------------------------------------------------------
def _fixture(directorio, familias, documento_total=None):
    """Construye un corpus mínimo coherente de ``suma`` reglas."""
    base = Path(directorio)
    (base / "docs" / "doctrina").mkdir(parents=True, exist_ok=True)
    (base / "badges").mkdir(parents=True, exist_ok=True)
    datos = {"origen": {"repo": "fixture"}, "familias": []}
    filas = []
    for i, (familia, nombres) in enumerate(familias, 1):
        archivo = "0%d_fixture.md" % i
        (base / "docs" / "doctrina" / archivo).write_text(
            "# %s\n\n" % familia + "".join("## %s — regla del dueño\n\ncuerpo\n\n" % n for n in nombres),
            encoding="utf-8",
        )
        datos["familias"].append({"familia": familia, "archivo": archivo, "nombres": nombres})
        filas.append("| %s | %s | [`docs/doctrina/%s`](docs/doctrina/%s) | `0000` |"
                     % (familia, SEPARADOR_NOMBRES.join(nombres), archivo, archivo))
    datos["total_reglas"] = sum(len(f["nombres"]) for f in datos["familias"])
    (base / "docs" / "DOCTRINA_MANIFIESTO.json").write_text(
        json.dumps(datos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (base / "INDICE_DOCTRINA.md").write_text(
        "# Índice\n\n| familia | reglas | archivo | blob HEAD |\n|---|---|---|---|\n"
        + "\n".join(filas) + "\n", encoding="utf-8")
    total = datos["total_reglas"] if documento_total is None else documento_total
    (base / "MINIMAL_CORPUS.md").write_text(
        "# Minimal\n\nEste archivo no es la constitución: %d reglas, %d familias.\n\n"
        "## no derivada uno\n\n## no derivada dos\n" % (total, len(familias)),
        encoding="utf-8")
    return base


def _caso(nombre, esperado, obtenido):
    return {"caso": nombre, "esperado": esperado, "obtenido": obtenido, "ok": esperado == obtenido}


def self_test():
    controles = []
    with tempfile.TemporaryDirectory() as tmp:
        base = _fixture(tmp, [("Uno", ["A", "B", "C"]), ("Dos", ["D", "E"])])
        manifiesto = base / "docs" / "DOCTRINA_MANIFIESTO.json"
        indice = base / "INDICE_DOCTRINA.md"
        minimal = base / "MINIMAL_CORPUS.md"

        # C1 — corpus coherente: verde y con la cifra exacta.
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C1_coherente_rc0", 0, rc))
        controles.append(_caso("C1_cuenta_5", 5, informe.get("total_reglas")))

        # C2 — el directorio doctrinal mide lo mismo que el manifiesto.
        salida = leer_doctrina(base / "docs" / "doctrina")
        controles.append(_caso("C2_encabezados_5", 5, sum(f["reglas"] for f in salida)))
        controles.append(_caso("C2_nombres", ["A", "B", "C", "D", "E"],
                               [n for f in salida for n in f["nombres"]]))

        # C3 — deriva del índice: un nombre de menos ⇒ RC 1 nombrando la fila.
        original = indice.read_text(encoding="utf-8")
        indice.write_text(original.replace(" · C", ""), encoding="utf-8")
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C3_indice_deriva_rc1", 1, rc))
        controles.append(_caso("C3_clase", "NOMBRES_DESALINEADOS", informe["deriva"][0]["clase"]))
        indice.write_text(original, encoding="utf-8")

        # C4 — cifra en prosa desalineada ⇒ RC 1.
        (base / "MINIMAL_CORPUS.md").write_text(
            "# Minimal\n\nEste archivo no es la constitución: 56 reglas, 2 familias.\n", encoding="utf-8")
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C4_prosa_deriva_rc1", 1, rc))
        controles.append(_caso("C4_clase", "CIFRA_DESALINEADA", informe["deriva"][0]["clase"]))

        # C5 — --aplicar reconstruye lo coherente byte a byte (control de ida y vuelta).
        aplicar(manifiesto, indice, ("MINIMAL_CORPUS.md",), base / "badges" / "reglas.json", base)
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C5_aplicar_cierra_deriva", 0, rc))
        controles.append(_caso("C5_prosa_restaurada", True, "5 reglas" in (base / "MINIMAL_CORPUS.md").read_text(encoding="utf-8")))

        # C6 — manifiesto ausente ⇒ RC 2, nunca 0.
        _, rc = medir(base / "no-existe.json", indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C6_sin_manifiesto_rc2", 2, rc))

        # C7 — manifiesto con universo vacío ⇒ RC 2.
        vacio = base / "vacio.json"
        vacio.write_text(json.dumps({"familias": [{"familia": "x", "nombres": []}]}), encoding="utf-8")
        _, rc = medir(vacio, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C7_universo_vacio_rc2", 2, rc))

        # C8 — manifiesto incoherente (total ≠ suma) ⇒ RC 2.
        roto = base / "roto.json"
        roto.write_text(json.dumps({"total_reglas": 99, "familias": [{"familia": "x", "nombres": ["A"]}]}),
                        encoding="utf-8")
        _, rc = medir(roto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C8_total_incoherente_rc2", 2, rc))

        # C9 — endpoint: la cifra del badge sale del manifiesto.
        datos, total = leer_manifiesto(manifiesto)
        ep = endpoint(total, len(datos["familias"]))
        controles.append(_caso("C9_endpoint_mensaje", "5 rules · 2 families", ep["message"]))
        controles.append(_caso("C9_endpoint_schema", 1, ep["schemaVersion"]))

        # C10 — el nombre del encabezado se corta en el guion largo, no en el emoji.
        controles.append(_caso("C10_nombre", "MEDICIÓN CON BLOB",
                               nombre_de_encabezado("🔬 MEDICIÓN CON BLOB — regla del dueño, 22-Oct-2026")))
        controles.append(_caso("C10_nombre_sin_emoji", "Regla 51",
                               nombre_de_encabezado("Regla 51 — ID de promesa canónico, nunca autoasignado")))

        # C13 — la cifra con énfasis en medio y la cifra sin la palabra que la nombra.
        mini5 = base / "MINIMAL_CORPUS.md"
        mini5.write_text(
            "Nada se retiró: las **7** reglas acumuladas siguen vigentes.\n"
            "La ley de la que las 7 son casos.\n",
            encoding="utf-8")
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), mini5, base)
        controles.append(_caso("C13_enfasis_y_elipsis_medidas", 1, rc))
        aplicar(manifiesto, indice, ("MINIMAL_CORPUS.md",), base / "badges" / "reglas.json", base)
        crudo = mini5.read_text(encoding="utf-8")
        controles.append(_caso("C13_reescribe_ambas_formas", True,
                               "**5** reglas" in crudo and "las 5 son casos" in crudo))
        controles.append(_caso("C13_no_sobrevive_la_cifra_vieja", 0, crudo.count("7")))

        # C12 — una cifra de subconjunto no es la cifra del corpus: ni deriva ni se toca.
        mini3 = base / "MINIMAL_CORPUS.md"
        mini3.write_text(
            "Total: 5 reglas, 2 familias. Las 51 reglas restantes y las 9 reglas de la familia.\n",
            encoding="utf-8")
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), mini3, base)
        controles.append(_caso("C12_subconjunto_no_deriva", 0, rc))
        aplicar(manifiesto, indice, ("MINIMAL_CORPUS.md",), base / "badges" / "reglas.json", base)
        crudo = mini3.read_text(encoding="utf-8")
        controles.append(_caso("C12_subconjunto_intacto", True,
                               "51 reglas restantes" in crudo and "9 reglas de la familia" in crudo))

        # C11 — MINIMAL_CORPUS: encabezados contra el número en palabras.
        mini2 = base / "MINIMAL_CORPUS.md"
        mini2.write_text("Cinco no se derivan.\n\n## a\n\n## b\n", encoding="utf-8")
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), mini2, base)
        clases = {d["clase"] for d in informe["deriva"]}
        controles.append(_caso("C11_no_derivadas_deriva", True, "NO_DERIVADAS_DESALINEADAS" in clases))

    fallos = [c for c in controles if not c["ok"]]
    for c in controles:
        print("%-34s esperado=%-28r obtenido=%-28r %s"
              % (c["caso"], c["esperado"], c["obtenido"], "OK" if c["ok"] else "FALLA"))
    print("SELF-TEST %s: %d/%d controles" % ("OK" if not fallos else "FALLA",
                                             len(controles) - len(fallos), len(controles)))
    return 0 if not fallos else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def emitir_manifiesto(ruta, directorio, indice=INDICE, origen_repo=None, origen_commit=None):
    familias = leer_familias_del_indice(indice)
    salida = leer_doctrina(directorio, familias)
    datos = {
        "sujeto": "encabezados '## ' de docs/doctrina/*.md",
        "comando": "python3 tools/medir_reglas.py --sujeto doctrinal --ruta %s --emitir-manifiesto %s"
                   % (directorio, ruta),
        "medido_en": medido_ahora(),
        "origen": {
            "repo": origen_repo or "NO_MEDIDO",
            "commit": origen_commit or "NO_MEDIDO",
            "nota": "El texto de la doctrina no se publica aquí; este manifiesto publica "
                    "los nombres y su cuenta, que es lo que el badge muestra.",
        },
        "total_reglas": sum(f["reglas"] for f in salida),
        "familias": salida,
    }
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(datos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return datos


def main(argv=None):
    p = argparse.ArgumentParser(description="Medidor de reglas del corpus (badge derivado).")
    p.add_argument("--sujeto", choices=("manifiesto", "doctrinal"), default="manifiesto")
    p.add_argument("--ruta", default=None, help="directorio doctrinal (sujeto=doctrinal)")
    p.add_argument("--emitir-manifiesto", metavar="PATH", default=None)
    p.add_argument("--origen-repo", default=None)
    p.add_argument("--origen-commit", default=None)
    p.add_argument("--manifiesto", default=str(MANIFIESTO))
    p.add_argument("--indice", default=str(INDICE))
    p.add_argument("--minimal", default=str(MINIMAL))
    p.add_argument("--endpoint", metavar="PATH", default=None)
    p.add_argument("--json", action="store_true", dest="como_json")
    p.add_argument("--check", action="store_true")
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--self-test", action="store_true", dest="self_test")
    args = p.parse_args(argv)

    if args.self_test:
        return self_test()

    if args.sujeto == "doctrinal":
        if not args.ruta:
            print("RC 20: --sujeto doctrinal exige --ruta DIR", file=sys.stderr)
            return 20
        try:
            familias = leer_familias_del_indice(args.indice)
            salida = leer_doctrina(args.ruta, familias)
        except NoMedido as exc:
            print("NO_MEDIDO: %s" % exc, file=sys.stderr)
            return 2
        total = sum(f["reglas"] for f in salida)
        if args.emitir_manifiesto:
            datos = emitir_manifiesto(args.emitir_manifiesto, args.ruta, args.indice,
                                      args.origen_repo, args.origen_commit)
            print("MANIFIESTO: %s · %d reglas en %d familias"
                  % (args.emitir_manifiesto, datos["total_reglas"], len(datos["familias"])))
        else:
            for f in salida:
                print("%-34s %3d  %s" % (f["familia"], f["reglas"], f["archivo"]))
            print("TOTAL: %d reglas en %d familias" % (total, len(salida)))
        return 0

    if args.emitir_manifiesto:
        print("RC 20: --emitir-manifiesto exige --sujeto doctrinal --ruta DIR", file=sys.stderr)
        return 20

    if args.aplicar:
        try:
            escritos = aplicar(args.manifiesto, args.indice, DOCUMENTOS, args.endpoint or ENDPOINT)
        except NoMedido as exc:
            print("NO_MEDIDO: %s" % exc, file=sys.stderr)
            return 2
        for ruta in escritos:
            print("ESCRITO: %s" % ruta)
        return 0

    informe, rc = medir(args.manifiesto, args.indice, DOCUMENTOS, args.minimal)
    if args.endpoint and rc == 0:
        destino = Path(args.endpoint)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(endpoint(informe["total_reglas"], len(informe["familias"])),
                                      indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("ESCRITO: %s" % destino)

    if args.como_json:
        print(json.dumps(informe, indent=2, ensure_ascii=False))
    else:
        if informe["veredicto"] == "NO_MEDIDO":
            print("NO_MEDIDO — %s" % informe["causa"])
        else:
            for f in informe["familias"]:
                print("%-34s %3d  %s" % (f["familia"], f["reglas"], f["archivo"]))
            print("TOTAL: %d reglas en %d familias · índice %d · %s"
                  % (informe["total_reglas"], len(informe["familias"]),
                     informe["superficies"]["indice_reglas"], informe["medido_en"]))
            if informe["deriva"]:
                print("DERIVA (%d):" % len(informe["deriva"]))
                for d in informe["deriva"]:
                    print("  · %-26s %-28s %s" % (d["superficie"], d["clase"], d["detalle"]))
            else:
                print("ALINEADO: manifiesto == índice == documentos. RC 0.")
    if args.check:
        return rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
