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
