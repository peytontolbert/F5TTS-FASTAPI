import torch
import torchaudio
import soundfile as sf
import os
import tempfile
import logging
from typing import Optional
from f5_tts.model import DiT, CFM
from f5_tts.infer.utils_infer import (
    load_vocoder,
    preprocess_ref_audio_text,
    infer_process,
)

logger = logging.getLogger(__name__)

class F5TTSService:
    def __init__(self, model_dir: str, voice_profile: str):
        """
        Initialize F5 TTS service
        
        Args:
            model_dir: Directory containing model files and voice profiles
            voice_profile: Name of the voice profile to use
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Setup paths
        self.model_dir = model_dir
        self.checkpoint_path = os.path.join("/app", model_dir, "final_finetuned_model.pt")
        self.vocab_path = os.path.join("/app", model_dir, "F5TTS_Base_vocab.txt")
        self.voice_profile_dir = os.path.join("/app/voice_profiles", voice_profile)
        
        # Validate paths
        self._validate_paths()
        
        # Initialize components
        self.vocab_char_map = None
        self.model = None
        self.vocoder = None
        self.ref_audio = None
        self.ref_text = None
        
        # Load everything
        self._initialize_components()
        
    def _validate_paths(self):
        """Validate all required paths exist"""
        logger.info(f"Validating paths in {self.model_dir}")
        if not os.path.exists(self.model_dir):
            logger.error(f"Model directory not found: {self.model_dir}")
            logger.error(f"Current working directory: {os.getcwd()}")
            logger.error(f"Directory contents: {os.listdir('/')}")
            raise ValueError(f"Model directory not found: {self.model_dir}")
        if not os.path.exists(self.checkpoint_path):
            logger.error(f"Checkpoint not found: {self.checkpoint_path}")
            logger.error(f"Model dir contents: {os.listdir(self.model_dir)}")
            raise ValueError(f"Checkpoint not found: {self.checkpoint_path}")
        if not os.path.exists(self.vocab_path):
            raise ValueError(f"Vocabulary file not found: {self.vocab_path}")
        if not os.path.exists(self.voice_profile_dir):
            raise ValueError(f"Voice profile not found: {self.voice_profile_dir}")
            
    def _load_vocab(self):
        """Load vocabulary from file"""
        logger.info("Loading vocabulary...")
        try:
            with open(self.vocab_path, 'r', encoding='utf-8') as f:
                vocab = [line.strip() for line in f.readlines()]
            
            vocab_char_map = {}
            for i, char in enumerate(vocab):
                if char:  # Skip empty lines
                    vocab_char_map[char] = i
                    
            return vocab_char_map, len(vocab_char_map) + 1
            
        except Exception as e:
            logger.error(f"Error loading vocabulary: {e}")
            raise
            
    def _create_model(self, vocab_size: int):
        """Create and configure the model"""
        logger.info("Creating model...")
        try:
            model_cfg = dict(
                dim=1024,
                depth=22,
                heads=16,
                ff_mult=2,
                text_dim=512,
                conv_layers=4
            )

            mel_spec_kwargs = dict(
                n_fft=1024,
                hop_length=256,
                win_length=1024,
                n_mel_channels=100,
                target_sample_rate=24000,
                mel_spec_type="vocos"
            )

            model = CFM(
                transformer=DiT(**model_cfg, text_num_embeds=vocab_size, mel_dim=100),
                mel_spec_kwargs=mel_spec_kwargs,
                vocab_char_map=self.vocab_char_map,
            )
            
            return model.to(self.device)
            
        except Exception as e:
            logger.error(f"Error creating model: {e}")
            raise
            
    def _initialize_components(self):
        """Initialize all components"""
        try:
            # Load vocabulary
            self.vocab_char_map, vocab_size = self._load_vocab()
            
            # Create model
            self.model = self._create_model(vocab_size)
            
            # Load checkpoint
            logger.info("Loading model checkpoint...")
            checkpoint = torch.load(self.checkpoint_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            
            # Load vocoder
            logger.info("Loading vocoder...")
            self.vocoder = load_vocoder(vocoder_name="vocos", is_local=False)
            
            # Load reference audio
            self._load_reference_audio()
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
            
    def _load_reference_audio(self):
        """Load reference audio from voice profile"""
        logger.info("Loading reference audio...")
        try:
            samples_file = os.path.join(self.voice_profile_dir, "samples.txt")
            logger.info(f"Reading samples from: {samples_file}")
            if not os.path.exists(samples_file):
                raise FileNotFoundError(f"Voice profile samples not found: {samples_file}")
                
            with open(samples_file, 'r') as f:
                first_sample = f.readline().strip().split('|')
                if len(first_sample) != 2:
                    raise ValueError("Invalid sample format in samples.txt")
                    
                audio_file, text = first_sample
                # Get absolute path of the audio file
                if not os.path.isabs(audio_file):
                    audio_file = os.path.join(self.voice_profile_dir, audio_file)
                logger.info(f"Loading audio from: {audio_file}")
                
                if not os.path.exists(audio_file):
                    raise FileNotFoundError(f"Audio file not found: {audio_file}")
                
                self.ref_audio, self.ref_text = preprocess_ref_audio_text(audio_file, text)
                
        except Exception as e:
            logger.error(f"Error loading reference audio: {e}")
            raise
            
    def synthesize(self, text: str) -> Optional[str]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            
        Returns:
            Path to generated audio file or None if synthesis failed
        """
        if not text:
            logger.error("Empty text provided")
            return None
            
        try:
            logger.info(f"Synthesizing text: {text[:50]}...")
            
            # Create output directory if needed
            output_dir = os.path.join(self.voice_profile_dir, "generated")
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate unique output path
            output_path = os.path.join(output_dir, f"speech_{hash(text)}.wav")
            
            # Generate audio
            with torch.no_grad():
                audio, sample_rate, _ = infer_process(
                    self.ref_audio,
                    self.ref_text,
                    text,
                    self.model,
                    self.vocoder,
                    mel_spec_type="vocos",
                    speed=1.0,
                    nfe_step=32,
                    cfg_strength=2.0,
                    sway_sampling_coef=-1.0
                )
                
                if audio is None or len(audio) == 0:
                    logger.error("Generated audio is empty")
                    return None
                    
                # Save audio file
                sf.write(
                    output_path,
                    audio,
                    sample_rate,
                    'PCM_16',
                    format='WAV'
                )
                
                logger.info(f"Audio saved to: {output_path}")
                return output_path
                
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            return None
            
    def cleanup(self):
        """Cleanup temporary files"""
        try:
            output_dir = os.path.join(self.voice_profile_dir, "generated")
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    try:
                        os.remove(os.path.join(output_dir, file))
                    except Exception as e:
                        logger.warning(f"Failed to remove file {file}: {e}")
                        
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")