# iClock-Sync

**iClock-Sync** is a Python-based tool that fetches and uploads attendance logs from ZKTeco iClock devices to Firestore. Built for seamless integration with school systems like **SchoolSync**, it's modular and expandable to support other databases in the future (MySQL, PostgreSQL, MongoDB, etc).

---

## 🚀 Features

- 🔄 Fetch attendance logs from multiple iClock devices
- 🧹 Normalize logs with consistent structure and unique IDs
- ☁️ Upload only new records to Firestore (deduplication supported)
- 💾 Save uploaded logs locally for auditing
- 🧠 Smart cache system using `uploaded_ids_cache.json`
- 🧪 `--dry-run` mode for safe testing
- ⏳ `--since` filter for recent log uploads
- 🔁 `--loop` mode for running as a periodic sync service

---

## 📁 Folder Structure (Recommended)

```
iclock-sync/
├── core/                        # Core logic (connector, normalizer, Firestore uploader, utils)
├── scripts/                     # One-time or support scripts
│   └── build_cache_from_output.py
├── cache/                       # Local cache (auto-created)
│   └── uploaded_ids_cache.json
├── output/                      # Log outputs saved as JSON
│   └── logs_YYYY-MM-DD_HH-MM-SS.json
├── main.py                      # Entry script for syncing
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (optional)
└── README.md
```

---

## ⚙️ Usage

### ✅ One-time: Build local cache from existing output files

```bash
python scripts/build_cache_from_output.py
```

### 🚀 Sync from devices and upload to Firestore

```bash
python main.py
```

### 🧪 Dry-run mode (preview without uploading)

```bash
python main.py --dry-run
```

### ⏳ Upload only logs from last 2 days

```bash
python main.py --since 2
```

### 🔁 Run every 5 minutes (auto-loop)

```bash
python main.py --loop 5 --since 1
```

You can combine flags as needed:
```bash
python main.py --dry-run --since 1
```

---

## 🔐 Environment & Secrets

You should have the following in place:

- `firebase-key.json` for Firestore access
- `.env` file for secrets and config (optional)
- `FIREBASE_KEY_PATH` in `config/settings.py` or `.env`

---

## 🛡️ Safety and Reliability

- Uploads are **idempotent** — same log will never be uploaded twice
- All logs are locally saved for verification
- Works with multiple devices

---

## 💡 Future Improvements

- Support for MySQL / MongoDB / other DBs
- Web dashboard for monitoring logs
- FastAPI service layer for integration

---

## 🧑‍💻 Built by

**Hussain Shareef**  
Makunudhoo School | Maldives 🇲🇻

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 👌 Contributing

Feel free to fork this repo, make changes, and submit pull requests!

