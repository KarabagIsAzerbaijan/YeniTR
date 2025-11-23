import requests
import dropbox

# ========================
# CONFIG
# ========================
DROPBOX_TOKEN = "sl.u.AGJPU18venTaQGah4_ye8x2qDXLCWmYrOSD8bqDzsB9TPSrOwfbpjKRVKjhhd_tpqK9HUkBHznxy-4CGqRis4cws8vgLp6QBiuJjt4iXmFfe0wf9SFcIlxiTB8a9QqMM6E0_cAdl9LKlM6P_Htxj9v7fayG1dc8tcOBLNORuBJ2ZpMOZAt_3WVSc0I68LT5aUlXxQOP5h6dUg0S3SH1ZfB480ksk62VFHDkbCzYhrny1NRtAPoTCVZYkmSrSvfvPXld6pM0inI4xom8WzFwYuJO-rxFzMvrPHUU8OQ70nZqRoJYGNfcAr1EZQjaMW8Lj6dDplu2nfPpSH5dzf8tXLS3KD4OnZs0sAY6bUg-nSYZ8KQ5ptG7XbTa5vWrrZlSoU5HWo-7G_f17Hz6n6Q5sqUvHYSD1_e87dbPr6baw-r2T1XzUEQxwWWSr9IP_Oj1UEZ_LzcpAPRegK1Y0txX5jt_ajnqyYQAkV-8cwcZH2845E72RVMnOXxzWh--iszXo_ugpDUo9uxrrtIoclP72-0W6gLNW-Jj-rNT5SSfs_RQUOmoXTGISmetr899yAyefo9qKZ4RExmkpe129qU1UK3XkySJy6t6EfHZf90ng6vahrj0nmAkZYAvimWkLhYzbtbm4gUAmby5FJLIaeS8KmGZ3t55RoSA0cYJduWD2zo84JC912XYtutAL0jZOjA34dpPQmWNNrAHsLYvJd-g_4CD4gi3tGzM1tK1mS6sf3-Z9LvbA1wxppqcGGWlCw5qTFJeuvhM2U-UFY_YTEKHOd1tW3nHg0KwpTsSFoe7_BaElvi-LdSH72IGzDnparKbRB_bqT_qAo9li-Co2-GB9kqxw6By5JIuvj9bzG1Aul5eqgk8qGtADrUO1htrw25eiCmzlpC20Ic25-2kcplcHF71BSA5aGAnI2biUn2fGldRrfNQQpLA_caaOLo_w8fNtjFaggt1tFsrpNQXyJferiuHkCLgKdE31Qy4_GiYMWMahzUAYumfjgjcWeEfw-98yYHOkl5HDWRjv0psctUy39QkxYIjVbUTWEIkyeB2jzogc1U02BtBAU5yv9tJ0LDzYhc5RCR3frO1ex9Wto-L8LbH2o6YeJgfx0Q4R38Agl7cMewNq0vVvKwCGWMbooFYiFQt3_41zd-Sp7qQaQOpelJe7FDxJFzWQNddptRxFn8zeF3pUG-ix2aFTtKyBqrhG6YKVdPwFCfYtk9wEWEMd1bN3kyetxxXI7VHjCD6u3Qe8yJ7nV5R0E1LifMF_KTGKyp3cBEV0sYLLbRIJrqefEGGp"
DROPBOX_PATH = "/nowtv/nowtv_playlist.m3u8"  # Üst-üzərinə yazılacaq
ERSTRM_URL = "https://www.nowtv.com.tr/canli-yayin"  # ERCdn
DAI_URL = "https://www.nowtv.com.tr/canli-dai"       # DAI

# ========================
# FUNCTIONS
# ========================
def get_tokened_link(url):
    """NOW TV-dən tokenli linki götürür"""
    resp = requests.get(url, verify=False)
    if resp.status_code == 200:
        # regex ilə linki tapır
        import re
        match = re.search(r"https?://[^\s'\"]+\.m3u8", resp.text)
        if match:
            return match.group(0)
    return None

def build_m3u8(ercdn_link, dai_link):
    """.m3u8 faylının multivariant formatını yaradır"""
    content = "#EXTM3U\n#EXT-X-VERSION:3\n"
    if ercdn_link:
        content += '#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS="avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5"\n'
        content += f"{ercdn_link}\n"
    if dai_link:
        content += '#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS="avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5"\n'
        content += f"{dai_link}\n"
    return content

def upload_to_dropbox(content, path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dbx.files_upload(content.encode(), path, mode=dropbox.files.WriteMode.overwrite)
    print(f"Uploaded to Dropbox: {path}")

# ========================
# MAIN
# ========================
def main():
    ercdn_link = get_tokened_link(ERSTRM_URL)
    dai_link = get_tokened_link(DAI_URL)
    
    if not ercdn_link and not dai_link:
        print("Heç bir link alınmadı!")
        return
    
    m3u8_content = build_m3u8(ercdn_link, dai_link)
    upload_to_dropbox(m3u8_content, DROPBOX_PATH)

if __name__ == "__main__":
    main()
