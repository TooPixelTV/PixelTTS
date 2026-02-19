"""Schémas Pydantic pour l'API."""
from pydantic import BaseModel


class TTSRequest(BaseModel):
    """Corps du POST /tts : nom de la voix et texte à synthétiser."""
    voice: str
    text: str