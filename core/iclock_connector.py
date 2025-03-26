import logging
from zk import ZK
from datetime import datetime

def get_logs_from_device(device_ip: str):
    """
    Connects to a ZKTeco device and retrieves raw logs.
    :param device_ip: IP address of the device
    :return: List of raw attendance logs
    """
    zk = ZK(device_ip, port=4370, timeout=5)
    try:
        conn = zk.connect()
        logs = conn.get_attendance()
        conn.disconnect()
        return logs
    except Exception as e:
        logging.error(f"Error connecting to {device_ip}: {e}")
        return []

def fetch_logs_from_multiple_devices(devices: list):
    """
    Fetches and combines logs from multiple iClock devices.
    :param devices: List of IP addresses
    :return: Combined list of raw SDK log objects
    """
    all_logs = []
    for ip in devices:
        raw_logs = get_logs_from_device(ip)
        all_logs.extend(raw_logs)
    return all_logs
