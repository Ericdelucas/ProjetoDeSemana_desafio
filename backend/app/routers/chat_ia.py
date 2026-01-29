from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services.ai.groq_client import groq_chat

router = APIRouter(prefix="/chat", tags=["Chat IA"])


class ChatPayload(BaseModel):
    prompt: str


@router.post("")
def chat(payload: ChatPayload):
    prompt = payload.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt vazio")

    system = (
        "Você é o Assistente do SmartSaúde SUS. "
        "Ajude o usuário a navegar no site, explicar funcionalidades e orientar o uso. "
        "Se a pergunta for médica, responda de forma educativa e segura, sem diagnóstico definitivo. "
        "Sempre que possível, recomende procurar um profissional de saúde."
    )

    # Fallback: nunca deixa o front “sem resposta”
    try:
        if settings.ai_provider.lower() == "groq":
            answer = groq_chat(prompt=prompt, system=system)
            return {"answer": answer, "provider": "groq"}
        return {
            "answer": "Chat em modo básico (sem IA). Configure AI_PROVIDER=groq e AI_KEY no backend/.env.",
            "provider": settings.ai_provider,
        }
    except Exception as e:
        return {
            "answer": "Estou com instabilidade no assistente agora. Tente novamente em instantes ou use as abas Unidades/Triagem.",
            "provider": "fallback",
            "error": str(e),
        }