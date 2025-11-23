import requests
import re
import os
import dropbox
from datetime import datetime

# Dropbox token və qovluq yolları
DROPBOX_TOKEN = os.environ['DROPBOX_TOKEN']
DROPBOX_ERSTRM_PATH = '/nowtur1/ERSTRM/'
DROPBOX_DASTRM_PATH = '/nowtur1/DASTRM/'

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

# Funksiya tokenli linki əldə etmək üçün
def get_tokened_link(url):
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code} error")
    match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", response.text)
    if not match:
        raise Exception("Tokenli link tapılmadı")
    return match.group(1)

# Funksiya .m3u8 faylını yaradıb Dropbox-a yükləyir
def upload_to_dropbox(name, content, folder):
    filename = f"{folder}{name}.m3u8"
    dbx.files_upload(content.encode(), filename, mode=dropbox.files.WriteMode.overwrite)

def main():
    url = "https://www.nowtv.com.tr/canli-yayin"

    # ERSTRM link
    erstrm_link = get_tokened_link(url)
    upload_to_dropbox('ERSTRM', erstrm_link, DROPBOX_ERSTRM_PATH)

    # DASTRM link
    dastrm_link = get_tokened_link(url)  # əgər ikinci link fərqlidirsə, burada ayrıca regex və ya URL qoy
    upload_to_dropbox('DASTRM', dastrm_link, DROPBOX_DASTRM_PATH)

if __name__ == "__main__":
    main()
