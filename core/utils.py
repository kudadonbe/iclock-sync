"""
utils.py - Utility functions for the iClock-Sync project

Provides common utilities required across different modules, including timestamp formatting,
document ID generation, and caching mechanisms to handle previously uploaded logs.

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

import glob
import json
import hashlib
import os
import logging
from datetime import datetime


# ----------------------------------------
# Smart Timing Helper Class
# ----------------------------------------

class SmartTiming:
    """Manages smart timing intervals with graduated rest levels: Active → Rest → Nap → Sleep → Dream."""
    
    def __init__(self, base_interval=5):
        """
        Initialize smart timing with graduated rest levels.
        
        Args:
            base_interval: Active sync interval (seconds)
        """
        self.base_interval = base_interval
        self.current_interval = base_interval
        self.no_activity_count = 0
        
        # Rest level definitions
        self.rest_levels = {
            'active': {'max_interval': 5, 'cycles': 0},           # Always 5s
            'rest': {'max_interval': 300, 'cycles': 1},           # 5 minutes max
            'nap': {'max_interval': 900, 'cycles': 3},            # 15 minutes max  
            'sleep': {'max_interval': 3600, 'cycles': 6},         # 1 hour max
            'dream': {'max_interval': 10800, 'cycles': 10}        # 3 hours max
        }
        
    def get_time_period(self):
        """Determine current time period based on hour of day."""
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 16:
            return 'active_hours'      # 06:00-16:00: Can only Rest
        elif 16 <= current_hour < 18:
            return 'nap_hours'         # 16:00-18:00: Can Nap
        elif 18 <= current_hour < 23:
            return 'sleep_hours'       # 18:00-23:00: Can Sleep
        else:
            return 'dream_hours'       # 23:00-06:00: Can Dream
    
    def get_max_rest_level(self, time_period):
        """Get maximum allowed rest level for current time period."""
        max_levels = {
            'active_hours': 'rest',    # Max: Rest (5min)
            'nap_hours': 'nap',        # Max: Nap (15min)  
            'sleep_hours': 'sleep',    # Max: Sleep (1hr)
            'dream_hours': 'dream'     # Max: Dream (3hr)
        }
        return max_levels[time_period]
    
    def get_current_rest_level(self):
        """Determine current rest level based on activity cycles."""
        if self.no_activity_count == 0:
            return 'active'
        elif self.no_activity_count < 3:
            return 'rest'
        elif self.no_activity_count < 6:
            return 'nap'
        elif self.no_activity_count < 10:
            return 'sleep'
        else:
            return 'dream'
    
    def get_next_interval(self, new_records_count):
        """Calculate next sync interval with smart rest progression."""
        current_hour = datetime.now().hour
        
        # Sharp wake-up at 06:00
        if current_hour == 6 and self.current_interval > self.base_interval:
            self.no_activity_count = 0
            self.current_interval = self.base_interval
            print("06:00 wake-up - reset to Active (5s intervals)")
            return self.current_interval
        
        # Activity detected - wake up
        if new_records_count > 0:
            self.no_activity_count = 0
            old_interval = self.current_interval
            self.current_interval = self.base_interval
            if old_interval > self.base_interval:
                print(f"Activity detected - wake up to Active (5s intervals)")
            return self.current_interval
        
        # No activity - progress through rest levels
        time_period = self.get_time_period()
        max_allowed_level = self.get_max_rest_level(time_period)
        current_level = self.get_current_rest_level()
        
        # Don't exceed time period limits
        if self.rest_levels[current_level]['cycles'] > self.rest_levels[max_allowed_level]['cycles']:
            current_level = max_allowed_level
        
        self.no_activity_count += 1
        old_interval = self.current_interval
        
        # Get max interval for current level
        max_interval = self.rest_levels[current_level]['max_interval']
        
        # Gradual scaling within the level
        if current_level == 'active':
            self.current_interval = self.base_interval
        else:
            self.current_interval = min(
                int(self.current_interval * 1.5), 
                max_interval
            )
        
        # Log level changes
        if self.current_interval != old_interval:
            level_name = current_level.title()
            max_time = self._format_duration(max_interval)
            print(f"Entering {level_name} (max {max_time}) - interval: {old_interval}s → {self.current_interval}s")
        
        return self.current_interval
    
    def _format_duration(self, seconds):
        """Format seconds into human-readable duration."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds//60}min"
        else:
            return f"{seconds//3600}hr"
    
    def reset(self):
        """Reset to active state."""
        self.current_interval = self.base_interval
        self.no_activity_count = 0

# ----------------------------------------
# Timestamp Formatting Utilities
# ----------------------------------------

def format_timestamp_str(timestamp: datetime) -> str:
    """
    Converts a datetime object into a standardized timestamp string.

    Example: "2025-03-24 07:26:55"

    Parameters:
        timestamp (datetime): Datetime object to format.

    Returns:
        str: Formatted timestamp string.
    """
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def format_timestamp_iso(timestamp: datetime) -> str:
    """
    Converts a datetime object into an ISO 8601 formatted string.

    Example: "2025-03-24T07:26:55Z"

    Parameters:
        timestamp (datetime): Datetime object to format.

    Returns:
        str: ISO 8601 formatted timestamp string.
    """
    return timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

# ----------------------------------------
# Document ID Generation Utility
# ----------------------------------------

def generate_doc_id(staff_id: str, timestamp: datetime) -> str:
    """
    Generates a unique MD5 hash-based document ID from a staff ID and timestamp.

    Parameters:
        staff_id (str): The unique identifier of the staff member.
        timestamp (datetime): The attendance timestamp.

    Returns:
        str: A unique MD5 hash document identifier.
    """
    raw_id = f"{staff_id}_{format_timestamp_str(timestamp)}"
    return hashlib.md5(raw_id.encode()).hexdigest()

# ----------------------------------------
# Cache Management Utilities
# ----------------------------------------

def load_uploaded_doc_ids(output_dir: str = "output") -> set:
    """
    Loads previously uploaded document IDs from JSON files within the specified output directory.

    Parameters:
        output_dir (str): Directory containing previously uploaded log files.

    Returns:
        set: A set containing all previously uploaded document IDs.
    """
    doc_ids = set()
    for file in glob.glob(f"{output_dir}/logs_*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for log in data:
                    doc_ids.add(log["doc_id"])
        except Exception as e:
            logging.warning(f"Skipped file {file}: {e}")
    return doc_ids


def load_uploaded_ids_cache(cache_path: str = "cache/uploaded_ids_cache.json") -> set:
    """
    Loads cached document IDs from a specified JSON cache file.

    Parameters:
        cache_path (str): Path to the cache file.

    Returns:
        set: Set of cached document IDs. Returns an empty set if the cache file does not exist or fails to read.
    """
    if not os.path.exists(cache_path):
        return set()
    with open(cache_path, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except Exception as e:
            logging.warning(f"Failed to read cache {cache_path}: {e}")
            return set()


def save_uploaded_ids_cache(doc_ids: set, cache_path: str = "cache/uploaded_ids_cache.json"):
    """
    Saves document IDs to a specified JSON cache file.

    Parameters:
        doc_ids (set): Set of document IDs to cache.
        cache_path (str): Path to save the cache file.
    """
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(list(doc_ids), f, indent=4)
