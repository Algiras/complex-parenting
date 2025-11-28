# Audiobook Generation

Scripts to convert the book to audiobook format using multiple TTS options:
- **ElevenLabs** (cloud, high quality, paid)
- **Kokoro** (local, fast, free)
- **OpenVoice 2 + Ollama** (local, emotional rewriting + voice cloning)

## Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Mac/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Emotional Audiobook (OpenVoice 2 + Ollama)

This method uses Ollama to emotionally rewrite the text and OpenVoice 2 for voice cloning.

### Prerequisites

1. Install and run [Ollama](https://ollama.ai)
2. Pull a model (recommended: fast models for audiobook generation):
   ```bash
   # Recommended (best balance):
   ollama pull gemma2:9b
   
   # Or other options:
   ollama pull gemma2:2b      # Fastest
   ollama pull llama3.2:3b    # Fast alternative
   ollama pull qwen:14b       # Slower but higher quality
   ```
3. Run setup script to download OpenVoice and MeloTTS:

```bash
python scripts/setup_openvoice.py
```

### Generate Audiobook

**Option 1: Simple (Better Quality - Recommended)**
```bash
python scripts/generate_emotional_simple.py
```
Uses MeloTTS voice directly without conversion for clearer audio.

**Option 2: With Voice Cloning**
```bash
python scripts/generate_emotional.py
```
Uses OpenVoice 2 to clone a custom voice (requires reference audio).

Both options will:
- Rewrite each chapter with emotional enhancement via Ollama
- Generate speech with MeloTTS and convert to your voice using OpenVoice 2
- Add intro (book title, author) and outro ("The End")
- Stitch all chapters into a single audiobook file

Output: `audiobook_output_emotional/full_audiobook.wav`

## ElevenLabs Generation (Original Method)

### Configuration

Copy `.env.example` from the root directory and add your ElevenLabs API key:

```bash
cp ../.env.example ../.env
# Edit .env and add your ELEVENLABS_API_KEY
```

### Usage

```bash
python scripts/generate_audiobook.py
```

Output will be in `audiobook_output/` (excluded from git).

## Local Generation with Kokoro

Fast, free, local generation:

```bash
python scripts/generate_local_kokoro.py
```

Output: `audiobook_output/full_audiobook.wav`
