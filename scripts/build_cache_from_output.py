"""
build_cache_from_output.py - Builds or rebuilds the uploaded IDs cache

This utility script scans the "output" directory for JSON log files containing attendance logs
that have already been uploaded, extracts their document IDs, and saves them to a cache file.
This helps prevent duplicate uploads by maintaining a reliable record of previously uploaded logs.

Run this script whenever you manually alter log records or need to refresh the cache.

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

import sys
import os

# Add project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.utils import load_uploaded_doc_ids, save_uploaded_ids_cache

# Ensure cache directory exists
os.makedirs("cache", exist_ok=True)


def main():
    """
    Main function to build or rebuild the uploaded IDs cache.

    Reads all JSON files in the output directory, extracts their document IDs,
    and saves them to the cache file.
    """
    doc_ids = load_uploaded_doc_ids()

    if not doc_ids:
        print("⚠️ No document IDs found in the output folder.")
        return

    print(f"🔍 Found {len(doc_ids)} uploaded document IDs in output/*.json")
    save_uploaded_ids_cache(doc_ids)
    print("✅ uploaded_ids_cache.json successfully created in the /cache directory")


if __name__ == "__main__":
    main()
