"""
Exportador a XLS usando xlwt via pandas.
Nota: XLS tiene límite de 65536 filas.

"""

import pandas as pd

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)


class Exportador_Xls(Exportador_Base):

    """
    Genera un archivo XLS con los highlights.

    """

    @property
    def Extension(self) -> str:
        return "xls"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Exporta el DataFrame a XLS.
        Advierte si se exceden 65536 filas.

        """

        if len(Dataframe) > 65536:
            Dataframe = Dataframe.head(65536)

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
            engine="xlwt",
        )

        return Ruta_Salida
