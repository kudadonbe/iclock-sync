"""
normalizer.py - Normalizes raw attendance logs retrieved from ZKTeco devices

This module provides functionality to convert raw SDK logs into a structured format suitable
for database uploads, adding essential metadata such as unique document IDs for deduplication.

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

from core.utils import generate_doc_id


def normalize_sdk_log(log):
    """
    Normalizes a raw attendance log from the ZKTeco SDK into a structured dictionary.

    Parameters:
        log: Raw attendance log object retrieved from ZKTeco device.
             Expected attributes:
             - user_id: The unique identifier of the staff member.
             - timestamp: The timestamp of the attendance event.
             - status: The attendance status (e.g., check-in or check-out).
             - punch: Work code associated with the attendance log.

    Returns:
        dict: Structured log dictionary with the following keys:
              - doc_id: Unique identifier (MD5 hash).
              - staffId: Staff ID as a string.
              - timestamp: Datetime object representing attendance time.
              - status: Integer status code.
              - workCode: Integer representing the work code.
              
    Raises:
        ValueError: If user_id is invalid (None, empty, 0, or non-numeric).
    """
    # Validate staffId before processing
    if not log.user_id or log.user_id == 0 or str(log.user_id).strip() == "" or str(log.user_id).strip() == "None":
        raise ValueError(f"Invalid staffId: {log.user_id} - cannot normalize log")
    
    # Additional validation: ensure staffId is numeric
    try:
        staff_id_int = int(log.user_id)
        if staff_id_int <= 0:
            raise ValueError(f"Invalid staffId: {log.user_id} - must be positive integer")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid staffId: {log.user_id} - must be numeric")
    
    doc_id = generate_doc_id(log.user_id, log.timestamp)

    return {
        "doc_id": doc_id,
        "staffId": str(log.user_id),
        "timestamp": log.timestamp,
        "status": int(log.status),
        "workCode": int(log.punch)
    }


def convert_to_simple_log(log):
    """
    Converts a raw ZKTeco SDK log into a simplified dictionary format.

    Parameters:
        log: Raw attendance log object retrieved from ZKTeco device.
             Expected attributes:
             - user_id: The unique identifier of the staff member.
             - timestamp: The timestamp of the attendance event.
             - status: The attendance status (e.g., check-in or check-out).
             - punch: Work code associated with the attendance log.

    Returns:
        dict: Simplified log dictionary with the following keys:
              - user_id (str)
              - date (str in YYYY-MM-DD format)
              - time (str in HH:MM:SS format)
              - punch_status (int)
              - log_status (int)
    """
    return {
        "user_id": str(log.user_id),
        "date": log.timestamp.strftime("%Y-%m-%d"),
        "time": log.timestamp.strftime("%H:%M:%S"),
        "punch_status": log.punch,
        "log_status": log.status,
    }

