"""
Parser para archivos DOCX con marcas de
formato tipo Markdown. Extrae highlights
y asigna tipos semánticos según las marcas.

"""

import re
from dataclasses import dataclass

from docx import Document


# Marcas predefinidas con su tipo semántico.
# El orden importa: marcas más largas primero.
MARCAS_PREDEFINIDAS: list[
    tuple[str, str]
] = [
    ("###", "heading"),
    (">", "quote"),
    ("!", "callout"),
    ("~", "toggle"),
]


@dataclass
class Highlight_Docx:

    """
    Un highlight extraído de un DOCX.

    """

    Texto: str
    Tipo_Semantico: str
    Orden_Original: int


def Parsear_Archivo_Docx(
    Ruta_Archivo: str,
    Reglas_Custom: list[
        tuple[str, str]
    ] | None = None,
) -> list[Highlight_Docx]:

    """
    Parsea un archivo DOCX extrayendo cada
    párrafo como highlight. Detecta marcas
    de formato al inicio para asignar tipo
    semántico.

    Las reglas custom tienen prioridad sobre
    las predefinidas.

    """

    Doc = Document(Ruta_Archivo)

    # Construir lista de reglas ordenadas
    # por largo de marca (más larga primero).
    Reglas = list(MARCAS_PREDEFINIDAS)

    if Reglas_Custom:
        # Custom tiene prioridad: agregar
        # al inicio.
        Reglas = Reglas_Custom + Reglas

    # Ordenar por largo descendente para
    # evitar matches parciales.
    Reglas.sort(
        key=lambda R: len(R[0]),
        reverse=True,
    )

    Highlights: list[Highlight_Docx] = []
    Orden = 0

    for Parrafo in Doc.paragraphs:
        Texto = Parrafo.text.strip()

        if not Texto:
            continue

        # Buscar marca al inicio.
        Tipo = "paragraph"
        for Marca, Tipo_Marca in Reglas:
            if Texto.startswith(Marca):
                Tipo = Tipo_Marca
                # Eliminar la marca del texto.
                Texto = Texto[len(Marca):].strip()
                break

        if not Texto:
            continue

        Highlights.append(
            Highlight_Docx(
                Texto=Texto,
                Tipo_Semantico=Tipo,
                Orden_Original=Orden,
            )
        )

        Orden += 1

    return Highlights
