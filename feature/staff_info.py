"""
File: feature/staff_info.py
staff_info.py - Handles uploading staff list from JSON to Firestore.

This module loads `staffList.json`, transforms keys to camelCase, and uploads
each entry to Firestore under the 'staff' collection.

Author: Hussain Shareef (@kudadonbe)
Date: 2025-05-03
"""


import json
import os
import logging
from core.firestore_uploader import db

def upload_staff_list(filepath: str = "src/data/staffList.json", collection: str = "staff"):
    """
    Uploads a list of staff entries to Firestore from a local JSON file.

    Parameters:
        filepath (str): Path to the staff list JSON file.
        collection (str): Name of the Firestore collection (default: "staff").
    """
    def to_camel_case(snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    def convert_keys(entry):
        return {to_camel_case(k): v for k, v in entry.items()}

    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        staff_list = json.load(f)

    uploaded = 0
    skipped = 0

    for entry in staff_list:
        transformed = convert_keys(entry)
        doc_id = transformed.get("userId")
        doc_ref = db.collection(collection).document(doc_id if doc_id else None)

        if doc_id and doc_ref.get().exists:
            logging.info(f"Staff entry already exists: {doc_id}")
            skipped += 1
            continue

        doc_ref.set(transformed)
        logging.info(f"Uploaded staff entry: {transformed.get('name', 'Unknown')}")
        uploaded += 1

    print(f"✅ Staff upload complete — {uploaded} uploaded, {skipped} skipped.")
