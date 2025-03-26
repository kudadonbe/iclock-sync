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
    """
    doc_id = generate_doc_id(log.user_id, log.timestamp)

    return {
        "doc_id": doc_id,
        "staffId": str(log.user_id),
        "timestamp": log.timestamp,
        "status": int(log.status),
        "workCode": int(log.punch)
    }
