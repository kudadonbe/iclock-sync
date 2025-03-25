from config.settings import DEVICE_IPS
from core.iclock_connector import fetch_logs_from_multiple_devices
from core.normalizer import normalize_sdk_log
# from core.firestore_uploader import upload_log_to_firestore

import json
import os
from datetime import datetime


print("🔍 Device IPs loaded:", DEVICE_IPS)

# 📁 Create output folder if not exists
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 📅 Timestamped file name
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(OUTPUT_DIR, f"logs_{timestamp_str}.json")

# 🔄 Fetch and normalize logs
raw_logs = fetch_logs_from_multiple_devices(DEVICE_IPS)
normalized_logs = [normalize_sdk_log(log) for log in raw_logs]

# 💾 Save to local JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(normalized_logs, f, indent=4, default=str)

print(f"\n✅ Saved {len(normalized_logs)} logs to {output_file}")

# ☁️ Optional: Upload to Firestore (commented out for now)
# for log in normalized_logs:
#     upload_log_to_firestore(log)
# print("☁️ Upload to Firestore complete.")
