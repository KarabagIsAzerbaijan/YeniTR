import os
import requests
import dropbox

# Environment variables
erstrm_url = os.environ.get("ERSTRM_URL")
dastrm_url = os.environ.get("DASTRM_URL")
dropbox_token = os.environ.get("DROPBOX_TOKEN")

# Function to download m3u8 content
def download_m3u8(url, filename):
    resp = requests.get(url)
    resp.raise_for_status()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"{filename} downloaded successfully.")

# Download ERSTRM and DASTRM m3u8 files
download_m3u8(erstrm_url, "erstrm.m3u8")
download_m3u8(dastrm_url, "dastrm.m3u8")

# Upload to Dropbox
dbx = dropbox.Dropbox(dropbox_token)

for file in ["erstrm.m3u8", "dastrm.m3u8"]:
    with open(file, "rb") as f:
        dest_path = f"/nowtur1/{file}"
        dbx.files_upload(f.read(), dest_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"{file} uploaded to Dropbox at {dest_path}")
