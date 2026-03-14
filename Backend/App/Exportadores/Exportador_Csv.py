"""
Exportador a CSV usando pandas.

"""

import pandas as pd

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)


class Exportador_Csv(Exportador_Base):

    """
    Genera un archivo CSV con los highlights.

    """

    @property
    def Extension(self) -> str:
        return "csv"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Exporta el DataFrame a CSV con
        encoding utf-8-sig para Excel.

        """

        Columnas = [
            "Texto", "Autor", "Libro",
            "Pagina", "Tipo_Semantico",
        ]
        Columnas_Existentes = [
            C for C in Columnas
            if C in Dataframe.columns
        ]

        Dataframe[Columnas_Existentes].to_csv(
            Ruta_Salida,
            index=False,
            encoding="utf-8-sig",
        )

        return Ruta_Salida
