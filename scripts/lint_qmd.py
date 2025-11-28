#!/usr/bin/env python3
"""
QMD Markdown linter for Bookie project.

Checks for common formatting issues that cause rendering problems.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

class LintError:
    def __init__(self, filepath: str, line_num: int, message: str, severity: str = "error"):
        self.filepath = filepath
        self.line_num = line_num
        self.message = message
        self.severity = severity
    
    def __str__(self):
        icon = "❌" if self.severity == "error" else "⚠️ "
        return f"{icon} {self.filepath}:{self.line_num}: {self.message}"

def lint_file(filepath: Path, autofix: bool = False) -> List[LintError]:
    """Lint a single QMD file."""
    errors = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Check 1: Asterisk bullets with multiple spaces
        if re.match(r'^\*   ', line):
            errors.append(LintError(
                str(filepath), line_num,
                "Use hyphen bullets (- ) instead of asterisk with spaces (*   )",
                "error"
            ))
        
        # Check 2: Unicode symbols outside bold text
        if re.match(r'^- ([✓✗☐]) \*\*', line):
            errors.append(LintError(
                str(filepath), line_num,
                f"Move Unicode symbol inside bold: '- **{line[2]} Text:**' not '- {line[2]} **Text:**'",
                "error"
            ))
        
        # Check 3: List after text without blank line
        needs_blank_line = False
        if i > 0 and line.startswith('- '):
            prev_line = lines[i-1].strip()
            if prev_line and not prev_line.startswith('#') and prev_line.endswith(':'):
                # Check if there isn't already a blank line
                if i > 1 and lines[i-1].strip():
                    needs_blank_line = True
                    errors.append(LintError(
                        str(filepath), line_num-1,
                        "Add blank line before list",
                        "warning"
                    ))
        
        # Check 4: Checkbox without dash marker
        needs_dash = False
        if line.startswith('☐ '):
            needs_dash = True
            errors.append(LintError(
                str(filepath), line_num,
                "Checkbox lists must start with dash: '- ☐' not '☐'",
                "error"
            ))
        
        # Autofix: Insert blank line before list
        if autofix and needs_blank_line:
            new_lines.append('\n')  # Add blank line
            modified = True
        
        # Autofix: Add dash before checkbox
        if autofix and needs_dash:
            new_lines.append('- ' + line)
            modified = True
        elif not needs_dash:
            new_lines.append(line)
    
    # Write back if modified
    if autofix and modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return errors

def main():
    """Lint all QMD files in chapters directory."""
    import sys
    
    # Check for --fix flag
    autofix = '--fix' in sys.argv
    
    chapter_dir = Path('chapters')
    if not chapter_dir.exists():
        print("Error: 'chapters' directory not found")
        return 1
    
    all_errors = []
    qmd_files = list(chapter_dir.glob('*.qmd'))
    
    if autofix:
        print(f"Fixing {len(qmd_files)} QMD files...\n")
    else:
        print(f"Linting {len(qmd_files)} QMD files...\n")
    
    for filepath in qmd_files:
        errors = lint_file(filepath, autofix=autofix)
        all_errors.extend(errors)
    
    if autofix:
        warnings = [e for e in all_errors if e.severity == "warning"]
        errors_only = [e for e in all_errors if e.severity == "error"]
        
        print(f"✅ Fixed {len(warnings)} warnings automatically")
        
        if errors_only:
            print(f"\n⚠️  {len(errors_only)} errors still remain (require manual fix):\n")
            for error in errors_only:
                print(error)
            return 1
        else:
            print("✅ No errors remaining!")
            return 0
    else:
        if all_errors:
            print(f"Found {len(all_errors)} issues:\n")
            for error in all_errors:
                print(error)
            print(f"\n❌ Linting failed with {len(all_errors)} issues")
            print(f"\nRun with --fix to automatically fix warnings:")
            print(f"  python scripts/lint_qmd.py --fix")
            return 1
        else:
            print("✅ All files passed linting!")
            return 0

if __name__ == '__main__':
    sys.exit(main())
