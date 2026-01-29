from sqlalchemy import String, Integer, Float, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

UNIDADE_TIPO = ("UPA", "UBS", "Hosp")


class Unidade(Base):
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    nome: Mapped[str] = mapped_column(String(180), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)

    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)

    medicos_ativos: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    pacientes_fila: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    tipo: Mapped[str] = mapped_column(Enum(*UNIDADE_TIPO), nullable=False)

    estoque_itens = relationship(
        "Estoque",
        back_populates="unidade",
        cascade="all, delete-orphan",
    )


Index("idx_unidades_lat_lng", Unidade.lat, Unidade.lng)