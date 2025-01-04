import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_directories():
    """Create required directories for F5-TTS"""
    dirs = [
        "models/weights",
        "models/configs",
        "voice_profiles",
        "f5_tts_cache"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

if __name__ == "__main__":
    setup_directories() 