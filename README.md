# iClock-Sync

**iClock-Sync** is a Python-based tool designed to fetch and upload attendance logs from ZKTeco iClock devices directly to Google Firestore. It integrates seamlessly with school management systems like **SchoolSync** and is built modularly, ensuring flexibility for future expansions to support databases such as MySQL, PostgreSQL, MongoDB, and more.

---

## 🚀 Features

- 🔄 **Multi-Device Support:** Fetch attendance logs from multiple ZKTeco iClock devices.
- 🧹 **Structured Normalization:** Logs are consistently formatted with unique IDs.
- ☁️ **Firestore Integration:** Uploads only new, deduplicated records.
- 💾 **Local Audit Logs:** Save uploaded logs locally for verification and auditing.
- 🧠 **Efficient Caching:** Smart cache management using `uploaded_ids_cache.json`.
- 🧪 **Dry-Run Mode:** Safely preview uploads without altering Firestore data.
- ⏳ **Date Filtering:** Easily filter logs to upload only recent records.
- 🔁 **Automated Syncing:** Supports periodic syncing with built-in looping capabilities.

---

## 🧰 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/iclock-sync.git
cd iclock-sync
```

### 2. Install Dependencies
We recommend using a virtual environment based on your operating system:

#### 🔹 macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 🔹 Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Firebase Credentials
Place your Firebase Admin SDK credentials in:
```
config/firebase-key.json
```
> You can generate this file from your Firebase project settings.

### 4. Configure Your Settings
Update `config/settings.py` or create a `.env` file based on `.env.example`:
```env
FIREBASE_KEY_PATH=config/firebase-key.json
```

### 5. (Optional) Test Run
Verify setup using dry-run:
```bash
python main.py --dry-run
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
│   ├── sync_20250326_143020.log
├── output/                            # Output logs (JSON)
│   ├── logs_20250326_143020.json
├── .env                               # Environment-specific variables (private)
├── .env.example                       # Template for environment variables
├── .gitattributes                     # Git attributes configuration
├── .gitignore                         # Ignored files for version control
├── main.py                            # Main application entry-point
├── pyproject.toml                     # Project metadata and configuration
├── README.md                          # Project documentation
├── requirements.lock.txt              # Locked dependencies
└── requirements.txt                   # Python dependencies
```

---

## ⚙️ Usage

### 🚀 Sync Logs to Firestore
Fetch logs from devices and upload to Firestore:
```bash
python main.py
```

### 🧪 Dry-Run (Preview Mode)
Safely preview what will be uploaded without making changes:
```bash
python main.py --dry-run
```

### ⏳ Recent Logs Only
Upload logs from the past two days:
```bash
python main.py --since 2
```

### 🔁 Periodic Sync (Looping)
Automatically sync every 5 minutes (useful for background operations):
```bash
python main.py --loop 5 --since 1
```

### ⚡ Combine Flags
Combine available flags according to your requirements:
```bash
python main.py --dry-run --since 1
```

---

## 🔐 Environment and Secrets

Ensure the following configurations and secrets are properly managed:

- **Firebase credentials**: `firebase-key.json` (stored securely).
- Optional configuration: `.env` file for sensitive settings.
- Ensure the path `FIREBASE_KEY_PATH` is correctly set in `config/settings.py` or your `.env` file.

---

## 🛡️ Reliability and Safety

- **Idempotent Operations:** Prevents duplicate log entries.
- **Audit Trail:** Locally saves all uploaded logs for easy verification.
- **Multi-Device Compatible:** Handles multiple ZKTeco devices seamlessly.

---

## 💡 Planned Future Improvements

- Integration with additional databases: MySQL, PostgreSQL, MongoDB.
- Web-based dashboard for monitoring attendance logs.
- REST API layer (FastAPI) for easier integration with external services.

---

## 🧑‍💻 Author

**Hussain Shareef (@kudadonbe)**\
Makunudhoo School, Maldives 🇲🇻

---

## 📄 License

This project is licensed under the **MIT License**, allowing free use for personal and commercial applications.

---

## 👌 Contributing

Contributions are welcome! Feel free to fork the repository, implement changes or improvements, and submit pull requests.

---

## 🙏 Acknowledgements

This project depends heavily on the incredible open-source work of others, especially:

- [**pyzk**](https://github.com/fananimi/pyzk) – A Python library for interacting with ZKTeco biometric devices
- [firebase-admin](https://pypi.org/project/firebase-admin/) – Firebase Admin SDK for server-side integration
- [tqdm](https://pypi.org/project/tqdm/) – For progress bar support in CLI
- [python-dotenv](https://pypi.org/project/python-dotenv/) – For loading environment variables from `.env` files

Big thanks to all contributors and maintainers of these projects!

