import math
from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class UnitScore:
    unidade_id: int
    nome: str
    tipo: str
    endereco: str
    distancia_km: float
    pacientes_fila: int
    medicos_ativos: int
    score: float
    tempo_espera_min: int
    badge: str  # Verde/Amarelo/Vermelho


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def calcular_viabilidade(unidades: Iterable, user_lat: float, user_lng: float) -> List[UnitScore]:
    """
    Fórmula (v3.0):
      Score = (Distância * 1.2) + (Pacientes/Medicos * 20)
    Retorna ordenado do menor score (melhor) para o maior (pior).
    """
    results: List[UnitScore] = []

    for u in unidades:
        medicos = max(int(getattr(u, "medicos_ativos", 0) or 0), 1)
        pacientes = max(int(getattr(u, "pacientes_fila", 0) or 0), 0)

        dist = _haversine_km(user_lat, user_lng, float(u.lat), float(u.lng))
        score = (dist * 1.2) + ((pacientes / medicos) * 20)

        # estimativa simples (MVP): 6 min por paciente por médico
        tempo = int(round((pacientes / medicos) * 6))

        if score < 35:
            badge = "Verde"
        elif score < 70:
            badge = "Amarelo"
        else:
            badge = "Vermelho"

        results.append(
            UnitScore(
                unidade_id=u.id,
                nome=u.nome,
                tipo=u.tipo,
                endereco=u.endereco,
                distancia_km=round(dist, 2),
                pacientes_fila=pacientes,
                medicos_ativos=medicos,
                score=round(score, 2),
                tempo_espera_min=tempo,
                badge=badge,
            )
        )

    results.sort(key=lambda x: x.score)
    return results