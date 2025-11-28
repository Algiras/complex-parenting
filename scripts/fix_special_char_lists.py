#!/usr/bin/env python3
"""Fix special character list formatting in QMD files.

Move Unicode symbols (✓, ✗, ☐) inside bold text for proper list rendering.
"""

import re
from pathlib import Path

def fix_file(filepath):
    """Fix special character lists in a single file."""
    path = Path(filepath)
    if not path.exists():
        return 0, f"File not found: {filepath}"
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern: -<space>SYMBOL<space>**TEXT**: Description
    # Replace with: - **SYMBOL TEXT**: Description
    # Don't require colon to immediately follow ** - there may be a space
    pattern = re.compile(r'^- ([✓✗☐]) \*\*([^*]+)\*\*', re.MULTILINE)
    content = pattern.sub(r'- **\1 \2**', content)
    
    if content == original_content:
        return 0, None
    
    # Count changes
    changes = len(pattern.findall(original_content))
    
    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes, None

files_to_fix = [
    'chapters/01c-sarahs-story-bipolar.qmd',
    'chapters/01d-marcus-story-adhd.qmd',
    'chapters/01e-emmas-story-autism.qmd',
    'chapters/07-sleep-is-medicine.qmd',
    'chapters/08-the-family-mobile.qmd',
    'chapters/09-strategies-for-success.qmd',
    'chapters/14-appendix-c-iep-samples.qmd',
]

total_fixed = 0
print("Fixing special character lists...\n")

for filepath in files_to_fix:
    changes, error = fix_file(filepath)
    if error:
        print(f"⚠️  {error}")
    elif changes > 0:
        print(f"✓ Fixed {changes} instances in {Path(filepath).name}")
        total_fixed += changes
    else:
        print(f"  No issues in {Path(filepath).name}")

print(f"\n✅ Total: Fixed {total_fixed} list items")
