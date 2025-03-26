"""
firestore_uploader.py - Handles uploading attendance logs to Google Firestore

This module initializes the connection to Firestore and provides functionality to upload individual
attendance logs, ensuring no duplicates are created by checking for existing records.

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

import firebase_admin
from firebase_admin import credentials, firestore
from config.settings import FIREBASE_KEY_PATH
import logging

# ----------------------------------------
# Firebase Initialization
# ----------------------------------------

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

# Firestore client instance
db = firestore.client()


# ----------------------------------------
# Firestore Upload Function
# ----------------------------------------

def upload_log_to_firestore(log: dict):
    """
    Uploads a single attendance log to Firestore if it doesn't already exist.

    Parameters:
        log (dict): A dictionary containing normalized log data. Expected keys:
            - doc_id: Unique document identifier (MD5 hash).
            - staffId: Unique staff ID.
            - timestamp: Attendance timestamp.
            - status: Attendance status (IN/OUT).
            - workCode: Associated work code or reason.

    Returns:
        bool: True if the log was successfully uploaded, False if it already existed.
    """
    doc_ref = db.collection("staffAttendanceLogs").document(log["doc_id"])

    # Check if the document already exists to prevent duplication
    if doc_ref.get().exists:
        logging.info(f"Log already exists in Firestore: {log['doc_id']}")
        return False

    # Prepare the data payload for Firestore
    doc_data = {
        "staffId": log["staffId"],
        "timestamp": log["timestamp"],
        "status": log["status"],
        "workCode": log["workCode"],
        "uploadedAt": firestore.SERVER_TIMESTAMP  # Records server-side timestamp
    }

    # Save the document to Firestore
    doc_ref.set(doc_data)
    # logging.info(f"Log uploaded to Firestore: {log['doc_id']}")
    return True
