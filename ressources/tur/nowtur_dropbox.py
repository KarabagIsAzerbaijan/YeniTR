import requests
import re
import dropbox
from datetime import datetime

# ==== CONFIG ====
DROPBOX_TOKEN = "sl.u.AG...YOUR_TOKEN_HERE..."  # Sənin token
DROPBOX_FOLDER = "/NowTur"                        # Dropbox qovluğu
CHANNELS = {
    "ERSTRM": "https://www.nowtv.com.tr/canli-yayin",
    "DAI": "https://www.nowtv.com.tr/canli-yayin"  # lazım gələrsə əlavə et
}
# =================

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_tokened_link(url):
    """NOWTV səhifəsindən tokenli linki götürür"""
    try:
        resp = requests.get(url, verify=False, timeout=10)
        resp.raise_for_status()
        match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error fetching tokened link: {e}")
    return None

def safe_filename(name):
    """Dropbox üçün təhlükəsiz ASCII fayl adı"""
    return re.sub(r'[^A-Za-z0-9_\-\.]', '_', name)

def upload_to_dropbox(channel_name, link):
    """Tokenli linki .m3u8 faylı kimi Dropbox-a yükləyir"""
    filename = f"{safe_filename(channel_name)}.m3u8"
    dropbox_path = f"{DROPBOX_FOLDER}/{filename}"
    try:
        dbx.files_upload(link.encode('utf-8'), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Uploaded {dropbox_path}")
    except Exception as e:
        print(f"Dropbox upload error: {e}")

def main():
    for name, url in CHANNELS.items():
        link = get_tokened_link(url)
        if link:
            upload_to_dropbox(name, link)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to get link for {name}")

if __name__ == "__main__":
    main()
