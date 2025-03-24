# iClock-Sync

**iClock-Sync** is a lightweight Python-based tool that fetches and uploads attendance logs from ZKTeco iClock devices to Firestore. Built for seamless integration with school systems like **SchoolSync**, it's modular and expandable to support other databases in the future (e.g., MySQL, PostgreSQL, MongoDB).

---

## 🚀 Features

- 🔄 Fetch attendance logs from ZKTeco iClock devices using SDK
- 🔐 Auto-generate unique document IDs using MD5 hash
- ☁️ Upload logs to Firestore (timestamped, structured)
- 📁 Organized data flow: fetch → normalize → upload
- 🧩 Modular design – easy to extend to other DBs
- 🕒 Future-ready for batch and scheduled syncs

---

## 📁 Folder Structure

```
iclock-sync/
├── core/
│   ├── iclock_connector.py       # Connect to iClock devices and fetch logs
│   ├── normalizer.py             # Normalize logs into Firestore format
│   └── firestore_uploader.py     # Upload logs to Firestore
├── config/
│   ├── firebase-key.json         # Firebase Admin SDK (keep secret!)
│   └── settings.py               # Device IPs and configuration
├── data/
│   └── sample_logs.txt           # Optional: raw backup or test data
├── output_example.json           # Example Firestore log structure
├── main.py                       # Main script to run sync
├── .env                          # Optional env settings (e.g., FIREBASE_KEY path)
├── .gitignore                    # Ignore sensitive/local files
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 📅 Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Firebase & Device IPs
- Place your Firebase Admin SDK key in `config/firebase-key.json`
- Add device IPs in `config/settings.py`

### 3. Run the Sync
```bash
python main.py
```

---

## 🔹 Roadmap

- [x] Firestore upload
- [ ] Read logs from raw text files (manual fallback)
- [ ] Scheduled syncing (with cron or APScheduler)
- [ ] Upload to MySQL / PostgreSQL / MongoDB
- [ ] Real-time sync (socket-based or push)

---

## 📄 License
MIT License — free for personal and commercial use.

---

## 👌 Contributing
Feel free to fork this repo, make changes, and submit pull requests!

