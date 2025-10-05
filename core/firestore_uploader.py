"""
file: core\firestore_uploader.py
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
        str: "exists" if the log already existed, "uploaded" if successfully uploaded, False on error.
    """
    # Validate required fields before upload
    required_fields = ["doc_id", "staffId", "timestamp", "status", "workCode"]
    for field in required_fields:
        if field not in log or log[field] is None:
            logging.error(f"Missing required field '{field}' in log: {log}")
            return False
    
    # Validate staffId is not empty or invalid
    staff_id = str(log["staffId"]).strip()
    if not staff_id or staff_id == "None" or staff_id == "0":
        logging.error(f"Invalid staffId '{log['staffId']}' in log: {log['doc_id']}")
        return False
    
    # Validate staffId is numeric
    try:
        staff_id_int = int(staff_id)
        if staff_id_int <= 0:
            logging.error(f"Invalid staffId '{staff_id}' must be positive integer: {log['doc_id']}")
            return False
    except (ValueError, TypeError):
        logging.error(f"Invalid staffId '{staff_id}' must be numeric: {log['doc_id']}")
        return False
    
    doc_ref = db.collection("staffAttendanceLogs").document(log["doc_id"])

    # Check if the document already exists to prevent duplication
    if doc_ref.get().exists:
        logging.info(f"Log already exists in Firestore: {log['doc_id']}")
        return "exists"

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
    return "uploaded"
