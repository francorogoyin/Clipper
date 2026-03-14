"""
Modelo de usuario y conexiones OAuth.

"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
    UniqueConstraint,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
    JSONB,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from Backend.App.Core.Base_De_Datos import Base


class Usuario(Base):

    """
    Tabla principal de usuarios.
    Almacena perfil, preferencias y suscripción.

    """

    __tablename__ = "usuarios"

    Id_Usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    Nickname: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    Avatar_Url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    Idioma: Mapped[str] = mapped_column(
        String(10),
        default="es",
    )
    Tema_Visual: Mapped[str] = mapped_column(
        String(10),
        default="claro",
    )
    Tipo_Suscripcion: Mapped[str] = mapped_column(
        String(10),
        default="free",
    )
    Formato_Preferido: Mapped[str] = mapped_column(
        String(20),
        default="pdf",
    )
    Estilo_Block: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )
    Confirmaciones_Silenciadas: Mapped[dict] = (
        mapped_column(
            JSONB,
            default=dict,
        )
    )
    Config_P_Display_Defecto: Mapped[bool] = (
        mapped_column(
            Boolean,
            default=False,
        )
    )
    Config_P_Processing_Defecto: Mapped[bool] = (
        mapped_column(
            Boolean,
            default=False,
        )
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
    Conexiones: Mapped[
        list["Conexion_Oauth"]
    ] = relationship(
        back_populates="Usuario_Rel",
        cascade="all, delete-orphan",
    )


class Conexion_Oauth(Base):

    """
    Tokens OAuth de Google y Notion por usuario.
    Los tokens se almacenan encriptados con Fernet.

    """

    __tablename__ = "conexiones_oauth"
    __table_args__ = (
        UniqueConstraint(
            "Id_Usuario",
            "Proveedor",
            name="uq_usuario_proveedor",
        ),
    )

    Id_Conexion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    Id_Usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.Id_Usuario"),
        nullable=False,
    )
    Proveedor: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    Access_Token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    Refresh_Token: Mapped[str | None] = (
        mapped_column(
            Text,
            nullable=True,
        )
    )
    Token_Expira_En: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    Id_Externo: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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
    Usuario_Rel: Mapped["Usuario"] = relationship(
        back_populates="Conexiones",
    )
