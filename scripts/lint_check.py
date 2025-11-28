import glob
import re
import sys


def check_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    errors = []
    for i, line in enumerate(lines):
        # Check for list items that might be run-on text
        # Pattern: Text followed immediately by * or - or 1. without newline
        # This is hard to detect with regex on a single line if it's already malformed as "Text. * Item"

        # Check for " * " or " - " or " 1. " in the middle of a line (potential run-on list)
        # Only flag if preceded by non-whitespace (e.g. "Text - Item")
        # Exclude bold/italic markers (*text* or **text**)
        if re.search(r"\S\s+[\*\-]\s+", line) or re.search(r"\S\s+\d+\.\s+", line):
            # Exclude common false positives like bold text with spaces or math or hyphens in text
            # We only care if it looks like a bullet point: " - " or " * "
            # But " - " is common in text. " * " is common in italics.
            # This is hard. Let's look for "Text. * Item" or "Text. - Item" (punctuation preceding)
            if re.search(r"[\.\:\!]\s+[\*\-]\s+", line) or re.search(r"[\.\:\!]\s+\d+\.\s+", line):
                errors.append(f"Line {i + 1}: Potential run-on list item: {line.strip()[:50]}...")

        # Check for list markers without space (e.g. "*Item")
        # Ignore bold text (**), headers (###), horizontal rules (---), and blockquotes (>)
        # Also ignore full-line italics (*Text*)
        if (
            re.match(r"^[\*\-][^\s]", line)
            and not line.startswith("**")
            and not line.startswith("---")
            and not line.startswith(">")
            and not line.startswith("###")
            and not (line.strip().startswith("*") and line.strip().endswith("*"))
        ):
            errors.append(f"Line {i + 1}: List marker missing space: {line.strip()[:50]}...")

    return errors


def main():
    files = glob.glob("*.qmd") + glob.glob("chapters/*.qmd")
    all_errors = {}

    print(f"Scanning {len(files)} files...")

    for file in files:
        errors = check_file(file)
        if errors:
            all_errors[file] = errors

    if all_errors:
        print("\nFound formatting issues:")
        for file, errs in all_errors.items():
            print(f"\n{file}:")
            for err in errs:
                print(f"  - {err}")
        sys.exit(1)
    else:
        print("\nNo obvious formatting issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
