# The Shadow of Extremism

<p align="center">
  <img src="books/cover.png" alt="The Shadow of Extremism - Book Cover" width="400">
</p>

A comprehensive exploration of Islamic extremism through history, ideology, and pathways to reform.

[![Buy Me a Coffee](https://img.shields.io/badge/Support-Buy%20Me%20a%20Coffee-yellow?logo=buy-me-a-coffee)](https://buymeacoffee.com/algiras)

**📖 [Read Online](https://algiras.github.io/the-shadow-of-extremism/)** | **📥 [Download PDF](https://github.com/Algiras/the-shadow-of-extremism/releases)**

## About

This book traces the **Extremism Cycle** - a 7-phase framework showing how extremism emerges, peaks, and collapses across civilizations.

**Stats**: ~49,000 words | ~180-185 pages | 28 chapters

**License**: [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) - Free to share and adapt with attribution

## Reading Options

### 🌐 Read Online (Recommended)
Visit **[algiras.github.io/the-shadow-of-extremism](https://algiras.github.io/the-shadow-of-extremism/)** for:
- **Full-text search** across all chapters
- **Dark mode** support
- **Direct chapter links** for citations and sharing
- **Mobile-friendly** responsive design
- **No download required**

### 📥 Download
- **PDF**: [Latest Release](https://github.com/Algiras/the-shadow-of-extremism/releases)
- **EPUB**: For e-readers (Kindle, Kobo, etc.)

## Support This Work

This book is **free** because knowledge about extremism should be accessible to everyone. If you find it valuable, consider supporting future research → **[Support Options](https://algiras.github.io/the-shadow-of-extremism/25-support.html)**

## Project Structure

```
the-shadow-of-extremism/
├── books/              # Book source files (Quarto)
│   ├── *.qmd          # Chapter files (~49k words)
│   └── _quarto.yml    # Book configuration
├── audiobook/          # Audiobook generation (TTS)
│   ├── scripts/       # Python scripts
│   └── requirements.txt
├── tools/              # Utility scripts
│   └── scrape_resources.py  # Download cited web resources
├── references/         # Research notes and sources
└── .github/workflows/  # CI/CD (auto PDF/EPUB/DOCX)
```

## Quick Start

### Build the Book

```bash
# Install Quarto: https://quarto.org/
quarto render books --to pdf    # or epub, docx
```

Output in `books/_output/`

### Generate Audiobook

```bash
cd audiobook
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Add your ElevenLabs API key to .env
cp ../.env.example ../.env

python scripts/generate_audiobook.py
```

### Scrape Web Resources

```bash
cd tools
pip install -r requirements.txt
python scrape_resources.py
```

## GitHub Actions

Automatically renders PDF/EPUB/DOCX on every push. Download from Actions tab.

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

© 2025 Algimantas Krasauskas. Some rights reserved.
