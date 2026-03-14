"""
Endpoints de autenticación: OAuth con
Google y Notion, logout, refresh.

"""

from fastapi import (
    APIRouter,
    Depends,
    Response,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from authlib.integrations.httpx_client import (
    AsyncOAuth2Client,
)

from Backend.App.Core.Config import Ajustes
from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Seguridad import (
    Crear_Token_Acceso,
    Verificar_Token,
    Encriptar_Token_Oauth,
)
from Backend.App.Modelos.Usuario import (
    Usuario,
    Conexion_Oauth,
)

Router_Auth = APIRouter()


async def Obtener_Usuario_Actual(
    Response_Obj: Response,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
) -> Usuario:

    """
    Dependencia que extrae el usuario actual
    desde la cookie JWT httpOnly.

    """

    # Placeholder: se implementa con
    # request.cookies en el middleware real.
    raise HTTPException(
        status_code=401,
        detail="No autenticado",
    )


@Router_Auth.get("/google/login")
async def Login_Google():

    """
    Redirige al usuario a la pantalla de
    consentimiento de Google OAuth.

    """

    Cliente = AsyncOAuth2Client(
        client_id=Ajustes.Google_Client_Id,
        client_secret=(
            Ajustes.Google_Client_Secret
        ),
        redirect_uri=(
            Ajustes.Google_Redirect_Uri
        ),
    )

    Uri, Estado = Cliente.create_authorization_url(
        "https://accounts.google.com/o/oauth2/v2/auth",
        scope="openid email profile",
    )

    return {"Url_Redireccion": Uri}


@Router_Auth.get("/google/callback")
async def Callback_Google(
    code: str,
    Respuesta: Response,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Callback de Google OAuth. Crea o actualiza
    el usuario y establece cookie JWT.

    """

    Cliente = AsyncOAuth2Client(
        client_id=Ajustes.Google_Client_Id,
        client_secret=(
            Ajustes.Google_Client_Secret
        ),
        redirect_uri=(
            Ajustes.Google_Redirect_Uri
        ),
    )

    Token = await Cliente.fetch_token(
        "https://oauth2.googleapis.com/token",
        code=code,
    )

    Info_Usuario = await Cliente.get(
        "https://www.googleapis.com"
        "/oauth2/v3/userinfo"
    )
    Datos = Info_Usuario.json()

    # Buscar o crear usuario.
    Consulta = select(Usuario).where(
        Usuario.Email == Datos["email"]
    )
    Resultado = await Sesion.execute(Consulta)
    Usuario_Db = Resultado.scalar_one_or_none()

    if not Usuario_Db:
        Usuario_Db = Usuario(
            Email=Datos["email"],
            Nickname=Datos.get("name"),
            Avatar_Url=Datos.get("picture"),
        )
        Sesion.add(Usuario_Db)
        await Sesion.flush()

    # Guardar o actualizar conexión OAuth.
    Consulta_Conexion = select(
        Conexion_Oauth
    ).where(
        Conexion_Oauth.Id_Usuario
        == Usuario_Db.Id_Usuario,
        Conexion_Oauth.Proveedor == "google",
    )
    Resultado_Conexion = await Sesion.execute(
        Consulta_Conexion
    )
    Conexion = (
        Resultado_Conexion.scalar_one_or_none()
    )

    Token_Encriptado = Encriptar_Token_Oauth(
        Token["access_token"]
    )

    if Conexion:
        Conexion.Access_Token = Token_Encriptado
        Conexion.Id_Externo = Datos["sub"]
    else:
        Conexion = Conexion_Oauth(
            Id_Usuario=Usuario_Db.Id_Usuario,
            Proveedor="google",
            Access_Token=Token_Encriptado,
            Id_Externo=Datos["sub"],
        )
        Sesion.add(Conexion)

    await Sesion.commit()

    # Crear JWT y setear cookie.
    Jwt = Crear_Token_Acceso(
        {"sub": str(Usuario_Db.Id_Usuario)}
    )

    Respuesta.set_cookie(
        key="Token_Acceso",
        value=Jwt,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )

    return {
        "Mensaje": "Login exitoso",
        "Usuario": {
            "Id": str(
                Usuario_Db.Id_Usuario
            ),
            "Email": Usuario_Db.Email,
            "Nickname": Usuario_Db.Nickname,
        },
    }


@Router_Auth.get("/notion/login")
async def Login_Notion():

    """
    Redirige al usuario a la pantalla de
    autorización de Notion OAuth.

    """

    Url_Base = (
        "https://api.notion.com/v1/oauth"
        "/authorize"
    )
    Params = (
        f"?client_id="
        f"{Ajustes.Notion_Client_Id}"
        f"&redirect_uri="
        f"{Ajustes.Notion_Redirect_Uri}"
        f"&response_type=code"
        f"&owner=user"
    )

    return {
        "Url_Redireccion": Url_Base + Params
    }


@Router_Auth.get("/notion/callback")
async def Callback_Notion(
    code: str,
    Respuesta: Response,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Callback de Notion OAuth. Asocia la cuenta
    de Notion al usuario existente o crea uno.

    """

    import httpx

    async with httpx.AsyncClient() as Http:
        Respuesta_Token = await Http.post(
            "https://api.notion.com"
            "/v1/oauth/token",
            json={
                "grant_type":
                    "authorization_code",
                "code": code,
                "redirect_uri":
                    Ajustes.Notion_Redirect_Uri,
            },
            auth=(
                Ajustes.Notion_Client_Id,
                Ajustes.Notion_Client_Secret,
            ),
        )

    if Respuesta_Token.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Error en OAuth de Notion",
        )

    Datos_Token = Respuesta_Token.json()
    Info_Owner = Datos_Token.get("owner", {})
    Info_User = Info_Owner.get("user", {})
    Email_Notion = (
        Info_User.get("person", {})
        .get("email", "")
    )

    # Buscar o crear usuario.
    Consulta = select(Usuario).where(
        Usuario.Email == Email_Notion
    )
    Resultado = await Sesion.execute(Consulta)
    Usuario_Db = Resultado.scalar_one_or_none()

    if not Usuario_Db:
        Usuario_Db = Usuario(
            Email=Email_Notion,
            Nickname=Info_User.get("name"),
        )
        Sesion.add(Usuario_Db)
        await Sesion.flush()

    # Guardar conexión.
    Token_Encriptado = Encriptar_Token_Oauth(
        Datos_Token["access_token"]
    )

    Consulta_Conexion = select(
        Conexion_Oauth
    ).where(
        Conexion_Oauth.Id_Usuario
        == Usuario_Db.Id_Usuario,
        Conexion_Oauth.Proveedor == "notion",
    )
    Resultado_Conexion = await Sesion.execute(
        Consulta_Conexion
    )
    Conexion = (
        Resultado_Conexion.scalar_one_or_none()
    )

    if Conexion:
        Conexion.Access_Token = Token_Encriptado
    else:
        Conexion = Conexion_Oauth(
            Id_Usuario=Usuario_Db.Id_Usuario,
            Proveedor="notion",
            Access_Token=Token_Encriptado,
            Id_Externo=Datos_Token.get(
                "bot_id", ""
            ),
        )
        Sesion.add(Conexion)

    await Sesion.commit()

    Jwt = Crear_Token_Acceso(
        {"sub": str(Usuario_Db.Id_Usuario)}
    )

    Respuesta.set_cookie(
        key="Token_Acceso",
        value=Jwt,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )

    return {
        "Mensaje": "Login con Notion exitoso",
        "Usuario": {
            "Id": str(
                Usuario_Db.Id_Usuario
            ),
            "Email": Usuario_Db.Email,
        },
    }


@Router_Auth.post("/logout")
async def Logout(Respuesta: Response):

    """
    Cierra la sesión eliminando la cookie JWT.

    """

    Respuesta.delete_cookie("Token_Acceso")
    return {"Mensaje": "Sesión cerrada"}


@Router_Auth.get("/me")
async def Obtener_Me(
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
):

    """
    Retorna el usuario autenticado.
    Placeholder hasta implementar middleware.

    """

    return {"Detalle": "Implementar con cookie"}
