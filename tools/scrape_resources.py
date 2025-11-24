#!/usr/bin/env python3
"""
Resource Scraper for The Shadow of Extremism
Downloads and archives web resources cited in the book for offline review.
"""

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

# Configuration
REFERENCES_DIR = Path("references/downloaded")
REFERENCES_DIR.mkdir(parents=True, exist_ok=True)


def extract_urls_from_markdown(file_path):
    """Extract all URLs from a markdown file."""
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Match markdown links [text](url) and plain URLs
    url_pattern = r'https?://[^\s\)>\]"]+'
    urls = re.findall(url_pattern, content)
    return list(set(urls))  # Remove duplicates


def extract_academic_sources(file_path):
    """Extract academic sources that might have online versions."""
    sources = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Extract book titles and authors for potential lookup
    # Pattern: Author. *Title*. Publisher, Year.
    pattern = r"([A-Z][a-z]+,\s+[A-Z][a-z]+(?:\s+[A-Z]\.)?)\.\s+\*([^*]+)\*"
    matches = re.findall(pattern, content)

    for author, title in matches:
        sources.append(
            {
                "author": author.strip(),
                "title": title.strip(),
                "search_url": f"https://www.google.com/search?q={author}+{title}+pdf",
            }
        )

    return sources


def sanitize_filename(url):
    """Create a safe filename from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/").replace("/", "_")

    # Limit filename length
    filename = f"{domain}_{path or 'index'}"
    if len(filename) > 200:
        filename = filename[:200]

    return f"{filename}.html"


def download_url(url, output_dir):
    """Download a URL and save it locally."""
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (Research purposes - The Shadow of Extremism book)"
            },
            allow_redirects=True,
        )
        response.raise_for_status()

        filename = sanitize_filename(url)
        output_path = output_dir / filename

        with open(output_path, "wb") as f:
            f.write(response.content)

        # Save metadata
        meta_path = output_dir / f"{filename}.meta.txt"
        with open(meta_path, "w") as f:
            f.write(f"URL: {url}\n")
            f.write(f"Downloaded: {datetime.now().isoformat()}\n")
            f.write(f"Status: {response.status_code}\n")
            f.write(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}\n")
            f.write(f"Final URL: {response.url}\n")  # After redirects

        print(f"✓ Downloaded: {url}")
        return True
    except requests.exceptions.Timeout:
        print(f"✗ Timeout: {url}")
        return False
    except requests.exceptions.TooManyRedirects:
        print(f"✗ Too many redirects: {url}")
        return False
    except Exception as e:
        print(f"✗ Failed: {url} - {str(e)}")
        return False


def main():
    """Main function to scrape all references."""
    print("=" * 60)
    print("The Shadow of Extremism - Reference Downloader")
    print("=" * 60)
    print()

    # Find all markdown files in the project
    markdown_files = list(Path("books").glob("*.qmd")) + list(Path("references").glob("**/*.md"))

    all_urls = []
    for file_path in markdown_files:
        urls = extract_urls_from_markdown(file_path)
        all_urls.extend(urls)

    all_urls = list(set(all_urls))  # Remove duplicates

    print(f"Found {len(all_urls)} unique URLs to download\n")
    print("Downloading web resources...")
    print("-" * 60)

    # Download each URL
    success = 0
    failed = 0
    for i, url in enumerate(all_urls, 1):
        print(f"[{i}/{len(all_urls)}] ", end="")
        if download_url(url, REFERENCES_DIR):
            success += 1
        else:
            failed += 1

    print()
    print("=" * 60)
    print(f"✓ Downloaded: {success}/{len(all_urls)} resources")
    print(f"✗ Failed: {failed}/{len(all_urls)} resources")
    print(f"Saved to: {REFERENCES_DIR.absolute()}")
    print("=" * 60)

    # Extract academic sources for reference
    print("\nAcademic sources found in bibliography:")
    print("-" * 60)
    bib_file = Path("books/21-bibliography.qmd")
    if bib_file.exists():
        sources = extract_academic_sources(bib_file)
        print(f"Found {len(sources)} academic sources")
        print("Note: Manual lookup required for books/papers without direct URLs")

    print("\n✓ Reference download complete!")


if __name__ == "__main__":
    main()
