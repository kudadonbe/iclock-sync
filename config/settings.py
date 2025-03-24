import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# iClock Devices
DEVICE_IPS = os.getenv("DEVICE_IPS", "").split(",")
DEVICE_PORT = int(os.getenv("DEVICE_PORT", 4370))
DEVICE_TIMEOUT = int(os.getenv("DEVICE_TIMEOUT", 5))

# Firebase Key Path
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY", "config/firebase-key.json")
