"""
Exportador a Obsidian (Markdown).

"""

import pandas as pd

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)

# Mapeo tipo semántico → Markdown.
TIPO_A_MARKDOWN = {
    "heading": "## ",
    "quote": "> ",
    "callout": "> [!note] ",
    "toggle": "<details><summary>",
    "paragraph": "",
}


class Exportador_Obsidian(Exportador_Base):

    """
    Genera un archivo Markdown compatible
    con Obsidian.

    """

    @property
    def Extension(self) -> str:
        return "md"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Genera el Markdown con tipos semánticos.

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
                Tipo = str(
                    Fila.get(
                        "Tipo_Semantico",
                        "paragraph",
                    )
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

                Prefijo = TIPO_A_MARKDOWN.get(
                    Tipo, ""
                )

                if Tipo == "toggle":
                    Archivo.write(
                        f"<details>"
                        f"<summary>{Texto}"
                        f"</summary>\n\n"
                    )
                    if Sub:
                        Archivo.write(
                            f"*{Sub}*\n"
                        )
                    Archivo.write(
                        "</details>\n\n"
                    )
                elif Tipo == "quote":
                    Archivo.write(
                        f"> {Texto}\n"
                    )
                    if Sub:
                        Archivo.write(
                            f"> *— {Sub}*\n"
                        )
                    Archivo.write("\n")
                elif Tipo == "callout":
                    Archivo.write(
                        f"> [!quote]\n"
                        f"> {Texto}\n"
                    )
                    if Sub:
                        Archivo.write(
                            f"> *— {Sub}*\n"
                        )
                    Archivo.write("\n")
                elif Tipo == "heading":
                    Archivo.write(
                        f"## {Texto}\n\n"
                    )
                    if Sub:
                        Archivo.write(
                            f"*{Sub}*\n\n"
                        )
                else:
                    Archivo.write(
                        f"{Texto}\n"
                    )
                    if Sub:
                        Archivo.write(
                            f"*— {Sub}*\n"
                        )
                    Archivo.write("\n")

        return Ruta_Salida
