#!/usr/bin/env python3
"""Fix checkbox lists that are missing the - bullet marker."""

from pathlib import Path

files_to_fix = [
    'chapters/07-sleep-is-medicine.qmd',
    'chapters/08-the-family-mobile.qmd',
    'chapters/09-strategies-for-success.qmd',
]

total_fixed = 0

print("Fixing checkbox lists...\n")

for filepath in files_to_fix:
    path = Path(filepath)
    if not path.exists():
        print(f"⚠️  File not found: {filepath}")
        continue

    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changes = 0

    for line in lines:
        # Check if line starts with ☐ (no dash)
        if line.startswith('☐ '):
            # Add dash at beginning
            new_line = '- ' + line
            new_lines.append(new_line)
            changes += 1
        else:
            new_lines.append(line)

    if changes > 0:
        # Write back
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"✓ Fixed {changes} checkbox items in {path.name}")
        total_fixed += changes
    else:
        print(f"  No issues in {path.name}")

print(f"\n✅ Total: Fixed {total_fixed} checkbox items")
