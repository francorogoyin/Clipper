"""
Exportador a ODT via pypandoc (desde DOCX).

"""

import os
import tempfile

import pandas as pd
import pypandoc

from Backend.App.Exportadores.Exportador_Docx import (
    Exportador_Docx,
)
from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)


class Exportador_Odt(Exportador_Base):

    """
    Genera un ODT creando primero un DOCX
    temporal y convirtiéndolo con pypandoc.

    """

    @property
    def Extension(self) -> str:
        return "odt"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Genera el ODT.

        """

        with tempfile.NamedTemporaryFile(
            suffix=".docx", delete=False
        ) as Temp:
            Ruta_Temp = Temp.name

        try:
            Exportador_Docx().Exportar(
                Dataframe, Ruta_Temp, Config_Estilo
            )
            pypandoc.convert_file(
                Ruta_Temp,
                "odt",
                outputfile=Ruta_Salida,
            )
        finally:
            if os.path.exists(Ruta_Temp):
                os.unlink(Ruta_Temp)

        return Ruta_Salida
