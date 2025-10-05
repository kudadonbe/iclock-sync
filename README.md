# iClock-Sync

**iClock-Sync** is a Python-based tool designed to fetch and upload attendance logs from ZKTeco iClock devices directly to Google Firestore. It integrates seamlessly with school management systems like **SchoolSync** and is built modularly, ensuring flexibility for future expansions to support databases such as MySQL, PostgreSQL, MongoDB, and more.

---

## 🚀 Features

- 🔄 **Multi-Device Support:** Fetch attendance logs from multiple ZKTeco iClock devices.
- 🩹 **Structured Normalization:** Logs are consistently formatted with unique IDs.
- ☁️ **Firestore Integration:** Uploads only new, deduplicated records.
- 💾 **Local Audit Logs:** Save uploaded logs locally for verification and auditing.
- 🧠 **Efficient Caching:** Smart cache management using `uploaded_ids_cache.json`.
- 🧪 **Dry-Run Mode:** Safely preview uploads without altering Firestore data.
- ⏳ **Date Filtering:** Easily filter logs to upload only recent records.
- 🔁 **Automated Syncing:** Supports periodic syncing with built-in looping capabilities.
- 🔧 **Command-Line Interface:** Run using `iclock --export-simple`, `--dry-run`, etc. after editable install.

---

## 🧰 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/iclock-sync.git
cd iclock-sync
```

### 2. Create and Activate Virtual Environment
We recommend using a virtual environment based on your OS:

#### 🔹 macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 🔹 Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
> ⚠️ If activation fails, run this once:
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Editable Install for CLI Command (`iclock`)
```bash
pip install -e .
```
> If using `python -m cli`, also set:
> ```powershell
> $env:PYTHONPATH = "$(Get-Location)"
> ```

### 5. Add Firebase Credentials
Place your Firebase Admin SDK credentials in:
```
config/firebase-key.json
```

### 6. Configure Your Settings
Update `config/settings.py` or use `.env`:
```env
FIREBASE_KEY_PATH=config/firebase-key.json
```

---

## 📁 Recommended Project Structure

```
iclock-sync/
├── cache/                             # Cached data
│   └── uploaded_ids_cache.json
├── config/                            # Configuration files
│   ├── firebase-key.json
│   └── settings.py
├── core/                              # Core application logic
│   ├── firestore_uploader.py
│   ├── iclock_connector.py
│   ├── normalizer.py
│   └── utils.py
├── data/                              # Sample or test data
│   ├── sample_logs.txt
├── logs/                              # Application log files
│   ├── sync_*.log
├── output/                            # Output logs (JSON)
│   ├── logs_*.json
├── .env                               # Environment-specific variables
├── .env.example                       # Template
├── cli.py                             # Main CLI entry-point
├── pyproject.toml                     # Project metadata
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## ⚙️ Usage

### 🚀 Sync Logs to Firestore
```bash
iclock
```

### 🧪 Dry-Run (Preview Mode)
```bash
iclock --dry-run
```

### ⏳ Recent Logs Only
```bash
iclock --since 2
```

### ♻️ Periodic Sync (Looping)
```bash
iclock --loop 5 --since 1
```

### ⚡ Export Logs
```bash
iclock --export-simple
iclock --export-normalized
```

### 🚀 Combine Options
```bash
iclock --dry-run --since 1
```

Or directly:
```bash
python -m cli --dry-run --since 1
```
> Use this if `iclock` command isn't recognized. Also set:
> ```powershell
> $env:PYTHONPATH = "$(Get-Location)"
> ```

---

## 🔐 Environment and Secrets

- **Firebase credentials**: `firebase-key.json`
- **Optional**: `.env` file with `FIREBASE_KEY_PATH`

---

## 🛡️ Reliability and Safety

- Idempotent uploads (no duplicates)
- Audit trail via output logs
- Handles multiple devices gracefully

---

## 💡 Planned Future Improvements

- MySQL, PostgreSQL, MongoDB support
- Web dashboard
- REST API layer via FastAPI

---

## 🧑‍💻 Author

**Hussain Shareef (@kudadonbe)**\
Makunudhoo School, Maldives 🇲🇻

---

## 📄 License

MIT License — free for personal/commercial use

---

## 🙏 Acknowledgements

