import sys
import os
import json

# 🔧 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.utils import load_uploaded_doc_ids, save_uploaded_ids_cache

# ✅ Ensure cache folder exists
os.makedirs("cache", exist_ok=True)

def main():
    doc_ids = load_uploaded_doc_ids()
    if not doc_ids:
        print("⚠️ No doc_ids found in output folder.")
        return

    print(f"🔍 Found {len(doc_ids)} uploaded doc_ids in output/*.json")
    save_uploaded_ids_cache(doc_ids)
    print("✅ uploaded_ids_cache.json created in /cache")

if __name__ == "__main__":
    main()
