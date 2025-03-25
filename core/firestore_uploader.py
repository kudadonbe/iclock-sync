import firebase_admin
from firebase_admin import credentials, firestore
from config.settings import FIREBASE_KEY_PATH

# 🔐 Initialize Firestore (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def upload_log_to_firestore(log: dict):
    """
    Upload a normalized log to Firestore using its doc_id as the document key.
    """
    doc_ref = db.collection("staffAttendanceLogs").document(log["doc_id"])

    doc_data = {
        "staffId": log["staffId"],
        "timestamp": log["timestamp"],
        "status": log["status"],
        "workCode": log["workCode"],
        "uploadedAt": firestore.SERVER_TIMESTAMP
    }

    doc_ref.set(doc_data)
    print(f"☁️ Uploaded: {log['staffId']} @ {log['timestamp']}")
