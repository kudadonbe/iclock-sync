"""
main.py - Entry point for iClock-Sync application

This script connects to configured ZKTeco iClock devices, retrieves attendance logs,
normalizes the logs, filters already uploaded records, and uploads new logs to Google Firestore.

Supports command-line arguments for:
    --dry-run: Preview uploads without performing actual uploads.
    --since X: Include only logs from the past X days.
    --loop X: Continuously run the sync every X minutes.
    --export-simple: Save simplified logs (user_id, date, time, punch_status, log_status)
    --export-normalized: Save normalized logs (includes doc_id, timestamp, etc.)

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

from config.settings import DEVICES
from core.iclock_connector import get_logs_from_device
from core.normalizer import normalize_sdk_log, convert_to_simple_log
from core.firestore_uploader import upload_log_to_firestore
from core.utils import (
    format_timestamp_str,
    load_uploaded_ids_cache,
    save_uploaded_ids_cache
)

import logging
import json
import argparse
import time
from datetime import datetime, timedelta
from tqdm import tqdm
from pathlib import Path

# ----------------------------------------
# Logging Configuration
# ----------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOG_DIR / f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ----------------------------------------
# Parse Command-Line Arguments
# ----------------------------------------
parser = argparse.ArgumentParser(description="Upload iClock logs to Firestore")
parser.add_argument("--dry-run", action="store_true", help="Preview upload without performing it")
parser.add_argument("--since", type=int, default=None, help="Include logs from past X days")
parser.add_argument("--loop", type=int, help="Run repeatedly every X minutes")
parser.add_argument("--export-simple", action="store_true", help="Export logs in simplified format (JSON array)")
parser.add_argument("--export-normalized", action="store_true", help="Export normalized logs without uploading")
args = parser.parse_args()

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_upload():
    """Executes the full log retrieval and upload process."""
    logging.info("iClock sync started.")
    device_names = [device['name'] for device in DEVICES]
    print("\U0001F50D Devices loaded:", device_names)
    logging.info(f"Devices loaded: {DEVICES}")

    timestamp_str = format_timestamp_str(datetime.now()).replace(":", "-").replace(" ", "_")
    output_file = OUTPUT_DIR / f"logs_{timestamp_str}.json"

    # Fetch Logs from Devices
    raw_logs = []
    for device in DEVICES:
        print(f"\u2705 Connecting to {device['name']}")
        logging.info(f"Connecting to {device['name']} at {device['ip']}")
        device_logs = get_logs_from_device(device['ip'])
        print(f"\U0001F4CC Retrieved {len(device_logs)} records from {device['name']}")
        logging.info(f"Retrieved {len(device_logs)} records from {device['name']} ({device['ip']})")
        raw_logs.extend(device_logs)

    total_records = len(raw_logs)
    print(f"\U0001F4CC Total records fetched from all devices: {total_records}")
    logging.info(f"Total records fetched from all devices: {total_records}")

    if args.since is not None:
        cutoff_time = datetime.now() - timedelta(days=args.since)
        raw_logs = [log for log in raw_logs if log.timestamp >= cutoff_time]
        logging.info(f"Filtered logs from past {args.since} days.")

    # Normalize Logs
    normalized_logs = [normalize_sdk_log(log) for log in raw_logs]

    # Export simplified logs if requested
    if args.export_simple:
        simple_logs = [convert_to_simple_log(log) for log in raw_logs]
        simple_output_file = OUTPUT_DIR / f"simplified_logs_{timestamp_str}.json"
        with open(simple_output_file, "w", encoding="utf-8") as f:
            json.dump(simple_logs, f, indent=4)
        logging.info(f"Exported simplified logs to {simple_output_file}")
        print(f"\U0001F4C4 Exported simplified logs to {simple_output_file}")

    # Export normalized logs if requested
    if args.export_normalized:
        normalized_output_file = OUTPUT_DIR / f"normalized_logs_{timestamp_str}.json"
        with open(normalized_output_file, "w", encoding="utf-8") as f:
            json.dump(normalized_logs, f, indent=4, default=str)
        logging.info(f"Exported normalized logs to {normalized_output_file}")
        print(f"\U0001F4C4 Exported normalized logs to {normalized_output_file}")

    if args.export_simple or args.export_normalized:
        return

    # Skip upload if export-only mode
    uploaded_doc_ids = load_uploaded_ids_cache()
    skipped_count = 0
    logs_to_upload = []
    for log in normalized_logs:
        if log["doc_id"] in uploaded_doc_ids:
            skipped_count += 1
            continue
        logs_to_upload.append(log)

    new_logs = []
    uploaded_count = 0
    for log in tqdm(logs_to_upload, desc="\u2601\ufe0f Uploading logs", unit=" log"):
        if args.dry_run:
            new_logs.append(log)
        else:
            try:
                success = upload_log_to_firestore(log)
                if success:
                    new_logs.append(log)
                    uploaded_count += 1
                else:
                    logging.warning(f"Log upload failed: {log['doc_id']}")
            except Exception as e:
                logging.error(f"Error uploading log {log['doc_id']}: {e}")

    if skipped_count:
        logging.info(f"Skipped {skipped_count} already-uploaded logs.")
        print(f"\u23e9 Skipped {skipped_count} already-uploaded logs.")

    if args.dry_run:
        print(f"\n\U0001F9EA Dry run complete — {len(new_logs)} logs *would* be uploaded.")
        logging.info(f"Dry run complete - {len(new_logs)} logs would be uploaded.")
    else:
        print(f"\n\u2601\ufe0f Upload complete — {uploaded_count} new logs uploaded.")
        logging.info(f"Upload complete - {uploaded_count} new logs uploaded.")

        if new_logs:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(new_logs, f, indent=4, default=str)
            logging.info(f"Saved {len(new_logs)} new logs to {output_file}")
            print(f"\U0001F4BE Saved {len(new_logs)} new logs to {output_file}")

            uploaded_doc_ids.update([log["doc_id"] for log in new_logs])
            save_uploaded_ids_cache(uploaded_doc_ids)
        else:
            print("\U0001F4C1 No new logs to save.")
            logging.info("No new logs to save.")

def main():
    """Main execution function, handles looping behavior."""
    if args.loop:
        print(f"\n\U0001F501 Starting loop: syncing every {args.loop} minutes (Ctrl+C to stop)\n")
        logging.info(f"Starting sync loop every {args.loop} minutes.")
        try:
            while True:
                run_upload()
                time.sleep(args.loop * 60)
        except KeyboardInterrupt:
            print("\n\U0001F6D1 Sync loop stopped by user.")
            logging.info("Sync loop stopped by user.")
    else:
        run_upload()

if __name__ == "__main__":
    main()
