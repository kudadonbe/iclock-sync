# iClock-Sync

**iClock-Sync** is a Python-based tool designed to fetch and upload attendance logs from ZKTeco iClock devices directly to Google Firestore. It integrates seamlessly with school management systems like **SchoolSync** and is built modularly, ensuring flexibility for future expansions to support databases such as MySQL, PostgreSQL, MongoDB, and more.

---

## 🚀 Features

- 🔄 **Multi-Device Support:** Fetch attendance logs from multiple ZKTeco iClock devices.
- 🩹 **Structured Normalization:** Logs are consistently formatted with unique IDs and comprehensive validation.
- ☁️ **Firestore Integration:** Uploads only new, deduplicated records with smart caching.
- 💾 **Local Audit Logs:** Save uploaded logs locally for verification and auditing.
- 🧠 **High-Performance Caching:** Smart cache management using `uploaded_ids_cache.json` (99%+ efficiency).
- 🧪 **Dry-Run Mode:** Safely preview uploads without altering Firestore data.
- ⏳ **Smart Date Filtering:** Efficiently filter logs to upload only recent records, reducing processing by 99%.
- 🔁 **Optimized Syncing:** Intelligent sync intervals with built-in performance optimization.
- 🛡️ **Data Validation:** Comprehensive validation prevents invalid records from reaching Firestore.
- 🔧 **Command-Line Interface:** Run using `iclock --export-simple`, `--dry-run`, etc. after editable install.

---

## 🧰 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kudadonbe/iclock-sync.git
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

