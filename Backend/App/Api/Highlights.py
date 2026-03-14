"""
Endpoints CRUD de highlights: listar, editar,
eliminar, combinar y dividir.

"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)

Router_Highlights = APIRouter()


@Router_Highlights.get("/")
async def Listar_Highlights(
    Pagina: int = 1,
    Limite: int = 20,
    Orden: str | None = None,
    Autor: str | None = None,
    Libro: str | None = None,
    Id_Archivo: str | None = None,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Lista highlights del usuario con filtros
    opcionales por autor, libro o archivo.
    Paginado y ordenable.

    """

    return {"Detalle": "Implementar"}


@Router_Highlights.get("/{Id_Highlight}")
async def Obtener_Highlight(
    Id_Highlight: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna un highlight específico.

    """

    return {"Detalle": "Implementar"}


@Router_Highlights.patch("/{Id_Highlight}")
async def Editar_Highlight(
    Id_Highlight: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Edita el texto o tipo semántico de
    un highlight.

    """

    return {"Detalle": "Implementar"}


@Router_Highlights.delete(
    "/{Id_Highlight}"
)
async def Eliminar_Highlight(
    Id_Highlight: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Soft delete de un highlight.

    """

    return {"Detalle": "Implementar"}


@Router_Highlights.post("/combinar")
async def Combinar_Highlights(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Combina varios F_Blocks en un solo C_Block.
    Requiere que sean del mismo Author-Book.
    Se elige qué Date mantener.

    """

    return {"Detalle": "Implementar"}


@Router_Highlights.post(
    "/dividir/{Id_Highlight}"
)
async def Dividir_Highlight(
    Id_Highlight: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Divide un F_Block en varios C_Blocks
    según los puntos de corte indicados.

    """

    return {"Detalle": "Implementar"}


@Router_Highlights.delete("/lote")
async def Eliminar_Lote(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Soft delete de varios highlights
    en una sola operación.

    """

    return {"Detalle": "Implementar"}
