"""
Modelos de configuración: exportación,
reglas de marcas y Notion.

"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
    JSONB,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from Backend.App.Core.Base_De_Datos import Base


class Config_Exportacion(Base):

    """
    Preferencias de estilo de exportación
    del usuario: fuente, color, tamaño,
    alineación para Highlight y Sub_Line.

    """

    __tablename__ = "config_exportacion"

    Id_Config_Exportacion: Mapped[
        uuid.UUID
    ] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Usuario: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey("usuarios.Id_Usuario"),
            unique=True,
            nullable=False,
        )
    )
    Estilo_Block: Mapped[int] = mapped_column(
        Integer, default=1,
    )
    Sub_Line_Campos: Mapped[list] = (
        mapped_column(
            JSONB,
            default=lambda: ["autor", "libro"],
        )
    )

    # Estilo del Highlight.
    Highlight_Formato: Mapped[str] = (
        mapped_column(
            String(20), default="normal"
        )
    )
    Highlight_Fuente: Mapped[str] = (
        mapped_column(
            String(100), default="Arial"
        )
    )
    Highlight_Color: Mapped[str] = (
        mapped_column(
            String(7), default="#000000"
        )
    )
    Highlight_Tamano: Mapped[int] = (
        mapped_column(Integer, default=12)
    )
    Highlight_Alineacion: Mapped[str] = (
        mapped_column(
            String(15), default="izquierda"
        )
    )

    # Estilo de la Sub_Line.
    Sub_Line_Formato: Mapped[str] = (
        mapped_column(
            String(20), default="cursiva"
        )
    )
    Sub_Line_Fuente: Mapped[str] = (
        mapped_column(
            String(100), default="Arial"
        )
    )
    Sub_Line_Color: Mapped[str] = (
        mapped_column(
            String(7), default="#666666"
        )
    )
    Sub_Line_Tamano: Mapped[int] = (
        mapped_column(Integer, default=10)
    )
    Sub_Line_Alineacion: Mapped[str] = (
        mapped_column(
            String(15), default="izquierda"
        )
    )


class Regla_Marca(Base):

    """
    Regla de mapeo entre una marca de formato
    en DOCX y un tipo semántico. Puede ser
    predefinida o personalizada por el usuario.

    """

    __tablename__ = "reglas_marcas"
    __table_args__ = (
        UniqueConstraint(
            "Id_Usuario",
            "Marca",
            name="uq_usuario_marca",
        ),
    )

    Id_Regla: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Usuario: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey("usuarios.Id_Usuario"),
            nullable=False,
        )
    )
    Marca: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )
    Tipo_Semantico: Mapped[str] = mapped_column(
        String(20), nullable=False,
    )
    Es_Predefinida: Mapped[bool] = (
        mapped_column(Boolean, default=False)
    )
    Prioridad: Mapped[int] = mapped_column(
        Integer, default=0,
    )


class Config_Notion(Base):

    """
    Configuración de Notion por defecto
    del usuario: base de datos, matcheo
    y formato de N_Block.

    """

    __tablename__ = "config_notion"

    Id_Config_Notion: Mapped[
        uuid.UUID
    ] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Usuario: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey("usuarios.Id_Usuario"),
            unique=True,
            nullable=False,
        )
    )
    Id_N_Database: Mapped[
        str | None
    ] = mapped_column(
        String(255), nullable=True,
    )
    Titulo_N_Database: Mapped[
        str | None
    ] = mapped_column(
        String(500), nullable=True,
    )
    Campo_Matcheo_Clipping: Mapped[str] = (
        mapped_column(
            String(50), default="nombre"
        )
    )
    Propiedad_Matcheo_N_Page: Mapped[str] = (
        mapped_column(
            String(100), default="title"
        )
    )
    N_Block_Tipo: Mapped[str] = mapped_column(
        String(20), default="paragraph",
    )
    N_Block_Formato: Mapped[str] = (
        mapped_column(
            String(20), default="normal"
        )
    )
    N_Block_Color: Mapped[str] = mapped_column(
        String(30), default="default",
    )
    N_Block_Color_Fondo: Mapped[str] = (
        mapped_column(
            String(30), default="default"
        )
    )
    N_Block_Alineacion: Mapped[str] = (
        mapped_column(
            String(15), default="izquierda"
        )
    )
    N_Block_Emoji: Mapped[
        str | None
    ] = mapped_column(
        String(10), nullable=True,
    )
    Fecha_Actualizacion: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(
                timezone.utc
            ),
            onupdate=lambda: datetime.now(
                timezone.utc
            ),
        )
    )


class N_Match(Base):

    """
    Conexión guardada entre un Clipping y una
    página de Notion (N_Page).

    """

    __tablename__ = "n_matches"
    __table_args__ = (
        UniqueConstraint(
            "Id_Clipping",
            "N_Page_Id",
            name="uq_clipping_npage",
        ),
    )

    Id_N_Match: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    Id_Usuario: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey("usuarios.Id_Usuario"),
            nullable=False,
        )
    )
    Id_Clipping: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "clippings.Id_Clipping"
            ),
            nullable=False,
        )
    )
    N_Page_Id: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    N_Page_Titulo: Mapped[
        str | None
    ] = mapped_column(
        String(500), nullable=True,
    )
    Posicion_Paste: Mapped[str] = (
        mapped_column(
            String(20), default="final"
        )
    )
    N_Block_Especifico_Id: Mapped[
        str | None
    ] = mapped_column(
        String(255), nullable=True,
    )
    Guardado_Permanente: Mapped[bool] = (
        mapped_column(Boolean, default=False)
    )
    Fecha_Creacion: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(
                timezone.utc
            ),
        )
    )
