"""
Endpoints CRUD de highlights: listar, editar,
eliminar, combinar y dividir.

"""

import uuid
from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from Backend.App.Core.Base_De_Datos import (
    Obtener_Sesion,
)
from Backend.App.Core.Dependencias import (
    Obtener_Usuario_Actual,
)
from Backend.App.Modelos.Usuario import Usuario
from Backend.App.Modelos.Highlight import (
    Highlight,
)
from Backend.App.Esquemas.Esquema_Highlight import (
    Peticion_Editar_Highlight,
    Peticion_Combinar,
    Peticion_Dividir,
    Peticion_Eliminar_Lote,
)

Router_Highlights = APIRouter()


@Router_Highlights.get("/")
async def Listar_Highlights(
    Pagina: int = 1,
    Limite: int = 20,
    Orden: str | None = None,
    Autor: str | None = None,
    Libro: str | None = None,
    Id_Archivo: str | None = None,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Lista highlights del usuario con filtros.
    Paginado y ordenable.

    """

    Offset = (Pagina - 1) * Limite

    # Consulta base (solo no eliminados).
    Condiciones = [
        Highlight.Id_Usuario
        == Usuario_Actual.Id_Usuario,
        Highlight.Eliminado_En.is_(None),
    ]

    if Autor:
        Condiciones.append(
            Highlight.Autor.ilike(f"%{Autor}%")
        )
    if Libro:
        Condiciones.append(
            Highlight.Libro.ilike(f"%{Libro}%")
        )
    if Id_Archivo:
        Condiciones.append(
            Highlight.Id_Archivo
            == uuid.UUID(Id_Archivo)
        )

    # Total.
    Consulta_Total = select(
        func.count(Highlight.Id_Highlight)
    ).where(*Condiciones)
    Total = (
        await Sesion.execute(Consulta_Total)
    ).scalar() or 0

    # Orden.
    Columna_Orden = desc(
        Highlight.Orden_Original
    )
    if Orden == "autor":
        Columna_Orden = Highlight.Autor
    elif Orden == "libro":
        Columna_Orden = Highlight.Libro
    elif Orden == "fecha":
        Columna_Orden = desc(
            Highlight.Fecha_Subrayado
        )

    # Página.
    Consulta = (
        select(Highlight)
        .where(*Condiciones)
        .order_by(Columna_Orden)
        .offset(Offset)
        .limit(Limite)
    )
    Resultado = await Sesion.execute(Consulta)
    Highlights = Resultado.scalars().all()

    return {
        "Highlights": [
            {
                "Id_Highlight": str(
                    H.Id_Highlight
                ),
                "Texto": H.Texto,
                "Autor": H.Autor,
                "Libro": H.Libro,
                "Pagina": H.Pagina,
                "Fecha_Subrayado": (
                    H.Fecha_Subrayado
                    .isoformat()
                    if H.Fecha_Subrayado
                    else None
                ),
                "Tipo_Semantico": (
                    H.Tipo_Semantico
                ),
                "Orden_Original": (
                    H.Orden_Original
                ),
            }
            for H in Highlights
        ],
        "Total": Total,
        "Pagina": Pagina,
    }


@Router_Highlights.get("/{Id_Highlight}")
async def Obtener_Highlight(
    Id_Highlight: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Retorna un highlight específico.

    """

    H = await _Obtener_Highlight_O_404(
        Sesion,
        Id_Highlight,
        Usuario_Actual.Id_Usuario,
    )

    return {
        "Id_Highlight": str(H.Id_Highlight),
        "Texto": H.Texto,
        "Autor": H.Autor,
        "Libro": H.Libro,
        "Pagina": H.Pagina,
        "Fecha_Subrayado": (
            H.Fecha_Subrayado.isoformat()
            if H.Fecha_Subrayado
            else None
        ),
        "Tipo_Semantico": H.Tipo_Semantico,
        "Orden_Original": H.Orden_Original,
    }


@Router_Highlights.patch("/{Id_Highlight}")
async def Editar_Highlight(
    Id_Highlight: str,
    Datos: Peticion_Editar_Highlight,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Edita el texto o tipo semántico.

    """

    H = await _Obtener_Highlight_O_404(
        Sesion,
        Id_Highlight,
        Usuario_Actual.Id_Usuario,
    )

    if Datos.Texto is not None:
        H.Texto = Datos.Texto
    if Datos.Tipo_Semantico is not None:
        H.Tipo_Semantico = (
            Datos.Tipo_Semantico
        )

    await Sesion.commit()

    return {"Mensaje": "Highlight actualizado"}


@Router_Highlights.delete(
    "/{Id_Highlight}"
)
async def Eliminar_Highlight(
    Id_Highlight: str,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Soft delete de un highlight.

    """

    H = await _Obtener_Highlight_O_404(
        Sesion,
        Id_Highlight,
        Usuario_Actual.Id_Usuario,
    )

    H.Eliminado_En = datetime.now(
        timezone.utc
    )
    await Sesion.commit()

    return {"Mensaje": "Highlight eliminado"}


@Router_Highlights.post("/combinar")
async def Combinar_Highlights(
    Datos: Peticion_Combinar,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Combina varios F_Blocks en un C_Block.
    Requiere mismo Author-Book.

    """

    if len(Datos.Ids_Highlights) < 2:
        raise HTTPException(
            status_code=400,
            detail="Se necesitan al menos 2 "
            "highlights para combinar.",
        )

    # Obtener highlights.
    Ids = [
        uuid.UUID(Id)
        for Id in Datos.Ids_Highlights
    ]
    Consulta = select(Highlight).where(
        Highlight.Id_Highlight.in_(Ids),
        Highlight.Id_Usuario
        == Usuario_Actual.Id_Usuario,
        Highlight.Eliminado_En.is_(None),
    )
    Resultado = await Sesion.execute(Consulta)
    Highlights = list(
        Resultado.scalars().all()
    )

    if len(Highlights) != len(Ids):
        raise HTTPException(
            status_code=404,
            detail="Algunos highlights no "
            "fueron encontrados.",
        )

    # Verificar mismo Author-Book.
    Pares = set(
        (H.Autor, H.Libro)
        for H in Highlights
    )
    if len(Pares) > 1:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden combinar "
            "highlights del mismo Author-Book.",
        )

    # Combinar textos.
    Highlights.sort(
        key=lambda H: H.Orden_Original
    )
    Texto_Combinado = " ".join(
        H.Texto for H in Highlights
    )

    # Obtener fecha a mantener.
    H_Fecha = next(
        (
            H for H in Highlights
            if str(H.Id_Highlight)
            == Datos.Id_Fecha_A_Mantener
        ),
        Highlights[0],
    )

    # Crear nuevo highlight combinado.
    Nuevo = Highlight(
        Id_Usuario=Usuario_Actual.Id_Usuario,
        Id_Archivo=Highlights[0].Id_Archivo,
        Texto=Texto_Combinado,
        Autor=Highlights[0].Autor,
        Libro=Highlights[0].Libro,
        Pagina=H_Fecha.Pagina,
        Fecha_Subrayado=(
            H_Fecha.Fecha_Subrayado
        ),
        Tipo_Semantico=(
            Highlights[0].Tipo_Semantico
        ),
        Orden_Original=(
            Highlights[0].Orden_Original
        ),
    )
    Sesion.add(Nuevo)

    # Soft delete de los originales.
    Ahora = datetime.now(timezone.utc)
    for H in Highlights:
        H.Eliminado_En = Ahora

    await Sesion.commit()

    return {
        "Id_Highlight": str(
            Nuevo.Id_Highlight
        ),
        "Texto": Nuevo.Texto,
        "Mensaje": "Highlights combinados",
    }


@Router_Highlights.post(
    "/dividir/{Id_Highlight}"
)
async def Dividir_Highlight(
    Id_Highlight: str,
    Datos: Peticion_Dividir,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Divide un F_Block en varios C_Blocks.

    """

    H = await _Obtener_Highlight_O_404(
        Sesion,
        Id_Highlight,
        Usuario_Actual.Id_Usuario,
    )

    Texto = H.Texto
    Puntos = sorted(Datos.Puntos_De_Corte)

    # Validar puntos de corte.
    for Punto in Puntos:
        if Punto < 0 or Punto >= len(Texto):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Punto de corte {Punto} "
                    "fuera de rango."
                ),
            )

    # Crear segmentos.
    Segmentos = []
    Inicio = 0
    for Punto in Puntos:
        Segmentos.append(
            Texto[Inicio:Punto].strip()
        )
        Inicio = Punto
    Segmentos.append(Texto[Inicio:].strip())

    # Filtrar segmentos vacíos.
    Segmentos = [S for S in Segmentos if S]

    if len(Segmentos) < 2:
        raise HTTPException(
            status_code=400,
            detail="La división no produce "
            "segmentos válidos.",
        )

    # Crear nuevos highlights.
    Nuevos = []
    for Indice, Segmento in enumerate(
        Segmentos
    ):
        Nuevo = Highlight(
            Id_Usuario=(
                Usuario_Actual.Id_Usuario
            ),
            Id_Archivo=H.Id_Archivo,
            Texto=Segmento,
            Autor=H.Autor,
            Libro=H.Libro,
            Pagina=H.Pagina,
            Fecha_Subrayado=H.Fecha_Subrayado,
            Tipo_Semantico=H.Tipo_Semantico,
            Orden_Original=(
                H.Orden_Original * 100
                + Indice
            ),
        )
        Sesion.add(Nuevo)
        Nuevos.append(Nuevo)

    # Soft delete del original.
    H.Eliminado_En = datetime.now(timezone.utc)
    await Sesion.commit()

    return {
        "Highlights_Resultantes": [
            {
                "Id_Highlight": str(
                    N.Id_Highlight
                ),
                "Texto": N.Texto,
            }
            for N in Nuevos
        ],
    }


@Router_Highlights.delete("/lote")
async def Eliminar_Lote(
    Datos: Peticion_Eliminar_Lote,
    Sesion: AsyncSession = Depends(
        Obtener_Sesion
    ),
    Usuario_Actual: Usuario = Depends(
        Obtener_Usuario_Actual
    ),
):

    """
    Soft delete de varios highlights.

    """

    Ids = [
        uuid.UUID(Id)
        for Id in Datos.Ids_Highlights
    ]
    Consulta = select(Highlight).where(
        Highlight.Id_Highlight.in_(Ids),
        Highlight.Id_Usuario
        == Usuario_Actual.Id_Usuario,
        Highlight.Eliminado_En.is_(None),
    )
    Resultado = await Sesion.execute(Consulta)
    Highlights = list(
        Resultado.scalars().all()
    )

    Ahora = datetime.now(timezone.utc)
    for H in Highlights:
        H.Eliminado_En = Ahora

    await Sesion.commit()

    return {
        "Cantidad_Eliminada": len(Highlights),
    }


async def _Obtener_Highlight_O_404(
    Sesion: AsyncSession,
    Id_Highlight: str,
    Id_Usuario: uuid.UUID,
) -> Highlight:

    """
    Busca un highlight por ID y usuario.
    Lanza 404 si no existe o está eliminado.

    """

    Consulta = select(Highlight).where(
        Highlight.Id_Highlight
        == uuid.UUID(Id_Highlight),
        Highlight.Id_Usuario == Id_Usuario,
        Highlight.Eliminado_En.is_(None),
    )
    Resultado = await Sesion.execute(Consulta)
    H = Resultado.scalar_one_or_none()

    if not H:
        raise HTTPException(
            status_code=404,
            detail="Highlight no encontrado",
        )

    return H
