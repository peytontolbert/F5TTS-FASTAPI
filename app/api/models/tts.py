from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    voice_profile: str = Field(..., min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, this is a test message.",
                "voice_profile": "Bane"
            }
        } 