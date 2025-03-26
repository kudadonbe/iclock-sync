import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Device IPs and Names
DEVICE_IPS = [ip.strip() for ip in os.getenv("DEVICE_IPS", "").split(",")]
DEVICE_NAMES = [name.strip() for name in os.getenv("DEVICE_NAMES", "").split(",")]

# Ensure both lists match in length
if len(DEVICE_IPS) != len(DEVICE_NAMES):
    raise ValueError("DEVICE_IPS and DEVICE_NAMES must have the same number of entries.")

# Combine names and IPs into structured DEVICES list
DEVICES = [{"name": name, "ip": ip} for name, ip in zip(DEVICE_NAMES, DEVICE_IPS)]

DEVICE_PORT = int(os.getenv("DEVICE_PORT", 4370))
DEVICE_TIMEOUT = int(os.getenv("DEVICE_TIMEOUT", 5))

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY", "config/firebase-key.json")
