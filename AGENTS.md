# AI Agent Writing Guidelines

This document provides formatting and style rules for AI agents writing content for this book project.

## Markdown Formatting Rules

### 1. Bullet Points - CRITICAL

**❌ WRONG - Never use asterisk with multiple spaces:**
```markdown
*   **Label:** Description
```

**✅ CORRECT - Always use hyphen with single space:**
```markdown
- **Label:** Description
```

**Why:** The `*` character conflicts with Markdown bold syntax (`**`), causing rendering issues in Quarto.

---

### 2. Special Characters in Lists

When using Unicode symbols (✓, ✗, ☐) in lists, **always ensure blank lines before and after the list block**.

**❌ WRONG:**
```markdown
Notice what Sarah does NOT have:
- ✗ **Sensory Sensitivities:** Not bothered by fluorescent lights
- ✗ **Social Communication Deficits:** Socially fluent
```

**✅ CORRECT:**
```markdown
Notice what Sarah does NOT have:

- ✗ **Sensory Sensitivities:** Not bothered by fluorescent lights
- ✗ **Social Communication Deficits:** Socially fluent
```

**Why:** Without blank lines, Quarto may render the list as a continuous paragraph, breaking the list formatting.

**VERIFIED SOLUTION:** For lists with special Unicode characters (✓, ✗, ☐) to render correctly, the symbol must be **inside** the bold text, not outside:

**❌ WRONG (renders as paragraph):**
```markdown
Notice what Sarah does NOT have:

- ✗ **Sensory Sensitivities:** Description
- ✓ **Social Issues:** Description
```

**✅ CORRECT (renders as proper list):**
```markdown
Notice what Sarah does NOT have:

- **✗ Sensory Sensitivities:** Description
- **✓ Social Issues:** Description
```

**Why:** Quarto's Markdown parser struggles when Unicode characters appear immediately after the list marker and before bold markup. Moving the symbol inside the bold ensures proper list parsing.

**To Fix Existing Content:**
Run `python scripts/fix_special_char_lists.py` to automatically convert all instances.

---

### 3. Nested Lists

**Use consistent indentation (4 spaces or 2 spaces, not mixed):**

**✅ CORRECT (4 spaces):**
```markdown
- Parent item
    - Child item
    - Another child
```

**✅ ALSO CORRECT (2 spaces):**
```markdown
- Parent item
  - Child item
  - Another child
```

**❌ WRONG (mixed indentation):**
```markdown
- Parent item
   - Child item (3 spaces)  
      - Another child (6 spaces)
```

---

### 4. Checkbox Lists

For task/checkbox lists, use `☐` (U+2610 BALLOT BOX) not other checkbox symbols.

**✅ CORRECT:**
```markdown
☐ **Task name:** Description
```

**Note:** These are visual-only in Markdown. For interactive checklists, use GitHub-style syntax:
```markdown
- [ ] Task name
- [x] Completed task
```

---

### 5. Bold in List Items

**Always put spaces around the inline bold elements:**

**✅ CORRECT:**
```markdown
- **This is bold:** Regular text follows
```

**❌ WRONG:**
```markdown
- **This is bold:**Regular text immediately follows (no space)
```

---

## Common Patterns to Avoid

### Pattern 1: Asterisk Bullets (Most Common Error)
```markdown
*   Text here  ❌
```
**Fix:** Replace with `- Text here`

### Pattern 2: Missing Blank Lines Around Lists
```markdown
Intro sentence:
- List item ❌
```
**Fix:** Add blank line after intro sentence

### Pattern 3: Inconsistent Indentation
```markdown
-  Item (2 spaces) ❌
```
**Fix:** Use exactly 1 space after `-`

---

## Quick Regex Fixes

### Fix Asterisk Bullets:
- **Find:** `^\*   ` (regex: asterisk + 3 spaces at line start)
- **Replace:** `- ` (hyphen + 1 space)

### Find lists without blank lines (manual review):
- **Find:** `:\n-` (colon followed immediately by list)
- **Action:** Add blank line between

---

## Validation Checklist

Before committing content, verify:

- [ ] No `*   ` patterns (all bullets use `-`)
- [ ] Blank lines before/after all list blocks
- [ ] Consistent indentation (all 4 spaces OR all 2 spaces)
- [ ] Special characters (✓, ✗, ☐) have proper spacing
- [ ] Bold elements have spaces: `**Text:** Description`

---

## Testing Process

After making bulk edits:
1. Run `quarto render --to html`
2. Open `_output/index.html` in browser
3. Visually inspect chapters with lists
4. Look for:
   - Lists rendering as continuous paragraphs
   - Missing bullet points
   - Asterisks appearing as literal text

---

*Last updated: 2025-11-26*
*See also: FORMATTING_NOTES.md for project-specific formatting issues*
