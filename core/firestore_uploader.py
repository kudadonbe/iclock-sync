import firebase_admin
from firebase_admin import credentials, firestore
from config.settings import FIREBASE_KEY_PATH
import logging

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def upload_log_to_firestore(log: dict):
    """
    Uploads a single log to Firestore if it doesn't already exist.
    Returns True if uploaded, False if already exists.
    """
    doc_ref = db.collection("staffAttendanceLogs").document(log["doc_id"])
    
    if doc_ref.get().exists:
        logging.info(f"Already exists: {log['doc_id']}")
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