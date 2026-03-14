"""
Exportador a XLSX usando openpyxl via pandas.

"""

import pandas as pd

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)


class Exportador_Xlsx(Exportador_Base):

    """
    Genera un archivo XLSX con los highlights.

    """

    @property
    def Extension(self) -> str:
        return "xlsx"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Exporta el DataFrame a XLSX.

        """

        Columnas = [
            "Texto", "Autor", "Libro",
            "Pagina", "Tipo_Semantico",
        ]
        Columnas_Existentes = [
            C for C in Columnas
            if C in Dataframe.columns
        ]

        Dataframe[Columnas_Existentes].to_excel(
            Ruta_Salida,
            index=False,
            engine="openpyxl",
        )

        return Ruta_Salida
