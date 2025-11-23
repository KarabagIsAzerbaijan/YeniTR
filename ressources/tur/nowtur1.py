import os
import requests
import dropbox
from urllib.parse import urlparse

# Secrets vəya environment variables
ERSTRM_URL = os.environ.get("ERSTRM_URL")
DASTRM_URL = os.environ.get("DASTRM_URL")
DROPBOX_TOKEN = os.environ.get("DROPBOX_TOKEN")

# Dropbox qovluqları
DROPBOX_ERSTRM_PATH = "/nowtur1/erstrm/"
DROPBOX_DASTRM_PATH = "/nowtur1/dastrm/"

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def download_segments(m3u8_url):
    resp = requests.get(m3u8_url)
    resp.raise_for_status()
    lines = resp.text.splitlines()
    ts_links = [line for line in lines if line and not line.startswith("#")]
    return ts_links

def upload_to_dropbox(ts_url, dropbox_path):
    filename = os.path.basename(urlparse(ts_url).path)
    resp = requests.get(ts_url)
    resp.raise_for_status()
    dbx.files_upload(resp.content, dropbox_path + filename, mode=dropbox.files.WriteMode.overwrite)
    print(f"Uploaded: {dropbox_path}{filename}")

def process_stream(m3u8_url, dropbox_folder):
    ts_links = download_segments(m3u8_url)
    for ts in ts_links:
        upload_to_dropbox(ts, dropbox_folder)

if __name__ == "__main__":
    if ERSTRM_URL:
        process_stream(ERSTRM_URL, DROPBOX_ERSTRM_PATH)
    if DASTRM_URL:
        process_stream(DASTRM_URL, DROPBOX_DASTRM_PATH)
