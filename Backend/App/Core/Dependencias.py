"""
Dependencias de FastAPI reutilizables:
autenticación, sesión de DB, etc.

"""

import uuid

from fastapi import (
    Request,
    HTTPException,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Seguridad import (
    Verificar_Token,
)
from Backend.App.Modelos.Usuario import Usuario


async def Obtener_Usuario_Actual(
    Request_Obj: Request,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
) -> Usuario:

    """
    Extrae el usuario actual desde la cookie
    JWT httpOnly. Lanza 401 si no hay cookie
    o el token es inválido.

    """

    Token = Request_Obj.cookies.get(
        "Token_Acceso"
    )
    if not Token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado",
        )

    Payload = Verificar_Token(Token)
    if not Payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
        )

    Id_Usuario_Str = Payload.get("sub")
    if not Id_Usuario_Str:
        raise HTTPException(
            status_code=401,
            detail="Token sin usuario",
        )

    try:
        Id_Usuario = uuid.UUID(Id_Usuario_Str)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="ID de usuario inválido",
        )

    Consulta = select(Usuario).where(
        Usuario.Id_Usuario == Id_Usuario
    )
    Resultado = await Sesion.execute(Consulta)
    Usuario_Db = Resultado.scalar_one_or_none()

    if not Usuario_Db:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado",
        )

    return Usuario_Db
