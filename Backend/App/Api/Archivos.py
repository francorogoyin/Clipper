"""
Endpoints para subir, listar y eliminar
archivos (TXT y DOCX).

"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)

Router_Archivos = APIRouter()


@Router_Archivos.post("/upload")
async def Subir_Archivo(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Sube un archivo TXT o DOCX, lo parsea,
    extrae highlights y los guarda en la DB.
    Verifica el límite free (50 highlights).
    Almacena el archivo original en S3.

    """

    return {"Detalle": "Implementar"}


@Router_Archivos.get("/")
async def Listar_Archivos(
    Pagina: int = 1,
    Limite: int = 20,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Lista los archivos subidos por el usuario,
    ordenados por fecha. Paginado.

    """

    return {"Detalle": "Implementar"}


@Router_Archivos.get("/{Id_Archivo}")
async def Obtener_Archivo(
    Id_Archivo: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna el detalle de un archivo subido
    con su metadata.

    """

    return {"Detalle": "Implementar"}


@Router_Archivos.delete("/{Id_Archivo}")
async def Eliminar_Archivo(
    Id_Archivo: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Elimina un archivo y todos sus highlights
    asociados.

    """

    return {"Detalle": "Implementar"}
