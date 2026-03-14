"""
Endpoints CRUD de reglas de marcas
personalizadas para parser DOCX.

"""

import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Dependencias import (
    Obtener_Usuario_Actual,
)
from Backend.App.Modelos.Usuario import Usuario
from Backend.App.Modelos.Configuracion import (
    Regla_Marca,
)

Router_Rules = APIRouter()

REGLAS_PREDEFINIDAS = [
    ("###", "heading"),
    (">", "quote"),
    ("!", "callout"),
    ("~", "toggle"),
]


class Peticion_Regla(BaseModel):
    Marca: str
    Tipo_Semantico: str


@Router_Rules.get("/")
async def Listar_Reglas(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Lista todas las reglas del usuario
    (predefinidas + personalizadas).

    """

    Consulta = select(Regla_Marca).where(
        Regla_Marca.Id_Usuario
        == Usuario_Actual.Id_Usuario
    ).order_by(Regla_Marca.Prioridad.desc())
    Resultado = await Sesion.execute(Consulta)
    Reglas = Resultado.scalars().all()

    return {
        "Reglas": [
            {
                "Id_Regla": str(R.Id_Regla),
                "Marca": R.Marca,
                "Tipo_Semantico": (
                    R.Tipo_Semantico
                ),
                "Es_Predefinida": (
                    R.Es_Predefinida
                ),
            }
            for R in Reglas
        ],
    }


@Router_Rules.post("/")
async def Crear_Regla(
    Datos: Peticion_Regla,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Crea una regla personalizada.

    """

    Regla = Regla_Marca(
        Id_Usuario=Usuario_Actual.Id_Usuario,
        Marca=Datos.Marca,
        Tipo_Semantico=Datos.Tipo_Semantico,
        Es_Predefinida=False,
        Prioridad=10,
    )

    Sesion.add(Regla)
    await Sesion.commit()

    return {
        "Id_Regla": str(Regla.Id_Regla),
        "Mensaje": "Regla creada",
    }


@Router_Rules.patch("/{Id_Regla}")
async def Editar_Regla(
    Id_Regla: str,
    Datos: Peticion_Regla,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Edita una regla existente.

    """

    Consulta = select(Regla_Marca).where(
        Regla_Marca.Id_Regla
        == uuid.UUID(Id_Regla),
        Regla_Marca.Id_Usuario
        == Usuario_Actual.Id_Usuario,
    )
    Resultado = await Sesion.execute(Consulta)
    Regla = Resultado.scalar_one_or_none()

    if not Regla:
        raise HTTPException(
            status_code=404,
            detail="Regla no encontrada",
        )

    Regla.Marca = Datos.Marca
    Regla.Tipo_Semantico = Datos.Tipo_Semantico
    await Sesion.commit()

    return {"Mensaje": "Regla actualizada"}


@Router_Rules.delete("/{Id_Regla}")
async def Eliminar_Regla(
    Id_Regla: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Elimina una regla personalizada.

    """

    Consulta = select(Regla_Marca).where(
        Regla_Marca.Id_Regla
        == uuid.UUID(Id_Regla),
        Regla_Marca.Id_Usuario
        == Usuario_Actual.Id_Usuario,
        Regla_Marca.Es_Predefinida == False,
    )
    Resultado = await Sesion.execute(Consulta)
    Regla = Resultado.scalar_one_or_none()

    if not Regla:
        raise HTTPException(
            status_code=404,
            detail="Regla no encontrada o es "
            "predefinida",
        )

    await Sesion.delete(Regla)
    await Sesion.commit()

    return {"Mensaje": "Regla eliminada"}


@Router_Rules.post("/reset")
async def Resetear_Reglas(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Elimina todas las reglas del usuario y
    restaura las predefinidas.

    """

    # Eliminar existentes.
    Consulta = select(Regla_Marca).where(
        Regla_Marca.Id_Usuario
        == Usuario_Actual.Id_Usuario
    )
    Resultado = await Sesion.execute(Consulta)
    for Regla in Resultado.scalars().all():
        await Sesion.delete(Regla)

    # Crear predefinidas.
    for Marca, Tipo in REGLAS_PREDEFINIDAS:
        Regla = Regla_Marca(
            Id_Usuario=(
                Usuario_Actual.Id_Usuario
            ),
            Marca=Marca,
            Tipo_Semantico=Tipo,
            Es_Predefinida=True,
            Prioridad=0,
        )
        Sesion.add(Regla)

    await Sesion.commit()

    return {"Mensaje": "Reglas reseteadas"}
