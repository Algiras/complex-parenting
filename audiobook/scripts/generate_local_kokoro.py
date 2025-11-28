import numpy as np

import os
import re
import yaml
import soundfile as sf
import urllib.request
from kokoro_onnx import Kokoro

# Configuration
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx"
VOICES_URL = "https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin"
MODEL_DIR = "audiobook/models"
OUTPUT_DIR = "audiobook_output"
MODEL_PATH = os.path.join(MODEL_DIR, "kokoro-v0_19.onnx")
VOICES_PATH = os.path.join(MODEL_DIR, "voices-v1.0.bin")

# Voice Selection (af_sarah is a good default female voice, am_michael for male)
VOICE_NAME = "af_sarah" 

def download_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    
    if not os.path.exists(MODEL_PATH):
        print(f"Downloading model to {MODEL_PATH}...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded.")

    if not os.path.exists(VOICES_PATH):
        print(f"Downloading voices to {VOICES_PATH}...")
        urllib.request.urlretrieve(VOICES_URL, VOICES_PATH)
        print("Voices downloaded.")

def clean_text(text):
    # Remove YAML frontmatter
    text = re.sub(r"^---[\s\S]*?---\n", "", text)
    # Remove images ![...](...)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    # Remove footnotes ^[...]
    text = re.sub(r"\^\[.*?\]", "", text)
    # Remove Quarto attributes {.unnumbered} etc
    text = re.sub(r"\{.*?\}", "", text)
    # Remove HTML comments <!-- ... -->
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    # Remove tables (lines starting with |)
    lines = text.split("\n")
    lines = [l for l in lines if not l.strip().startswith("|")]
    text = "\n".join(lines)
    
    # Narrative Enhancements
    # Remove Subheaders (##, ###, etc.) to improve flow
    text = re.sub(r"^#{2,}\s+.*$", "", text, flags=re.MULTILINE)
    # Remove bold/italic formatting
    text = re.sub(r"\*\*|__", "", text)
    text = re.sub(r"\*|_", "", text)
    # Remove links [text](url) -> text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    # Remove blockquotes (> text)
    text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)
    # Remove list bullets
    text = re.sub(r"^[\*\-\+]\s+", "", text, flags=re.MULTILINE)
    # Remove numbered lists
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
    # Collapse multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()

def main():
    print("--- Local Audiobook Generator (Kokoro) ---")
    
    # 1. Setup
    download_models()
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Loading Kokoro model...")
    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    print(f"Model loaded. Using voice: {VOICE_NAME}")

    # 2. Read Config
    with open("_quarto.yml") as f:
        config = yaml.safe_load(f)

    chapters = config["book"]["chapters"]
    print(f"Found {len(chapters)} chapters in _quarto.yml")

    # 3. Process Chapters
    all_samples = []
    sample_rate = 24000 # Default for Kokoro

    for i, chapter_entry in enumerate(chapters):
        # Handle 'part' sections
        if isinstance(chapter_entry, dict) and 'part' in chapter_entry:
            print(f"Skipping Part header: {chapter_entry['part']}")
            if 'chapters' in chapter_entry:
                for sub_chapter in chapter_entry['chapters']:
                    samples = process_chapter(sub_chapter, kokoro)
                    if samples is not None:
                        all_samples.append(samples)
            continue
        
        # Handle regular string entries
        if isinstance(chapter_entry, str):
            samples = process_chapter(chapter_entry, kokoro)
            if samples is not None:
                all_samples.append(samples)

    # 4. Stitch and Save Full Audiobook
    if all_samples:
        print("\nStitching full audiobook...")
        full_audio = np.concatenate(all_samples)
        output_path = os.path.join(OUTPUT_DIR, "full_audiobook.wav")
        sf.write(output_path, full_audio, sample_rate)
        print(f"🎉 Full audiobook saved to: {output_path}")

def process_chapter(chapter_file, kokoro):
    if chapter_file.endswith("index.qmd") or "cover" in chapter_file:
        # Optional: Include index/preface if desired. Let's include it.
        pass 
    
    if chapter_file in ["chapters/17-references.qmd"]:
        return None

    print(f"Processing {chapter_file}...")
    
    path = chapter_file 
    if not os.path.exists(path):
        print(f"Warning: {path} not found.")
        return None

    with open(path) as f:
        content = f.read()

    text = clean_text(content)
    
    if not text:
        print("  (Skipping empty text)")
        return None

    # Generate Audio
    print(f"  Generating audio ({len(text)} chars)...")
    try:
        samples, sample_rate = kokoro.create(
            text, 
            voice=VOICE_NAME, 
            speed=1.0, 
            lang="en-us"
        )
        
        # Save individual chapter
        filename = os.path.basename(chapter_file).replace(".qmd", ".wav")
        output_path = os.path.join(OUTPUT_DIR, filename)
        sf.write(output_path, samples, sample_rate)
        print(f"  Saved to {output_path}")
        
        return samples
        
    except Exception as e:
        print(f"  Error generating audio: {e}")
        return None

if __name__ == "__main__":
    main()
