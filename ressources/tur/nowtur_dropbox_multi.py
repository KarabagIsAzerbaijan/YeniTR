import os
import requests
import dropbox
import re
from datetime import datetime

# ---------------- CONFIG ----------------
DROPBOX_TOKEN = os.environ.get("DROPBOX_TOKEN")
DROPBOX_BASE_FOLDER = "/NOWTV"  # Dropbox əsas qovluğu
NOWTV_URLS = {
    "NOWTV": "https://www.nowtv.com.tr/canli-yayin",
    "ERCDN": "https://www.ercdn.com.tr/stream",
    "DAI": "https://www.dai.com.tr/stream"
}
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
            print(f"Tokened link not found for {url}")
            return None
    except Exception as e:
        print(f"Error fetching tokened link: {e}")
        return None

def upload_to_dropbox(name, link):
    if not link:
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    folder = f"{DROPBOX_BASE_FOLDER}/{name}"
    filename = f"{folder}/{name}_{timestamp}.m3u8"
    try:
        # Dropbox qovluğu yoxdursa yarat
        try:
            dbx.files_get_metadata(folder)
        except dropbox.exceptions.ApiError:
            dbx.files_create_folder_v2(folder)
        
        dbx.files_upload(link.encode('utf-8'), filename, mode=dropbox.files.WriteMode.overwrite)
        print(f"Uploaded to Dropbox: {filename}")
    except Exception as e:
        print(f"Dropbox upload error: {e}")

def main():
    for name, url in NOWTV_URLS.items():
        link = get_tokened_link(url)
        upload_to_dropbox(name, link)

if __name__ == "__main__":
    main()
