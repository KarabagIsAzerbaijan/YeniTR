import requests
import dropbox

# === CONFIG ===
DROPBOX_TOKEN = 'sl.u.AGIrYioX-ZDdpakiGqmPs31bzvpqTSyatPfUhvrNnb2CRTQqk0CW2lTQz5BXrqXUZJdM4K8jdYONGW1WSMKF0KACxGOIGvkwO8w2D7PBLcRvn4VefRMJUHr9XKzrIh9XfBG94sDY3eYBqftuNQpMJoqkgmki1jFa1UWFzCDADl51NVEeY-CBU65yY8-6H1pZMmPxCxxMsiAdqN0LAVhi7e_iAevQ8_IM8b_GcvXdqQuGdX6J-XS1jI-MDXZ7_dYLU8PN-bKFq0LOxtjvqCmyenLzLxGQbjRIrVydPUqyh8HBrM72ciUDowsKKH1quiUln9DSnfnSWvAFHsjAxnQ6OSRehb_OsJXLuOHsVyicpYiB_7btqaar6uW4L78bw_UYNFk7F83zubVCZGWNW7quMTRBBPxEIaqt2aiMZMyw6fA-0esRuiZTd6de-_Swi1nRhjMtFb3O2C_8qu7RbbsjQxCRXxlK9t7Z9mOi536xaIvhrV-lGmVB1wvNZ67_pLRQ2O6l3ZX5iJF2zgg4P0vuzhbdgTFOXleAIY-DtK24ZO7UKxpD4y-AoGFUGqav-U98XXxAvP_yhOv3UjB9IN4W8_RDALcWjzPKNMJN1u-W2po3fr_FfM0xfMo_NqE7FupGiRVSTpdHcsNj3zgP3s5mR3o_4wcfiHsPLOof8zrU8EHn-GUMXtsq3hRsk9ZHbCbzgDZQZpAirJTS0tM98mRIsaCJF8ICUbavZVUhMfyDSwoCklHPQrg172AAMly1z9HcBAqrvy5KOnO31wP301GyN411DFIgz-LYneRv4naP9uCnjHTySzqHuBljLLSUesq9T5sE3Lh4vNT8j6Jw_qGUD91Ikdai1xst3LrXkZpvi75iuZaFKfsSTivztphtEdQUaJGiHTriyWwlW6h6mLKALs8nHWh_eW-TU8ZTijUQuXcO5k3eoohZbqkoC1GpgD6m6k0W9BQha0qmP1_7aGMzbLqgIMeN9ShYphnpcNkNwGSzPK-AXg3S5KGY3VaJHqjywSVZ51x93PH-yDdiO4RX6oDok_moPUSppQRFTX7ZCUi-0nAThWAnRuYOgctfZZuj8-x88ooy1qLwRXRQnDQAFaCinh-iAoSBgS6HJ7ObJrc9UVTEuG9DV0cn0SInj4kmumassDvmEVirWXp4-2K2LauvWWW1mKmI3Eh0ExGq_7p4aZfheaduAIRZ83N7RfKfYehhv1pHWT_GfwTYsbIcRccBMiZrl1RP_Fz3ocf0_hJiEb9gMRSN6_btabypvuYCDfafUtc-sat7t-Q-AZd9Gu-K'
DROPBOX_ERSTRM_PATH = '/ercdn.m3u8'
DROPBOX_DAI_PATH = '/dai.m3u8'

ERSTRM_URL = 'https://www.nowtv.com.tr/canli-yayin'
DAI_URL = 'https://www.nowtv.com.tr/canli-yayin-dai'

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_tokened_link(url):
    """URL-dən tokenli linki çıxarır"""
    resp = requests.get(url, verify=False)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url}")
    match = re.search(r"(https?://[^\']+)", resp.text)
    if not match:
        raise Exception(f"No tokened link found in {url}")
    return match.group(1)

def build_m3u8_content(link):
    """EXO2-mod və DRM üçün uyğun .m3u8 content"""
    content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS="avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5"
{link}"""
    return content

def upload_to_dropbox(content, path):
    """Dropbox-a yazır"""
    dbx.files_upload(content.encode(), path, mode=dropbox.files.WriteMode.overwrite)
    print(f"Uploaded to {path}")

def main():
    erstrm_link = get_tokened_link(ERSTRM_URL)
    dai_link = get_tokened_link(DAI_URL)

    erstrm_content = build_m3u8_content(erstrm_link)
    dai_content = build_m3u8_content(dai_link)

    upload_to_dropbox(erstrm_content, DROPBOX_ERSTRM_PATH)
    upload_to_dropbox(dai_content, DROPBOX_DAI_PATH)

if __name__ == "__main__":
    main()
