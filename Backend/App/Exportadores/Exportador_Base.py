"""
Clase abstracta base para todos los
exportadores. Patrón Strategy.

"""

from abc import ABC, abstractmethod

import pandas as pd


class Exportador_Base(ABC):

    """
    Interfaz que todos los exportadores
    deben implementar.

    """

    @abstractmethod
    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Genera el archivo de exportación.

        Retorna la ruta del archivo generado.

        """

        pass

    @property
    @abstractmethod
    def Extension(self) -> str:

        """
        Extensión del archivo generado
        (sin punto).

        """

        pass
