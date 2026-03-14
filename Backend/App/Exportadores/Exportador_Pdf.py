"""
Exportador a PDF usando fpdf2.
Soporta los 6 estilos de Block y configuración
de fuente, color, tamaño y alineación.

"""

import os

import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)


# Mapeo de alineación.
ALINEACIONES = {
    "izquierda": "L",
    "derecha": "R",
    "centro": "C",
    "justificada": "J",
}


class Exportador_Pdf(Exportador_Base):

    """
    Genera un archivo PDF con los highlights
    usando el estilo de Block configurado.

    """

    @property
    def Extension(self) -> str:
        return "pdf"

    def Exportar(
        self,
        Dataframe: pd.DataFrame,
        Ruta_Salida: str,
        Config_Estilo: dict,
    ) -> str:

        """
        Genera el PDF con los highlights.

        """

        Pdf = FPDF()
        Pdf.set_auto_page_break(
            auto=True, margin=15
        )

        # Cargar fuente unicode si existe.
        Ruta_Fuente = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(
                                __file__
                            )
                        )
                    )
                )
            ),
            "Fuentes",
            "arial-unicode-ms.ttf",
        )

        if os.path.exists(Ruta_Fuente):
            Pdf.add_font(
                "ArialUnicode",
                "",
                Ruta_Fuente,
            )
            Fuente_Default = "ArialUnicode"
        else:
            Fuente_Default = "Helvetica"

        Estilo = Config_Estilo.get(
            "Estilo_Block", 1
        )
        Highlight_Config = {
            "Fuente": Config_Estilo.get(
                "Highlight_Fuente",
                Fuente_Default,
            ),
            "Tamano": Config_Estilo.get(
                "Highlight_Tamano", 12
            ),
            "Color": Config_Estilo.get(
                "Highlight_Color", "#000000"
            ),
            "Formato": Config_Estilo.get(
                "Highlight_Formato", "normal"
            ),
            "Alineacion": Config_Estilo.get(
                "Highlight_Alineacion",
                "izquierda",
            ),
        }
        Sub_Line_Config = {
            "Fuente": Config_Estilo.get(
                "Sub_Line_Fuente",
                Fuente_Default,
            ),
            "Tamano": Config_Estilo.get(
                "Sub_Line_Tamano", 10
            ),
            "Color": Config_Estilo.get(
                "Sub_Line_Color", "#666666"
            ),
            "Formato": Config_Estilo.get(
                "Sub_Line_Formato", "cursiva"
            ),
            "Alineacion": Config_Estilo.get(
                "Sub_Line_Alineacion",
                "izquierda",
            ),
        }

        Pdf.add_page()

        for _, Fila in Dataframe.iterrows():
            Texto = str(Fila.get("Texto", ""))
            Autor = str(
                Fila.get("Autor", "") or ""
            )
            Libro = str(
                Fila.get("Libro", "") or ""
            )

            # Construir Sub_Line.
            Campos_Sub = Config_Estilo.get(
                "Sub_Line_Campos",
                ["autor", "libro"],
            )
            Partes_Sub = []
            if "autor" in Campos_Sub and Autor:
                Partes_Sub.append(Autor)
            if "libro" in Campos_Sub and Libro:
                Partes_Sub.append(Libro)

            Sub_Line = " — ".join(Partes_Sub)

            _Renderizar_Block(
                Pdf,
                Texto,
                Sub_Line,
                Estilo,
                Highlight_Config,
                Sub_Line_Config,
                Fuente_Default,
            )

        Pdf.output(Ruta_Salida)
        return Ruta_Salida


