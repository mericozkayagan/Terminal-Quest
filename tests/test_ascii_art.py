import os
import unittest
from src.utils.ascii_art import display_ascii_art, load_ascii_art


class TestAsciiArt(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_filename = "test_art.txt"
        self.test_content = "Test ASCII Art"

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_load_ascii_art(self):
        """Test loading ASCII art from a file."""
        # Create test file
        with open(self.test_filename, "w") as file:
            file.write(self.test_content)

    def test_display_ascii_art(self):
        ascii_art = "Test ASCII Art"
        from unittest.mock import patch

        with patch("builtins.print") as mock_print:
            display_ascii_art(ascii_art)
            mock_print.assert_called_once_with(ascii_art)

    def test_load_ascii_art_file_not_found(self):
        """Test handling of non-existent files."""
        with self.assertRaises(FileNotFoundError):
            load_ascii_art("nonexistent_file.txt")


if __name__ == "__main__":
    unittest.main()
