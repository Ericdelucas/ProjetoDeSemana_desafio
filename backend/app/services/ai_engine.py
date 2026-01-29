from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.config import settings
from app.models.unidade import Unidade
from app.models.estoque import Estoque

import google.generativeai as genai


SYSTEM_PROMPT = """
Você é um assistente do SUS para orientação de fluxo e informação logística do sistema.
Regras obrigatórias:
1) Você NÃO pode fornecer diagnóstico médico, prescrever medicamentos ou orientar tratamento.
2) Você pode: orientar fluxo, priorização (quando já calculado), disponibilidade de unidades, filas e estoque.
3) Sempre baseie respostas em dados do contexto fornecido (banco). Se não houver dados, diga claramente.
4) Seja objetivo, humano e use listas quando ajudar.
""".strip()


def _build_context(db: Session, message: str) -> Dict[str, Any]:
    """
    MVP de RAG: busca unidades e itens de estoque relacionados ao texto do usuário.
    """
    ctx: Dict[str, Any] = {"unidades": [], "estoque": []}

    unidades = db.execute(select(Unidade).limit(10)).scalars().all()
    ctx["unidades"] = [
        {
            "id": u.id,
            "nome": u.nome,
            "tipo": u.tipo,
            "endereco": u.endereco,
            "lat": u.lat,
            "lng": u.lng,
            "medicos_ativos": u.medicos_ativos,
            "pacientes_fila": u.pacientes_fila,
        }
        for u in unidades
    ]

    # Heurística simples: procura token grande no nome do medicamento (LIKE)
    tokens = [t.strip().lower() for t in message.split() if len(t.strip()) >= 4]
    if tokens:
        like_token = f"%{tokens[0]}%"
        itens = (
            db.execute(select(Estoque).where(Estoque.medicamento_nome.ilike(like_token)).limit(15))
            .scalars()
            .all()
        )
    else:
        itens = db.execute(select(Estoque).limit(15)).scalars().all()

    ctx["estoque"] = [
        {
            "unidade_id": e.unidade_id,
            "medicamento_nome": e.medicamento_nome,
            "categoria": e.categoria,
            "qtd_status": e.qtd_status,
        }
        for e in itens
    ]

    return ctx


def answer_with_rag(db: Session, message: str, lat: Optional[float] = None, lng: Optional[float] = None) -> str:
    """
    Obrigatório:
    1) Consulta MySQL
    2) Injeta contexto na IA
    3) Retorna resposta baseada em dados reais
    """
    ctx = _build_context(db, message)

    if not settings.ai_key:
        return (
            "A chave de IA não está configurada (AI_KEY). "
            "Consigo consultar banco e listar dados, mas não chamar a IA ainda."
        )

    genai.configure(api_key=settings.ai_key)
    model = genai.GenerativeModel(settings.ai_model)

    prompt = f"""
{SYSTEM_PROMPT}

Contexto do sistema (dados reais do MySQL):
{ctx}

Pergunta do usuário:
{message}

Responda seguindo as regras.
""".strip()

    resp = model.generate_content(prompt)
    return getattr(resp, "text", None) or "Não consegui gerar uma resposta agora."
