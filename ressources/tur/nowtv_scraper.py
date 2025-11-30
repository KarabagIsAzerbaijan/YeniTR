import requests, re
import dropbox

# ===== Konfiqurasiya =====
DROPBOX_TOKEN = "sl.u.AGKrJeBEeaHK-87mutJAZLf3zGqPsR7viX6CLnghdbZIlDfbqhR0n7IbF70Z9vTJp5UrIELOsIUKCQiP8WhydgRidX2BcBdjkv73QlV0oM36DlxnfOL9Q2GWYbw_eZNybIkOw-AwMmDLIsbqhsKcDMJisZEoc9-pZ1U8dNk808JIW7eIb5lKuk2wW4tElTXlc2h_9WLIkmPphVrNx6IiKDribnM2zzrGWrBNx9hgaOGrwEcsJ1K1gYAT5u7witP6cpoSKABtyzDL7pj4yeCWUba76oXruQ2-_yLnPAU63ERmofLKwVDmaU8fyy5oQuS-LkPpm5g93EdcM_Lf6KlF22qg7Ks8xJiR33eaFo1bRiOZD_XH5j5hKQfjVrWheeA77bye1ghzU5aOoFQLS7evuMu77rLdTyU6g7uRkhzrWzqQGLE5ITdVM6pp-orFSyaMhI0rAD5FACvK_-9rek2OIdyuSUfX0Iuv2dFeXu1tVOeJIaliC4IOX5TSrO15a1rNclFauRf3jf59M7c8ckCQV1d2epM3vt4Z2wvgntfxabCy-VzUhccaUarM68NQHpsI2a3Iqz_tNoqkiydshxr1JV6nS2O9LtP_Kncno_aHrAPVYQlFKczRWOXUX8h7G2k6iEj4vgz9F4-toOdlt_w-DyQ9MinNQmtd5UDl5Jvw8_lkVGfNuhmCtvOxFmL_cXQR8EXU4idQ2iLp7MqAnAIWyJSwh-krSqkfKPmn6zPgRugFVjJoQ8k_jhU8WiP2Kslcbb2B6TUa-xYOKHS79OEywNNwo4aG_pzJ2KcZ0Il79AjALWDAbKfBkYjLM-18xp03LBAHrs_tstEi33eKEDTvUnSrcPkudzqmzgkqXhuR7dIqHsh_NzCw6wgvD706O2iSbSZkQ04u7F0yXilQ8n0IuxnJrxLKc4jOF3SeLIDLTxQkjMY4V0AFOUpZEO9kZ7vRqRVgoAFMnXjTjexzV6Z59GDM-R2TtyUcfyF57PTFUm7pVUvZpDN6edwCo3J0RhP3EGL7NWOrVk8d7Q83DxSgLSW6frpRt6Hwd1VlPmdbNlRCzptJSvcjMF61vwyIxGuBKnDV998-crhCND6fwTECRpdP1FWjdVXcvTPBWpYj7vukOTCcpKsUcHX1jtFR9TnG-d3qpqDYXJwGQtLIOoBvkiGGPJ4gesKPCKwZjQ2Qo3PCyf_bK-kNKKy41t00_Z9jSWaRi7Eyypstl1mGFFF2pLYKNBGx2HTC1mFCPz9bvKZ_k79419IK2znua-g7WnmpHOBo0-4vMImjiEgMVhDyQKNE"  # Dropbox access token
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
