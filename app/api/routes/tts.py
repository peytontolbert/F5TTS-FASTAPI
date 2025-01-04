from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from app.core.security import validate_token
from app.api.models.tts import TTSRequest
from app.services.tts_service import F5TTSService
import logging
import os
from app.core.config import settings

router = APIRouter(prefix="/tts")
logger = logging.getLogger(__name__)
tts_service = None

@router.post("/synthesize")
async def synthesize_speech(
    request: TTSRequest,
    token: str = Depends(validate_token)
):
    """
    Synthesize speech from text using specified voice profile
    """
    try:
        global tts_service
        if tts_service is None:
            logger.info("Initializing TTS service")
            tts_service = F5TTSService(
                model_dir=settings.MODEL_DIR,
                voice_profile=request.voice_profile
            )
        
        logger.info(f"Synthesizing speech for text: {request.text[:50]}...")
        output_path = tts_service.synthesize(
            text=request.text
        )
        
        if not output_path:
            raise HTTPException(status_code=500, detail="Speech synthesis failed")
            
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename="synthesized_speech.wav"
        )
        
    except Exception as e:
        logger.error(f"Error in speech synthesis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))