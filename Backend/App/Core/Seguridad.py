"""
Funciones de seguridad: JWT, hashing,
encriptación de tokens OAuth.

"""

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from cryptography.fernet import Fernet

from Backend.App.Core.Config import Ajustes


def Crear_Token_Acceso(
    Datos: dict,
    Expiracion_Delta: timedelta | None = None,
) -> str:

    """
    Crea un JWT con los datos proporcionados
    y una expiración configurable.

    """

    Datos_A_Codificar = Datos.copy()

    if Expiracion_Delta:
        Expiracion = (
            datetime.now(timezone.utc)
            + Expiracion_Delta
        )
    else:
        Expiracion = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=Ajustes
                .Access_Token_Expire_Minutes
            )
        )

    Datos_A_Codificar.update(
        {"exp": Expiracion}
    )

    Token = jwt.encode(
        Datos_A_Codificar,
        Ajustes.Secret_Key,
        algorithm=Ajustes.Algorithm,
    )

    return Token


def Verificar_Token(Token: str) -> dict | None:

    """
    Decodifica y verifica un JWT.
    Retorna los datos del payload o None
    si el token es inválido.

    """

    try:
        Payload = jwt.decode(
            Token,
            Ajustes.Secret_Key,
            algorithms=[Ajustes.Algorithm],
        )
        return Payload
    except JWTError:
        return None


def Encriptar_Token_Oauth(
    Valor_Token: str,
) -> str:

    """
    Encripta un token OAuth con Fernet para
    almacenamiento seguro en la base de datos.

    """

    Cifrador = Fernet(
        Ajustes.Fernet_Key.encode()
    )

    return Cifrador.encrypt(
        Valor_Token.encode()
    ).decode()


def Desencriptar_Token_Oauth(
    Token_Encriptado: str,
) -> str:

    """
    Desencripta un token OAuth almacenado
    en la base de datos.

    """

    Cifrador = Fernet(
        Ajustes.Fernet_Key.encode()
    )

    return Cifrador.decrypt(
        Token_Encriptado.encode()
    ).decode()
