"""
Servicio para subir archivos, parsearlos
y guardar los highlights en la base de datos.

"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from Backend.App.Modelos.Highlight import (
    Archivo_Subido,
    Highlight,
)
from Backend.App.Modelos.Usuario import Usuario
from Backend.App.Parsers.Parser_Kindle_Txt import (
    Parsear_Archivo_Kindle,
    Highlight_Parseado,
)
from Backend.App.Core.Config import Ajustes


async def Verificar_Limite_Free(
    Sesion: AsyncSession,
    Id_Usuario: uuid.UUID,
    Cantidad_Nueva: int,
) -> bool:

    """
    Verifica que el usuario no exceda el
    límite de highlights del plan free.
    Retorna True si puede agregar, False si no.

    """

    Consulta = select(
        func.count(Highlight.Id_Highlight)
    ).where(
        Highlight.Id_Usuario == Id_Usuario,
        Highlight.Eliminado_En.is_(None),
    )
    Resultado = await Sesion.execute(Consulta)
    Cantidad_Actual = Resultado.scalar() or 0

    # Obtener tipo de suscripción.
    Consulta_Usuario = select(
        Usuario.Tipo_Suscripcion
    ).where(
        Usuario.Id_Usuario == Id_Usuario
    )
    Resultado_Usuario = await Sesion.execute(
        Consulta_Usuario
    )
    Tipo = Resultado_Usuario.scalar()

    if Tipo == "premium":
        return True

    return (
        Cantidad_Actual + Cantidad_Nueva
        <= Ajustes.Limite_Highlights_Free
    )


async def Procesar_Archivo_Kindle(
    Sesion: AsyncSession,
    Id_Usuario: uuid.UUID,
    Nombre_Archivo: str,
    Contenido: str,
    Tamano: int,
    Ruta_S3: str,
) -> dict:

    """
    Parsea un archivo Kindle TXT, verifica
    el límite free, y guarda el archivo y sus
    highlights en la base de datos.

    Retorna un diccionario con el archivo
    creado y la lista de highlights.

    """

    # Parsear el contenido.
    Highlights_Parseados = (
        Parsear_Archivo_Kindle(Contenido)
    )

    Cantidad = len(Highlights_Parseados)

    if Cantidad == 0:
        raise ValueError(
            "El archivo no contiene highlights "
            "con formato válido de Kindle."
        )

    # Verificar límite.
    Puede_Agregar = (
        await Verificar_Limite_Free(
            Sesion, Id_Usuario, Cantidad
        )
    )
    if not Puede_Agregar:
        raise PermissionError(
            "Se excede el límite de "
            f"{Ajustes.Limite_Highlights_Free}"
            " highlights del plan free."
        )

    # Crear registro del archivo.
    Archivo = Archivo_Subido(
        Id_Usuario=Id_Usuario,
        Nombre_Original=Nombre_Archivo,
        Tipo_Archivo="txt",
        Tamano_Bytes=Tamano,
        Ruta_Almacenamiento=Ruta_S3,
        Cantidad_Highlights=Cantidad,
    )
    Sesion.add(Archivo)
    await Sesion.flush()

    # Crear highlights.
    Highlights_Db = []
    for Hp in Highlights_Parseados:
        H = Highlight(
            Id_Usuario=Id_Usuario,
            Id_Archivo=Archivo.Id_Archivo,
            Texto=Hp.Texto,
            Autor=Hp.Autor,
            Libro=Hp.Libro,
            Pagina=Hp.Pagina,
            Fecha_Subrayado=Hp.Fecha_Subrayado,
            Tipo_Semantico="paragraph",
            Orden_Original=Hp.Orden_Original,
        )
        Sesion.add(H)
        Highlights_Db.append(H)

    await Sesion.commit()

    return {
        "Archivo": Archivo,
        "Highlights": Highlights_Db,
        "Cantidad": Cantidad,
    }
