import requests
import dropbox
from datetime import datetime

# ==========================
# CONFIG
# ==========================
DROPBOX_TOKEN = "sl.u.AGINH3siOpXt5hRkFvEop8UU2JKz81O0dGZirMIAwTgJLidHm7--mQTudeRK3aJXVSnRe5mwcd4U9SlQ8yNewxLJn5S6uCqcHowuZpflEqioKXIJ2Gz4t15LeRhG-SlnbwrrP2aEPHVI39s7A1GpNQyK4ja5u4nDWOooC87rkoEDmukyZHKKR2JeGKKVXtP58JVrWP2UqpmiarxExJuHW7oBIlcq59abqWqM2dgki4XNvn7rrhfPkp1E6gO85k9ni26oOLfSdnsjVDaEijk-PxyFiMm123C-awvjBdRZrvslmVtk85iWl7N8cP3Vewjr55sbxQPkqka92wStntFkk6AV4PIl_uw10Y0p_Hj7viaIIJFNFuqZjU7MGxcxgRgt0b4NA6X0jGhqMqRZ-4W6V9JAXWJOCK4x8z2rlvw7SR_w6AGULNoJW90IotHomhCkbPwjl2_EPG1XIjsggswi90Yawjq5cPUlTK_LMe4spDkQ8QUMZYpyXscmBaP6JBVwDFao778qrk_d25563lA-pYHBiAcwYAgY1y1XaewWiYvYqdFzQJgK_jGl5Vl9eITnROPZtEEN5xKv6RgLq224iTQ1lS2h3GpdprCrsBcGOZr-hPMfj9CUQA_2Y5XM9_5CrLrrizb_vtLM41vn2_AT6n_uQvMfhiY52VISBm0O1ruSJjelOFigDmJBvDzriMavbqAxAn6Yo8aT69zCXw_EtdB24uYZDLUsQbz58Y0XEnbz-5nOMH2GKX12iCwfNFSVMRH9u5O0A8ohmI9li6456Cv1B8lJhA2Bz7J9sI_Y3uvFmWWl_sHADGKjgWnXCreIcKTK9Gg8vZhhv484DolaqQbDRx4RHgkJOek6XHkL5N_3aqhl0mPwHgrC59WSDtHqVZaU_V47bBW_6eg06FkRXW-ezg8v2z7qZ9J5PxzX9W0cgoozHtWqFyfc8YIxtFPAfMHUC08TbmtekM1hHVfXKIY3h_ZVho1zQq3_e43gCx7rGM1yYwbKRCud4aPfXATBTNVggP2GTgXQi0Y-9snBVBkiFfSY3wTwnHkSoXdBdtbkSuV2yCsK1AOMCTMNPLTYse6NGKYtJrVThV2nVUcjKAjh3lJnbVToyXnpAYsZ2fUCdPga_OaEQMA01PIK42Lx7cR4mvn82TFZIDjczM7ubiR-zhWyYnsKLUUggRvQ09OYAf3prt6V9uMwH_LC12CYBuZawMqLvNizPPbEZtXDbUXX9VGQoYdzo1AMLa0QMOSwuPurfztZLob0yVuX1r0lPdj9nwKVcxmxk642i4VrisSo"
DROPBOX_ERSTRM_PATH = "/ercdn.m3u8"
DROPBOX_DAI_PATH = "/dai.m3u8"

ERCdn_URL = "https://www.nowtv.com.tr/canli-yayin"  # ERCdn üçün ana link
DAI_URL = "https://www.nowtv.com.tr/canli-yayin"    # DAI üçün ana link (lazım gələrsə dəyişdir)

# ==========================
# DROPBOX CONNECT
# ==========================
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

# ==========================
# TOKENLI LINK ALMA FUNKSİYASI
# ==========================
def get_tokened_link(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code == 200:
        import re
        match = re.search(r"(https?://[^\']+)", resp.text)
        if match:
            return match.group(1)
    return None

# ==========================
# M3U8 FORMATINA YAZ
# ==========================
def build_m3u8_content(tokened_link):
    content = "#EXTM3U\n"
    content += "#EXT-X-VERSION:3\n"
    content += '#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS="avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5"\n'
    content += tokened_link + "\n"
    return content

# ==========================
# DROPBOX-A YAZ
# ==========================
def upload_to_dropbox(filename, content):
    dbx.files_upload(content.encode(), filename, mode=dropbox.files.WriteMode.overwrite)

# ==========================
# MAIN
# ==========================
def main():
    # ERCdn
    erstrm_link = get_tokened_link(ERCdn_URL)
    if erstrm_link:
        er_content = build_m3u8_content(erstrm_link)
        upload_to_dropbox(DROPBOX_ERSTRM_PATH, er_content)
        print(f"[{datetime.now()}] ERCdn faylı Dropbox-a yazıldı.")
    else:
        print("ERCdn link alınmadı.")

    # DAI
    dai_link = get_tokened_link(DAI_URL)
    if dai_link:
        dai_content = build_m3u8_content(dai_link)
        upload_to_dropbox(DROPBOX_DAI_PATH, dai_content)
        print(f"[{datetime.now()}] DAI faylı Dropbox-a yazıldı.")
    else:
        print("DAI link alınmadı.")

if __name__ == "__main__":
    main()
