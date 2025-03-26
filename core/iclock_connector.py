"""
iclock_connector.py - Connects to ZKTeco iClock devices to fetch attendance logs

This module provides functionality for connecting to one or multiple ZKTeco iClock devices,
retrieving raw attendance logs, and aggregating them for further processing.

Author: Hussain Shareef (@kudadonbe)
Date: 2025-03-26
"""

import logging
from zk import ZK


# ----------------------------------------
# Device Connection and Log Retrieval
# ----------------------------------------

def get_logs_from_device(device_ip: str):
    """
    Connects to a ZKTeco iClock device and retrieves raw attendance logs.

    Parameters:
        device_ip (str): IP address of the ZKTeco device.

    Returns:
        list: A list of raw attendance log objects from the device. Returns an empty list if the connection fails.
    """
    zk = ZK(device_ip, port=4370, timeout=5)
    try:
        conn = zk.connect()
        logs = conn.get_attendance()
        conn.disconnect()
        logging.info(f"Successfully retrieved {len(logs)} logs from device at {device_ip}")
        return logs
    except Exception as e:
        logging.error(f"Error connecting to device at {device_ip}: {e}")
        return []


# ----------------------------------------
# Multiple Device Log Aggregation
# ----------------------------------------

def fetch_logs_from_multiple_devices(devices: list):
    """
    Fetches and aggregates logs from multiple ZKTeco iClock devices.

    Parameters:
        devices (list): A list of IP addresses for the devices.

    Returns:
        list: A combined list of raw attendance logs from all specified devices.
    """
    all_logs = []
    for ip in devices:
        device_logs = get_logs_from_device(ip)
        all_logs.extend(device_logs)
        # logging.info(f"Aggregated {len(device_logs)} logs from device {ip}")

    # logging.info(f"Total aggregated logs from all devices: {len(all_logs)}")
    return all_logs
