import requests
import re
import dropbox

# Dropbox access token
DROPBOX_TOKEN = "sl.u.AGJHP-QsUSJQYOYCoHbyZllHpCuGXcuBvds67LzjdNdJrNLw7mpivB3zyTdzvMIRyUWb-y5Ccd9XpIeM-8QSPZNd_qgGBmL4yQ7gGc9lDdcuQv95KKQ_cbemQyD82z5LGd271f3IKJCQHmMRmtuj6vH25uNlb8T7X3EAJUMNQdsDn4dzf7thNAWG41Gj1rmA6mRS5gMLUAhohTYoFy1-mhSw7T-rYU2-PFoj3gCMdhc5pRLYEgCLKedp-t1YmywLTO8uft2HN79QidHzQSrE60oeVFP9lunS-lleBkotkTVUDJpACRmrhLr_EZNIyn666LkXcgsBL3kpuZRcAi7ggo_gC5ZbkFJThz7RpASyQfSboBCT_dXWX1Z8BaytH4mzvqPAjwcy6FYVu1CucH55_vKPvyHsaNEorlxa6FvcfXm6V_oaLhlLbBnVxhZQZ7fgnS7Fxo1rhJUbsgylFk3ZasgAG3eUC6U-sdEvuKUrl0syHq86Ux3FhX01fGf6hPgKGIBjcv1e8pQslZoxto_s6IFVAlHLHtGaa2euzKUviAWaCjAaNvCsr7CKR0vAHWq-kuQJxLPidiIL2PTMdkbe1AEI460_-F31tplxO_Ilumj1oPs50H3EF9PhOrGpd_fsCrv1wIOhUseE2WwlJ8BfH0Re1R00Xk9TUul60lD6us7S69TeJWVPQ-v9IRHYRN-ac1Bw9n2ceCC74cL00s2_R0cqkiX4GhmLjgJEfO7eGA1_ecfbsPtqK4LfQnAGX4KtSaNFBxtgRef7I3qURCeP3k6Rfsb-FYB-7Eh-eBA_1DQvDPEDyHaFx3Uvk-kkTkKwcZ06HLkIbokIx_0SZi-asASk3gHynSYOKcgA7ZMekW5Sq4i8OnV4FANsAoWpG768vZMNrvijqFD3VzmApIEvi9FbnuSy5S0Z2-gIMSXxBkxEltgE3KtMHiORKoJWv7adLNtLrM6hoxRBciYJgVCWNKrj1lKCk9uMLcb_7J1u7Q-66XvPnDNV-rLJq9IZh8m3DoeuaBRR6xDd62ttaq_w1ab4sQzNl0z-yHJsd2j2YIgLC--AdimiNgMISftu9Os_tbONWB_eogKWjy_KOQ-J9OfE_TfqJdw8kTomf34i1z9COHOvfxA31S-jr6IZckuaNjG061WLzeGCKaamMeTxkR9oT9IggJXtxzfySTWrpuzEYCju1HT1qHSG1fHcCcjYlZR4HUrbRjs8dp7zbfE9o0Q2q5tewB2u4zRHfCbExJx1USCkWCuPm71Cql9QrFbIK-uPN2gGQc1S4QTSII5J-bGi"
DROPBOX_PATH_ERC = "/ercdn.m3u8"
DROPBOX_PATH_DAI = "/dai.m3u8"

# Source URLs
ERSTRM_URL = "https://www.nowtv.com.tr/canli-yayin"
DAI_URL = "https://www.nowtv.com.tr/canli-yayin"

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_tokened_link(url):
    resp = requests.get(url, verify=False)
    resp.raise_for_status()
    # Tokeni çıxarmaq üçün regex
    match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
    if match:
        return match.group(1)
    else:
        # Alternativ: ERcdn token
        match2 = re.search(r"erUrl\s*:\s*'(https?://[^\']+)'", resp.text)
        if match2:
            return match2.group(1)
    raise Exception("Tokenli link tapılmadı.")

def create_m3u8_content(tokened_url):
    return f"""#EXTM3U
#EXT-X-VERSION:1
#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS="avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5"
{tokened_url}
"""

def upload_to_dropbox(content, path):
    dbx.files_upload(content.encode(), path, mode=dropbox.files.WriteMode.overwrite)

def main():
    # ERC faylı
    er_link = get_tokened_link(ERSTRM_URL)
    er_content = create_m3u8_content(er_link)
    upload_to_dropbox(er_content, DROPBOX_PATH_ERC)

    # DAI faylı
    dai_link = get_tokened_link(DAI_URL)
    dai_content = create_m3u8_content(dai_link)
    upload_to_dropbox(dai_content, DROPBOX_PATH_DAI)

    print("ERC və DAI faylları Dropbox-a yazıldı.")

if __name__ == "__main__":
    main()
