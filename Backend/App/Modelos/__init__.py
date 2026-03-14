"""
Exporta todos los modelos para que Alembic
los detecte automáticamente.

"""

from Backend.App.Modelos.Usuario import (
    Usuario,
    Conexion_Oauth,
)
from Backend.App.Modelos.Highlight import (
    Archivo_Subido,
    Highlight,
    Clipping,
    Clipping_Highlight,
    Config_H_Processing,
)
from Backend.App.Modelos.Configuracion import (
    Config_Exportacion,
    Regla_Marca,
    Config_Notion,
    N_Match,
)

__all__ = [
    "Usuario",
    "Conexion_Oauth",
    "Archivo_Subido",
    "Highlight",
    "Clipping",
    "Clipping_Highlight",
    "Config_H_Processing",
    "Config_Exportacion",
    "Regla_Marca",
    "Config_Notion",
    "N_Match",
]
