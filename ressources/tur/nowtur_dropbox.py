import requests
import re
import json
import dropbox

# Dropbox access token
DROPBOX_TOKEN = "sl.u.AGJ1SmE0kpXWl_zIVahqw5HZAGDRDIhF5zGoyczvPka7IzTWbkLRlqaLQSCnrhxqRNqy4h_5NXlupG8bYHiiGPctIxG60Z-RZ8YiE4FKW3TSKDnj7Sv5o4QuxWc5SD_sIF1ynuUZkGKW3p1ffjpNhpmuyhEx3yIemictYRnpjPdIJ-zEJ_wDCUwPD0j3E-_CC_5jNsOui1AESZVowOEQCKZDMzwbChDuBTG2nmuBvZYiiA2aksqZwcOcoTvnYJULty3ec6p5qfDBjjsQU0Y5KqtC39-WsovP8MkLBtiNCogOAsZtdNj-yQR4_pQjcnQjFCpiW9vvpkZFcrTdm19ByZ6BTfTWYJI_VdGWJTe6l_wvww7fWaFPKrmxwqWQ88YMmUUwO1OrG7iaxRw1uSUJASjQ_2FrFRjeI81eF3ACfpkzK0s3SIQ_LRmJrC7uT-rHXRmA3z4ly4JQL4680VxTcsc9oD0DKNQd9uXNVom5yAR_fY6_YTwjmAhpib46psXgbqWrwOai3KqtoB-YBzvqhSnoJz1gEOS-Hps3LIa8O_USJC58UMihKhI2XTfy6qBNoQUqyvtOEL9PVoM1wejmLMMr5MJwPokHUj53P5Gx98OlH-9d0tHYumIfOpzIph5SS6Rs_6NKeKQjjl0DSmHvLIKfRBvoggsY6vThAD2ZWCfmbVrHN8Et8IhpwHpAFiGCuBkH5uiu4V7ZIjj2frlNnuAbgkp22eZSxG_DGjdwUgysqRTZgN7KRbnw0rBhRmoyXmfyocTH84bre5tcRQ5FQA4ep0sg1EFPidazqt0EVqrauDKeVgAYKroBtwL4x0otya3MyVCSEfFWSe4sLlRPxLuBr69-teJDCXnFOcrZ7K4EnLAiHlTmKVy5i5Bb36tM4b51_JoPIun86XGQJ5JLdea3OeuyNMAvx2l_AzVsrLtIMJWcuZDSa0Jjc9RujSQcZRD49yUufysbKiScJSKSHw389glabQEWH0OXsExVTmcI_JxkBjTSjfmPqfiQofRC-HlByaidilCfHz4rx5xB-szecGMC_gVzyZmn2twimSNIb5NVhjDDu8b-N9LRj32ryxu33jsMk2Ph8eUezevy1GS140UxNJKFbAqYI2tGPbu0hgCBPEzWsALlJzELEmCfHFNCvctEmqLCBZXG5UDQCAA-I3ThKeohaBFZeCVF-mYKb2PZQydKUI_DTaajBmAfPHYgj-fF7LKxJp92ADWp6lZ2NY_jawyZFPacjS4pAKQw8TF_HnTkw375S_zGnbvKFEEDDDM-_GKjCY7PBdMCs6GW"

DROPBOX_PATH_ERC = "/ercdn.m3u8"
DROPBOX_PATH_DAI = "/dai.m3u8"

NOWTV_URL = "https://www.nowtv.com.tr/canli-yayin"

dbx = dropbox.Dropbox(DROPBOX_TOKEN)


def extract_token_url(html):
    nuxt = re.search(r"window\.__NUXT__=(\{.*?\});", html, re.S)
    if not nuxt:
        raise Exception("NUXT JSON tapılmadı")

    data = json.loads(nuxt.group(1))

    try:
        url = data["state"]["live"]["player"]["source"]["url"]
        return url
    except Exception:
        raise Exception("Tokenli HLS url tapılmadı")


def create_m3u8(url):
    return f"#EXTM3U\n{url}\n"


def upload(path, content):
    dbx.files_upload(
        content.encode(),
        path,
        mode=dropbox.files.WriteMode.overwrite
    )


def main():
    resp = requests.get(NOWTV_URL)
    resp.raise_for_status()

    token_url = extract_token_url(resp.text)

    content = create_m3u8(token_url)

    upload(DROPBOX_PATH_ERC, content)
    upload(DROPBOX_PATH_DAI, content)

    print("Hazır: ERC və DAI düzgün yazıldı.")


if __name__ == "__main__":
    main()
