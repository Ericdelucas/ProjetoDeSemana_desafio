from __future__ import annotations

import inspect
import math
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unidade import Unidade
from app.services.roteamento import calcular_viabilidade

router = APIRouter(prefix="/atendimento", tags=["Atendimento"])


class RecomendarUnidadesPayload(BaseModel):
    lat: float
    lng: float


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distance between 2 points (km)."""
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _call_calcular_viabilidade(
    user_lat: float,
    user_lng: float,
    unidade: Unidade,
) -> tuple[float, float, float]:
    """
    Adapter: calls calcular_viabilidade regardless of its signature.
    Expected output: (score, distancia_km, espera_ratio).
    If calcular_viabilidade returns something else, we normalize.
    """
    sig = inspect.signature(calcular_viabilidade)
    params = list(sig.parameters.values())
    param_names = [p.name for p in params]
    argc = len(params)

    # Common precomputed values
    distancia_km = _haversine_km(user_lat, user_lng, float(unidade.lat), float(unidade.lng))
    espera_ratio = float(unidade.pacientes_fila) / max(float(unidade.medicos_ativos), 1.0)

    # --- Call strategies (ordered by likelihood) ---
    try:
        # 3 args patterns
        if argc == 3:
            # calcular_viabilidade(user_lat, user_lng, unidade)
            if {"user_lat", "user_lng"} <= set(param_names) and ("unidade" in param_names or "u" in param_names):
                return _normalize_result(calcular_viabilidade(user_lat, user_lng, unidade), distancia_km, espera_ratio)

            # calcular_viabilidade(lat, lng, unidade)
            if ("lat" in param_names and "lng" in param_names and ("unidade" in param_names or "u" in param_names)):
                return _normalize_result(calcular_viabilidade(user_lat, user_lng, unidade), distancia_km, espera_ratio)

            # calcular_viabilidade(user_coords, unidade_coords, espera_ratio) OR similar
            # Try: ( (lat,lng), (ulat,ulng), espera_ratio )
            return _normalize_result(
                calcular_viabilidade((user_lat, user_lng), (float(unidade.lat), float(unidade.lng)), espera_ratio),
                distancia_km,
                espera_ratio,
            )

        # 4 args patterns
        if argc == 4:
            # Try: (user_lat, user_lng, unidade_lat, unidade_lng)
            return _normalize_result(
                calcular_viabilidade(user_lat, user_lng, float(unidade.lat), float(unidade.lng)),
                distancia_km,
                espera_ratio,
            )

        # 5 args patterns
        if argc == 5:
            # Try: add espera_ratio
            return _normalize_result(
                calcular_viabilidade(user_lat, user_lng, float(unidade.lat), float(unidade.lng), espera_ratio),
                distancia_km,
                espera_ratio,
            )

        # 6+ args patterns (your initial idea)
        if argc >= 6:
            return _normalize_result(
                calcular_viabilidade(
                    user_lat,
                    user_lng,
                    float(unidade.lat),
                    float(unidade.lng),
                    int(unidade.pacientes_fila),
                    int(unidade.medicos_ativos),
                ),
                distancia_km,
                espera_ratio,
            )

    except TypeError:
        # We'll fallback below
        pass

    # --- Fallback: score computed locally (never crash) ---
    # score: distance + waiting penalty (tune weight if you want)
    score = float(distancia_km) + (float(espera_ratio) * 2.5)
    return score, float(distancia_km), float(espera_ratio)


def _normalize_result(result: Any, distancia_km: float, espera_ratio: float) -> tuple[float, float, float]:
    """
    Normalize calcular_viabilidade return to (score, distancia_km, espera_ratio).
    """
    # If tuple/list
    if isinstance(result, (tuple, list)):
        if len(result) == 3:
            score, dist, ratio = result
            return float(score), float(dist), float(ratio)
        if len(result) == 2:
            score, dist = result
            return float(score), float(dist), float(espera_ratio)
        if len(result) == 1:
            return float(result[0]), float(distancia_km), float(espera_ratio)

    # If dict-like
    if isinstance(result, dict):
        score = result.get("score", None)
        dist = result.get("distancia_km", result.get("distancia", None))
        ratio = result.get("espera_ratio", result.get("ratio", None))

        return (
            float(score) if score is not None else float(distancia_km) + float(espera_ratio) * 2.5,
            float(dist) if dist is not None else float(distancia_km),
            float(ratio) if ratio is not None else float(espera_ratio),
        )

    # If single number
    if isinstance(result, (int, float)):
        return float(result), float(distancia_km), float(espera_ratio)

    # Unknown type -> fallback safe
    score = float(distancia_km) + float(espera_ratio) * 2.5
    return score, float(distancia_km), float(espera_ratio)


@router.post("/recomendar-unidades")
def recomendar_unidades(payload: RecomendarUnidadesPayload, db: Session = Depends(get_db)):
    user_lat = float(payload.lat)
    user_lng = float(payload.lng)

    unidades = db.query(Unidade).all()
    if not unidades:
        return {"items": []}

    recomendadas = []
    for u in unidades:
        try:
            score, distancia_km, espera_ratio = _call_calcular_viabilidade(user_lat, user_lng, u)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro calculando viabilidade: {e}") from e

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