"""
Parser para el archivo My Clippings.txt
que genera Kindle. Extrae highlights con
su metadata: autor, libro, página, fecha
y texto resaltado.

"""

import re
from datetime import datetime
from dataclasses import dataclass


# Mapeo de meses en español a número.
MESES_ESPANOL: dict[str, int] = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

# Regex para la línea de metadata del Kindle.
# Ejemplo: "- Tu subrayado en la página 1081
#   | posición 16565-16566
#   | Añadido el martes, 18 de junio de 2024
#   3:24:35"
PATRON_METADATA = re.compile(
    r"-\s+Tu\s+subrayado\s+en\s+la\s+"
    r"p[aá]gina\s+(\d+)"
    r"\s*\|\s*posici[oó]n\s+(\d+-\d+)"
    r"\s*\|\s*[Aa][nñ]adido\s+el\s+"
    r"\w+,\s+"
    r"(\d{1,2})\s+de\s+(\w+)\s+de\s+"
    r"(\d{4})\s+"
    r"(\d{1,2}):(\d{2}):(\d{2})",
    re.IGNORECASE,
)

# Regex para extraer autor y libro.
# Ejemplo: "Séneca (Lucio Anneo Séneca)"
# El libro es lo que está antes del
# paréntesis, el autor entre paréntesis.
PATRON_AUTOR_LIBRO = re.compile(
    r"^(.+?)\s*\(([^)]+)\)\s*$"
)

# Separador entre highlights en Kindle.
SEPARADOR = "=========="


@dataclass
class Highlight_Parseado:

    """
    Estructura de un highlight extraído
    del archivo Kindle.

    """

    Texto: str
    Autor: str
    Libro: str
    Pagina: str
    Posicion: str
    Fecha_Subrayado: datetime | None
    Orden_Original: int


def Parsear_Archivo_Kindle(
    Contenido: str,
) -> list[Highlight_Parseado]:

    """
    Parsea el contenido completo de un archivo
    My Clippings.txt de Kindle y retorna una
    lista de highlights con su metadata.

    El formato esperado es:
    1. Línea de autor/libro.
    2. Línea de metadata (página, posición,
       fecha).
    3. Línea vacía.
    4. Texto del highlight (puede ser
       multilínea).
    5. Línea con "==========".

    """

    # Eliminar BOM si existe.
    Contenido = Contenido.lstrip("\ufeff")

    Bloques = Contenido.split(SEPARADOR)
    Highlights: list[Highlight_Parseado] = []
    Orden = 0

    for Bloque in Bloques:
        Bloque = Bloque.strip()
        if not Bloque:
            continue

        Lineas = Bloque.split("\n")

        # Necesitamos al menos 3 líneas:
        # autor/libro, metadata, texto.
        if len(Lineas) < 3:
            continue

        # Limpiar BOM de cada línea.
        Lineas = [
            Linea.lstrip("\ufeff").strip()
            for Linea in Lineas
        ]

        # Línea 1: Autor y Libro.
        Linea_Autor_Libro = Lineas[0]
        Autor, Libro = _Extraer_Autor_Libro(
            Linea_Autor_Libro
        )

        # Línea 2: Metadata.
        Linea_Metadata = Lineas[1]
        Pagina, Posicion, Fecha = (
            _Extraer_Metadata(Linea_Metadata)
        )

        # Líneas 3+: Texto del highlight.
        # Saltar líneas vacías después de
        # la metadata.
        Lineas_Texto = [
            Linea
            for Linea in Lineas[2:]
            if Linea
        ]

        Texto = " ".join(Lineas_Texto)

        if not Texto:
            continue

        Highlights.append(
            Highlight_Parseado(
                Texto=Texto,
                Autor=Autor,
                Libro=Libro,
                Pagina=Pagina,
                Posicion=Posicion,
                Fecha_Subrayado=Fecha,
                Orden_Original=Orden,
            )
        )

        Orden += 1

    return Highlights


def _Extraer_Autor_Libro(
    Linea: str,
) -> tuple[str, str]:

    """
    Extrae el autor y el libro de la primera
    línea de un bloque Kindle.

    Formato: "Libro (Autor)"
    Si no matchea, usa la línea completa como
    libro y deja autor vacío.

    """

    Match = PATRON_AUTOR_LIBRO.match(Linea)
    if Match:
        return (
            Match.group(2).strip(),
            Match.group(1).strip(),
        )

    return ("", Linea.strip())


def _Extraer_Metadata(
    Linea: str,
) -> tuple[str, str, datetime | None]:

    """
    Extrae página, posición y fecha de la
    línea de metadata del Kindle.

    Retorna (Pagina, Posicion, Fecha).
    Si el regex no matchea, retorna valores
    vacíos y None para la fecha.

    """

    Match = PATRON_METADATA.search(Linea)
    if not Match:
        return ("", "", None)

    Pagina = Match.group(1)
    Posicion = Match.group(2)
    Dia = int(Match.group(3))
    Nombre_Mes = Match.group(4).lower()
    Anio = int(Match.group(5))
    Hora = int(Match.group(6))
    Minuto = int(Match.group(7))
    Segundo = int(Match.group(8))

    Mes = MESES_ESPANOL.get(Nombre_Mes, 1)

    try:
        Fecha = datetime(
            year=Anio,
            month=Mes,
            day=Dia,
            hour=Hora,
            minute=Minuto,
            second=Segundo,
        )
    except ValueError:
        Fecha = None

    return (Pagina, Posicion, Fecha)
