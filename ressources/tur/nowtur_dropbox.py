import requests
import re
import json
import dropbox

# Dropbox access token
DROPBOX_TOKEN = "sl.u.AGJHP-QsUSJQYOYCoHbyZllHpCuGXcuBvds67LzjdNdJrNLw7mpivB3zyTdzvMIRyUWb-y5Ccd9XpIeM-8QSPZNd_qgGBmL4yQ7gGc9lDdcuQv95KKQ_cbemQyD82z5LGd271f3IKJCQHmMRmtuj6vH25uNlb8T7X3EAJUMNQdsDn4dzf7thNAWG41Gj1rmA6mRS5gMLUAhohTYoFy1-mhSw7T-rYU2-PFoj3gCMdhc5pRLYEgCLKedp-t1YmywLTO8uft2HN79QidHzQSrE60oeVFP9lunS-lleBkotkTVUDJpACRmrhLr_EZNIyn666LkXcgsBL3kpuZRcAi7ggo_gC5ZbkFJThz7RpASyQfSboBCT_dXWX1Z8BaytH4mzvqPAjwcy6FYVu1CucH55_vKPvyHsaNEorlxa6FvcfXm6V_oaLhlLbBnVxhZQZ7fgnS7Fxo1rhJUbsgylFk3ZasgAG3eUC6U-sdEvuKUrl0syHq86Ux3FhX01fGf6hPgKGIBjcv1e8pQslZoxto_s6IFVAlHLHtGaa2euzKUviAWaCjAaNvCsr7CKR0vAHWq-kuQJxLPidiIL2PTMdkbe1AEI460_-F31tplxO_Ilumj1oPs50H3EF9PhOrGpd_fsCrv1wIOhUseE2WwlJ8BfH0Re1R00Xk9TUul60lD6us7S69TeJWVPQ-v9IRHYRN-ac1Bw9n2ceCC74cL00s2_R0cqkiX4GhmLjgJEfO7eGA1_ecfbsPtqK4LfQnAGX4KtSaNFBxtgRef7I3qURCeP3k6Rfsb-FYB-7Eh-eBA_1DQvDPEDyHaFx3Uvk-kkTkKwcZ06HLkIbokIx_0SZi-asASk3gHynSYOKcgA7ZMekW5Sq4i8OnV4FANsAoWpG768vZMNrvijqFD3VzmApIEvi9FbnuSy5S0Z2-gIMSXxBkxEltgE3KtMHiORKoJWv7adLNtLrM6hoxRBciYJgVCWNKrj1lKCk9uMLcb_7J1u7Q-66XvPnDNV-rLJq9IZh8m3DoeuaBRR6xDd62ttaq_w1ab4sQzNl0z-yHJsd2j2YIgLC--AdimiNgMISftu9Os_tbONWB_eogKWjy_KOQ-J9OfE_TfqJdw8kTomf34i1z9COHOvfxA31S-jr6IZckuaNjG061WLzeGCKaamMeTxkR9oT9IggJXtxzfySTWrpuzEYCju1HT1qHSG1fHcCcjYlZR4HUrbRjs8dp7zbfE9o0Q2q5tewB2u4zRHfCbExJx1USCkWCuPm71Cql9QrFbIK-uPN2gGQc1S4QTSII5J-bGi"

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
