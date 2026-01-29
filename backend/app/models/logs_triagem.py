from sqlalchemy import Column, DateTime, Enum, Integer, Text, func

from app.database import Base


class LogTriagem(Base):
    __tablename__ = "logs_triagem"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())

    risco_cor = Column(
        Enum("Vermelho", "Amarelo", "Verde", name="risco_cor_enum"),
        nullable=False,
    )

    sintomas_resumo = Column(Text, nullable=True)