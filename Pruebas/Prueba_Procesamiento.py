"""
Pruebas del servicio de procesamiento
de texto (H_Processing).

"""

import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
)

from Backend.App.Servicios.Servicio_Procesamiento import (
    Procesar_Texto,
)


def Probar_Primera_Letra_Mayuscula():

    """
    Verifica que la primera letra se ponga
    en mayúscula.

    """

    Resultado = Procesar_Texto(
        "hola mundo",
        Primera_Letra_Mayuscula=True,
    )
    assert Resultado.startswith("H"), (
        f"No empieza con H: {Resultado}"
    )
    print("OK: Primera letra mayúscula")


def Probar_Signos_Faltantes():

    """
    Verifica que se agreguen signos de
    cierre faltantes.

    """

    # Comilla de apertura sin cierre.
    Resultado = Procesar_Texto(
        "«Hola mundo",
        Agregar_Signos_Faltantes=True,
    )
    assert Resultado.endswith("»"), (
        f"No cierra con »: {Resultado}"
    )

    # Texto sin punto final.
    Resultado = Procesar_Texto(
        "Hola mundo",
        Agregar_Signos_Faltantes=True,
    )
    assert Resultado.endswith("."), (
        f"No termina en punto: {Resultado}"
    )

    # Texto que ya tiene punto.
    Resultado = Procesar_Texto(
        "Hola mundo.",
        Agregar_Signos_Faltantes=True,
    )
    assert Resultado == "Hola mundo.", (
        f"Cambió: {Resultado}"
    )

    print("OK: Signos faltantes")


def Probar_Borrar_Caracteres():

    """
    Verifica que se borren caracteres
    específicos.

    """

    Resultado = Procesar_Texto(
        "H*o*l*a",
        Borrar_Caracteres=True,
        Caracteres_A_Borrar="*",
        Agregar_Signos_Faltantes=False,
    )
    assert "*" not in Resultado, (
        f"Quedan asteriscos: {Resultado}"
    )
    print("OK: Borrar caracteres")


def Probar_Primer_Caracter_Letra():

    """
    Verifica que el primer carácter
    alfabético se ponga en mayúscula.

    """

    Resultado = Procesar_Texto(
        "«hola mundo»",
        Primer_Caracter_Letra_Mayus=True,
        Primera_Letra_Mayuscula=False,
        Agregar_Signos_Faltantes=False,
    )
    assert "H" in Resultado, (
        f"No tiene H: {Resultado}"
    )
    print("OK: Primer carácter letra mayúscula")


def Probar_Espacios_Multiples():

    """
    Verifica que se eliminen espacios
    múltiples.

    """

    Resultado = Procesar_Texto(
        "Hola    mundo   test",
        Agregar_Signos_Faltantes=False,
    )
    assert "    " not in Resultado, (
        f"Quedan espacios: {Resultado}"
    )
    print("OK: Espacios múltiples")


if __name__ == "__main__":
    Probar_Primera_Letra_Mayuscula()
    Probar_Signos_Faltantes()
    Probar_Borrar_Caracteres()
    Probar_Primer_Caracter_Letra()
    Probar_Espacios_Multiples()
    print("\nTodas las pruebas pasaron.")
