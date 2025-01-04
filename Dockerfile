FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    git \
    python3-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install F5-TTS from source
RUN git clone https://github.com/SWivid/F5-TTS.git /tmp/f5-tts \
    && cd /tmp/f5-tts \
    && pip install -e .

# Copy application code
COPY . .

# Run the application
CMD ["python", "-m", "app.main"] 