import requests
import dropbox
import json

# Dropbox token və fayl yolları
DROPBOX_TOKEN = "sl.u.AGKD4Yljk4YTSxZAKrRIrVv6h_X3X7pVWAahld7IUd6-X9iJCpTGqRBOXSug8m6L70XvL4_pwPPvGeV12w5ugXzVe5xy1f8EFg_i4xHUge6qgqLN2eyWDwJE47MlbNP3eMQ0FiegQAbA2fgduGbUswUPT7NYCDi9Bn2qDftHQdqkNxOtS5YnURySg5x8F7UwxQs17JIitSpXWpS9LdvdCND6LqdyZv03lc4ltMYGEGEpjDQHqjFfAAgEaAeBQl22t43Lz4DdgXgenERZGxJJZu1nc8iPT1crbut5EtehsgqrwcuxQ9XEdex4mEV68Egxdcx3Hr0d_iw0NBn7-KjV9RrLNZWXxkOhBAnllYKy0HJIkvyvNGA-HONxvYCPn-qTtY4oEYqCx3oEn9JcSJVVq2B4th9OxYlZpcpRpWZCk27zQLgExOnu7UqVbG45YtdH50ebs-a2Lqijr5SodQhKeZdq3FftTH_OW6Qs4ahn00_xwpLT7ye7ZBqXZMa0PGqPQ9lv9jLnBIPXAvamDIEIJCE0BASaOVakfH03ZQ-XH3R54jb6maBhLsbp9enwdhddpe4tnzhaXOd2uFAAKPiD1NJFsJTKMsv4Hs9xaDU9xnWX5IgaTCezXxm5VvK3pLVu8u0WMxpN0QBi2-C6pT9MLJxL2XNlqliHPZzMtuBqKop3_sI5tk5D1B5I__JEA9_fuBOZsQnDLwXRTbaw7BpG0ucJj9qpxKX1IirgTZqlzf2G6GBm_ldkWmTfoOKbRNthflOgpw0ioh3YqPaQbadk6BKvrxqoOYauDobLw1VC0xD7oH-e6mXT_6Mdit7HUd5tRd0_WIbd452bV8IrDfRnDxSxP3zzo--XDIMpzC_B86N38vBwqzOAU-E9J2ZxlluxJV20Ss2QSW-nd0HiYco2e8frCZpe-V9UJ0uN-MN-GRTW_iZ31H6UAgdAIsiPVGDPWGwFJcUI8D-a80ey8Maan4Wf2jOSLQuTWFjyVmlSxwlcxrS9REVut8uZAz-unS7RxruU3Ic_Z-lh8Io2ywLzvjJZ4iW-yLzfZA--pWu9dJF9EnONa6jE-U4GivVYGgAnDDF3ToyoIum_q7qohlSSrUTieyLM0yL58PPJJYcuu5tux0Lrvz4z0xz4J1AZvOebRC-Yal0Zx5NI-8UpRZyovLwzF4pI58u0P6A8RiW2uQH7KlRnwFqR9FrTop2ZGX1hc8eZNC7XawCcnY-HY4BLngBs-GX8ShtZ0F1uOIXIuHJIVuWTuzeyPXe-SA62hS-2l7fUYgETx2I4vjBpBrSjHaef"
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
