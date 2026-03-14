"""
Endpoints de H_Processing: preview en tiempo
real y aplicación a clippings.

"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
    Config_H_Processing,
)
from Backend.App.Esquemas.Esquema_Highlight import (
    Peticion_Procesamiento,
)
from Backend.App.Servicios.Servicio_Procesamiento import (
    Procesar_Texto,
)

Router_Processing = APIRouter()


@Router_Processing.post("/preview")
async def Preview_Procesamiento(
    Datos: Peticion_Procesamiento,
):

    """
    Procesa un texto con la configuración
    dada y retorna el resultado. Para preview
    en tiempo real (debounce 300ms en frontend).

    """

    if not Datos.Texto:
        raise HTTPException(
            status_code=400,
            detail="Texto requerido",
        )

    Resultado = Procesar_Texto(
        Texto=Datos.Texto,
        Primera_Letra_Mayuscula=(
            Datos.Primera_Letra_Mayuscula
        ),
        Borrar_Caracteres=(
            Datos.Borrar_Caracteres
        ),
        Caracteres_A_Borrar=(
            Datos.Caracteres_A_Borrar
        ),
        Primer_Caracter_Letra_Mayus=(
            Datos.Primer_Caracter_Letra_Mayus
        ),
        Agregar_Signos_Faltantes=(
            Datos.Agregar_Signos_Faltantes
        ),
    )

    return {"Texto_Procesado": Resultado}


@Router_Processing.post(
    "/aplicar/{Id_Clipping}"
)
async def Aplicar_A_Clipping(
    Id_Clipping: str,
    Datos: Peticion_Procesamiento,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Aplica H_Processing a todos los highlights
    de un clipping.

    """

    import uuid

    # Obtener highlights del clipping.
    Consulta = (
        select(Highlight)
        .join(
            Clipping_Highlight,
            Clipping_Highlight.Id_Highlight
            == Highlight.Id_Highlight,
        )
        .where(
            Clipping_Highlight.Id_Clipping
            == uuid.UUID(Id_Clipping),
            Highlight.Id_Usuario
            == Usuario_Actual.Id_Usuario,
            Highlight.Eliminado_En.is_(None),
        )
    )
    Resultado = await Sesion.execute(Consulta)
    Highlights = list(
        Resultado.scalars().all()
    )

    if not Highlights:
        raise HTTPException(
            status_code=404,
            detail="Clipping sin highlights",
        )

    # Aplicar procesamiento a cada highlight.
    for H in Highlights:
        H.Texto = Procesar_Texto(
            Texto=H.Texto,
            Primera_Letra_Mayuscula=(
                Datos.Primera_Letra_Mayuscula
            ),
            Borrar_Caracteres=(
                Datos.Borrar_Caracteres
            ),
            Caracteres_A_Borrar=(
                Datos.Caracteres_A_Borrar
            ),
            Primer_Caracter_Letra_Mayus=(
                Datos.Primer_Caracter_Letra_Mayus
            ),
            Agregar_Signos_Faltantes=(
                Datos.Agregar_Signos_Faltantes
            ),
        )

    await Sesion.commit()

    return {
        "Highlights_Procesados": [
            {
                "Id_Highlight": str(
                    H.Id_Highlight
                ),
                "Texto": H.Texto,
            }
            for H in Highlights
        ],
    }


@Router_Processing.get(
    "/config/{Id_Clipping}"
)
async def Obtener_Config_Clipping(
    Id_Clipping: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Retorna la configuración de H_Processing
    guardada para un clipping.

    """

    import uuid

    Consulta = select(
        Config_H_Processing
    ).where(
        Config_H_Processing.Id_Clipping
        == uuid.UUID(Id_Clipping),
    )
    Resultado = await Sesion.execute(Consulta)
    Config = Resultado.scalar_one_or_none()

    if not Config:
        return {
            "Primera_Letra_Mayuscula": True,
            "Borrar_Caracteres": False,
            "Caracteres_A_Borrar": "",
            "Primer_Caracter_Letra_Mayus": True,
            "Agregar_Signos_Faltantes": True,
        }

    return {
        "Primera_Letra_Mayuscula": (
            Config.Primera_Letra_Mayuscula
        ),
        "Borrar_Caracteres": (
            Config.Borrar_Caracteres
        ),
        "Caracteres_A_Borrar": (
            Config.Caracteres_A_Borrar
        ),
        "Primer_Caracter_Letra_Mayus": (
            Config.Primer_Caracter_Letra_Mayus
        ),
        "Agregar_Signos_Faltantes": (
            Config.Agregar_Signos_Faltantes
        ),
    }


@Router_Processing.put(
    "/config/{Id_Clipping}"
)
async def Guardar_Config_Clipping(
    Id_Clipping: str,
    Datos: Peticion_Procesamiento,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Guarda la configuración de H_Processing
    para un clipping.

    """

    import uuid

    Id = uuid.UUID(Id_Clipping)

    Consulta = select(
        Config_H_Processing
    ).where(
        Config_H_Processing.Id_Clipping == Id,
    )
    Resultado = await Sesion.execute(Consulta)
    Config = Resultado.scalar_one_or_none()

    if Config:
        Config.Primera_Letra_Mayuscula = (
            Datos.Primera_Letra_Mayuscula
        )
        Config.Borrar_Caracteres = (
            Datos.Borrar_Caracteres
        )
        Config.Caracteres_A_Borrar = (
            Datos.Caracteres_A_Borrar
        )
        Config.Primer_Caracter_Letra_Mayus = (
            Datos.Primer_Caracter_Letra_Mayus
        )
        Config.Agregar_Signos_Faltantes = (
            Datos.Agregar_Signos_Faltantes
        )
    else:
        Config = Config_H_Processing(
            Id_Clipping=Id,
            Primera_Letra_Mayuscula=(
                Datos.Primera_Letra_Mayuscula
            ),
            Borrar_Caracteres=(
                Datos.Borrar_Caracteres
            ),
            Caracteres_A_Borrar=(
                Datos.Caracteres_A_Borrar
            ),
            Primer_Caracter_Letra_Mayus=(
                Datos.Primer_Caracter_Letra_Mayus
            ),
            Agregar_Signos_Faltantes=(
                Datos.Agregar_Signos_Faltantes
            ),
        )
        Sesion.add(Config)

    await Sesion.commit()

    return {"Mensaje": "Config guardada"}
