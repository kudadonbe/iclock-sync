"""
settings.py - Central configuration for iClock-Sync

This file manages all configurations for the iClock-Sync project by loading environment variables.
It includes device information, connection settings, and Firebase credentials, ensuring easy and secure
configuration across different environments (development, staging, production).

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

import os
from dotenv import load_dotenv

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------
load_dotenv()

# ----------------------------------------
# iClock Device Configuration
# ----------------------------------------

# Load comma-separated device IPs and names from environment variables
DEVICE_IPS = [ip.strip() for ip in os.getenv("DEVICE_IPS", "").split(",")]
DEVICE_NAMES = [name.strip() for name in os.getenv("DEVICE_NAMES", "").split(",")]

# Validate that each IP has a corresponding name
if len(DEVICE_IPS) != len(DEVICE_NAMES):
    raise ValueError("DEVICE_IPS and DEVICE_NAMES must have the same number of entries.")

# Combine device names and IP addresses into structured list
DEVICES = [
    {"name": name, "ip": ip} for name, ip in zip(DEVICE_NAMES, DEVICE_IPS)
]

# Device connection port (default: 4370)
DEVICE_PORT = int(os.getenv("DEVICE_PORT", 4370))

# Device connection timeout in seconds (default: 5)
DEVICE_TIMEOUT = int(os.getenv("DEVICE_TIMEOUT", 5))

# ----------------------------------------
# Firebase Configuration
# ----------------------------------------

# Path to Firebase Admin SDK key (JSON file)
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY", "config/firebase-key.json")
