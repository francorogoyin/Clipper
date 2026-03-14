"""
Endpoints para subir, listar y eliminar
archivos (TXT y DOCX).

"""

import uuid

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Dependencias import (
    Obtener_Usuario_Actual,
)
from Backend.App.Modelos.Usuario import Usuario
from Backend.App.Modelos.Highlight import (
    Archivo_Subido,
)
from Backend.App.Servicios.Servicio_Archivos import (
    Procesar_Archivo_Kindle,
)
from Backend.App.Servicios.Servicio_S3 import (
    Subir_Archivo as Subir_A_S3,
)

Router_Archivos = APIRouter()

FORMATOS_PERMITIDOS = {"txt", "docx"}


@Router_Archivos.post("/upload")
async def Subir_Archivo(
    Archivo: UploadFile = File(...),
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Sube un archivo TXT o DOCX, lo parsea,
    extrae highlights y los guarda en la DB.
    Verifica el límite free (50 highlights).
    Almacena el archivo original en S3.

    """

    # Validar formato.
    Nombre = Archivo.filename or "archivo"
    Extension = Nombre.rsplit(".", 1)[-1].lower()

    if Extension not in FORMATOS_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Formato .{Extension} no "
                "soportado. Usar .txt o .docx."
            ),
        )

    # Leer contenido.
    Contenido_Bytes = await Archivo.read()
    Tamano = len(Contenido_Bytes)

    # Subir a S3.
    Ruta_S3 = Subir_A_S3(
        Contenido_Bytes,
        Nombre,
        str(Usuario_Actual.Id_Usuario),
    )

    # Parsear según formato.
    if Extension == "txt":
        Contenido_Texto = (
            Contenido_Bytes.decode("utf-8")
        )
        try:
            Resultado = (
                await Procesar_Archivo_Kindle(
                    Sesion,
                    Usuario_Actual.Id_Usuario,
                    Nombre,
                    Contenido_Texto,
                    Tamano,
                    Ruta_S3,
                )
            )
        except ValueError as Error:
            raise HTTPException(
                status_code=400,
                detail=str(Error),
            )
        except PermissionError as Error:
            raise HTTPException(
                status_code=403,
                detail=str(Error),
            )
    else:
        # DOCX: Fase 2.
        raise HTTPException(
            status_code=501,
            detail=(
                "Parser DOCX no implementado "
                "todavía."
            ),
        )

    return {
        "Id_Archivo": str(
            Resultado["Archivo"].Id_Archivo
        ),
        "Cantidad_Highlights": (
            Resultado["Cantidad"]
        ),
        "Highlights": [
            {
                "Id_Highlight": str(
                    H.Id_Highlight
                ),
                "Texto": H.Texto,
                "Autor": H.Autor,
                "Libro": H.Libro,
                "Pagina": H.Pagina,
                "Tipo_Semantico": (
                    H.Tipo_Semantico
                ),
            }
            for H in Resultado["Highlights"]
        ],
    }


@Router_Archivos.get("/")
async def Listar_Archivos(
    Pagina: int = 1,
    Limite: int = 20,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Lista los archivos subidos por el usuario,
    ordenados por fecha. Paginado.

    """

    Offset = (Pagina - 1) * Limite

    # Contar total.
    Consulta_Total = select(
        func.count(Archivo_Subido.Id_Archivo)
    ).where(
        Archivo_Subido.Id_Usuario
        == Usuario_Actual.Id_Usuario
    )
    Total = (
        await Sesion.execute(Consulta_Total)
    ).scalar() or 0

    # Obtener página.
    Consulta = (
        select(Archivo_Subido)
        .where(
            Archivo_Subido.Id_Usuario
            == Usuario_Actual.Id_Usuario
        )
        .order_by(
            desc(Archivo_Subido.Fecha_Subida)
        )
        .offset(Offset)
        .limit(Limite)
    )
    Resultado = await Sesion.execute(Consulta)
    Archivos = Resultado.scalars().all()

    return {
        "Archivos": [
            {
                "Id_Archivo": str(
                    A.Id_Archivo
                ),
                "Nombre_Original": (
                    A.Nombre_Original
                ),
                "Tipo_Archivo": A.Tipo_Archivo,
                "Cantidad_Highlights": (
                    A.Cantidad_Highlights
                ),
                "Fecha_Subida": (
                    A.Fecha_Subida.isoformat()
                ),
            }
            for A in Archivos
        ],
        "Total": Total,
    }


@Router_Archivos.get("/{Id_Archivo}")
async def Obtener_Archivo(
    Id_Archivo: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Retorna el detalle de un archivo subido
    con su metadata.

    """

    Consulta = select(Archivo_Subido).where(
        Archivo_Subido.Id_Archivo
        == uuid.UUID(Id_Archivo),
        Archivo_Subido.Id_Usuario
        == Usuario_Actual.Id_Usuario,
    )
    Resultado = await Sesion.execute(Consulta)
    Archivo = Resultado.scalar_one_or_none()

    if not Archivo:
        raise HTTPException(
            status_code=404,
            detail="Archivo no encontrado",
        )

    return {
        "Id_Archivo": str(Archivo.Id_Archivo),
        "Nombre_Original": (
            Archivo.Nombre_Original
        ),
        "Tipo_Archivo": Archivo.Tipo_Archivo,
        "Tamano_Bytes": Archivo.Tamano_Bytes,
        "Cantidad_Highlights": (
            Archivo.Cantidad_Highlights
        ),
        "Fecha_Subida": (
            Archivo.Fecha_Subida.isoformat()
        ),
    }


@Router_Archivos.delete("/{Id_Archivo}")
async def Eliminar_Archivo(
    Id_Archivo: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Elimina un archivo y todos sus highlights
    asociados (cascade).

    """

    Consulta = select(Archivo_Subido).where(
        Archivo_Subido.Id_Archivo
        == uuid.UUID(Id_Archivo),
        Archivo_Subido.Id_Usuario
        == Usuario_Actual.Id_Usuario,
    )
    Resultado = await Sesion.execute(Consulta)
    Archivo = Resultado.scalar_one_or_none()

    if not Archivo:
        raise HTTPException(
            status_code=404,
            detail="Archivo no encontrado",
        )

    await Sesion.delete(Archivo)
    await Sesion.commit()

    return {
        "Mensaje": "Archivo eliminado",
    }
