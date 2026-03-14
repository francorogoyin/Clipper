"""
Modelos de Highlight, Archivo_Subido,
Clipping y la tabla intermedia.

"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
    Text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from Backend.App.Core.Base_De_Datos import Base


class Archivo_Subido(Base):

    """
    Registro de cada archivo TXT o DOCX que
    el usuario sube a la plataforma.

    """

    __tablename__ = "archivos_subidos"

    Id_Archivo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.Id_Usuario"),
        nullable=False,
    )
    Nombre_Original: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    Tipo_Archivo: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    Tamano_Bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    Ruta_Almacenamiento: Mapped[str] = (
        mapped_column(
            String(500),
            nullable=False,
        )
    )
    Cantidad_Highlights: Mapped[int] = (
        mapped_column(
            Integer,
            default=0,
        )
    )
    Fecha_Subida: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(
                timezone.utc
            ),
        )
    )

    # Relaciones.
    Highlights: Mapped[
        list["Highlight"]
    ] = relationship(
        back_populates="Archivo_Rel",
        cascade="all, delete-orphan",
    )


class Highlight(Base):

    """
    Un resaltado individual extraído de un libro.
    Contiene el texto, metadata y tipo semántico.

    """

    __tablename__ = "highlights"

    Id_Highlight: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    Id_Usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.Id_Usuario"),
        nullable=False,
    )
    Id_Archivo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "archivos_subidos.Id_Archivo"
        ),
        nullable=False,
    )
    Texto: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    Autor: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )
    Libro: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    Pagina: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    Fecha_Subrayado: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    Tipo_Semantico: Mapped[str] = mapped_column(
        String(20),
        default="paragraph",
    )
    Orden_Original: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    Eliminado_En: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    Fecha_Creacion: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(
                timezone.utc
            ),
        )
    )

    # Relaciones.
    Archivo_Rel: Mapped[
        "Archivo_Subido"
    ] = relationship(
        back_populates="Highlights",
    )
    Clipping_Highlights: Mapped[
        list["Clipping_Highlight"]
    ] = relationship(
        back_populates="Highlight_Rel",
        cascade="all, delete-orphan",
    )


class Clipping(Base):

    """
    Agrupación de highlights con nombre
    personalizable por el usuario.

    """

    __tablename__ = "clippings"

    Id_Clipping: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    Id_Usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.Id_Usuario"),
        nullable=False,
    )
    Nombre: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )
    Eliminado_En: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    Fecha_Creacion: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(
                timezone.utc
            ),
        )
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

    # Relaciones.
    Clipping_Highlights: Mapped[
        list["Clipping_Highlight"]
    ] = relationship(
        back_populates="Clipping_Rel",
        cascade="all, delete-orphan",
    )
    Config_Processing: Mapped[
        "Config_H_Processing | None"
    ] = relationship(
        back_populates="Clipping_Rel",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Clipping_Highlight(Base):

    """
    Tabla intermedia N:M entre Clippings
    y Highlights. Almacena el orden dentro
    del clipping (F_Order).

    """

    __tablename__ = "clipping_highlights"
    __table_args__ = (
        UniqueConstraint(
            "Id_Clipping",
            "Id_Highlight",
            name="uq_clipping_highlight",
        ),
    )

    Id_Clipping_Highlight: Mapped[
        uuid.UUID
    ] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Clipping: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "clippings.Id_Clipping",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    Id_Highlight: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "highlights.Id_Highlight",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    Orden_En_Clipping: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    # Relaciones.
    Clipping_Rel: Mapped[
        "Clipping"
    ] = relationship(
        back_populates="Clipping_Highlights",
    )
    Highlight_Rel: Mapped[
        "Highlight"
    ] = relationship(
        back_populates="Clipping_Highlights",
    )


class Config_H_Processing(Base):

    """
    Configuración de procesamiento de texto
    guardada por clipping.

    """

    __tablename__ = "config_h_processing"

    Id_Config_Processing: Mapped[
        uuid.UUID
    ] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Clipping: Mapped[uuid.UUID] = (
        mapped_column(
            UUID(as_uuid=True),
            ForeignKey(
                "clippings.Id_Clipping"
            ),
            unique=True,
            nullable=False,
        )
    )
    Primera_Letra_Mayuscula: Mapped[bool] = (
        mapped_column(Boolean, default=True)
    )
    Borrar_Caracteres: Mapped[bool] = (
        mapped_column(Boolean, default=False)
    )
    Caracteres_A_Borrar: Mapped[str] = (
        mapped_column(
            String(100), default=""
        )
    )
    Primer_Caracter_Letra_Mayus: Mapped[
        bool
    ] = mapped_column(
        Boolean, default=True
    )
    Agregar_Signos_Faltantes: Mapped[
        bool
    ] = mapped_column(
        Boolean, default=True
    )

    # Relaciones.
    Clipping_Rel: Mapped[
        "Clipping"
    ] = relationship(
        back_populates="Config_Processing",
    )
