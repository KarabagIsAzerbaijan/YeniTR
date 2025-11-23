import requests
import dropbox
import re
import warnings

warnings.filterwarnings("ignore")  # HTTPS sertifikat xəbərdarlıqları üçün

# ====== CONFIG ======
DROPBOX_TOKEN = "SƏNİN_DROPBOX_TOKEN"  # buraya tokeni qoy
DROPBOX_FOLDER = "/NOWTV"
DROPBOX_FILENAME = "nowtv.m3u8"
DROPBOX_PATH = f"{DROPBOX_FOLDER}/{DROPBOX_FILENAME}"
NOWTV_URL = "https://www.nowtv.com.tr/canli-yayin"
# ===================

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_tokened_link(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", response.text)
        if match:
            return match.group(1)
    return None

def upload_to_dropbox(content, path):
    try:
        dbx.files_upload(content.encode("utf-8"), path, mode=dropbox.files.WriteMode.overwrite)
        print(f"NOWTV link Dropbox-a yeniləndi: {path}")
    except Exception as e:
        print(f"Dropbox-a yüklənmə zamanı xəta: {e}")

def main():
    tokened_link = get_tokened_link(NOWTV_URL)
    if tokened_link:
        upload_to_dropbox(tokened_link, DROPBOX_PATH)
    else:
        print("Tokenli link tapılmadı!")

if __name__ == "__main__":
    main()
