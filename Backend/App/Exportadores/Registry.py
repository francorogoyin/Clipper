"""
Registry de exportadores. Mapea formato
string a la clase exportadora correspondiente.

"""

from Backend.App.Exportadores.Exportador_Base import (
    Exportador_Base,
)
from Backend.App.Exportadores.Exportador_Pdf import (
    Exportador_Pdf,
)
from Backend.App.Exportadores.Exportador_Docx import (
    Exportador_Docx,
)
from Backend.App.Exportadores.Exportador_Doc import (
    Exportador_Doc,
)
from Backend.App.Exportadores.Exportador_Odt import (
    Exportador_Odt,
)
from Backend.App.Exportadores.Exportador_Csv import (
    Exportador_Csv,
)
from Backend.App.Exportadores.Exportador_Xlsx import (
    Exportador_Xlsx,
)
from Backend.App.Exportadores.Exportador_Xls import (
    Exportador_Xls,
)
from Backend.App.Exportadores.Exportador_Txt import (
    Exportador_Txt,
)
from Backend.App.Exportadores.Exportador_Obsidian import (
    Exportador_Obsidian,
)


EXPORTADORES: dict[str, type[Exportador_Base]] = {
    "pdf": Exportador_Pdf,
    "docx": Exportador_Docx,
    "doc": Exportador_Doc,
    "odt": Exportador_Odt,
    "csv": Exportador_Csv,
    "xlsx": Exportador_Xlsx,
    "xls": Exportador_Xls,
    "txt": Exportador_Txt,
    "obsidian": Exportador_Obsidian,
}


def Obtener_Exportador(
    Formato: str,
) -> Exportador_Base:

    """
    Retorna una instancia del exportador
    para el formato solicitado.
    Lanza KeyError si el formato no existe.

    """

    Clase = EXPORTADORES.get(Formato.lower())
    if not Clase:
        raise KeyError(
            f"Formato '{Formato}' no soportado."
            f" Disponibles: "
            f"{', '.join(EXPORTADORES.keys())}"
        )

    return Clase()
