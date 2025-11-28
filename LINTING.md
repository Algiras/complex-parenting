# Markdown Linting for Bookie

This document describes linting strategies to catch formatting issues in QMD files before rendering.

## Available Linters

### 1. markdownlint (Recommended)

**markdownlint** is a widely-used Markdown linter that can catch many formatting issues.

**Installation:**
```bash
npm install -g markdownlint-cli
```

**Usage:**
```bash
markdownlint chapters/*.qmd
```

**Configuration:** Create `.markdownlint.json`:
```json
{
  "MD001": false,
  "MD013": false,
  "MD024": false,
  "MD033": true,
  "MD041": false
}
```

### 2. Custom Lint Script for This Project

Created `scripts/lint_qmd.py` to catch project-specific issues:

- Asterisk bullets (`*   `) instead of hyphens
- Unicode symbols outside bold text (`- ✗ **Text:**`)
- Missing blank lines before/after lists
- Inconsistent indentation

**Usage:**
```bash
python scripts/lint_qmd.py
```

## Integration with Quarto

Add to `.github/workflows/lint.yml` (if using GitHub Actions):
```yaml
name: Lint QMD Files
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run custom linter
        run: python scripts/lint_qmd.py
```

## Pre-commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python scripts/lint_qmd.py
if [ $? -ne 0 ]; then
    echo "Linting failed. Fix issues or use 'git commit --no-verify'"
    exit 1
fi
```

---

*See FORMATTING_NOTES.md for discovered issues and AGENTS.md for writing guidelines*
