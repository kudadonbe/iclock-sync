"""
cli.py - Entry point for iClock-Sync application

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
    save_uploaded_ids_cache,
    SmartTiming
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
parser.add_argument("--loop", type=float, help="Continuously sync every X seconds (e.g., 5, 30, 0.5)")
parser.add_argument("--export-simple", action="store_true", help="Export logs in simplified format (JSON array)")
parser.add_argument("--export-normalized", action="store_true", help="Export normalized logs without uploading")
args = parser.parse_args()

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_upload():
    """Executes the full log retrieval and upload process."""
    # Returns: uploaded_count for SmartTiming
    logging.info("iClock sync started.")
    device_names = [device['name'] for device in DEVICES]
    print("Devices loaded:", device_names)
    logging.info(f"Devices loaded: {DEVICES}")

    timestamp_str = format_timestamp_str(datetime.now()).replace(":", "-").replace(" ", "_")
    output_file = OUTPUT_DIR / f"logs_{timestamp_str}.json"

    # Fetch Logs from Devices
    raw_logs = []
    for device in DEVICES:
        print(f"Connecting to {device['name']}")
        logging.info(f"Connecting to {device['name']} at {device['ip']}")
        device_logs = get_logs_from_device(device['ip'])
        print(f"Retrieved {len(device_logs)} records from {device['name']}")
        logging.info(f"Retrieved {len(device_logs)} records from {device['name']} ({device['ip']})")
        raw_logs.extend(device_logs)

    total_records = len(raw_logs)
    print(f"Total records fetched from all devices: {total_records}")
    logging.info(f"Total records fetched from all devices: {total_records}")

    if args.since is not None:
        cutoff_time = datetime.now() - timedelta(days=args.since)
        raw_logs = [log for log in raw_logs if log.timestamp >= cutoff_time]
        logging.info(f"Filtered logs from past {args.since} days.")

    # Normalize Logs with validation
    normalized_logs = []
    invalid_count = 0
    for log in raw_logs:
        try:
            normalized_log = normalize_sdk_log(log)
            normalized_logs.append(normalized_log)
        except ValueError as e:
            invalid_count += 1
            logging.warning(f"Skipped invalid log: {e}")
    
    if invalid_count > 0:
        print(f"⚠️  Skipped {invalid_count} logs with invalid staffId")
        logging.info(f"Skipped {invalid_count} logs with invalid staffId")

    # Skip logs with empty staffId values
    normalized_logs = [log for log in normalized_logs if str(log["staffId"]).strip()]

    # Export simplified logs if requested
    if args.export_simple:
        simple_logs = [convert_to_simple_log(log) for log in raw_logs]
        simple_output_file = OUTPUT_DIR / f"simplified_logs_{timestamp_str}.json"
        with open(simple_output_file, "w", encoding="utf-8") as f:
            json.dump(simple_logs, f, indent=4)
        logging.info(f"Exported simplified logs to {simple_output_file}")
        print(f"Exported simplified logs to {simple_output_file}")

    # Export normalized logs if requested
    if args.export_normalized:
        normalized_output_file = OUTPUT_DIR / f"normalized_logs_{timestamp_str}.json"
        with open(normalized_output_file, "w", encoding="utf-8") as f:
            json.dump(normalized_logs, f, indent=4, default=str)
        logging.info(f"Exported normalized logs to {normalized_output_file}")
        print(f"Exported normalized logs to {normalized_output_file}")

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

    # Abort if suspiciously high volume of logs is queued for upload
    if len(logs_to_upload) > 300:
        logging.error(f"Aborting upload: {len(logs_to_upload)} logs to upload exceeds safety limit")
        print(f"Too many logs to upload ({len(logs_to_upload)} > 300). Exiting to prevent potential error.")
        return

    new_logs = []
    uploaded_count = 0
    for log in tqdm(logs_to_upload, desc="Uploading logs", unit=" log"):
        if args.dry_run:
            new_logs.append(log)
        else:
            try:
                result = upload_log_to_firestore(log)
                if result == "uploaded":
                    new_logs.append(log)
                    uploaded_count += 1
                elif result == "exists":
                    # Add existing record ID to cache to prevent future attempts
                    uploaded_doc_ids.add(log["doc_id"])
                    logging.info(f"Added existing record to cache: {log['doc_id']}")
                else:
                    logging.warning(f"Log upload failed: {log['doc_id']}")
            except Exception as e:
                logging.error(f"Error uploading log {log['doc_id']}: {e}")

    if skipped_count:
        logging.info(f"Skipped {skipped_count} already-uploaded logs.")
        print(f"Skipped {skipped_count} already-uploaded logs.")

    if args.dry_run:
        print(f"Dry run complete - {len(new_logs)} logs would be uploaded.")
        logging.info(f"Dry run complete - {len(new_logs)} logs would be uploaded.")
    else:
        print(f"Upload complete - {uploaded_count} new logs uploaded.")
        logging.info(f"Upload complete - {uploaded_count} new logs uploaded.")

        # Save uploaded logs to file if any
        if new_logs:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(new_logs, f, indent=4, default=str)
            logging.info(f"Saved {len(new_logs)} new logs to {output_file}")
            print(f"Saved {len(new_logs)} new logs to {output_file}")

        # Update cache with both newly uploaded and existing record IDs
        if new_logs:
            uploaded_doc_ids.update([log["doc_id"] for log in new_logs])
        
        # Save updated cache (includes both new uploads and discovered existing records)
        save_uploaded_ids_cache(uploaded_doc_ids)
        
        if not new_logs:
            print("No new logs to save.")
            logging.info("No new logs to save.")
    
    # Return upload count for SmartTiming
    return uploaded_count if not args.dry_run else len(new_logs) if 'new_logs' in locals() else 0

def main():
    """Main execution function, handles looping behavior."""
    if args.loop:
        # Use SmartTiming for graduated rest levels
        smart_timer = SmartTiming(base_interval=args.loop)
        print(f"Starting smart sync: base {args.loop}s with graduated rest (Active → Rest → Nap → Sleep → Dream)")
        print("Schedule: Active(6-16) → Nap(16-18) → Sleep(18-23) → Dream(23-6)")
        logging.info(f"Starting smart sync loop with base interval {args.loop}s.")
        try:
            while True:
                uploaded_count = run_upload()
                
                # Get next interval based on activity and time of day
                next_interval = smart_timer.get_next_interval(uploaded_count)
                
                print(f"Next sync in {next_interval}s")
                time.sleep(next_interval)
        except KeyboardInterrupt:
            print("Smart sync stopped by user.")
            logging.info("Smart sync stopped by user.")
    else:
        run_upload()

def entrypoint():
    main()


# Example Usage:
# python cli.py --loop 30                  # sync every 30 seconds
# python cli.py --since 2 --dry-run        # preview past 2 days of logs
# python cli.py --export-simple            # export only

