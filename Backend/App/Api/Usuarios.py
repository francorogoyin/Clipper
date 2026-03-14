"""
Endpoints de perfil, configuración y
suscripción del usuario.

"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)

Router_Usuarios = APIRouter()


@Router_Usuarios.get("/perfil")
async def Obtener_Perfil(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna el perfil del usuario autenticado:
    nickname, avatar, email, suscripción,
    idioma y tema visual.

    """

    # Placeholder.
    return {"Detalle": "Implementar"}


@Router_Usuarios.patch("/perfil")
async def Actualizar_Perfil(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Actualiza campos del perfil: nickname,
    avatar, idioma, tema visual.

    """

    return {"Detalle": "Implementar"}


@Router_Usuarios.get("/config")
async def Obtener_Config(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna la configuración completa del
    usuario: exportación, confirmaciones,
    defaults de P_Display y P_Processing.

    """

    return {"Detalle": "Implementar"}


@Router_Usuarios.patch("/config")
async def Actualizar_Config(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Actualiza campos parciales de la
    configuración del usuario.

    """

    return {"Detalle": "Implementar"}


@Router_Usuarios.post(
    "/confirmaciones/reset"
)
async def Resetear_Confirmaciones(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Resetea todas las confirmaciones
    silenciadas del usuario.

    """

    return {"Detalle": "Implementar"}


@Router_Usuarios.get("/suscripcion")
async def Obtener_Suscripcion(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna el tipo de suscripción, límite
    de highlights y cantidad usada.

    """

    return {"Detalle": "Implementar"}
