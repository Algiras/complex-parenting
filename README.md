# The Shadow of Extremism

**A Journey Through History, Ideology, and the Path to Reform**

[![Book Status](https://img.shields.io/badge/status-publication%20ready-green)](https://github.com/Algiras/the-shadow-of-extremism)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 📖 About This Book

**"The Shadow of Extremism"** is a paradigm-shifting exploration of how extremist movements emerge, sustain themselves, and collapse. It moves beyond simple "clash of civilizations" narratives to reveal the **5 Universal Dynamics** that drive extremism across all cultures—from ISIS to the Inquisition, from Buddhist nationalism to secular revolutionary terror.

**New in this Edition (v11.5):**
- **Actionable Epilogue**: A "Now What?" guide converting readers into active change agents.
- **Mechanism Cheatsheet**: A practical tool for recognizing extremist patterns in real-time.
- **Comparative Rigor**: New analysis of the Rwandan genocide and Christian entropy.
- **AI-Amplified Research**: Pioneering methodology using LLMs for multi-language primary source analysis.

**Read Online**: [algiras.github.io/the-shadow-of-extremism](https://algiras.github.io/the-shadow-of-extremism/)

---

## 🔍 Seeking Anonymous Peer Reviewers

**This book is currently seeking critical feedback from reviewers with expertise in:**

- Islamic theology, jurisprudence (*fiqh*), or history
- Middle Eastern studies or colonial history
- Counter-terrorism, intelligence analysis, or security studies
- Political science, psychology of radicalization, or social movements
- Comparative religion (Buddhism, Christianity, Hinduism)

### What I'm Looking For

I need reviewers who will:
- **Challenge my arguments** - Point out logical flaws, oversimplifications, or biases
- **Fact-check** - Verify historical claims, theological interpretations, and statistical assertions
- **Identify blind spots** - What perspectives am I missing? What voices am I ignoring?
- **Suggest improvements** - Better sources, clearer explanations, sharper framing

### How to Contribute

1. **Read the book** online or download the [PDF/EPUB](https://github.com/Algiras/the-shadow-of-extremism/releases)
2. **Submit feedback** via:
   - GitHub Issues: [Report errors or suggest improvements](https://github.com/Algiras/the-shadow-of-extremism/issues)
   - GitHub Discussions: [Broader questions or thematic critiques](https://github.com/Algiras/the-shadow-of-extremism/discussions)
   - Email: [Contact the author](https://github.com/Algiras)
3. **Optional anonymity** - You can remain anonymous if preferred; I'm interested in the substance of the critique, not credentials

### What Gets Acknowledged

Substantive reviewers will be acknowledged in the front matter as "anonymous peer reviewers" unless you prefer to be named. Your feedback directly shapes the final published version.

---

## 🤖 AI Methodology

This book represents a pioneering use of **AI-Amplified Scholarship**. It was researched and refined in partnership with advanced Large Language Models (Google Gemini 2.0 Flash Thinking, Anthropic Claude) to:
- Analyze primary sources in classical Arabic, Ottoman Turkish, and Latin
- Identify structural patterns across 7 different religious/ideological movements
- Generate data-driven visualizations and infographics
- Ensure rigorous logical consistency

**Note**: AI was the telescope; the author was the astronomer. All interpretations, judgments, and conclusions are human-verified and the sole responsibility of the author.

---

## 🏗️ Project Structure

```
bookie/
├── pyproject.toml        # Python project configuration (dependencies, scripts)
├── Makefile              # Task runner for common operations
├── scripts/              # Utility scripts (lint checking, validation)
├── audiobook/            # Audiobook generation tools
├── tools/                # Additional utilities
├── books/                # Book content (Quarto markdown)
│   ├── index.qmd         # Introduction
│   ├── 01-20.qmd         # Main chapters
│   ├── 21-25.qmd         # Appendices and back matter
│   └── _quarto.yml       # Book configuration
└── .github/workflows/    # CI/CD (automatic builds)
```

---

## 🛠️ Building Locally

### Prerequisites
- [Quarto](https://quarto.org/docs/get-started/) (latest version)
- [TeX Live](https://www.tug.org/texlive/) (for PDF)
- Amiri font (for Arabic text rendering)
- Python 3.8+ (for utility scripts)

### Quick Start

```bash
# Install Python dependencies and scripts
make install

# Run content validation
make lint-check    # Check markdown formatting
make scan-chars    # Scan for invalid characters

# Render the book
cd books
quarto render --to html    # Generate HTML version
quarto render --to pdf     # Generate PDF version
quarto render --to epub    # Generate EPUB version

# Serve locally with live reload
quarto preview books
```

### Available Make Commands

```bash
make help          # Show all available commands
make install       # Install project in development mode
make lint-check    # Validate markdown formatting
make scan-chars    # Scan for invalid characters in content
make clean         # Remove build artifacts
```

### Using Python Scripts Directly

After running `make install`, scripts are available as commands:

```bash
lint-check         # Check markdown formatting in books/
scan-chars         # Scan for invalid characters
```

---

## 📜 License

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes without permission
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

[Full License Text](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 🙏 Acknowledgements

See [Acknowledgements](https://algiras.github.io/the-shadow-of-extremism/acknowledgements.html) for the full list of contributors.

Special thanks to my wife, a fierce defender of free speech, and my mother, a historian whose methodology shaped this work.

---

## 💬 Contact & Support

- **GitHub**: [Algiras](https://github.com/Algiras)
- **LinkedIn**: [Algimantas Krasauskas](https://www.linkedin.com/in/asimplek/)
- **Support**: [Buy me a coffee](https://buymeacoffee.com/algiras) to fund audiobook production

---

**Note**: This is a living document. All feedback, corrections, and suggestions are welcome as we work toward a final published version.
