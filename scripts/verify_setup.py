import os
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_setup():
    """Verify all required directories and files exist"""
    required_dirs = [
        "weights",
        "voice_profiles",
        "f5_tts_cache"
    ]
    
    required_files = [
        ("weights/final_finetuned_model.pt", "Model checkpoint"),
        ("weights/F5TTS_Base_vocab.txt", "Vocabulary file")
    ]
    
    # Check directories
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            logger.info(f"Creating directory: {dir_name}")
            os.makedirs(dir_name, exist_ok=True)
    
    # Check files
    missing_files = []
    for file_path, description in required_files:
        if not os.path.exists(file_path):
            missing_files.append((file_path, description))
    
    if missing_files:
        logger.error("Missing required files:")
        for file_path, description in missing_files:
            logger.error(f"  - {description}: {file_path}")
        return False
    
    return True

if __name__ == "__main__":
    if verify_setup():
        logger.info("All required files and directories are present")
    else:
        logger.error("Please ensure all required files are in place before running the server") 