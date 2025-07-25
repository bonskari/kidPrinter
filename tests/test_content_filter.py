import unittest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from content_filter import ContentFilter


class TestContentFilter(unittest.TestCase):
    """Test cases for the ContentFilter class."""
    
    def setUp(self):
        self.filter = ContentFilter()
    
    def test_safe_content_allowed(self):
        """Test that safe content is allowed."""
        safe_texts = [
            "tulosta kuva kissasta",
            "haluan värityskuvan",
            "tee kuva perhosesta",
            "kirjoita tarina"
        ]
        
        for text in safe_texts:
            with self.subTest(text=text):
                self.assertTrue(self.filter.is_safe(text))
    
    def test_inappropriate_content_blocked(self):
        """Test that inappropriate content is blocked."""
        # Note: Using mild examples for testing
        inappropriate_texts = [
            "perkele",
            "helvetti tämä",
        ]
        
        for text in inappropriate_texts:
            with self.subTest(text=text):
                self.assertFalse(self.filter.is_safe(text))
    
    def test_empty_content_blocked(self):
        """Test that empty content is blocked."""
        self.assertFalse(self.filter.is_safe(""))
        self.assertFalse(self.filter.is_safe(None))
    
    def test_long_content_blocked(self):
        """Test that excessively long content is blocked."""
        long_text = "a" * 250  # Longer than 200 character limit
        self.assertFalse(self.filter.is_safe(long_text))
    
    def test_spam_patterns_blocked(self):
        """Test that spam patterns are blocked."""
        spam_text = "aaaaaa tulosta"  # Repeated characters
        self.assertFalse(self.filter.is_safe(spam_text))
    
    def test_educational_content_detection(self):
        """Test educational content detection."""
        educational_texts = [
            "oppi laskemaan",
            "matematiikka tehtävä",
            "luonto kuva"
        ]
        
        for text in educational_texts:
            with self.subTest(text=text):
                self.assertTrue(self.filter.is_educational_content(text))


if __name__ == "__main__":
    unittest.main()
