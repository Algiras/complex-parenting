# Linting and Quality Checks

This project uses automated linting to ensure consistent markdown formatting.

## Markdown Linting

We use `markdownlint-cli` to enforce proper list formatting, heading structure, and markdown best practices.

### Run Locally

```bash
# Install markdownlint
npm install -g markdownlint-cli

# Run linter
./tools/lint-markdown.sh

# Or manually
markdownlint books/*.qmd --config .markdownlint.json
```

### Key Rules

- **MD031/MD032**: Fenced code blocks and lists must be surrounded by blank lines
- **MD001**: Heading levels increment by one
- **MD022**: Headings should be surrounded by blank lines
- **MD030**: Spaces after list markers

### CI/CD Integration

The linting runs automatically on every push via GitHub Actions. Warnings are shown but don't block the build.

## Configuration

See `.markdownlint.json` for the complete rule configuration.
