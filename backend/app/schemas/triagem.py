from pydantic import BaseModel, Field
from typing import List, Optional


class TriagemInput(BaseModel):
    sintomas: List[str] = Field(default_factory=list)
    intensidade: int = Field(ge=1, le=10, default=5)
    historico: Optional[str] = None

    lat: float
    lng: float


class TriagemOutput(BaseModel):
    risco_cor: str
    justificativa: str
