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
          raiz=RAIZ, endpoint_ruta=None):
    """Coteja todas las superficies contra el manifiesto. RC 0/1/2.

    El endpoint pertenece al corpus que lo publica: si no se declara, se busca bajo
    `raiz`, no bajo el checkout desde el que corre el instrumento. Un endpoint
    tomado del árbol del invocador mediría el badge de otro repositorio.
    """
    manifiesto = Path(manifiesto)
    endpoint_ruta = Path(endpoint_ruta) if endpoint_ruta else Path(raiz) / "badges" / "reglas.json"
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

    # Superficie 4 — el endpoint que lee el badge: la cifra publicada al mundo.
    # Sin esta superficie `--check` puede estar verde mientras shields.io publica
    # otra cifra: el defecto que el manifiesto vino a cerrar, una capa más afuera.
    publicada = None
    etiqueta = _ruta_visible(endpoint_ruta, raiz)
    try:
        publicada = leer_endpoint(endpoint_ruta)
    except NoMedido as exc:
        deriva.append({"superficie": etiqueta, "clase": "ENDPOINT_ILEGIBLE",
                       "detalle": str(exc)})
    else:
        esperada = endpoint(total, n_familias)
        if publicada is None:
            deriva.append({
                "superficie": etiqueta,
                "clase": "ENDPOINT_AUSENTE",
                "detalle": "sin endpoint: el badge publica su texto de reserva, no una medición",
            })
        else:
            for campo in ("schemaVersion", "label", "message"):
                if publicada.get(campo) != esperada[campo]:
                    deriva.append({
                        "superficie": etiqueta,
                        "clase": "ENDPOINT_DESALINEADO",
                        "detalle": "%s publica %r · manifiesto %r"
                                   % (campo, publicada.get(campo), esperada[campo]),
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
            "endpoint": publicada,
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


def leer_endpoint(ruta):
    """El JSON que shields.io lee. `None` si no existe; NoMedido si no es legible."""
    ruta = Path(ruta)
    if not ruta.exists():
        return None
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise NoMedido("endpoint ilegible (%s): %s" % (ruta, exc))
    if not isinstance(datos, dict):
        raise NoMedido("endpoint no es un objeto JSON: %s" % ruta)
    return datos


def _ruta_visible(ruta, raiz):
    """Ruta relativa a la raíz del corpus, para que la deriva nombre una superficie."""
    try:
        return str(Path(ruta).resolve().relative_to(Path(raiz).resolve()))
    except ValueError:
        return str(ruta)


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
    (base / "badges" / "reglas.json").write_text(
        json.dumps(endpoint(datos["total_reglas"], len(datos["familias"])), indent=2,
                   ensure_ascii=False) + "\n", encoding="utf-8")
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

        # C14 — el comparador ignora el reloj: `medido_en` distinto, cero deriva.
        doctrinal = base / "docs" / "doctrina"
        medido = construir_manifiesto(doctrinal, indice, "platino-labs", "abc1234", base / "m.json")
        publicado = json.loads(json.dumps(medido))
        publicado["medido_en"] = "1999-01-01T00:00:00Z"
        controles.append(_caso("C14_reloj_no_es_deriva", 0, len(comparar_manifiestos(medido, publicado))))

        # C15 — una cuenta que se mueve sí es deriva, y la clase se nombra.
        publicado["total_reglas"] = 6
        publicado["familias"][0]["reglas"] = 4
        clases = {d["clase"] for d in comparar_manifiestos(medido, publicado)}
        controles.append(_caso("C15_total_deriva", True, "TOTAL_DESALINEADO" in clases))
        controles.append(_caso("C15_familia_deriva", True, "CUENTA_FAMILIA_DESALINEADA" in clases))

        # C16 — el pin de origen es estado del objeto: otro commit, misma cuenta, deriva.
        igual = json.loads(json.dumps(medido))
        igual["origen"]["commit"] = "def5678"
        clases = {d["clase"] for d in comparar_manifiestos(medido, igual)}
        controles.append(_caso("C16_origen_desfasado", True, "ORIGEN_DESFASADO" in clases))

        # C21 — el pin corto y el largo son la misma afirmación; el formato no es deriva.
        largo = json.loads(json.dumps(medido))
        largo["origen"]["commit"] = "abc1234" + "0" * 33
        controles.append(_caso("C21_sha_corto_vs_largo", True,
                               not comparar_manifiestos(medido, largo)))
        corto_ajeno = json.loads(json.dumps(medido))
        corto_ajeno["origen"]["commit"] = "abc1235"
        controles.append(_caso("C21_prefijo_ajeno_deriva", True,
                               bool(comparar_manifiestos(medido, corto_ajeno))))

        # C17 — familia ausente en el publicado: se nombra, no se colapsa en el total.
        sin_una = json.loads(json.dumps(medido))
        sin_una["familias"] = sin_una["familias"][1:]
        clases = {d["clase"] for d in comparar_manifiestos(medido, sin_una)}
        controles.append(_caso("C17_familia_ausente", True, "FAMILIA_AUSENTE" in clases))

        # C18 — el endpoint que lee shields.io es superficie medida: una cifra
        # tecleada en el badge deriva aunque el manifiesto y la prosa coincidan.
        # La prosa se repone primero: aquí la única variable es el badge.
        (base / "MINIMAL_CORPUS.md").write_text(
            "# Minimal\n\nEste archivo no es la constitución: 5 reglas, 2 familias.\n\n"
            "## no derivada uno\n\n## no derivada dos\n", encoding="utf-8")
        ep = base / "badges" / "reglas.json"
        ep.write_text(json.dumps({"schemaVersion": 1, "label": "doctrina",
                                  "message": "56 rules · 7 families"}), encoding="utf-8")
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        clases = {d["clase"] for d in informe["deriva"]}
        controles.append(_caso("C18_endpoint_tecleado_rc1", 1, rc))
        controles.append(_caso("C18_clase", True, "ENDPOINT_DESALINEADO" in clases))

        # C19 — sin endpoint el badge publica su texto de reserva: es deriva
        # declarada, no NO_MEDIDO, porque el manifiesto dice cuál sería la cifra.
        ep.unlink()
        informe, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        clases = {d["clase"] for d in informe["deriva"]}
        controles.append(_caso("C19_endpoint_ausente_rc1", 1, rc))
        controles.append(_caso("C19_clase", True, "ENDPOINT_AUSENTE" in clases))

        # C20 — el escritor único repara el endpoint, y la medición lo confirma.
        aplicar(manifiesto, indice, ("MINIMAL_CORPUS.md",), ep, base)
        _, rc = medir(manifiesto, indice, ("MINIMAL_CORPUS.md",), minimal, base)
        controles.append(_caso("C20_aplicar_repara_endpoint", 0, rc))

        # C22 — el comando publicado no hereda la ruta absoluta de quien lo invoca.
        # En CI sería `$GITHUB_WORKSPACE/docs/doctrina` y en una simulación
        # `/tmp/...`; las dos se leen como reproducibles sin serlo.
        m = construir_manifiesto(base / "docs" / "doctrina", indice,
                                 origen_repo="r/x", origen_commit="a" * 40)
        controles.append(_caso("C22_sin_ruta_absoluta", False, str(base) in m["comando"]))
        controles.append(_caso("C22_comando_canonico", True,
                               "--ruta docs/doctrina" in m["comando"]
                               and "--emitir-manifiesto docs/DOCTRINA_MANIFIESTO.json" in m["comando"]))
        controles.append(_caso("C22_comando_lleva_origen", True,
                               "r/x" in m["comando"] and "a" * 40 in m["comando"]))

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
def construir_manifiesto(directorio, indice=INDICE, origen_repo=None, origen_commit=None, ruta=None):
    """Mide la doctrina y devuelve el manifiesto en memoria, sin escribir.

    Separado de `emitir_manifiesto` para que `--comparar-manifiesto` pueda medir sin
    tocar el disco: comparar no es publicar, y un comparador que escribe no puede
    correr sobre un árbol ajeno.
    """
    familias = leer_familias_del_indice(indice)
    salida = leer_doctrina(directorio, familias)
    return {
        "sujeto": "encabezados '## ' de docs/doctrina/*.md",
        # HUELLA-MEDIDOR-COMANDO-CANONICO-20261106
        # El comando publicado no hereda la ruta absoluta de quien lo invoca: en CI
        # seria `$GITHUB_WORKSPACE/docs/doctrina` y en una simulación `/tmp/...`, y
        # las dos se leen como reproducibles sin serlo. Publica rutas relativas a su
        # raíz y `desde` declara de qué raíz son y qué repo vive en `--ruta`.
        "comando": "python3 tools/medir_reglas.py --sujeto doctrinal --ruta docs/doctrina "
                   "--emitir-manifiesto docs/DOCTRINA_MANIFIESTO.json "
                   "--origen-repo %s --origen-commit %s"
                   % (origen_repo or "NO_MEDIDO", origen_commit or "NO_MEDIDO"),
        "desde": "raíz de corpus-medido; `--ruta` es el `docs/doctrina` de `origen.repo`",
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


def emitir_manifiesto(ruta, directorio, indice=INDICE, origen_repo=None, origen_commit=None):
    datos = construir_manifiesto(directorio, indice, origen_repo, origen_commit, ruta)
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(datos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return datos


def _firma_familias(datos):
    """{familia: (archivo, reglas)}, tolerante al orden y al formato del lado publicado."""
    firmas = {}
    for f in datos.get("familias") or []:
        if not isinstance(f, dict):
            continue
        reglas = f.get("reglas")
        if reglas is None and isinstance(f.get("nombres"), list):
            reglas = len(f["nombres"])
        firmas[f.get("familia")] = (f.get("archivo") or "", reglas)
    return firmas


def _mismo_commit(a, b):
    """Un sha corto y el largo son la MISMA afirmación; dos prefijos distintos no.

    El manifiesto se emite a mano con `git rev-parse --short` (8 caracteres) y una
    corrida de CI dispone de `GITHUB_SHA` (40). Compararlos por igualdad textual
    enrojece el pin por formato y no por deriva, que es el falso rojo que enseña a
    ignorar el rojo. Se comparan por prefijo común y se exige un mínimo de 7 para
    que una coincidencia de 4 caracteres no pase por identidad.
    """
    if not a or not b:
        return a == b
    a, b = str(a).strip().lower(), str(b).strip().lower()
    n = min(len(a), len(b))
    return n >= 7 and a[:n] == b[:n]


def comparar_manifiestos(medido, publicado):
    """Deriva entre el manifiesto recién medido y el publicado.

    `medido_en` NO se compara: es reloj de pared, no estado del objeto — dos
    corridas sobre la misma doctrina difieren en ese campo y coinciden en todo lo
    demás. Lo que sí se compara es `origen.commit`: un manifiesto que declara otro
    commit no describe a éste, aunque las cuentas coincidan.
    """
    deriva = []

    def _anota(clase, detalle):
        deriva.append({"superficie": "manifiesto_publicado", "clase": clase, "detalle": detalle})

    if medido.get("total_reglas") != publicado.get("total_reglas"):
        _anota("TOTAL_DESALINEADO", "medido %r · publicado %r"
               % (medido.get("total_reglas"), publicado.get("total_reglas")))

    commit_medido = (medido.get("origen") or {}).get("commit")
    commit_publicado = (publicado.get("origen") or {}).get("commit")
    if not _mismo_commit(commit_medido, commit_publicado):
        _anota("ORIGEN_DESFASADO", "medido %s · publicado %s"
               % (commit_medido or "NO_MEDIDO", commit_publicado or "NO_MEDIDO"))

    nuestro, suyo = _firma_familias(medido), _firma_familias(publicado)
    for nombre in sorted(set(nuestro) - set(suyo), key=str):
        _anota("FAMILIA_AUSENTE", "%s (%s reglas)" % (nombre, nuestro[nombre][1]))
    for nombre in sorted(set(suyo) - set(nuestro), key=str):
        _anota("FAMILIA_SOBRANTE", "%s (%s reglas)" % (nombre, suyo[nombre][1]))
    for nombre in sorted(set(nuestro) & set(suyo), key=str):
        if nuestro[nombre][1] != suyo[nombre][1]:
            _anota("CUENTA_FAMILIA_DESALINEADA", "%s medido %s · publicado %s"
                   % (nombre, nuestro[nombre][1], suyo[nombre][1]))
    return deriva


def main(argv=None):
    p = argparse.ArgumentParser(description="Medidor de reglas del corpus (badge derivado).")
    p.add_argument("--sujeto", choices=("manifiesto", "doctrinal"), default="manifiesto")
    p.add_argument("--ruta", default=None, help="directorio doctrinal (sujeto=doctrinal)")
    p.add_argument("--emitir-manifiesto", metavar="PATH", default=None)
    p.add_argument("--comparar-manifiesto", metavar="PATH", default=None,
                   help="compara la doctrina medida con el manifiesto publicado (RC 0/1/2)")
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
        if args.comparar_manifiesto:
            try:
                publicado = json.loads(Path(args.comparar_manifiesto).read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                print("NO_MEDIDO: no se pudo leer el manifiesto publicado (%s): %s"
                      % (args.comparar_manifiesto, exc), file=sys.stderr)
                return 2
            medido = construir_manifiesto(args.ruta, args.indice, args.origen_repo,
                                          args.origen_commit, args.comparar_manifiesto)
            deriva = comparar_manifiestos(medido, publicado)
            if not deriva:
                print("PUBLICADO ALINEADO: %d reglas en %d familias · origen %s"
                      % (medido["total_reglas"], len(medido["familias"]),
                         medido["origen"]["commit"]))
                return 0
            print("DERIVA PUBLICADA (%d):" % len(deriva))
            for d in deriva:
                print("  · %-26s %-28s %s" % (d["superficie"], d["clase"], d["detalle"]))
            return 1
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

    if args.comparar_manifiesto:
        print("RC 20: --comparar-manifiesto exige --sujeto doctrinal --ruta DIR", file=sys.stderr)
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

    informe, rc = medir(args.manifiesto, args.indice, DOCUMENTOS, args.minimal,
                        endpoint_ruta=args.endpoint or ENDPOINT)
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
                print("ALINEADO: manifiesto == índice == documentos == endpoint. RC 0.")
    if args.check:
        return rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
