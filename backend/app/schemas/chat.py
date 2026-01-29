from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    lat: Optional[float] = None
    lng: Optional[float] = None


class ChatResponse(BaseModel):
    answer: str
    used_context: bool = True