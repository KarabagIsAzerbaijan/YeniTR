import os
import requests
import re
import time
import dropbox
from dropbox.exceptions import AuthError, ApiError

APP_KEY = os.environ.get("DROPBOX_APP_KEY")
APP_SECRET = os.environ.get("DROPBOX_APP_SECRET")
REFRESH_TOKEN = os.environ.get("DROPBOX_REFRESH_TOKEN")

DROPBOX_PATH_ERC = "/ercdn.m3u8"
DROPBOX_PATH_DAI = "/dai.m3u8"

def get_dropbox_client():
    """Dropbox client yaratmaq və refresh token ilə avtomatik yeniləmə"""
    return dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

def get_tokened_link(url, retries=3, delay=5):
    """Tokenli linki saytdan çəkmək, retry əlavə edilmiş"""
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            # daiUrl yoxla
            match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
            if match:
                return match.group(1)
            # erUrl yoxla
            match2 = re.search(r"erUrl\s*:\s*'(https?://[^\']+)'", resp.text)
            if match2:
                return match2.group(1)
            raise Exception("Tokenli link tapılmadı.")
        except requests.RequestException as e:
            if attempt < retries - 1:
                print(f"Retrying... ({attempt+1}/{retries})")
                time.sleep(delay)
            else:
                raise Exception(f"Linki almaq mümkün olmadı: {e}")

def create_m3u8_content(tokened_url, channel_name="NowTV"):
    """EXTINF formatlı M3U8 faylı yaratmaq"""
    return f"""#EXTM3U
#EXTINF:-1,{channel_name}
{tokened_url}
"""

def upload_to_dropbox(dbx, content, path, retries=3, delay=5):
    """Faylı Dropbox-a yükləmək, AuthError olduqda client-i yenidən yarat və retry et"""
    for attempt in range(retries):
        try:
            dbx.files_upload(content.encode(), path, mode=dropbox.files.WriteMode.overwrite)
            return
        except AuthError:
            if attempt < retries - 1:
                print("AuthError alındı, Dropbox client yenilənir və retry olunur...")
                dbx = get_dropbox_client()
                time.sleep(delay)
            else:
                raise
        except ApiError as e:
            if attempt < retries - 1:
                print(f"Dropbox API error: {e}, retrying...")
                time.sleep(delay)
            else:
                raise

def main():
    dbx = get_dropbox_client()

    # ERC faylı
    er_link = get_tokened_link("https://www.nowtv.com.tr/canli-yayin")
    er_content = create_m3u8_content(er_link, channel_name="ERC NowTV")
    upload_to_dropbox(dbx, er_content, DROPBOX_PATH_ERC)

    # DAI faylı
    dai_link = get_tokened_link("https://www.nowtv.com.tr/canli-yayin")
    dai_content = create_m3u8_content(dai_link, channel_name="DAI NowTV")
    upload_to_dropbox(dbx, dai_content, DROPBOX_PATH_DAI)

    print("ERC və DAI faylları Dropbox-a avtomatik yazıldı.")

if __name__ == "__main__":
    main()
