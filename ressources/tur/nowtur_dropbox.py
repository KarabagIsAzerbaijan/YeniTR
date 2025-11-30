import os
import requests
import re
import dropbox

APP_KEY = os.environ.get("DROPBOX_APP_KEY")
APP_SECRET = os.environ.get("DROPBOX_APP_SECRET")
REFRESH_TOKEN = os.environ.get("DROPBOX_REFRESH_TOKEN")

DROPBOX_PATH_ERC = "/ercdn.m3u8"
DROPBOX_PATH_DAI = "/dai.m3u8"

def get_dropbox_client():
    # Automatic token refresh
    dbx = dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )
    return dbx

def get_tokened_link(url):
    resp = requests.get(url, verify=False)
    resp.raise_for_status()
    match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
    if match:
        return match.group(1)
    match2 = re.search(r"erUrl\s*:\s*'(https?://[^\']+)'", resp.text)
    if match2:
        return match2.group(1)
    raise Exception("Tokenli link tapılmadı.")

def create_m3u8_content(tokened_url):
    return f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS="avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5"
{tokened_url}
"""

def upload_to_dropbox(dbx, content, path):
    dbx.files_upload(content.encode(), path, mode=dropbox.files.WriteMode.overwrite)

def main():
    dbx = get_dropbox_client()

    er_link = get_tokened_link("https://www.nowtv.com.tr/canli-yayin")
    er_content = create_m3u8_content(er_link)
    upload_to_dropbox(dbx, er_content, DROPBOX_PATH_ERC)

    dai_link = get_tokened_link("https://www.nowtv.com.tr/canli-yayin")
    dai_content = create_m3u8_content(dai_link)
    upload_to_dropbox(dbx, dai_content, DROPBOX_PATH_DAI)

    print("ERC və DAI faylları Dropbox-a avtomatik yazıldı.")

if __name__ == "__main__":
    main()
