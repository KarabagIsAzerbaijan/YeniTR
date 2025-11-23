import os
import requests
import dropbox
import re
from datetime import datetime

# ---------------- CONFIG ----------------
DROPBOX_TOKEN = os.environ.get("DROPBOX_TOKEN")
DROPBOX_FOLDER = "/NOWTV"  # Dropbox-da qovluq adı
NOWTV_URL = "https://www.nowtv.com.tr/canli-yayin"
# ----------------------------------------

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_tokened_link(url):
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url} : {response.status_code}")
            return None
        match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", response.text)
        if match:
            return match.group(1)
        else:
            print("Tokened link not found")
            return None
    except Exception as e:
        print(f"Error fetching tokened link: {e}")
        return None

def upload_to_dropbox(name, link):
    if not link:
        return
    # Fayl adı: NOWTV_YYYYMMDD_HHMM.m3u8
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{DROPBOX_FOLDER}/{name}_{timestamp}.m3u8"
    try:
        dbx.files_upload(link.encode('utf-8'), filename, mode=dropbox.files.WriteMode.overwrite)
        print(f"Uploaded to Dropbox: {filename}")
    except Exception as e:
        print(f"Dropbox upload error: {e}")

def main():
    link = get_tokened_link(NOWTV_URL)
    upload_to_dropbox("NOWTV", link)

if __name__ == "__main__":
    main()
