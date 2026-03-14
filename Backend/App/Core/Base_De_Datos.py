"""
Configuración de la conexión a PostgreSQL
con SQLAlchemy async.

"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

from Backend.App.Core.Config import Ajustes


Motor = create_async_engine(
    Ajustes.Database_Url,
    echo=False,
    future=True,
)

Sesion_Local = async_sessionmaker(
    bind=Motor,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):

    """
    Clase base para todos los modelos
    de SQLAlchemy.

    """

    pass


async def Obtener_Sesion():

    """
    Generador de sesiones de base de datos
    para inyección de dependencias en FastAPI.

    """

    async with Sesion_Local() as Sesion:
        try:
            yield Sesion
        finally:
            await Sesion.close()
