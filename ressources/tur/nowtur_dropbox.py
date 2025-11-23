import requests
import dropbox
import json

# Dropbox token və fayl yolları
DROPBOX_TOKEN = "YOUR_DROPBOX_TOKEN"
DROPBOX_PATH_ERC = "/ercdn.m3u8"
DROPBOX_PATH_DAI = "/dai.m3u8"

API_URL = "https://www.nowtv.com.tr/api/v1/live/stream"

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_stream_urls():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    resp = requests.get(API_URL, headers=headers)
    resp.raise_for_status()

    data = resp.json()

    # JSON strukturu dəyişə bilər, amma əsas olaraq belədir:
    ercdn = data["data"]["sources"]["ercdn"]
    dai = data["data"]["sources"]["dai"]

    return ercdn, dai

def create_m3u8(url):
    return f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=2500000
{url}
"""

def upload(path, content):
    dbx.files_upload(
        content.encode(),
        path,
        mode=dropbox.files.WriteMode.overwrite
    )

def main():
    print("Token alınır...")

    ercdn_url, dai_url = get_stream_urls()

    er_m3u8 = create_m3u8(ercdn_url)
    dai_m3u8 = create_m3u8(dai_url)

    upload(DROPBOX_PATH_ERC, er_m3u8)
    upload(DROPBOX_PATH_DAI, dai_m3u8)

    print("ERC və DAI faylları uğurla Dropbox-a yazıldı!")

if __name__ == "__main__":
    main()
