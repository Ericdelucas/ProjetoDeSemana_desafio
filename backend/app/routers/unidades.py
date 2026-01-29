from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unidade import Unidade

router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.get("")
def listar_unidades(db: Session = Depends(get_db)):
    unidades = db.query(Unidade).all()
    return {
        "items": [
            {
                "id": u.id,
                "nome": u.nome,
                "endereco": u.endereco,
                "tipo": u.tipo,
                "lat": float(u.lat),
                "lng": float(u.lng),
                "medicos_ativos": int(u.medicos_ativos),
                "pacientes_fila": int(u.pacientes_fila),
            }
            for u in unidades
        ]
    }