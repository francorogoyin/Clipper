"""
Endpoints de exportación: generar archivo,
consultar estado y descargar.

"""

import uuid
import tempfile
import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import pandas as pd

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Dependencias import (
    Obtener_Usuario_Actual,
)
from Backend.App.Modelos.Usuario import Usuario
from Backend.App.Modelos.Highlight import (
    Highlight,
    Clipping,
    Clipping_Highlight,
)
from Backend.App.Exportadores.Registry import (
    Obtener_Exportador,
)
from pydantic import BaseModel

Router_Export = APIRouter()


class Peticion_Exportar(BaseModel):

    """
    Payload para generar una exportación.

    """

    Formato: str
    Ids_Clippings: list[str] | None = None
    Config_Estilo: dict = {}


@Router_Export.post("/generar")
async def Generar_Exportacion(
    Datos: Peticion_Exportar,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Genera un archivo de exportación en el
    formato solicitado. Por ahora sincrónico
    (migrar a Celery en producción).

    """

    # Validar formato.
    try:
        Exportador = Obtener_Exportador(
            Datos.Formato
        )
    except KeyError as Error:
        raise HTTPException(
            status_code=400,
            detail=str(Error),
        )

    # Obtener highlights.
    if Datos.Ids_Clippings:
        # Highlights de clippings específicos.
        Ids_Clippings = [
            uuid.UUID(Id)
            for Id in Datos.Ids_Clippings
        ]
        Consulta = (
            select(Highlight)
            .join(
                Clipping_Highlight,
                Clipping_Highlight.Id_Highlight
                == Highlight.Id_Highlight,
            )
            .where(
                Clipping_Highlight.Id_Clipping
                .in_(Ids_Clippings),
                Highlight.Id_Usuario
                == Usuario_Actual.Id_Usuario,
                Highlight.Eliminado_En.is_(
                    None
                ),
            )
            .order_by(
                Clipping_Highlight
                .Orden_En_Clipping
            )
        )
    else:
        # Todos los highlights del usuario.
        Consulta = (
            select(Highlight)
            .where(
                Highlight.Id_Usuario
                == Usuario_Actual.Id_Usuario,
                Highlight.Eliminado_En.is_(
                    None
                ),
            )
            .order_by(
                Highlight.Orden_Original
            )
        )

    Resultado = await Sesion.execute(Consulta)
    Highlights = list(
        Resultado.scalars().all()
    )

    if not Highlights:
        raise HTTPException(
            status_code=400,
            detail="No hay highlights para "
            "exportar.",
        )

    # Construir DataFrame.
    Datos_Df = [
        {
            "Texto": H.Texto,
            "Autor": H.Autor,
            "Libro": H.Libro,
            "Pagina": H.Pagina,
            "Tipo_Semantico": H.Tipo_Semantico,
        }
        for H in Highlights
    ]
    Df = pd.DataFrame(Datos_Df)

    # Generar archivo temporal.
    Sufijo = f".{Exportador.Extension}"
    with tempfile.NamedTemporaryFile(
        suffix=Sufijo, delete=False
    ) as Temp:
        Ruta_Temp = Temp.name

    Exportador.Exportar(
        Df, Ruta_Temp, Datos.Config_Estilo
    )

    # Retornar archivo directamente.
    Nombre_Descarga = (
        f"highlights{Sufijo}"
    )

    return FileResponse(
        path=Ruta_Temp,
        filename=Nombre_Descarga,
        media_type="application/octet-stream",
        background=None,
    )