def _Renderizar_Block(
    Pdf: FPDF,
    Texto: str,
    Sub_Line: str,
    Estilo: int,
    H_Config: dict,
    S_Config: dict,
    Fuente_Default: str,
):

    """
    Renderiza un block (highlight + sub_line)
    según el estilo elegido.

    """

    # Configurar fuente del highlight.
    _Aplicar_Fuente(
        Pdf, H_Config, Fuente_Default
    )
    _Aplicar_Color(Pdf, H_Config["Color"])

    Alineacion_H = ALINEACIONES.get(
        H_Config["Alineacion"], "L"
    )
    Alineacion_S = ALINEACIONES.get(
        S_Config["Alineacion"], "L"
    )

    if Estilo == 1:
        # Clásico: highlight, línea, sub_line.
        Pdf.multi_cell(
            w=0,
            h=6,
            text=Texto,
            align=Alineacion_H,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        Pdf.line(
            Pdf.l_margin,
            Pdf.get_y() + 2,
            Pdf.w - Pdf.r_margin,
            Pdf.get_y() + 2,
        )
        Pdf.ln(5)
        _Aplicar_Fuente(
            Pdf, S_Config, Fuente_Default
        )
        _Aplicar_Color(Pdf, S_Config["Color"])
        Pdf.multi_cell(
            w=0,
            h=5,
            text=Sub_Line,
            align=Alineacion_S,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    elif Estilo == 2:
        # Cita: barra izquierda.
        X_Inicio = Pdf.get_x()
        Y_Inicio = Pdf.get_y()
        Pdf.set_x(X_Inicio + 8)
        Pdf.multi_cell(
            w=Pdf.w - Pdf.l_margin
            - Pdf.r_margin - 8,
            h=6,
            text=Texto,
            align=Alineacion_H,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        Pdf.set_x(X_Inicio + 8)
        _Aplicar_Fuente(
            Pdf, S_Config, Fuente_Default
        )
        _Aplicar_Color(Pdf, S_Config["Color"])
        Pdf.multi_cell(
            w=Pdf.w - Pdf.l_margin
            - Pdf.r_margin - 8,
            h=5,
            text=f"— {Sub_Line}",
            align=Alineacion_S,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        Y_Fin = Pdf.get_y()
        Pdf.set_draw_color(180, 180, 180)
        Pdf.line(
            X_Inicio + 3,
            Y_Inicio,
            X_Inicio + 3,
            Y_Fin,
        )
        Pdf.set_draw_color(0, 0, 0)

    elif Estilo == 3:
        # Tarjeta: recuadro.
        Y_Inicio = Pdf.get_y()
        Pdf.set_x(Pdf.l_margin + 4)
        Pdf.multi_cell(
            w=Pdf.w - Pdf.l_margin
            - Pdf.r_margin - 8,
            h=6,
            text=Texto,
            align=Alineacion_H,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        Y_Fin = Pdf.get_y() + 2
        Pdf.set_draw_color(200, 200, 200)
        Pdf.rect(
            Pdf.l_margin,
            Y_Inicio - 2,
            Pdf.w - Pdf.l_margin - Pdf.r_margin,
            Y_Fin - Y_Inicio + 4,
        )
        Pdf.set_draw_color(0, 0, 0)
        Pdf.ln(4)
        _Aplicar_Fuente(
            Pdf, S_Config, Fuente_Default
        )
        _Aplicar_Color(Pdf, S_Config["Color"])
        Pdf.multi_cell(
            w=0,
            h=5,
            text=Sub_Line,
            align=Alineacion_S,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    elif Estilo == 4:
        # Minimalista: centrado, sin separador.
        Pdf.multi_cell(
            w=0,
            h=6,
            text=Texto,
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        Pdf.ln(2)
        _Aplicar_Fuente(
            Pdf, S_Config, Fuente_Default
        )
        _Aplicar_Color(Pdf, S_Config["Color"])
        Pdf.multi_cell(
            w=0,
            h=5,
            text=Sub_Line,
            align="C",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    elif Estilo == 5:
        # Numerado.
        Numero = Pdf.page_no()
        Pdf.multi_cell(
            w=0,
            h=6,
            text=f"{Numero}.  {Texto}",
            align=Alineacion_H,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        _Aplicar_Fuente(
            Pdf, S_Config, Fuente_Default
        )
        _Aplicar_Color(Pdf, S_Config["Color"])
        Pdf.multi_cell(
            w=0,
            h=5,
            text=Sub_Line,
            align="R",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    else:
        # Estilo 6 (Destacado) y fallback.
        Pdf.set_fill_color(245, 245, 220)
        Pdf.multi_cell(
            w=0,
            h=6,
            text=Texto,
            align=Alineacion_H,
            fill=True,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        Pdf.ln(2)
        _Aplicar_Fuente(
            Pdf, S_Config, Fuente_Default
        )
        _Aplicar_Color(Pdf, S_Config["Color"])
        Pdf.multi_cell(
            w=0,
            h=5,
            text=Sub_Line,
            align=Alineacion_S,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    Pdf.ln(8)


def _Aplicar_Fuente(
    Pdf: FPDF,
    Config: dict,
    Fuente_Default: str,
):

    """
    Aplica fuente, tamaño y formato al PDF.

    """

    Formato = Config.get("Formato", "normal")
    Estilo_Fuente = ""
    if "negrita" in Formato:
        Estilo_Fuente += "B"
    if "cursiva" in Formato:
        Estilo_Fuente += "I"

    try:
        Pdf.set_font(
            Config.get("Fuente", Fuente_Default),
            Estilo_Fuente,
            Config.get("Tamano", 12),
        )
    except RuntimeError:
        Pdf.set_font(
            Fuente_Default,
            Estilo_Fuente,
            Config.get("Tamano", 12),
        )


def _Aplicar_Color(
    Pdf: FPDF,
    Color_Hex: str,
):

    """
    Aplica color de texto desde hex (#RRGGBB).

    """

    Color_Hex = Color_Hex.lstrip("#")
    R = int(Color_Hex[0:2], 16)
    G = int(Color_Hex[2:4], 16)
    B = int(Color_Hex[4:6], 16)
    Pdf.set_text_color(R, G, B)
