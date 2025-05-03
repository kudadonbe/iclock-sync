# file: feature/time_logs.py

"""
time_logs.py - Handles uploading attendance logs to Firestore.

Author: Hussain Shareef (@kudadonbe)
"""

import logging
from core.firestore_uploader import db
from firebase_admin import firestore

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

    if doc_ref.get().exists:
        logging.info(f"Log already exists in Firestore: {log['doc_id']}")
        return False

    doc_data = {
        "staffId": log["staffId"],
        "timestamp": log["timestamp"],
        "status": log["status"],
        "workCode": log["workCode"],
        "uploadedAt": firestore.SERVER_TIMESTAMP
    }

    doc_ref.set(doc_data)
    return True
