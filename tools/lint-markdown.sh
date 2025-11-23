#!/bin/bash
# Markdown linting script for book content

echo "Running markdownlint on book chapters..."

# Install markdownlint-cli if not present
if ! command -v markdownlint &> /dev/null; then
    echo "Installing markdownlint-cli..."
    npm install -g markdownlint-cli
fi

# Run linter
markdownlint books/*.qmd --config .markdownlint.json

if [ $? -eq 0 ]; then
    echo "✅ All markdown files pass linting"
    exit 0
else
    echo "❌ Markdown linting failed - please fix the issues above"
    exit 1
fi
