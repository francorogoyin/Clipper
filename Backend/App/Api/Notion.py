"""
Endpoints de integración con Notion:
explorar páginas, matcheo, paste y config.

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
from notion_client import Client

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Dependencias import (
    Obtener_Usuario_Actual,
)
from Backend.App.Core.Seguridad import (
    Desencriptar_Token_Oauth,
)
from Backend.App.Modelos.Usuario import (
    Usuario,
    Conexion_Oauth,
)
from Backend.App.Modelos.Configuracion import (
    Config_Notion,
    N_Match,
)

Router_Notion = APIRouter()


# --- Helpers ---

async def _Obtener_Cliente_Notion(
    Sesion: AsyncSession,
    Id_Usuario: uuid.UUID,
) -> Client:

    """
    Obtiene un Client de Notion autenticado
    con el token OAuth del usuario.

    """

    Consulta = select(Conexion_Oauth).where(
        Conexion_Oauth.Id_Usuario == Id_Usuario,
        Conexion_Oauth.Proveedor == "notion",
    )
    Resultado = await Sesion.execute(Consulta)
    Conexion = Resultado.scalar_one_or_none()

    if not Conexion:
        raise HTTPException(
            status_code=400,
            detail="No hay conexión con Notion."
            " Conectá tu cuenta primero.",
        )

    Token = Desencriptar_Token_Oauth(
        Conexion.Access_Token
    )

    return Client(auth=Token)


# --- Schemas ---

class Peticion_Match_Auto(BaseModel):
    Ids_Clippings: list[str]
    Campo_Matcheo: str = "nombre"
    Propiedad_N_Page: str = "title"


class Peticion_Match_Manual(BaseModel):
    Id_Clipping: str
    N_Page_Id: str
    N_Page_Titulo: str | None = None
    Guardar_Permanente: bool = False


class Peticion_Crear_Pagina(BaseModel):
    Titulo: str
    Emoji: str | None = None
    Id_Padre: str


class Peticion_Config_Notion(BaseModel):
    Id_N_Database: str | None = None
    Titulo_N_Database: str | None = None
    Campo_Matcheo_Clipping: str = "nombre"
    Propiedad_Matcheo_N_Page: str = "title"
    N_Block_Tipo: str = "paragraph"
    N_Block_Formato: str = "normal"
    N_Block_Color: str = "default"
    N_Block_Color_Fondo: str = "default"
    N_Block_Alineacion: str = "izquierda"
    N_Block_Emoji: str | None = None


# --- Endpoints ---

@Router_Notion.get("/paginas")
async def Explorar_Paginas(
    Id_Padre: str | None = None,
    Busqueda: str | None = None,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Explora páginas de Notion para el
    N_Explorer. Si Id_Padre está presente,
    retorna hijos. Si Busqueda, filtra.

    """

    Cliente = await _Obtener_Cliente_Notion(
        Sesion, Usuario_Actual.Id_Usuario
    )

    if Busqueda:
        Resultado = Cliente.search(
            query=Busqueda,
            filter={"property": "object",
                    "value": "page"},
            page_size=20,
        )
    elif Id_Padre:
        Resultado = Cliente.blocks.children.list(
            block_id=Id_Padre,
            page_size=50,
        )
    else:
        Resultado = Cliente.search(
            filter={"property": "object",
                    "value": "page"},
            page_size=20,
        )

    Paginas = []
    for Item in Resultado.get("results", []):
        Titulo = ""
        Props = Item.get("properties", {})
        Titulo_Prop = Props.get("title", {})

        if isinstance(Titulo_Prop, dict):
            Titulo_Array = Titulo_Prop.get(
                "title", []
            )
            if Titulo_Array:
                Titulo = Titulo_Array[0].get(
                    "plain_text", ""
                )

        if not Titulo:
            Title_List = Item.get(
                "title", []
            )
            if Title_List:
                Titulo = Title_List[0].get(
                    "plain_text", ""
                )

        Paginas.append({
            "Id": Item.get("id", ""),
            "Titulo": Titulo,
            "Tipo": Item.get("object", ""),
            "Icono": Item.get(
                "icon", {}
            ).get("emoji", ""),
        })

    return {"Paginas": Paginas}


