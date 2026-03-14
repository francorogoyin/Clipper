"""
Esquemas Pydantic para highlights.

"""

from datetime import datetime
from pydantic import BaseModel


class Respuesta_Highlight(BaseModel):

    """
    Un highlight con toda su metadata.

    """

    Id_Highlight: str
    Texto: str
    Autor: str | None
    Libro: str | None
    Pagina: str | None
    Fecha_Subrayado: datetime | None
    Tipo_Semantico: str
    Orden_Original: int

    model_config = {
        "from_attributes": True,
    }


class Respuesta_Lista_Highlights(BaseModel):

    """
    Lista paginada de highlights.

    """

    Highlights: list[Respuesta_Highlight]
    Total: int
    Pagina: int


class Peticion_Editar_Highlight(BaseModel):

    """
    Campos editables de un highlight.

    """

    Texto: str | None = None
    Tipo_Semantico: str | None = None


class Peticion_Combinar(BaseModel):

    """
    Payload para combinar highlights.

    """

    Ids_Highlights: list[str]
    Id_Fecha_A_Mantener: str


class Peticion_Dividir(BaseModel):

    """
    Payload para dividir un highlight.

    """

    Puntos_De_Corte: list[int]


class Peticion_Eliminar_Lote(BaseModel):

    """
    Payload para eliminar varios highlights.

    """

    Ids_Highlights: list[str]


class Peticion_Procesamiento(BaseModel):

    """
    Configuración de H_Processing para
    aplicar a un texto o clipping.

    """

    Texto: str | None = None
    Primera_Letra_Mayuscula: bool = True
    Borrar_Caracteres: bool = False
    Caracteres_A_Borrar: str = ""
    Primer_Caracter_Letra_Mayus: bool = True
    Agregar_Signos_Faltantes: bool = True
