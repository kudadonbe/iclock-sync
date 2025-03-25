from config.settings import DEVICE_IPS
from core.iclock_connector import fetch_logs_from_multiple_devices
from core.normalizer import normalize_sdk_log
from core.firestore_uploader import upload_log_to_firestore
from core.utils import (
    format_timestamp_str,
    load_uploaded_ids_cache,
    save_uploaded_ids_cache
)

import json
import os
import argparse
from datetime import datetime, timedelta
from tqdm import tqdm  # For progress bar

# ----------------------------------------
# 📌 Parse command-line arguments
# ----------------------------------------
parser = argparse.ArgumentParser(description="Upload iClock logs to Firestore")
parser.add_argument("--dry-run", action="store_true", help="Preview what would be uploaded without actually uploading")
parser.add_argument("--since", type=int, default=None, help="Only include logs from the past X days")
parser.add_argument("--loop", type=int, help="Run repeatedly every X minutes")
args = parser.parse_args()

# Output directory for saving uploaded logs
OUTPUT_DIR = "output"


def run_upload():
    print("🔍 Device IPs loaded:", DEVICE_IPS)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ----------------------------------------
    # 📅 Prepare output file with timestamp
    # ----------------------------------------
    timestamp_str = format_timestamp_str(datetime.now()).replace(":", "-").replace(" ", "_")
    output_file = os.path.join(OUTPUT_DIR, f"logs_{timestamp_str}.json")

    # ----------------------------------------
    # 🔄 Fetch logs from devices
    # ----------------------------------------
    raw_logs = fetch_logs_from_multiple_devices(DEVICE_IPS)

    # Optional: filter logs by --since days
    if args.since is not None:
        cutoff_time = datetime.now() - timedelta(days=args.since)
        raw_logs = [log for log in raw_logs if log.timestamp >= cutoff_time]
        print(f"⏳ Filtered logs to only include entries from the past {args.since} days.")

    # Normalize logs
    normalized_logs = [normalize_sdk_log(log) for log in raw_logs]

    # Load uploaded doc_ids from cache
    uploaded_doc_ids = load_uploaded_ids_cache()

    # Filter out already-uploaded logs
    skipped_count = 0
    logs_to_upload = []
    for log in normalized_logs:
        if log["doc_id"] in uploaded_doc_ids:
            skipped_count += 1
            continue
        logs_to_upload.append(log)

    # ----------------------------------------
    # ☁️ Upload (or preview) with progress bar
    # ----------------------------------------
    new_logs = []
    uploaded_count = 0

    for log in tqdm(logs_to_upload, desc="☁️  Uploading logs", unit=" log"):
        if args.dry_run:
            new_logs.append(log)
        else:
            if upload_log_to_firestore(log):
                new_logs.append(log)
                uploaded_count += 1

    # ----------------------------------------
    # 📊 Final summary output
    # ----------------------------------------
    if skipped_count:
        print(f"⏩ Skipped {skipped_count} already-uploaded logs.")

    if args.dry_run:
        print(f"\n🧪 Dry run complete — {len(new_logs)} logs *would* be uploaded.")
    else:
        print(f"\n☁️  Upload complete — {uploaded_count} new logs uploaded.")

        if new_logs:
            # Save new logs to local file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(new_logs, f, indent=4, default=str)
            print(f"💾 Saved {len(new_logs)} new logs to {output_file}")

            # Update the uploaded_ids cache
            uploaded_doc_ids.update([log["doc_id"] for log in new_logs])
            save_uploaded_ids_cache(uploaded_doc_ids)
        else:
            print("📁 No new logs to save.")


def main():
    if args.loop:
        import time
        print(f"\n🔁 Starting loop: syncing every {args.loop} minutes (Press Ctrl+C to stop)\n")
        while True:
            run_upload()
            time.sleep(args.loop * 60)
    else:
        run_upload()


# ----------------------------------------
# 🚀 Start the app
# ----------------------------------------
if __name__ == "__main__":
    main()
