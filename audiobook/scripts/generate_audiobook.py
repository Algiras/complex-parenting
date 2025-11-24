import os
import re

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv(
    "ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"
)  # Default to "Rachel" if not set
MODEL_ID = "eleven_multilingual_v2"
CHUNK_SIZE = 1024  # Chunk size for streaming response

if not ELEVENLABS_API_KEY:
    print("Error: ELEVENLABS_API_KEY not found in .env file.")
    print("Please create a .env file with: ELEVENLABS_API_KEY=your_key_here")
    exit(1)


def generate_audio(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY,
    }

    data = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    print(f"Generating audio for: {os.path.basename(output_path)}...")

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        print(f"Saved to {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error generating audio: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}")
        return False


def parse_script(script_path):
    with open(script_path) as f:
        content = f.read()

    # Split by file markers
    # Pattern: --- START OF FILE: filename --- ... --- END OF FILE ---
    pattern = r"--- START OF FILE: (.*?) ---\n(.*?)\n--- END OF FILE ---"
    matches = re.findall(pattern, content, re.DOTALL)

    return matches


def validate_api():
    """Validates the API key and Voice ID."""
    print("Validating API credentials...")

    # 1. Check API Key (Get User Info)
    user_url = "https://api.elevenlabs.io/v1/user"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    try:
        response = requests.get(user_url, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        print(
            f"✅ API Key Valid. User: {user_data.get('subscription', {}).get('tier', 'Unknown Tier')}"
        )

        # Check character count
        chars_used = user_data.get("subscription", {}).get("character_count", 0)
        chars_limit = user_data.get("subscription", {}).get("character_limit", 0)
        print(f"   Usage: {chars_used:,} / {chars_limit:,} characters")

        if chars_used >= chars_limit:
            print("⚠️  WARNING: You have exceeded your character limit!")

    except requests.exceptions.RequestException as e:
        # Handle permission error specifically (API key might be valid for TTS but not for User info)
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code in [401, 403]:
                print("⚠️  Warning: Could not validate subscription details (Permission Denied).")
                print("   Proceeding assuming API key is valid for generation.")
                return True  # Allow to proceed
            print(f"❌ API Key Validation Failed: {e}")
            print(f"   Response: {e.response.text}")
            return False
        else:
            print(f"❌ Connection Error: {e}")
            return False

    # 2. Check Voice ID
    voice_url = f"https://api.elevenlabs.io/v1/voices/{VOICE_ID}"
    try:
        response = requests.get(voice_url, headers=headers)
        response.raise_for_status()
        voice_data = response.json()
        print(f"✅ Voice ID Valid. Name: {voice_data.get('name', 'Unknown')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Voice ID Validation Failed: {e}")
        print(f"   Voice ID: {VOICE_ID}")
        return False

    return True


def main():
    script_path = "audiobook_script.txt"
    output_dir = "audiobook_output"

    if not validate_api():
        print("Exiting due to validation errors.")
        exit(1)

    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found. Please run prepare_audiobook.py first.")
        exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chapters = parse_script(script_path)
    print(f"Found {len(chapters)} chapters in script.")

    # Calculate total characters
    total_chars = sum(len(text) for _, text in chapters)

    # Estimate cost (Standard rate is approx $0.30 per 1000 characters, but varies by plan)
    COST_PER_1K_CHARS = 0.30
    estimated_cost = (total_chars / 1000) * COST_PER_1K_CHARS

    print("\n--- Options ---")
    print(f"Total Book Length: {total_chars:,} characters")
    print(f"Estimated Cost (Full): ${estimated_cost:.2f}")
    print("-----------------------")
    print("1. Generate Full Book")
    print("2. Generate Sample (First ~10,000 characters - Free Tier Friendly)")

    choice = input("\nEnter choice (1 or 2): ").strip()

    limit_chars = None
    if choice == "2":
        limit_chars = 10000
        print(f"\nSelected: Sample Mode (Limit: {limit_chars} chars)")
    elif choice == "1":
        print("\nSelected: Full Book")
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    confirm = input("Ready to proceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("Operation cancelled.")
        exit(0)

    print("\nStarting generation...")

    current_chars_generated = 0

    for filename, text in chapters:
        # Check limit
        if limit_chars is not None:
            if current_chars_generated >= limit_chars:
                print(f"Reached sample limit of {limit_chars} characters. Stopping.")
                break

            # If this chapter pushes us over, truncate it?
            # Or just generate it if it's close?
            # Let's truncate strictly to respect the "Free Tier" safety.
            remaining = limit_chars - current_chars_generated
            if len(text) > remaining:
                print(f"Truncating {filename} to {remaining} characters to fit sample limit...")
                text = text[:remaining]
                # Add a note that it was truncated
                text += "... [End of Sample]"

        # Create a clean filename for the mp3
        base_name = os.path.splitext(filename)[0]
        safe_name = "".join([c for c in base_name if c.isalnum() or c in ("-", "_")])
        mp3_filename = f"{safe_name}.mp3"
        output_path = os.path.join(output_dir, mp3_filename)

        if os.path.exists(output_path):
            print(f"Skipping {mp3_filename} (already exists)")
            current_chars_generated += len(text)
            continue

        # ElevenLabs has a character limit per request
        if len(text) > 5000:
            print(f"Warning: {filename} is {len(text)} chars long. Splitting...")

            paragraphs = text.split("\n\n")
            current_chunk = ""
            part = 1

            for para in paragraphs:
                if len(current_chunk) + len(para) < 4500:
                    current_chunk += para + "\n\n"
                else:
                    part_filename = f"{safe_name}_part{part:02d}.mp3"
                    part_path = os.path.join(output_dir, part_filename)
                    if generate_audio(current_chunk.strip(), part_path):
                        current_chars_generated += len(current_chunk)

                    current_chunk = para + "\n\n"
                    part += 1

            if current_chunk:
                part_filename = f"{safe_name}_part{part:02d}.mp3"
                part_path = os.path.join(output_dir, part_filename)
                if generate_audio(current_chunk.strip(), part_path):
                    current_chars_generated += len(current_chunk)

        else:
            if generate_audio(text.strip(), output_path):
                current_chars_generated += len(text)


if __name__ == "__main__":
    main()
