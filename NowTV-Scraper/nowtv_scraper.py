import requests, re
import dropbox

# ===== Konfiqurasiya =====
DROPBOX_TOKEN = "sl.u.AGLYilvjzMzhepko7fN-awdjAzlE2WAhevk5n4bd8uwuw_-nbwLee4vFL1TUlt7Q0494UVFM-gghO-FBpcnDqeicz01Gl9aMtWEffiCvjMWCB8VHaQMDW5wudLgYxfoKaOtpEDUOmkcDcU2dCBrPpbXH6Sv-rTDmkp3_M9U5yT-y1jvy11fgfYhNH4LDzWBGtrpHl95F2jvMamWCeXrVuPbTBm-zZ7laH3opwBqGr1GIwoWpmzEJzlxDuNYvXlTpz85gCZcgvrRTC-w1wSs8jdc5YliMGiQga-RmE_6VX-tXAS254bPfMaU-QfaDlF-QUVsBkamtwdZKZSxOaN6hpCL3Qucz_G76OzT69eRQL3xMIplVte0WXLJzgC8SF-F5NWZtLw47SDLE_KrhHhzZ3pJ9IyDgjdY3O07PxqdSYBTVWmEHbTqB_dskFMcTPMPZ0W8pJsFwHsgywX_uyBzn0y2TthS7ANWsRIeJnbPjAyF-UjIpSzKV_Uauh7rKegP4rPgYZ4fS1wQ2fKsRZ4I8iSYu3eoDeLJFeffqOf5-6sJTYPB7wrTjA6G45OjVd8_fz26BrLYfch80x2oS5X33OTcbyJFAAT4VxNj60BvLRAcyYz7NbBaMEDytOlI034BQElz39-Drz8bCKUDAS6IL5cMV-4KPtGSYalLGbQc8U2Q00IKC99MLgRQoWg3mg8VfIjGueDPQty5yYcuXrXC8CTdWzZXbxY-IZbg0rihxzP2SDAYCr5SZkc1Gg4DDjqTg1oqDmGpkZIkUxdVuziHmoZrLwx98Wlk5WU63KP9aIatSpN0sqf8YiDqMSHpU1fBAr6XyOy_FC-DKNV011seQdWkB8zgGTNvmpQcHKdXDeeQk3aTrppvYhAn-DjBATxqu4ZPrtWUEZxcC_Y7nI6Tt6pFa2nOovSiauBlVHSYCqaykvIPnV7VVNfLgn0BgUhz3LKxQJ7xu9C087Qyi9LI-a9GsIVP-oKhU38v__FsdBmEOs_kjV9avrREsrjUrJ51wMKGM0Jvi5RsGFOud9J-THbqDrgvW2ZSMqnLthpe2cmzeZ5QGZ6MklzaMH6MWGulGUtU6XGCoBkeCTvz7882cJxVQ1UL1HiycutWOl5uaQcUi96mDSzzBp3XZgEOggym0qccSirvxr59AqD0uQ8gOnFDsNz4GjWPZpQzD103CRZzjsW1_v0Hyb9BNCGTiy8e7QMAhxBuXZqeRc9Csx6PVocmkULR0IBgKMOVAOGF4FKIBDcjHQ5F8RZDLwUIQenfuJBtm658kOK8zxXwZOsde0SiZ"  # Dropbox access token
URL = "https://www.nowtv.com.tr/canli-yayin"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ===== Funksiyalar =====
def extract_tokens(html):
    erc, dai = None, None
    m1 = re.search(r"https://nowtv-live-ad\.ercdn\.net/nowtv/playlist\.m3u8\?[^\"']+", html)
    if m1: erc = m1.group(0)
    m2 = re.search(r"daiTagUrl\s*:\s*'([^']+)'", html)
    if m2: dai = m2.group(1)
    return erc, dai

def save_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def upload_dropbox(local_path, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

# ===== Əsas İş =====
print("Sayt yüklənir...")
r = requests.get(URL, headers=HEADERS, verify=False)
erc, dai = extract_tokens(r.text)
print("Tapılan ERC:", erc)
print("Tapılan DAI:", dai)

# Faylları yarat
if erc: save_file("erc.m3u8", f"#EXTM3U\n#EXTINF:-1,NOW TV (ERC)\n{erc}\n")
if dai: save_file("dai.m3u8", f"#EXTM3U\n#EXTINF:-1,NOW TV (DAI)\n{dai}\n")
if erc or dai:
    save_file("multi.m3u8", f"#EXTM3U\n{('#EXTINF:-1,NOW TV (ERC)\n'+erc+'\n') if erc else ''}{('#EXTINF:-1,NOW TV (DAI)\n'+dai+'\n') if dai else ''}")

# Faylları Dropbox-a yüklə
for f in ["erc.m3u8", "dai.m3u8", "multi.m3u8"]:
    try:
        upload_dropbox(f, f"/NowTV/{f}")
        print(f"{f} Dropbox-a yükləndi!")
    except Exception as e:
        print(f"{f} yüklənmədi:", e)

print("\nHazırdır! Fayllar: erc.m3u8, dai.m3u8, multi.m3u8")
