# core/utils.py

import glob
import json
import hashlib
import os
from datetime import datetime




def format_timestamp_str(timestamp: datetime) -> str:
    """
    Converts a datetime object to a standard timestamp string.
    Example: 2025-03-24 07:26:55
    """
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def format_timestamp_iso(timestamp: datetime) -> str:
    """ 
    Converts a datetime object to ISO 8601 string.
    Example: 2025-03-24T07:26:55Z
    """
    return timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')



def generate_doc_id(staff_id: str, timestamp: datetime):
    
    raw_id = f"{staff_id}_{format_timestamp_str(timestamp)}"
    return hashlib.md5(raw_id.encode()).hexdigest()


def load_uploaded_doc_ids(output_dir: str = "output") -> set:
    """
    Loads all previously uploaded doc_ids from JSON files in the output directory.
    """
    doc_ids = set()
    for file in glob.glob(f"{output_dir}/logs_*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for log in data:
                    doc_ids.add(log["doc_id"])
        except Exception as e:
            print(f"⚠️ Skipped {file}: {e}")
    return doc_ids  # ✅ Make sure to return the set


def load_uploaded_ids_cache(cache_path: str = "cache/uploaded_ids_cache.json") -> set:
    if not os.path.exists(cache_path):
        return set()
    with open(cache_path, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except Exception as e:
            print(f"⚠️ Failed to read cache: {e}")
            return set()
        

def save_uploaded_ids_cache(doc_ids: set, cache_path: str = "cache/uploaded_ids_cache.json"):
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(list(doc_ids), f, indent=4)



