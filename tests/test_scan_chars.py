"""Tests for the scan_chars script."""

import tempfile
from pathlib import Path

from scripts.scan_chars import check_file


class TestScanChars:
    """Test cases for character scanning."""

    def test_valid_utf8(self):
        """Test that valid UTF-8 text passes without errors."""
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".qmd", delete=False
        ) as f:
            f.write("# Valid UTF-8 Content\n\n")
            f.write("This is normal text with some Unicode: café, naïve, Москва\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) == 0

    def test_replacement_character(self):
        """Test detection of Unicode replacement character."""
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".qmd", delete=False
        ) as f:
            f.write("Text with invalid char: \ufffd here\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) > 0
        assert "Invalid char" in errors[0]

    def test_null_character(self):
        """Test detection of null bytes."""
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".qmd", delete=False
        ) as f:
            f.write("Text with null: \x00 here\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) > 0
        assert "Invalid char" in errors[0]

    def test_tabs_allowed(self):
        """Test that tab characters are allowed."""
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".qmd", delete=False
        ) as f:
            f.write("Text with\ttab character\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) == 0

    def test_arabic_text(self):
        """Test that Arabic/RTL Unicode is valid."""
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".qmd", delete=False
        ) as f:
            f.write("Arabic text: السلام عليكم\n")
            f.flush()

            errors = check_file(f.name)
            Path(f.name).unlink()

        assert len(errors) == 0
