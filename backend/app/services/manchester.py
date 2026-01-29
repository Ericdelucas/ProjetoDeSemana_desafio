from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ManchesterResult:
    risco_cor: str
    justificativa: str


EMERGENCIA_TERMS = {
    "dor precordial",
    "falta de ar",
    "dispneia",
    "desmaio",
    "convulsão",
    "inconsciência",
}

URGENTE_TERMS = {
    "dor intensa",
    "febre muito alta",
    "sangramento",
    "vômitos persistentes",
}


def classificar_manchester(sintomas: List[str], intensidade: int) -> ManchesterResult:
    normalized = {s.strip().lower() for s in sintomas if s.strip()}

    if normalized & EMERGENCIA_TERMS:
        return ManchesterResult(
            risco_cor="Vermelho",
            justificativa="Sinais compatíveis com emergência (Manchester). Procure atendimento imediato.",
        )

    if (normalized & URGENTE_TERMS) or intensidade >= 8:
        return ManchesterResult(
            risco_cor="Amarelo",
            justificativa="Sinais compatíveis com urgência (Manchester). Procure atendimento com prioridade.",
        )

    return ManchesterResult(
        risco_cor="Verde",
        justificativa="Sinais compatíveis com baixa urgência (Manchester). Monitorar e buscar assistência se piorar.",
    )