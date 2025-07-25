import unittest
import sys
from pathlib import Path
from datetime import date
import tempfile
import shutil

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from daily_limits import DailyLimitManager


class TestDailyLimitManager(unittest.TestCase):
    """Test cases for the DailyLimitManager class."""
    
    def setUp(self):
        # Create temporary directory for test config
        self.temp_dir = tempfile.mkdtemp()
        self.limit_manager = DailyLimitManager(max_daily_prints=5, config_dir=self.temp_dir)
    
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_initial_state(self):
        """Test initial state of limit manager."""
        self.assertEqual(self.limit_manager.get_today_count(), 0)
        self.assertTrue(self.limit_manager.can_print())
        self.assertEqual(self.limit_manager.get_remaining_prints(), 5)
    
    def test_record_print(self):
        """Test recording print operations."""
        # Record first print
        self.limit_manager.record_print()
        self.assertEqual(self.limit_manager.get_today_count(), 1)
        self.assertEqual(self.limit_manager.get_remaining_prints(), 4)
        
        # Record more prints
        for i in range(3):
            self.limit_manager.record_print()
        
        self.assertEqual(self.limit_manager.get_today_count(), 4)
        self.assertEqual(self.limit_manager.get_remaining_prints(), 1)
        self.assertTrue(self.limit_manager.can_print())
    
    def test_daily_limit_reached(self):
        """Test behavior when daily limit is reached."""
        # Use up all prints
        for i in range(5):
            self.assertTrue(self.limit_manager.can_print())
            self.limit_manager.record_print()
        
        # Should not be able to print more
        self.assertFalse(self.limit_manager.can_print())
        self.assertEqual(self.limit_manager.get_remaining_prints(), 0)
    
    def test_limit_update(self):
        """Test updating daily limit."""
        self.limit_manager.set_daily_limit(10)
        self.assertEqual(self.limit_manager.max_daily_prints, 10)
        self.assertEqual(self.limit_manager.get_remaining_prints(), 10)
    
    def test_usage_stats(self):
        """Test usage statistics."""
        self.limit_manager.record_print()
        stats = self.limit_manager.get_usage_stats()
        
        self.assertEqual(stats["today_count"], 1)
        self.assertEqual(stats["daily_limit"], 5)
        self.assertEqual(stats["remaining"], 4)
        self.assertTrue(stats["can_print"])


if __name__ == "__main__":
    unittest.main()
