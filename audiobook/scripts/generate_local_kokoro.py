import hashlib
import json
import os
import re
import urllib.request

import numpy as np
import ollama
import soundfile as sf
import yaml
from kokoro_onnx import Kokoro

# Configuration
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx"
VOICES_URL = "https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin"
MODEL_DIR = "audiobook/models"
OUTPUT_DIR = "audiobook_output"
CACHE_DIR = "audiobook/cache"
MODEL_PATH = os.path.join(MODEL_DIR, "kokoro-v0_19.onnx")
VOICES_PATH = os.path.join(MODEL_DIR, "voices-v1.0.bin")

# Voice Selection (af_sarah is a good default female voice, am_michael for male)
VOICE_NAME = "af_sarah"

# LLM Model for emotional rewriting
# Recommended models (pull with: ollama pull <model>):
#   - gemma3:12b (excellent quality, good speed)
#   - gemma2:9b (balanced speed/quality)
#   - gemma2:2b (fastest, good quality)
#   - llama3.2:3b (fast, good quality)
OLLAMA_MODEL = "gemma3:12b"  # High quality, good speed

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

def setup_dirs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache_path(text, model):
    hash_obj = hashlib.md5(f"{text}{model}".encode())
    return os.path.join(CACHE_DIR, f"{hash_obj.hexdigest()}.json")

def remove_punctuation_words(text):
    """Remove punctuation names that Kokoro would read aloud."""
    # Common punctuation words LLMs might generate
    punct_words = [
        r'\bperiod\b', r'\bcomma\b', r'\bsemicolon\b', r'\bcolon\b',
        r'\bquestion mark\b', r'\bexclamation mark\b', r'\bexclamation point\b',
        r'\bellipsis\b', r'\bdash\b', r'\bhyphen\b', r'\bquote\b',
        r'\bapostrophe\b', r'\bparenthesis\b', r'\bbracket\b',
        # Bracketed versions
        r'\[period\]', r'\[comma\]', r'\[semicolon\]', r'\[colon\]',
        r'\[question mark\]', r'\[exclamation mark\]', r'\[exclamation point\]',
        r'\[ellipsis\]', r'\[dash\]', r'\[hyphen\]',
    ]

    for pattern in punct_words:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Clean up resulting double spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def validate_kokoro_controls(text):
    """Clean up and validate Kokoro TTS control tokens."""
    # First remove punctuation words
    text = remove_punctuation_words(text)

    # Kokoro supports: [laughter], [laughs], and basic punctuation
    # Remove unsupported speed controls like <speed=...>
    text = re.sub(r'<speed=[0-9.]+>', '', text)
    text = re.sub(r'</speed>', '', text)

    # Remove other unsupported XML-like tags
    text = re.sub(r'<[^>]+>', '', text)

    # Keep only valid tokens: [laughter], [laughs]
    # Remove any other bracketed tokens the LLM might have invented
    valid_tokens = ['laughter', 'laughs', 'sigh', 'gasp']
    def validate_token(match):
        token = match.group(1).lower()
        if token in valid_tokens:
            return f'[{token}]'
        return ''  # Remove invalid token

    text = re.sub(r'\[([^\]]+)\]', validate_token, text)

    # Remove # symbols (markdown headers, hashtags)
    text = re.sub(r'#', '', text)

    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([,.!?])', r'\1', text)  # Remove space before punctuation

    return text.strip()

