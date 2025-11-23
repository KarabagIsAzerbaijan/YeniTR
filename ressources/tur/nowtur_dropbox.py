import requests
import re
import dropbox

# Dropbox tokenini buraya əlavə et
DROPBOX_TOKEN = 'sənin_dropbox_token'

# Kanallar və onların URL-ləri
CHANNELS = {
    'ERSTRM': 'https://www.nowtv.com.tr/canli-yayin',
    'DAISTRM': 'https://www.nowtv.com.tr/canli-dai'
}

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def fetch_tokened_link(url):
    try:
        resp = requests.get(url, verify=False)
        if resp.status_code == 200:
            match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Xəta: {e}")
    return None

def upload_to_dropbox(channel_name, link):
    filename = f'/NowTV/{channel_name}/{channel_name}.m3u8'
    try:
        dbx.files_upload(link.encode(), filename, mode=dropbox.files.WriteMode.overwrite)
        print(f'{channel_name} faylı Dropbox-a yazıldı: {filename}')
    except dropbox.exceptions.ApiError as e:
        print(f'Dropbox API xətası: {e}')

def main():
    for name, url in CHANNELS.items():
        link = fetch_tokened_link(url)
        if link:
            upload_to_dropbox(name, link)
        else:
            print(f'{name} üçün link tapılmadı!')

if __name__ == "__main__":
    main()