@Router_Notion.get(
    "/paginas/{N_Page_Id}/bloques"
)
async def Obtener_Bloques_Pagina(
    N_Page_Id: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Retorna los bloques de una página Notion.
    Para seleccionar posición de paste.

    """

    Cliente = await _Obtener_Cliente_Notion(
        Sesion, Usuario_Actual.Id_Usuario
    )

    Resultado = Cliente.blocks.children.list(
        block_id=N_Page_Id,
        page_size=100,
    )

    Bloques = [
        {
            "Id": B.get("id", ""),
            "Tipo": B.get("type", ""),
            "Texto": _Extraer_Texto_Bloque(B),
        }
        for B in Resultado.get("results", [])
    ]

    return {"Bloques": Bloques}


@Router_Notion.post("/match/auto")
async def Matcheo_Automatico(
    Datos: Peticion_Match_Auto,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Matcheo automático configurable entre
    Clippings y N_Pages.

    """

    Cliente = await _Obtener_Cliente_Notion(
        Sesion, Usuario_Actual.Id_Usuario
    )

    # Obtener todas las páginas.
    Resultado = Cliente.search(
        filter={"property": "object",
                "value": "page"},
        page_size=100,
    )

    # Indexar páginas por título.
    Paginas_Por_Titulo = {}
    for P in Resultado.get("results", []):
        Titulo = _Extraer_Titulo_Pagina(P)
        if Titulo:
            Paginas_Por_Titulo[
                Titulo.lower().strip()
            ] = {
                "Id": P.get("id", ""),
                "Titulo": Titulo,
            }

    Matches = []
    Sin_Match = []

    for Id_Clipping in Datos.Ids_Clippings:
        # Placeholder: obtener nombre del
        # clipping de la DB.
        Nombre_Clipping = Id_Clipping
        Nombre_Lower = (
            Nombre_Clipping.lower().strip()
        )

        if Nombre_Lower in Paginas_Por_Titulo:
            Pagina = Paginas_Por_Titulo[
                Nombre_Lower
            ]
            Matches.append({
                "Id_Clipping": Id_Clipping,
                "N_Page_Id": Pagina["Id"],
                "N_Page_Titulo": Pagina[
                    "Titulo"
                ],
            })
        else:
            Sin_Match.append(Id_Clipping)

    return {
        "Matches": Matches,
        "Sin_Match": Sin_Match,
    }


@Router_Notion.post("/match/manual")
async def Match_Manual(
    Datos: Peticion_Match_Manual,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Asigna un match manual entre Clipping
    y N_Page.

    """

    Match = N_Match(
        Id_Usuario=Usuario_Actual.Id_Usuario,
        Id_Clipping=uuid.UUID(
            Datos.Id_Clipping
        ),
        N_Page_Id=Datos.N_Page_Id,
        N_Page_Titulo=Datos.N_Page_Titulo,
        Guardado_Permanente=(
            Datos.Guardar_Permanente
        ),
    )

    Sesion.add(Match)
    await Sesion.commit()

    return {
        "Id_N_Match": str(Match.Id_N_Match),
        "Mensaje": "Match creado",
    }


@Router_Notion.delete("/match/{Id_N_Match}")
async def Eliminar_Match(
    Id_N_Match: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Elimina un match.

    """

    Consulta = select(N_Match).where(
        N_Match.Id_N_Match
        == uuid.UUID(Id_N_Match),
        N_Match.Id_Usuario
        == Usuario_Actual.Id_Usuario,
    )
    Resultado = await Sesion.execute(Consulta)
    Match = Resultado.scalar_one_or_none()

    if not Match:
        raise HTTPException(
            status_code=404,
            detail="Match no encontrado",
        )

    await Sesion.delete(Match)
    await Sesion.commit()

    return {"Mensaje": "Match eliminado"}


@Router_Notion.get("/matches")
async def Listar_Matches(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Lista todos los N_Matches del usuario.

    """

    Consulta = select(N_Match).where(
        N_Match.Id_Usuario
        == Usuario_Actual.Id_Usuario
    )
    Resultado = await Sesion.execute(Consulta)
    Matches = Resultado.scalars().all()

    return {
        "Matches": [
            {
                "Id_N_Match": str(
                    M.Id_N_Match
                ),
                "Id_Clipping": str(
                    M.Id_Clipping
                ),
                "N_Page_Id": M.N_Page_Id,
                "N_Page_Titulo": (
                    M.N_Page_Titulo
                ),
                "Posicion_Paste": (
                    M.Posicion_Paste
                ),
                "Guardado_Permanente": (
                    M.Guardado_Permanente
                ),
            }
            for M in Matches
        ],
    }


@Router_Notion.post("/paginas")
async def Crear_Pagina_Notion(
    Datos: Peticion_Crear_Pagina,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Crea una nueva N_Page en Notion.

    """

    Cliente = await _Obtener_Cliente_Notion(
        Sesion, Usuario_Actual.Id_Usuario
    )

    Props_Pagina: dict = {
        "parent": {
            "page_id": Datos.Id_Padre,
        },
        "properties": {
            "title": [
                {
                    "text": {
                        "content": Datos.Titulo,
                    }
                }
            ]
        },
    }

    if Datos.Emoji:
        Props_Pagina["icon"] = {
            "type": "emoji",
            "emoji": Datos.Emoji,
        }

    Pagina = Cliente.pages.create(
        **Props_Pagina
    )

    return {
        "Id": Pagina.get("id", ""),
        "Titulo": Datos.Titulo,
        "Mensaje": "Página creada",
    }


@Router_Notion.get("/config")
async def Obtener_Config_Notion(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Retorna la config de Notion del usuario.

    """

    Consulta = select(Config_Notion).where(
        Config_Notion.Id_Usuario
        == Usuario_Actual.Id_Usuario
    )
    Resultado = await Sesion.execute(Consulta)
    Config = Resultado.scalar_one_or_none()

    if not Config:
        return Peticion_Config_Notion(
        ).model_dump()

    return {
        "Id_N_Database": Config.Id_N_Database,
        "Titulo_N_Database": (
            Config.Titulo_N_Database
        ),
        "Campo_Matcheo_Clipping": (
            Config.Campo_Matcheo_Clipping
        ),
        "Propiedad_Matcheo_N_Page": (
            Config.Propiedad_Matcheo_N_Page
        ),
        "N_Block_Tipo": Config.N_Block_Tipo,
        "N_Block_Formato": (
            Config.N_Block_Formato
        ),
        "N_Block_Color": Config.N_Block_Color,
        "N_Block_Color_Fondo": (
            Config.N_Block_Color_Fondo
        ),
        "N_Block_Alineacion": (
            Config.N_Block_Alineacion
        ),
        "N_Block_Emoji": Config.N_Block_Emoji,
    }


@Router_Notion.put("/config")
async def Guardar_Config_Notion(
    Datos: Peticion_Config_Notion,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Guarda la config de Notion del usuario.

    """

    Consulta = select(Config_Notion).where(
        Config_Notion.Id_Usuario
        == Usuario_Actual.Id_Usuario
    )
    Resultado = await Sesion.execute(Consulta)
    Config = Resultado.scalar_one_or_none()

    if Config:
        for Campo, Valor in (
            Datos.model_dump().items()
        ):
            setattr(Config, Campo, Valor)
    else:
        Config = Config_Notion(
            Id_Usuario=(
                Usuario_Actual.Id_Usuario
            ),
            **Datos.model_dump(),
        )
        Sesion.add(Config)

    await Sesion.commit()

    return {"Mensaje": "Config guardada"}


# --- Utilidades ---

def _Extraer_Texto_Bloque(
    Bloque: dict,
) -> str:

    """
    Extrae el texto plano de un bloque Notion.

    """

    Tipo = Bloque.get("type", "")
    Contenido = Bloque.get(Tipo, {})
    Rich_Text = Contenido.get(
        "rich_text", []
    )

    return "".join(
        T.get("plain_text", "")
        for T in Rich_Text
    )


def _Extraer_Titulo_Pagina(
    Pagina: dict,
) -> str:

    """
    Extrae el título de una página Notion.

    """

    Props = Pagina.get("properties", {})

    for Valor in Props.values():
        if Valor.get("type") == "title":
            Title_Array = Valor.get(
                "title", []
            )
            if Title_Array:
                return Title_Array[0].get(
                    "plain_text", ""
                )

    return ""
