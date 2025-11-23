import requests
import re
import dropbox
from datetime import datetime

# =============================
# CONFIG
# =============================
DROPBOX_TOKEN = "sl.u.AGK4...sənin_token_daxil_et"  # Buraya Dropbox token
DROPBOX_FOLDER_ERSTRM = "/nowturk1/ERSTRM/"
DROPBOX_FOLDER_DASTRM = "/nowturk1/DASTRM/"

URL_ERSTRM = "https://www.nowtv.com.tr/canli-yayin"
URL_DASTRM = "https://www.nowtv.com.tr/canli-yayin"  # lazım gələrsə dəyiş

# =============================
# HELPERS
# =============================
def get_tokened_link(url):
    resp = requests.get(url, verify=False)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch URL {url}")
    
    match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
    if match:
        tokened_link = match.group(1)
        return tokened_link
    else:
        raise Exception("Tokenli link tapılmadı")

def upload_to_dropbox(file_content, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dbx.files_upload(file_content.encode(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    print(f"Uploaded: {dropbox_path}")

# =============================
# MAIN
# =============================
def main():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # ERSTRM
    erstrm_link = get_tokened_link(URL_ERSTRM)
    erstrm_filename = f"ERSTRM_{timestamp}.m3u8"
    upload_to_dropbox(erstrm_link, DROPBOX_FOLDER_ERSTRM + erstrm_filename)

    # DASTRM
    dastrm_link = get_tokened_link(URL_DASTRM)
    dastrm_filename = f"DASTRM_{timestamp}.m3u8"
    upload_to_dropbox(dastrm_link, DROPBOX_FOLDER_DASTRM + dastrm_filename)

    print("Bütün fayllar Dropbox-a əlavə olundu.")

if __name__ == "__main__":
    main()
