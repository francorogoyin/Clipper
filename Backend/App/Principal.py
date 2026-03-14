"""
Punto de entrada de la API FastAPI.
Configura CORS, routers y eventos de vida.

"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from Backend.App.Core.Config import Ajustes
from Backend.App.Core.Base_De_Datos import (
    Motor,
    Base,
)
from Backend.App.Api.Auth import (
    Router_Auth,
)
from Backend.App.Api.Usuarios import (
    Router_Usuarios,
)
from Backend.App.Api.Archivos import (
    Router_Archivos,
)
from Backend.App.Api.Highlights import (
    Router_Highlights,
)
from Backend.App.Api.Clippings import (
    Router_Clippings,
)
from Backend.App.Api.Processing import (
    Router_Processing,
)
from Backend.App.Api.Export import (
    Router_Export,
)
from Backend.App.Api.Notion import (
    Router_Notion,
)


@asynccontextmanager
async def Ciclo_De_Vida(App: FastAPI):

    """
    Crea las tablas al iniciar y cierra
    el motor al apagar.

    """

    async with Motor.begin() as Conexion:
        await Conexion.run_sync(
            Base.metadata.create_all
        )
    yield
    await Motor.dispose()


App = FastAPI(
    title="Highlighter API",
    version="0.1.0",
    lifespan=Ciclo_De_Vida,
)

# CORS para el frontend.
App.add_middleware(
    CORSMiddleware,
    allow_origins=[Ajustes.Frontend_Url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers.
App.include_router(
    Router_Auth,
    prefix="/api/auth",
    tags=["Auth"],
)
App.include_router(
    Router_Usuarios,
    prefix="/api/users",
    tags=["Users"],
)
App.include_router(
    Router_Archivos,
    prefix="/api/files",
    tags=["Files"],
)
App.include_router(
    Router_Highlights,
    prefix="/api/highlights",
    tags=["Highlights"],
)
App.include_router(
    Router_Clippings,
    prefix="/api/clippings",
    tags=["Clippings"],
)
App.include_router(
    Router_Processing,
    prefix="/api/processing",
    tags=["Processing"],
)
App.include_router(
    Router_Export,
    prefix="/api/export",
    tags=["Export"],
)
App.include_router(
    Router_Notion,
    prefix="/api/notion",
    tags=["Notion"],
)


@App.get("/api/health")
async def Health_Check():

    """
    Endpoint de salud para verificar que
    la API está corriendo.

    """

    return {"Estado": "ok"}
