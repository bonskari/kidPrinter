"""
Daily Print Limits Module

Manages daily printing limits to prevent excessive usage.
"""

import logging
import json
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any


class DailyLimitManager:
    """Manages daily printing limits for children."""
    
    def __init__(self, max_daily_prints: int = 10, config_dir: str = "config"):
        self.logger = logging.getLogger(__name__)
        self.max_daily_prints = max_daily_prints
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.usage_file = self.config_dir / "daily_usage.json"
        
        self.usage_data = self._load_usage_data()
        self.logger.info(f"Daily limit manager initialized (max: {max_daily_prints} prints/day)")
    
    def _load_usage_data(self) -> Dict[str, Any]:
        """Load usage data from file."""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.logger.debug("Loaded existing usage data")
                return data
            except Exception as e:
                self.logger.error(f"Error loading usage data: {e}")
        
        # Return empty data structure
        return {"daily_counts": {}, "last_reset": str(date.today())}
    
    def _save_usage_data(self) -> None:
        """Save usage data to file."""
        try:
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)
            self.logger.debug("Saved usage data")
        except Exception as e:
            self.logger.error(f"Error saving usage data: {e}")
    
    def _get_today_key(self) -> str:
        """Get today's date as a string key."""
        return str(date.today())
    
    def _reset_if_new_day(self) -> None:
        """Reset counters if it's a new day."""
        today = self._get_today_key()
        last_reset = self.usage_data.get("last_reset", "")
        
        if today != last_reset:
            self.logger.info(f"New day detected, resetting counters (was: {last_reset}, now: {today})")
            self.usage_data["daily_counts"] = {}
            self.usage_data["last_reset"] = today
            self._save_usage_data()
    
    def get_today_count(self) -> int:
        """Get today's print count."""
        self._reset_if_new_day()
        today = self._get_today_key()
        return self.usage_data["daily_counts"].get(today, 0)
    
    def can_print(self) -> bool:
        """
        Check if printing is allowed based on daily limits.
        
        Returns:
            True if printing is allowed
        """
        current_count = self.get_today_count()
        can_print = current_count < self.max_daily_prints
        
        self.logger.debug(f"Print check: {current_count}/{self.max_daily_prints} - {'ALLOWED' if can_print else 'BLOCKED'}")
        return can_print
    
    def record_print(self) -> None:
        """Record a print operation."""
        self._reset_if_new_day()
        today = self._get_today_key()
        
        current_count = self.usage_data["daily_counts"].get(today, 0)
        self.usage_data["daily_counts"][today] = current_count + 1
        
        self._save_usage_data()
        
        new_count = self.usage_data["daily_counts"][today]
        self.logger.info(f"Print recorded. Today's count: {new_count}/{self.max_daily_prints}")
    
    def get_remaining_prints(self) -> int:
        """Get number of remaining prints for today."""
        current_count = self.get_today_count()
        remaining = max(0, self.max_daily_prints - current_count)
        return remaining
    
    def set_daily_limit(self, new_limit: int) -> None:
        """Update the daily print limit."""
        if new_limit <= 0:
            self.logger.warning("Daily limit must be positive")
            return
        
        old_limit = self.max_daily_prints
        self.max_daily_prints = new_limit
        self.logger.info(f"Daily limit updated: {old_limit} -> {new_limit}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "today_count": self.get_today_count(),
            "daily_limit": self.max_daily_prints,
            "remaining": self.get_remaining_prints(),
            "can_print": self.can_print(),
            "last_reset": self.usage_data.get("last_reset", ""),
            "total_days": len(self.usage_data.get("daily_counts", {}))
        }
