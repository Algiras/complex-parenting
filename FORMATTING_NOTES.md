# Formatting and Style Issues

## Markdown Bullet Point Formatting

### Issue
Throughout the book, many bullet lists use the pattern `*   **Label:**` which can cause inconsistent rendering in Quarto/Markdown:

```markdown
*   **Label:** Description
```

### Problem
- The `*` character is used both for the bullet point AND for bold formatting
- Multiple spaces after `*` can cause rendering issues
- This pattern affects ~200+ lines across chapters: 02, 06, 07, 08, 15

### Solution
Use the hyphen `-` for bullet points instead:

```markdown
- **Label:** Description
```

### Files Affected
- `chapters/02-bipolar-teen-brain.qmd`
- `chapters/06-managing-the-rage.qmd`
- `chapters/07-sleep-is-medicine.qmd`
- `chapters/08-the-family-mobile.qmd`
- `chapters/15-appendix-d-adults.qmd`
- And potentially others

### Future Action
Run a find-and-replace across all `.qmd` files:
- Find: `^\*   ` (regex: asterisk + 3 spaces at line start)
- Replace: `- ` (hyphen + 1 space)

---

*Last updated: 2025-11-26*
