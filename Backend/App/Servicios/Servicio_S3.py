"""
Servicio para subir y descargar archivos
desde S3 o Cloudflare R2.

"""

import uuid

import boto3
from botocore.config import Config

from Backend.App.Core.Config import Ajustes


def _Crear_Cliente_S3():

    """
    Crea y retorna un cliente de boto3
    configurado para S3 o Cloudflare R2.

    """

    return boto3.client(
        "s3",
        endpoint_url=Ajustes.S3_Endpoint_Url,
        aws_access_key_id=Ajustes.S3_Access_Key,
        aws_secret_access_key=(
            Ajustes.S3_Secret_Key
        ),
        region_name=Ajustes.S3_Region,
        config=Config(
            signature_version="s3v4"
        ),
    )


def Subir_Archivo(
    Contenido_Bytes: bytes,
    Nombre_Original: str,
    Id_Usuario: str,
) -> str:

    """
    Sube un archivo a S3 y retorna la ruta
    (key) donde fue almacenado.

    La ruta tiene formato:
    uploads/{Id_Usuario}/{uuid}_{nombre}

    """

    Id_Unico = str(uuid.uuid4())[:8]
    Key = (
        f"uploads/{Id_Usuario}/"
        f"{Id_Unico}_{Nombre_Original}"
    )

    Cliente = _Crear_Cliente_S3()
    Cliente.put_object(
        Bucket=Ajustes.S3_Bucket_Name,
        Key=Key,
        Body=Contenido_Bytes,
    )

    return Key


def Descargar_Archivo(Key: str) -> bytes:

    """
    Descarga un archivo de S3 y retorna
    su contenido como bytes.

    """

    Cliente = _Crear_Cliente_S3()
    Respuesta = Cliente.get_object(
        Bucket=Ajustes.S3_Bucket_Name,
        Key=Key,
    )

    return Respuesta["Body"].read()


def Generar_Url_Descarga(
    Key: str,
    Expiracion_Segundos: int = 3600,
) -> str:

    """
    Genera una URL pre-firmada para descargar
    un archivo de S3 sin autenticación.
    Expira en 1 hora por defecto.

    """

    Cliente = _Crear_Cliente_S3()

    return Cliente.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": Ajustes.S3_Bucket_Name,
            "Key": Key,
        },
        ExpiresIn=Expiracion_Segundos,
    )