def react_agent_review(text, chapter_title, idx, total_chapters):
    """
    ReAct agent that reviews and fixes text issues.
    Can iterate to fix: gaps, irrational pauses, flow problems, repetition.
    """

    # Tools available to the agent
    tools_description = """
Available tools:
1. fix_gaps - Fix logical gaps or missing transitions
2. fix_pauses - Fix awkward or irrational pauses/punctuation
3. fix_flow - Improve sentence flow and readability
4. fix_repetition - Remove redundant phrases
5. approve - Text is ready, no more changes needed
"""

    max_iterations = 3
    current_text = text

    for iteration in range(max_iterations):
        review_prompt = f"""You are a quality control agent reviewing audiobook text for narration.

CONTEXT:
- Chapter {idx + 1} of {total_chapters}
- Title: {chapter_title}
- Iteration: {iteration + 1}/{max_iterations}

TEXT TO REVIEW:
{current_text[:1500]}{"..." if len(current_text) > 1500 else ""}

{tools_description}

CRITICAL EVALUATION CRITERIA:

1. PAUSE EVALUATION:
   - Are commas used appropriately for natural breathing pauses?
   - Are there too many commas creating choppy reading?
   - Are there missing commas where pauses would help clarity?
   - Do periods mark proper sentence endings?
   - Are ellipses (...) used only for dramatic effect, not excessively?

2. SENTENCE STRUCTURE:
   - Are sentences grammatically complete?
   - Is each sentence logically structured (subject-verb-object)?
   - Are there run-on sentences that should be split?
   - Are there fragments that should be combined?
   - Does sentence length vary for natural rhythm?

3. LOGICAL FLOW:
   - Do ideas connect smoothly paragraph to paragraph?
   - Are transitions between thoughts natural?
   - Is there redundant information?
   - Are concepts introduced in logical order?

4. AUDIOBOOK READABILITY:
   - Will this sound natural when read aloud?
   - Are there tongue-twisters or awkward phrases?
   - Is the tone consistent with the book's voice?

RESPONSE FORMAT:
Thought: [Detailed analysis addressing all 4 criteria above]
Action: [tool_name - fix_gaps, fix_pauses, fix_flow, fix_repetition, or approve]
Action Input: [specific issue to fix with example, or 'none' if approving]

If you find ANY issues in the criteria above, select the MOST critical one and fix it.
Only use 'approve' if ALL criteria are met and the text is ready for narration.
"""

        try:
            response = ollama.chat(model=OLLAMA_MODEL, messages=[
                {'role': 'user', 'content': review_prompt}
            ])

            agent_response = response['message']['content']

            # Parse agent response
            action_match = re.search(r'Action:\s*(\w+)', agent_response)
            action_input_match = re.search(r'Action Input:\s*(.+?)(?=\n\n|$)', agent_response, re.DOTALL)

            if not action_match:
                break

            action = action_match.group(1).lower()
            action_input = action_input_match.group(1).strip() if action_input_match else "none"

            if action == 'approve':
                if iteration > 0:
                    print(f"    Agent approved after {iteration + 1} iteration(s)")
                break

            # Apply fix based on action
            if action in ['fix_gaps', 'fix_pauses', 'fix_flow', 'fix_repetition']:
                fix_prompt = f"""Fix the following issue in this audiobook text:

Issue to fix: {action_input}

Current text:
{current_text}

Provide ONLY the fixed text, no explanations. Maintain the emotional tone and narrative flow."""

                fix_response = ollama.chat(model=OLLAMA_MODEL, messages=[
                    {'role': 'user', 'content': fix_prompt}
                ])

                current_text = fix_response['message']['content'].strip()
                print(f"    Agent applied: {action} - {action_input[:60]}...")

        except Exception as e:
            print(f"    Agent review error: {e}")
            break

    # Final validation after agent fixes
    return validate_kokoro_controls(current_text)

def rewrite_text(text, previous_context="", next_context=""):
    """Rewrites text to be more emotional and engaging using Ollama with context."""
    # Cache key includes context for uniqueness
    cache_key = f"{text}{previous_context[:200]}{next_context[:200]}{OLLAMA_MODEL}"
    hash_obj = hashlib.md5(cache_key.encode())
    cache_path = os.path.join(CACHE_DIR, f"{hash_obj.hexdigest()}.json")

    if os.path.exists(cache_path):
        print("  (Using cached rewrite)")
        with open(cache_path) as f:
            return json.load(f)['rewritten']

    # Build context sections
    context_parts = []
    if previous_context:
        context_parts.append(f"PREVIOUS CHAPTER CONTEXT (for continuity):\n{previous_context[:500]}...\n")
    if next_context:
        context_parts.append(f"NEXT CHAPTER PREVIEW (for flow):\n{next_context[:500]}...\n")

    context_str = "\n".join(context_parts) if context_parts else ""

    prompt = f"""You are a professional audiobook editor and narrator.
Rewrite the following text to be more emotional, engaging, and suitable for audio narration.

{context_str}
IMPORTANT INSTRUCTIONS:
1. Use ONLY English. Do not use any other languages or characters.
2. Add Kokoro TTS control tokens sparingly for emotional prosody:
   - Use [laughter] or [laughs] ONLY for genuinely humorous moments
   - Use commas for brief pauses, periods for longer pauses
   - Use ellipses (...) for dramatic or contemplative pauses
   - DO NOT use speed controls, XML tags, or other markup
3. CRITICAL: Do NOT write out punctuation names (like "period", "comma", "exclamation mark")
   - Just use the actual punctuation marks naturally in the text
   - Bad: "This is important period"
   - Good: "This is important."
4. Maintain the original meaning and key information
5. Improve the flow, tone, and emotional resonance
6. Consider the context from previous and next chapters to maintain narrative continuity
7. Do not add any introductory or concluding remarks
8. Provide the rewritten text directly with minimal control tokens

TEXT TO REWRITE:
{text}
"""

    print(f"  Rewriting with {OLLAMA_MODEL} (with context)...")
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {'role': 'user', 'content': prompt},
        ])
        rewritten = response['message']['content']

        # Validate and clean Kokoro controls
        rewritten = validate_kokoro_controls(rewritten)

        with open(cache_path, 'w') as f:
            json.dump({
                'original': text,
                'rewritten': rewritten,
                'model': OLLAMA_MODEL,
                'had_context': bool(previous_context or next_context)
            }, f)

        return rewritten
    except Exception as e:
        print(f"  Error calling Ollama: {e}")
        return text  # Fallback to original

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

