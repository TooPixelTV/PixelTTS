from pydantic import BaseModel

class TTSRequest(BaseModel):
    voice: str
    text: str