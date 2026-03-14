"""
Servicio de procesamiento de texto
(H_Processing). Aplica transformaciones
configurables a los highlights.

"""

import re


def Procesar_Texto(
    Texto: str,
    Primera_Letra_Mayuscula: bool = True,
    Borrar_Caracteres: bool = False,
    Caracteres_A_Borrar: str = "",
    Primer_Caracter_Letra_Mayus: bool = True,
    Agregar_Signos_Faltantes: bool = True,
) -> str:

    """
    Aplica las transformaciones de H_Processing
    a un texto de highlight según la config.

    Retorna el texto procesado.

    """

    Resultado = Texto.strip()

    if not Resultado:
        return Resultado

    # Borrar caracteres específicos.
    if Borrar_Caracteres and Caracteres_A_Borrar:
        for Caracter in Caracteres_A_Borrar:
            Resultado = Resultado.replace(
                Caracter, ""
            )
        Resultado = Resultado.strip()

    # Eliminar espacios múltiples.
    Resultado = re.sub(
        r"\s+", " ", Resultado
    )

    # Cambiar primera letra a mayúscula.
    if Primera_Letra_Mayuscula and Resultado:
        Resultado = (
            Resultado[0].upper()
            + Resultado[1:]
        )

    # Cambiar primer carácter que sea letra
    # a mayúscula (puede estar después de
    # signos como «, ", etc.).
    if Primer_Caracter_Letra_Mayus:
        Resultado = _Mayuscula_Primera_Letra(
            Resultado
        )

    # Agregar signos faltantes.
    if Agregar_Signos_Faltantes:
        Resultado = _Agregar_Signos_Faltantes(
            Resultado
        )

    return Resultado


def _Mayuscula_Primera_Letra(
    Texto: str,
) -> str:

    """
    Encuentra el primer carácter alfabético
    del texto y lo pone en mayúscula.
    Útil cuando el texto empieza con signos
    como «, ", (, etc.

    """

    for Indice, Caracter in enumerate(Texto):
        if Caracter.isalpha():
            return (
                Texto[:Indice]
                + Caracter.upper()
                + Texto[Indice + 1:]
            )

    return Texto


# Pares de signos de apertura y cierre.
PARES_SIGNOS: dict[str, str] = {
    "'": "'",
    '"': '"',
    "\u00ab": "\u00bb",
    "(": ")",
    "\u00bf": "?",
    "\u00a1": "!",
    "<": ">",
}


def _Agregar_Signos_Faltantes(
    Texto: str,
) -> str:

    """
    Si el texto tiene un signo de apertura
    sin su cierre (o viceversa), lo agrega.
    Pares soportados: ', ", «», (), ¿?, ¡!, <>.

    """

    for Apertura, Cierre in PARES_SIGNOS.items():
        Cantidad_Apertura = Texto.count(
            Apertura
        )
        Cantidad_Cierre = Texto.count(Cierre)

        # Evitar doble conteo si apertura
        # y cierre son el mismo carácter.
        if Apertura == Cierre:
            continue

        if (
            Cantidad_Apertura
            > Cantidad_Cierre
        ):
            Texto = Texto + Cierre
        elif (
            Cantidad_Cierre
            > Cantidad_Apertura
        ):
            Texto = Apertura + Texto

    # Agregar punto final si no termina
    # en puntuación.
    if Texto and Texto[-1] not in ".!?»)\"'":
        Texto = Texto + "."

    return Texto
