import requests
import re
import dropbox
from datetime import datetime

# =============================
# CONFIG
# =============================
DROPBOX_TOKEN = "sl.u.AGKgWFIT84_BVE1qyPeDMi47cOhNCuy7OaQjZSUAP3duvfc_J0d_IQZTC8_T2l65-bQJrId-e9s29cj-GCJjT0N5mWOztUhT1YRoOW2G4pqkkq_lOEUw6c6ZwyHx_4YrYNWC0Zac_Ejtpo88Wnwmy7Eghz5WcUGZ8K_-wzo_-HNwa0bgb-QDe0HXHBZzdrCMrReSTCSz4b_nSp_Umh5eSu2Og05I8g9z6kAaVDeY3x2nkzaxePbw201er1_Pcda6varzzR72Z1P3IYm3oRF_RgsjkSDj7g-N35G8oniQUdAAtwYCIM4wewy9t-fc8wQ0ob9xpFleutbBvfwCh0SEj_dVcLvKh5BpP10Xo2DCNTDVviciFt-3mQDIbyaVteW76xYz3dZquIV4pHihzFEuKGzv4i5OwiGiE7I4dvunP2U6CvMaeBo8LG8mTKb7-q7wrAR068qhP1kscBEr7NfVzTYYiiliOrFxRhDFClybBss6014T9tUESeXP2qQHgRkn6ufxsfi6RsVMif0AmtKtgXfaHaAF4PTMNUUWA5gHw-nUBca03BMs4bUYrN3NLklKUEs3SWLFACLeSgnQ3jtJahE1YHaldUj78i9cDr4ywrYcXWi5IANi6aJMkx6wL1tJw62utLLGqXl3Yk4-89hlrCOLp4d2QAk_au1T8uiq0gqS04inAi4PkVTcknAl9EKE-x9MxFdfSLO8lHR3Zszk8-4RSHytu0Ah7odqdl6avDiodgXA2RU8yBw2NJgsdW8TxSvtgxAojj4YhfrHfv6zPOXEWUtp4v4wI-8b65_9Qkc2JczHW-65TyoRGTltEJctEWM6HkuxgrNoxJeVaR4ZIf4WM2dNSFaib1Z0-fWPRn8yvbGOZ2cOoC52X1FSVLt1DDoiAV3ixAidZHEYGW5RygOn6umO-2ANE60SD0lLqMxEfuVKEwh_N2PTjuvIuXAHdY6-RofnkfqM63a5jD616-KV3Rbomfqa8-WxDEon6URdZplqn6aeMu41PshsGLAR4q_aaxECPO4fTfxae6M5deQ5XHZkooKTEESyg5bALoWREy_y2NnCIk-43H5MM52cMXXcou-l5z0jFXCEOAjB715elOmaHh6vtcFE-GwMVxg1wa19e-7wkhjj_dbWlrMBuwYtQbI4ZlJ0ppm1RV5lm9RVhzzQqQmoA3cWSvi_vDE6MkIsowkQnagiKzzIK1yD1WvgOhji6FgUKA-0fce7zyAweufMfrDgHdM2R3pOTeqtYUJh5zb_QM5caDsndjjE25h9U3uiOf7CKEJKJImoWZQ6"  # Buraya Dropbox token
DROPBOX_FOLDER_ERSTRM = "/nowturk1/ERSTRM/"
DROPBOX_FOLDER_DASTRM = "/nowturk1/DASTRM/"

URL_ERSTRM = "https://www.nowtv.com.tr/canli-yayin"
URL_DASTRM = "https://www.nowtv.com.tr/canli-yayin"  # lazım gələrsə dəyiş

# =============================
# HELPERS
# =============================
def get_tokened_link(url):
    resp = requests.get(url, verify=False)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch URL {url}")
    
    match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
    if match:
        tokened_link = match.group(1)
        return tokened_link
    else:
        raise Exception("Tokenli link tapılmadı")

def upload_to_dropbox(file_content, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dbx.files_upload(file_content.encode(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    print(f"Uploaded: {dropbox_path}")

# =============================
# MAIN
# =============================
def main():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # ERSTRM
    erstrm_link = get_tokened_link(URL_ERSTRM)
    erstrm_filename = f"ERSTRM_{timestamp}.m3u8"
    upload_to_dropbox(erstrm_link, DROPBOX_FOLDER_ERSTRM + erstrm_filename)

    # DASTRM
    dastrm_link = get_tokened_link(URL_DASTRM)
    dastrm_filename = f"DASTRM_{timestamp}.m3u8"
    upload_to_dropbox(dastrm_link, DROPBOX_FOLDER_DASTRM + dastrm_filename)

    print("Bütün fayllar Dropbox-a əlavə olundu.")

if __name__ == "__main__":
    main()
