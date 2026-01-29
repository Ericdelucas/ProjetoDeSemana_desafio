from sqlalchemy import String, Integer, ForeignKey, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

QTD_STATUS = ("Disponível", "Crítico", "Indisponível")


class Estoque(Base):
    __tablename__ = "estoque"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    unidade_id: Mapped[int] = mapped_column(
        ForeignKey("unidades.id"),
        nullable=False,
        index=True,
    )

    medicamento_nome: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    categoria: Mapped[str] = mapped_column(String(120), nullable=False, index=True)

    qtd_status: Mapped[str] = mapped_column(
        Enum(*QTD_STATUS),
        nullable=False,
        default="Disponível",
    )

    unidade = relationship("Unidade", back_populates="estoque_itens")


Index("idx_estoque_unidade_categoria", Estoque.unidade_id, Estoque.categoria)