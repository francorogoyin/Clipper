"""
Esquemas Pydantic para archivos subidos.

"""

from datetime import datetime
from pydantic import BaseModel


class Respuesta_Archivo(BaseModel):

    """
    Respuesta al subir o consultar un archivo.

    """

    Id_Archivo: str
    Nombre_Original: str
    Tipo_Archivo: str
    Cantidad_Highlights: int
    Fecha_Subida: datetime

    model_config = {
        "from_attributes": True,
    }


class Respuesta_Lista_Archivos(BaseModel):

    """
    Lista paginada de archivos.

    """

    Archivos: list[Respuesta_Archivo]
    Total: int
