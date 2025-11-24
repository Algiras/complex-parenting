import os
import re

import yaml


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

    # --- Narrative Enhancements ---

    # Remove Subheaders (##, ###, etc.) to improve flow
    # We keep Level 1 (#) if it's a Chapter title, but usually those are handled by the file separation.
    # Let's remove lines starting with ## or ###
    text = re.sub(r"^#{2,}\s+.*$", "", text, flags=re.MULTILINE)

    # Remove bold/italic formatting (**text**, *text*)
    text = re.sub(r"\*\*|__", "", text)
    text = re.sub(r"\*|_", "", text)

    # Remove links [text](url) -> text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    # Remove blockquotes (> text)
    text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)

    # Remove list bullets (*, -, +) to make it sound less like a list
    # We replace them with a slight pause (comma) if appropriate, or just remove.
    # Ideally, lists should be read naturally.
    text = re.sub(r"^[\*\-\+]\s+", "", text, flags=re.MULTILINE)

    # Remove numbered lists (1. )
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

    # Collapse multiple newlines to max 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove bold/italic markers (optional, but good for raw TTS)
    # text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # text = re.sub(r'\*(.*?)\*', r'\1', text)

    return text.strip()


def main():
    # Read config to get chapter order
    with open("books/_quarto.yml") as f:
        config = yaml.safe_load(f)

    chapters = config["book"]["chapters"]
    full_script = ""

    print(f"Found {len(chapters)} chapters.")

    for chapter_file in chapters:
        if chapter_file == "00-cover.qmd":
            continue

        # Skip bibliography/indices for audio
        if chapter_file in ["15-bibliography.qmd", "17-source-index.qmd"]:
            continue

        path = os.path.join("books", chapter_file)
        if not os.path.exists(path):
            print(f"Warning: {path} not found.")
            continue

        print(f"Processing {chapter_file}...")

        with open(path) as f:
            content = f.read()

        cleaned = clean_text(content)

        # Add a marker for the audio script
        full_script += f"\n\n--- START OF FILE: {chapter_file} ---\n\n"
        full_script += cleaned
        full_script += "\n\n--- END OF FILE ---\n"

    output_file = "audiobook_script.txt"
    with open(output_file, "w") as f:
        f.write(full_script)

    print(f"Successfully created {output_file}")


if __name__ == "__main__":
    main()
