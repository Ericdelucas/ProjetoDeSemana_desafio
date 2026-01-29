from __future__ import annotations

from typing import Any

from groq import Groq

from app.config import settings


def groq_chat(prompt: str, system: str = "", history: list[dict[str, str]] | None = None) -> str:
    """
    Sends a chat request to Groq and returns the assistant text.
    history: [{"role":"user"|"assistant","content":"..."}]
    """
    if not settings.ai_key:
        raise RuntimeError("AI_KEY não configurada no .env")

    client = Groq(api_key=settings.ai_key)

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": prompt})

    resp: Any = client.chat.completions.create(
        model=settings.ai_model,
        messages=messages,
        temperature=0.2,
        max_tokens=350,
    )

    return (resp.choices[0].message.content or "").strip()