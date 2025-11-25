# New Book Project

This repository contains a Quarto book project.

## Getting Started

1. **Edit Book Metadata**  
   Update `_quarto.yml` to set your book title, author name, and other configuration options.

2. **Add Content**  
   - Edit `index.qmd` for your home page
   - Add chapters in the `chapters/` directory
   - Update the `chapters:` list in `_quarto.yml` to include your new files

3. **Build the Book**  
   ```bash
   quarto render
   ```
   
   The output will be generated in `_output/`

4. **Preview Locally**  
   ```bash
   quarto preview
   ```

## Project Structure

```
├── _quarto.yml              # Book configuration
├── index.qmd                # Home page
├── chapters/                # Book chapters
│   └── 01-introduction.qmd
├── styles.css               # Custom CSS
├── .github/workflows/       # CI/CD for automatic deployment
└── README.md               # This file
```

## CI/CD

The GitHub Actions workflow in `.github/workflows/render-book.yml` automatically builds and deploys the book to GitHub Pages on every push to `main`.

## Audiobook Generation

This project includes scripts to generate audiobooks using ElevenLabs TTS.

### Setup

1. **Install Python dependencies**:
   ```bash
   pip install -e .
   pip install -r audiobook/requirements.txt
   ```

2. **Configure ElevenLabs API**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ELEVENLABS_API_KEY
   ```

3. **Generate audiobook**:
   ```bash
   generate-audiobook
   ```

Output will be in `audiobook_output/` (excluded from git).

For more details, see [`audiobook/README.md`](audiobook/README.md).

## Learn More

- [Quarto Books Documentation](https://quarto.org/docs/books/)
- [Quarto Publishing Guide](https://quarto.org/docs/publishing/)
