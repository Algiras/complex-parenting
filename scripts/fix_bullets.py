#!/usr/bin/env python3
"""Fix bullet point formatting in QMD files."""

import re
from pathlib import Path

# Pattern: asterisk followed by 3 spaces at start of line
PATTERN = re.compile(r'^(\*   )', re.MULTILINE)
REPLACEMENT = '- '

# Files to fix
files_to_fix = [
    'chapters/02-bipolar-teen-brain.qmd',
    'chapters/06-managing-the-rage.qmd',
    'chapters/07-sleep-is-medicine.qmd',
    'chapters/08-the-family-mobile.qmd',
    'chapters/15-appendix-d-adults.qmd',
]

# Also check other chapter files
chapter_dir = Path('chapters')
all_qmd_files = list(chapter_dir.glob('*.qmd'))

fixed_count = 0

for filepath in all_qmd_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count matches before replacing
    matches = PATTERN.findall(content)
    
    if matches:
        # Replace pattern
        new_content = PATTERN.sub(REPLACEMENT, content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Fixed {len(matches)} instances in {filepath.name}")
        fixed_count += len(matches)

print(f"\n✅ Total: Fixed {fixed_count} bullet points across {len([f for f in all_qmd_files if PATTERN.search(open(f).read())])} files")
