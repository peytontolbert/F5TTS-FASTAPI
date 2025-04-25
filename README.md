# F5-TTS FastAPI Service

A FastAPI service for text-to-speech synthesis using the F5-TTS model.

## Features

- Text-to-speech synthesis with voice profile support
- JWT authentication
- Docker containerization
- GPU support
- Voice profile management
- Health monitoring

## Prerequisites

- Python 3.11 or higher
- Docker with NVIDIA Container Toolkit
- NVIDIA GPU with CUDA support
- F5-TTS model weights

## Directory Structure
```python
├── app/
│ ├── api/
│ │ ├── models/
│ │ └── routes/
│ ├── core/
│ ├── services/
│ └── voice_profiles/
├── scripts/
├── tests/
├── voice_profiles/
├── weights/
└── docker-compose.yml
```


## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```


2. Download https://huggingface.co/SWivid/F5-TTS & Place model files:
   - Put `model_1200000.pt` in `weights/`
   - Put `F5TTS_Base_vocab.txt` in `weights/`

3. Set up voice profiles:
```bash
python scripts/setup_test_voice.py
```

4. Verify setup:
```bash
python scripts/verify_setup.py
```

## Running the Service

1. Start the service:
```bash
docker-compose up --build
```


2. Generate an authentication token:
```
bash
python scripts/generate_token.py
```

3. Test the API:
```bash
python scripts/test_api.py
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/voices/list` - List available voice profiles
- `POST /api/v1/tts/synthesize` - Generate speech from text

### TTS Request Format
```json
{
"text": "Text to convert to speech",
"voice_profile": "bane"
}
```

## Environment Variables

- `PORT` - Server port (default: 8081)
- `MODEL_DIR` - Directory containing model files
- `VOICE_PROFILES_DIR` - Directory containing voice profiles
- `SECRET_KEY` - JWT secret key

## Development

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```


2. Install development dependencies:
```bash
pip install -r requirements.txt
```


3. Run tests:
```bash
python -m pytest tests/
```

## License

This project uses the F5-TTS model. Please ensure compliance with the model's license terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request