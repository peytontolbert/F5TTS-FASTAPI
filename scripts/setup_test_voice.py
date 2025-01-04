import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_test_voice():
    """Set up test voice profiles"""
    # Set up Bane profile
    voice_dir = "voice_profiles/bane"
    os.makedirs(voice_dir, exist_ok=True)
    
    # Check if source audio exists in app directory
    src_audio = "app/voice_profiles/bane/video_chunk_000.wav"
    dst_audio = os.path.join(voice_dir, "video_chunk_000.wav")
    
    if os.path.exists(src_audio):
        # Copy audio file from app directory
        shutil.copy2(src_audio, dst_audio)
        logger.info(f"Copied audio file from {src_audio} to {dst_audio}")
    else:
        logger.error(f"Source audio file not found: {src_audio}")
        logger.info("Please place your audio file in app/voice_profiles/bane directory")
        return
    
    # Create samples.txt
    samples_file = os.path.join(voice_dir, "samples.txt")
    with open(samples_file, 'w') as f:
        f.write(f"video_chunk_000.wav|This is a test sample.")
    
    # Create generated directory
    os.makedirs(os.path.join(voice_dir, "generated"), exist_ok=True)
    
    logger.info(f"Created voice profile in {voice_dir}")

if __name__ == "__main__":
    setup_test_voice() 