from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unidade import Unidade
from app.services.roteamento import calcular_viabilidade

router = APIRouter(prefix="/atendimento", tags=["Atendimento"])


class RecomendarUnidadesPayload(BaseModel):
    lat: float
    lng: float


@router.post("/recomendar-unidades")
def recomendar_unidades(
    payload: RecomendarUnidadesPayload,
    db: Session = Depends(get_db),
):
    user_lat = float(payload.lat)
    user_lng = float(payload.lng)

    unidades = db.query(Unidade).all()

    recomendadas = []
    for u in unidades:
        # CHAMADA POSICIONAL (sem kwargs) pra não dar mismatch de nomes
        score, distancia_km, espera_ratio = calcular_viabilidade(
            user_lat,
            user_lng,
            float(u.lat),
            float(u.lng),
            int(u.pacientes_fila),
            int(u.medicos_ativos),
        )

        recomendadas.append(
            {
                "id": u.id,
                "nome": u.nome,
                "endereco": u.endereco,
                "tipo": u.tipo,
                "lat": float(u.lat),
                "lng": float(u.lng),
                "medicos_ativos": int(u.medicos_ativos),
                "pacientes_fila": int(u.pacientes_fila),
                "distancia_km": round(float(distancia_km), 2),
                "score": round(float(score), 2),
                "espera_ratio": round(float(espera_ratio), 2),
            }
        )

    recomendadas.sort(key=lambda x: x["score"])
    return {"items": recomendadas}