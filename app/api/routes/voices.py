from fastapi import APIRouter, HTTPException, Depends
from app.core.security import validate_token
import os
from app.core.config import settings
import logging

router = APIRouter(prefix="/voices")
logger = logging.getLogger(__name__)

@router.get("/list")
async def list_voice_profiles(token: str = Depends(validate_token)):
    """
    List available voice profiles
    """
    try:
        profiles_dir = settings.VOICE_PROFILES_DIR
        if not os.path.exists(profiles_dir):
            return {"profiles": []}
            
        profiles = [d for d in os.listdir(profiles_dir) 
                   if os.path.isdir(os.path.join(profiles_dir, d))]
        return {"profiles": profiles}
        
    except Exception as e:
        logger.error(f"Error listing voice profiles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 