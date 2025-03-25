import firebase_admin  # ← This was missing!

from firebase_admin import credentials, firestore
from config.settings import FIREBASE_KEY_PATH


# Initialize Firestore
if not firestore._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