- [pyzk](https://github.com/fananimi/pyzk)
- [firebase-admin](https://pypi.org/project/firebase-admin/)
- [tqdm](https://pypi.org/project/tqdm/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

# iClock Sync Tool

A Python application for synchronizing attendance data from iClock devices to Firebase Firestore.

## Features

- Connects to multiple iClock devices via TCP/IP
- Retrieves attendance logs from iClock devices
- Validates and normalizes attendance data
- Uploads valid records to Firebase Firestore
- Comprehensive logging for monitoring and debugging
- Configurable sync intervals and device management

## ⚠️ Known Issues

### Critical: Empty staffId Records Bug
**Status**: Active Issue - High Priority

The system is currently logging thousands of invalid records with empty `staffId` values:

```
WARNING - Skipped invalid log: Invalid staffId:  - cannot normalize log
```

**Impact**:
- Database pollution with invalid records
- Performance degradation during sync operations
- Storage of unusable attendance data
- Difficulty in data analysis and reporting

**Investigation Required**:
- Check iClock device configuration for data integrity
- Review staff ID mapping in iClock system
- Validate data at source before upload
- Consider implementing stricter validation rules

See [Bug Report](docs/BUG_REPORT_ICLOCK_EMPTY_STAFFID.md) for detailed analysis.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/iclock-sync.git
cd iclock-sync
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Firebase credentials:
   - Download your Firebase service account key
   - Place it in the project directory
   - Update the path in your configuration

4. Configure devices:
   - Update `config/devices.json` with your iClock device details
   - Set appropriate IP addresses and device names

## Configuration

### Device Configuration
```json
{
  "devices": [
    {
      "name": "Admin Office Device",
      "ip": "172.16.15.73"
    },
    {
      "name": "Staff Room Device", 
      "ip": "172.16.15.72"
    }
  ]
}
```

### Sync Settings
- Default sync interval: 5 seconds
- Configurable via environment variables
- Supports multiple device polling

## Usage

### Basic Operation
```bash
python main.py
```

### With Custom Configuration
```bash
python main.py --config custom_config.json
```

## Monitoring

### Log Files
Logs are automatically generated in the `logs/` directory:
- Format: `sync_YYYYMMDD_HHMMSS.log`
- Contains detailed sync operations, errors, and warnings
- Monitor for validation failures and connection issues

### Key Metrics to Monitor
- Total records fetched per sync cycle
- Invalid records skipped (should be minimal)
- Connection success rate to devices
- Upload success rate to Firebase

## Troubleshooting

### High Invalid Record Count
If you see many "Invalid staffId" warnings:

1. **Check iClock Device Setup**:
   - Verify staff IDs are properly configured
   - Ensure device time synchronization
   - Check device firmware version

2. **Validate Source Data**:
   - Access iClock web interface
   - Review staff registration data
   - Check for empty or malformed staff IDs

3. **Database Cleanup**:
   - Consider cleaning existing invalid records
   - Implement stricter validation before upload

### Connection Issues
```
ERROR - Failed to connect to device at [IP]
```

Solutions:
- Verify network connectivity
- Check device IP addresses
- Ensure devices are powered on
- Verify firewall settings

### Firebase Upload Failures
```
ERROR - Failed to upload to Firebase
```

Solutions:
- Verify Firebase credentials
- Check internet connectivity
- Validate Firestore permissions
- Monitor Firebase quotas

## Performance Optimization

### Current Recommendations
- **Avoid continuous sync**: Current 5-second intervals may be too aggressive
- **Consider scheduled sync**: Run every 15-30 minutes instead
- **Monitor system resources**: CPU, memory, and network usage
- **Implement batching**: Upload records in batches rather than individually

### System Health
- Monitor log file sizes (they can grow rapidly with high invalid record counts)
- Watch for memory leaks during continuous operation
- Consider log rotation for long-running deployments

## Data Validation

The system validates the following fields:
- `staffId`: Must not be empty or null
- `timestamp`: Must be valid datetime
- `workCode`: Numeric values only
- `status`: Valid status codes

Invalid records are logged and skipped to maintain data integrity.

## Development

### Project Structure
```
iclock-sync/
├── main.py              # Entry point
├── src/                 # Source code
├── config/              # Configuration files
├── logs/                # Log files (auto-generated)
├── docs/                # Documentation
└── requirements.txt     # Dependencies
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the logs for detailed error information
2. Review the troubleshooting section
3. Create an issue with log excerpts and device configuration
4. Include system specifications and network setup details

## License

[Your License Here]

---

**Last Updated**: October 2025  
**Version**: 1.0.0  
**Status**: Active Development - Known Issues Under Investigation

