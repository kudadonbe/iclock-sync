# core/utils.py

import hashlib
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


