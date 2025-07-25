"""
Content Filter Module

Ensures all content is appropriate for children.
"""

import logging
import re
from typing import List, Set


class ContentFilter:
    """Filters content to ensure it's appropriate for children."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Finnish inappropriate words/phrases to filter
        self.blocked_words: Set[str] = {
            # Add Finnish inappropriate words here
            "perkele", "helvetti", "saatana", "vittu", "jumalauta"
        }
        
        # Kid-friendly keywords that are always allowed
        self.safe_words: Set[str] = {
            "kissa", "koira", "lintu", "kukka", "aurinko", "kuu", "tähti",
            "perhe", "ystävä", "leikki", "kirja", "väri", "numero",
            "eläin", "kala", "perhonen", "sieni", "puu", "lehti"
        }
        
        self.logger.info("Content filter initialized")
    
    def is_safe(self, text: str) -> bool:
        """
        Check if text content is safe for children.
        
        Args:
            text: Text to check
            
        Returns:
            True if content is safe for children
        """
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Check for blocked words
        for word in self.blocked_words:
            if word in text_lower:
                self.logger.warning(f"Blocked inappropriate content: {word}")
                return False
        
        # Check for excessive length (prevent spam)
        if len(text) > 200:
            self.logger.warning("Content too long, potentially spam")
            return False
        
        # Check for repeated characters (prevent spam patterns)
        if re.search(r'(.)\1{5,}', text):
            self.logger.warning("Detected repeated character pattern")
            return False
        
        self.logger.debug(f"Content approved: {text[:50]}...")
        return True
    
    def suggest_alternatives(self, blocked_text: str) -> List[str]:
        """
        Suggest kid-friendly alternatives for blocked content.
        
        Args:
            blocked_text: The blocked text
            
        Returns:
            List of suggested alternatives
        """
        suggestions = [
            "Mitä jos tulostaisimme kuvan kissasta?",
            "Haluaisitko tulostaa värityskuvan?",
            "Voisimme tulostaa hauskan tarinan!",
            "Mitä jos tehdään kuva perhosesta?"
        ]
        
        return suggestions
    
    def add_safe_word(self, word: str) -> None:
        """Add a word to the safe words list."""
        self.safe_words.add(word.lower())
        self.logger.info(f"Added safe word: {word}")
    
    def add_blocked_word(self, word: str) -> None:
        """Add a word to the blocked words list."""
        self.blocked_words.add(word.lower())
        self.logger.info(f"Added blocked word: {word}")
    
    def is_educational_content(self, text: str) -> bool:
        """Check if content has educational value."""
        educational_keywords = {
            "oppi", "laske", "kirjain", "numero", "väri", "muoto",
            "historia", "tiede", "luonto", "matematiikka", "lukeminen"
        }
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in educational_keywords)
