import requests
import dropbox

# ========================
# CONFIG
# ========================
DROPBOX_TOKEN = "sl.u.AGIi96IyqQoR5qHzGds06APEuzq_x1_RjGPHkhhBghDJUMctABEs57p9MnGaqK1-Jw6yq0YIxCyCVvvUOnG7jN9SHFaNmg7ZNbJBC6LGRWEHuqIabzNq4hwo9o9qAVGQJaJR6YLtbFGsFH-hNvHw-GOoaaelxCpttAAwS2GSwZ0dEIzUB0pZkgpReIeSdJNu21NgcaKiwJgOVdMuwePbRm7vOVV95EDbuwm9QQp2xvPp3NREr21jjgQdvWXZUzciO3CWHV9J7HtqUcL-a3RFr6nkHwKWPRY5iZ6oewU05kNOHrp194TMaL4xMkh-upFrt3-e8FXHBDwdZe8GL0bvlgbGlxncKt2qP67_fadGs8kHvT6Ym1elr-g7QqSiaK-JZ9_8eZrXK83d6zJxUcx64RzBoucUXURp2xmcWUJX3FmyZosuXpflan1M_UUWrh2wTpB-SrSJGjuSQ9GVn3EIxKxhfnczAmqAcFvkYyGwpTSmNuYOp7S7Fc7wHYpJOLnnqIRMSDLcs2ob1z5tC10qhFGLCC_P2VmoHV7JMykNKhY_B0CV_leCLPkAaiVmZI5DPmpazKG7gDgyydKJT6za3J6YZCk9odNe-Rf9k_8pKsXdgLYMvrsK2UKb3u3tE_i6kJLHPGsXFylsTPmz4qylHgEOXc_MWP-Lj7kejaggqHDSVOx9mmzYncEPicxY7iZj9SnSMDsdQtnCsxJUPuEPs_aDgYTEFIiD5jxqRVrmRosqSHGKfSTdf9Pj9G_MmdEnPH2-5-_pUx_o79HwNd1a0Moh33YFojHHtS8PzFSvJEUWu9n7ErBTM15rEaTCwASUHkd4vwmUOv2_qYllkDg-fDRZNMN0cDNEDS0Z_kynt0yJ3MFCnbmz7-zKP_dnSjeEcyBQBqqWg0mYmG18YElFLpnevvSSf4uhfDaEXx9loeyv4n1tl1EcXBKgOhz8W_2__kyzOxPOQAbxP3p8dNjjbIjr7lSwxY5Irlr9xLgUa1uJgjOmwDKU2lGP_ZiWqPtOfqVZRwpkV8UPx74kfL8OKPIEXI-PAeVvdHOWvK_2MxFbxZDaz63XeKInndQwNVb72zEsN3LKmdzqeX9Uq9wabcc9Jwm9EhSLSk0vPWkCFiE8rPTV5yT_smVmUm0w0YjypJhXoA5BD0I04rj1N8-XKJ5SlcMMjts9EMZXEftFy7ouWEozZPozK_ZZJ-zFFzgNikbyxC9VyvnXirrX3GaC5yqjorfsLLVRLmleCky-pdjSxLGLvjXpaxsYmAxjzC9kIWFXZG_F7_ZyRYfjwtHI5O4x"
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
