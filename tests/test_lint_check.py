"""Tests for the lint_check script."""

import tempfile
from pathlib import Path

from scripts.lint_check import check_file


class TestLintCheck:
    """Test cases for markdown lint checking."""

    def test_valid_markdown(self):
        """Test that valid markdown passes without errors."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".qmd", delete=False) as f:
            f.write("# Header\n\n")
            f.write("- Valid list item\n")
            f.write("- Another item\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) == 0

    def test_missing_space_after_marker(self):
        """Test detection of list markers without spaces."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".qmd", delete=False) as f:
            f.write("# Header\n\n")
            f.write("*Missing space\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) > 0
        assert "List marker missing space" in errors[0]

    def test_run_on_list_item(self):
        """Test detection of run-on list items."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".qmd", delete=False) as f:
            f.write("# Header\n\n")
            f.write("Some text. * List item on same line\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) > 0
        assert "run-on list item" in errors[0].lower()

    def test_bold_text_not_flagged(self):
        """Test that bold text is not incorrectly flagged."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".qmd", delete=False) as f:
            f.write("# Header\n\n")
            f.write("This is **bold text** in a paragraph.\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) == 0
