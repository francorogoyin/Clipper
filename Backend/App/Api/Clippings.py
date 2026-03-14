"""
Endpoints CRUD de clippings: crear, agrupar
automáticamente, renombrar, reordenar.

"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)

Router_Clippings = APIRouter()


@Router_Clippings.get("/")
async def Listar_Clippings(
    Pagina: int = 1,
    Limite: int = 20,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Lista clippings del usuario. Paginado.

    """

    return {"Detalle": "Implementar"}


@Router_Clippings.post("/")
async def Crear_Clipping(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Crea un clipping con un nombre y una
    lista de IDs de highlights.

    """

    return {"Detalle": "Implementar"}


@Router_Clippings.post("/agrupar")
async def Agrupar_Automaticamente(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Agrupa highlights automáticamente por
    criterio: autor, libro, dia, mes o año.

    """

    return {"Detalle": "Implementar"}


@Router_Clippings.get("/{Id_Clipping}")
async def Obtener_Clipping(
    Id_Clipping: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna un clipping con sus highlights
    ordenados por Orden_En_Clipping.

    """

    return {"Detalle": "Implementar"}


@Router_Clippings.patch("/{Id_Clipping}")
async def Renombrar_Clipping(
    Id_Clipping: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Renombra un clipping.

    """

    return {"Detalle": "Implementar"}


@Router_Clippings.delete("/{Id_Clipping}")
async def Eliminar_Clipping(
    Id_Clipping: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Soft delete de un clipping.

    """

    return {"Detalle": "Implementar"}


@Router_Clippings.patch(
    "/{Id_Clipping}/orden"
)
async def Reordenar_Highlights(
    Id_Clipping: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Reordena los highlights dentro de un
    clipping según el nuevo F_Order.

    """

    return {"Detalle": "Implementar"}
