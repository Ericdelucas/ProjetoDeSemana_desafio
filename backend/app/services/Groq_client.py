from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class GroqClient:
    """
    Minimal Groq chat client using OpenAI-compatible endpoint via HTTP.
    """

    def __init__(self) -> None:
        self.base_url = "https://api.groq.com/openai/v1"
        self.api_key = getattr(settings, "ai_key", "") or ""
        self.model = getattr(settings, "ai_model", "llama-3.1-8b-instant") or "llama-3.1-8b-instant"

    def is_configured(self) -> bool:
        return bool(self.api_key.strip())

    def chat(self, messages: list[dict[str, str]]) -> str:
        if not self.is_configured():
            return (
                "No momento o chat inteligente não está configurado (faltando AI_KEY). "
                "Eu consigo te orientar pelo site, mas para respostas inteligentes ative a chave Groq no .env."
            )

        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 400,
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()

            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            return (content or "").strip() or "Não consegui gerar uma resposta agora."
        except httpx.HTTPStatusError as e:
            # mostra erro claro sem vazar key
            return f"Falha ao chamar Groq (HTTP {e.response.status_code}). Verifique AI_MODEL e AI_KEY."
        except Exception:
            return "Falha ao chamar o chat agora. Tente novamente."