"""
Pruebas del parser de Kindle TXT.
Valida que el regex extraiga correctamente
autor, libro, página, fecha y texto.

"""

import sys
import os

# Agregar raíz del proyecto al path.
sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
)

from Backend.App.Parsers.Parser_Kindle_Txt import (
    Parsear_Archivo_Kindle,
    _Extraer_Autor_Libro,
    _Extraer_Metadata,
)


def Probar_Extraccion_Autor_Libro():

    """
    Verifica que se extraigan autor y libro
    correctamente del formato Kindle.

    """

    Autor, Libro = _Extraer_Autor_Libro(
        "Séneca (Lucio Anneo Séneca)"
    )
    assert Autor == "Lucio Anneo Séneca", (
        f"Autor incorrecto: {Autor}"
    )
    assert Libro == "Séneca", (
        f"Libro incorrecto: {Libro}"
    )

    # Sin paréntesis.
    Autor, Libro = _Extraer_Autor_Libro(
        "Un libro sin autor"
    )
    assert Autor == ""
    assert Libro == "Un libro sin autor"

    print("OK: Extracción autor/libro")


def Probar_Extraccion_Metadata():

    """
    Verifica que se extraiga página, posición
    y fecha de la línea de metadata.

    """

    Linea = (
        "- Tu subrayado en la página 1081"
        " | posición 16565-16566"
        " | Añadido el martes, 18 de junio"
        " de 2024 3:24:35"
    )

    Pagina, Posicion, Fecha = (
        _Extraer_Metadata(Linea)
    )

    assert Pagina == "1081", (
        f"Página incorrecta: {Pagina}"
    )
    assert Posicion == "16565-16566", (
        f"Posición incorrecta: {Posicion}"
    )
    assert Fecha is not None, (
        "Fecha es None"
    )
    assert Fecha.year == 2024
    assert Fecha.month == 6
    assert Fecha.day == 18
    assert Fecha.hour == 3
    assert Fecha.minute == 24
    assert Fecha.second == 35

    print("OK: Extracción metadata")


def Probar_Parseo_Completo():

    """
    Parsea el archivo Notas.txt real y verifica
    que se extraigan highlights correctamente.

    """

    Ruta_Notas = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "Notas.txt",
    )

    if not os.path.exists(Ruta_Notas):
        print("SKIP: Notas.txt no encontrado")
        return

    with open(
        Ruta_Notas, "r", encoding="utf-8"
    ) as Archivo:
        Contenido = Archivo.read()

    Highlights = Parsear_Archivo_Kindle(
        Contenido
    )

    assert len(Highlights) > 0, (
        "No se parsearon highlights"
    )

    # Verificar primer highlight.
    Primero = Highlights[0]
    assert Primero.Autor == (
        "Lucio Anneo Séneca"
    ), f"Autor: {Primero.Autor}"
    assert "Séneca" in Primero.Libro, (
        f"Libro: {Primero.Libro}"
    )
    assert Primero.Pagina == "1081", (
        f"Página: {Primero.Pagina}"
    )
    assert Primero.Fecha_Subrayado is not None
    assert Primero.Orden_Original == 0

    # Verificar que no hay fechas None
    # (el bug viejo del parseo).
    Fechas_None = [
        H for H in Highlights
        if H.Fecha_Subrayado is None
    ]
    assert len(Fechas_None) == 0, (
        f"{len(Fechas_None)} highlights sin "
        f"fecha de {len(Highlights)} totales"
    )

    print(
        f"OK: Parseo completo — "
        f"{len(Highlights)} highlights "
        f"extraídos sin errores"
    )


if __name__ == "__main__":
    Probar_Extraccion_Autor_Libro()
    Probar_Extraccion_Metadata()
    Probar_Parseo_Completo()
    print("\nTodas las pruebas pasaron.")
