"""
Exportador a TXT (texto plano).

"""

import pandas as pd

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)


class Exportador_Txt(Exportador_Base):

    """
    Genera un archivo TXT con los highlights
    separados por líneas en blanco.

    """

    @property
    def Extension(self) -> str:
        return "txt"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Escribe cada highlight como texto plano
        con su Sub_Line debajo.

        """

        Campos_Sub = Config_Estilo.get(
            "Sub_Line_Campos",
            ["autor", "libro"],
        )

        with open(
            Ruta_Salida, "w", encoding="utf-8"
        ) as Archivo:

            for _, Fila in Dataframe.iterrows():
                Texto = str(
                    Fila.get("Texto", "")
                )
                Autor = str(
                    Fila.get("Autor", "") or ""
                )
                Libro = str(
                    Fila.get("Libro", "") or ""
                )

                Partes = []
                if (
                    "autor" in Campos_Sub
                    and Autor
                ):
                    Partes.append(Autor)
                if (
                    "libro" in Campos_Sub
                    and Libro
                ):
                    Partes.append(Libro)

                Sub = " — ".join(Partes)

                Archivo.write(f"{Texto}\n")
                if Sub:
                    Archivo.write(f"— {Sub}\n")
                Archivo.write("\n")

        return Ruta_Salida