def extract_chapter_title(chapter_file):
    """Extract chapter title from filename or content."""
    with open(chapter_file) as f:
        content = f.read()

    # Try to find title in frontmatter
    frontmatter_match = re.search(r"^---[\s\S]*?title:\s*[\"']?(.*?)[\"']?\s*$[\s\S]*?---", content, re.MULTILINE)
    if frontmatter_match:
        return frontmatter_match.group(1)

    # Try to find first # heading
    heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading_match:
        return heading_match.group(1)

    # Fallback to filename
    basename = os.path.basename(chapter_file).replace(".qmd", "").replace("-", " ").title()
    return basename

def main():
    print("--- Emotional Audiobook Generator (Kokoro + Ollama) ---")

    # 1. Setup
    download_models()
    setup_dirs()

    print("Loading Kokoro model...")
    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    print(f"Model loaded. Using voice: {VOICE_NAME}")

    # 2. Read Config
    with open("_quarto.yml") as f:
        config = yaml.safe_load(f)

    chapters = config["book"]["chapters"]
    title = config["book"].get("title", "Audiobook")
    author = config["book"].get("author", "Unknown Author")

    print(f"Found {len(chapters)} chapters in _quarto.yml")
    print(f"Generating: {title} by {author}\n")

    # 3. Pre-collect chapter texts for context
    print("Pre-loading chapters for context...")
    chapter_texts = []
    chapter_files = []

    def collect_chapters(entries):
        """Recursively collect chapter files."""
        collected = []
        for entry in entries:
            if isinstance(entry, dict) and 'chapters' in entry:
                collected.extend(collect_chapters(entry['chapters']))
            elif isinstance(entry, str):
                if not entry.endswith("index.qmd") and "cover" not in entry and "references.qmd" not in entry:
                    collected.append(entry)
        return collected

    chapter_files = collect_chapters(chapters)

    # Load and clean all chapter texts
    for chapter_file in chapter_files:
        if os.path.exists(chapter_file):
            with open(chapter_file) as f:
                content = f.read()
            cleaned = clean_text(content)
            chapter_texts.append(cleaned if cleaned else "")
        else:
            chapter_texts.append("")

    print(f"Loaded {len(chapter_texts)} chapters\n")

    # 4. STEP 1: Generate all rewritten text first
    print("=" * 60)
    print("STEP 1: Generating emotional rewrites for all chapters...")
    print("=" * 60)

    rewritten_texts = []
    chapter_titles = []

    for idx, chapter_file in enumerate(chapter_files):
        previous_text = chapter_texts[idx - 1] if idx > 0 else ""
        next_text = chapter_texts[idx + 1] if idx < len(chapter_texts) - 1 else ""

        chapter_title = extract_chapter_title(chapter_file)
        chapter_titles.append(chapter_title)

        print(f"\n[{idx}] {chapter_file}")
        print(f"    Chapter {idx + 1}: {chapter_title}")

        # Rewrite with context
        rewritten = rewrite_text(chapter_texts[idx], previous_text, next_text)
        rewritten_texts.append(rewritten)

        print(f"    ✓ Rewritten ({len(rewritten)} chars)")

    # 5. STEP 2: Review and validate all text
    print("\n" + "=" * 60)
    print("STEP 2: Reviewing and validating all rewrites...")
    print("=" * 60)

    validated_texts = []
    for idx, rewritten in enumerate(rewritten_texts):
        validated = validate_kokoro_controls(rewritten)
        validated_texts.append(validated)

        # Show what was cleaned
        if validated != rewritten:
            removed = len(rewritten) - len(validated)
            print(f"[{idx}] Cleaned chapter {idx + 1} (removed {removed} chars of invalid content)")

    print(f"\n✓ All {len(validated_texts)} chapters validated for Kokoro\n")

    # 5.5. STEP 2.5: Agent Quality Review
    print("\n" + "=" * 60)
    print("STEP 2.5: Agent quality review and fixes...")
    print("=" * 60)

    reviewed_texts = []
    for idx, validated in enumerate(validated_texts):
        print(f"\n[{idx}] Reviewing chapter {idx + 1}: {chapter_titles[idx]}")

        # Agent reviews and potentially fixes the text
        reviewed = react_agent_review(
            validated,
            chapter_titles[idx],
            idx,
            len(validated_texts)
        )
        reviewed_texts.append(reviewed)

        if reviewed != validated:
            print("    ✓ Text improved by agent")

    print("\n✓ All chapters reviewed\n")

    # 6. STEP 3: Generate audio from validated text
    print("=" * 60)
    print("STEP 3: Generating audio with Kokoro...")
    print("=" * 60)

    all_samples = []
    sample_rate = 24000  # Default for Kokoro

    # Add Intro
    intro_text = f"{title}, by {author}. An audiobook narration."
    print("\nGenerating intro...")
    samples, _ = kokoro.create(intro_text, voice=VOICE_NAME, speed=1.0, lang="en-us")
    all_samples.append(samples)

    # Add a pause after intro
    silence = np.zeros(int(sample_rate * 1.5))
    all_samples.append(silence)

    # Process each chapter audio
    for idx, chapter_file in enumerate(chapter_files):
        announcement = f"Chapter {idx + 1}: {chapter_titles[idx]}"

        print(f"\n[{idx}] {chapter_file}")
        print(f"    {announcement}")

        # Generate chapter announcement
        announcement_samples, _ = kokoro.create(announcement, voice=VOICE_NAME, speed=1.0, lang="en-us")

        # Generate content audio
        print(f"    Generating audio ({len(reviewed_texts[idx])} chars)...")
        try:
            content_samples, _ = kokoro.create(
                reviewed_texts[idx],
                voice=VOICE_NAME,
                speed=1.0,
                lang="en-us"
            )

            # Save individual chapter
            filename = os.path.basename(chapter_file).replace(".qmd", ".wav")
            output_path = os.path.join(OUTPUT_DIR, filename)

            # Combine announcement + content
            chapter_audio = np.concatenate([
                announcement_samples,
                np.zeros(int(sample_rate * 0.8)),  # Short pause
                content_samples
            ])

            sf.write(output_path, chapter_audio, sample_rate)
            all_samples.append(chapter_audio)
            all_samples.append(silence)  # Pause between chapters

            print(f"    ✓ Saved to {output_path}")

        except Exception as e:
            print(f"    ✗ Error generating audio: {e}")
            continue

    # Add Outro
    outro_text = "The End. Thank you for listening."
    print("\n\nGenerating outro...")
    samples, _ = kokoro.create(outro_text, voice=VOICE_NAME, speed=1.0, lang="en-us")
    all_samples.append(samples)

    # 7. Stitch and Save Full Audiobook
    if all_samples:
        print("\n" + "=" * 60)
        print("FINAL: Stitching full audiobook...")
        print("=" * 60)
        full_audio = np.concatenate(all_samples)
        output_path = os.path.join(OUTPUT_DIR, "full_audiobook.wav")
        sf.write(output_path, full_audio, sample_rate)

        duration_mins = len(full_audio) / sample_rate / 60
        print(f"\n🎉 Full audiobook saved to: {output_path}")
        print(f"   Duration: {duration_mins:.1f} minutes")
        print(f"   Chapters: {len(reviewed_texts)}")

if __name__ == "__main__":
    main()
