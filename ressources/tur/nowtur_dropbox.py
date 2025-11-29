import requests
import re
import dropbox

# Dropbox tokenini buraya əlavə et
DROPBOX_TOKEN = 'sl.u.AGJSV1m-FltpVzneKyDVpMVtCjJZaKfGR3HGdaKpRfrYWcHRQ6WkT4XUSCj6tYKx-5g_PcbR-VI7hV_eWWy3hJ8GeRB33SL3nNc1f3omm3na-0cOK53fNqoRRCp5ZD0Hy04r36bScyh-oWi6QS4TczIk4MZ3_UX0t4kApZrJF_MHUHlz5WeevjjxSApdZkvli9kNBAc1hAptUVQNtItr_EAF69BEzVnPQjhhzBwUPWs6C6JOGZlEvfrN1RKDlhBkdR3_U2N4mI27b0AMAa7xJ0N9UZWbyf-07s0xLNfYwI6pSu2DcG2gkhBMOPn6UrGu47v_b7Y3IceYkYQDTVq1S0YvQVWlSWDc0HlFWS-hhfTSJEChT8NH67Fy6FSgjbixNf1-s_hJPxI1O6-iI0K6XSzeIL0e79yy09R--bYU98ibzJaKoZRanJONUi1X4C1joFnYlN0ASP11H0QymSU7zFCcIE9KHPQJb24UQjN7EDPDKf78PKvsaHS-El-AfN6Hvt6mUCI_cDlnbxhyeQ0M6zVvy7FWHjpTZ8MC-W1vaRcAmZvE63gJdY2kMj6SOU6ws35ImrFe0j0mIjl90lOMVP1tbjO3MfPrxoSSQ58XTch0Gb4pbZMrqIhE2dPSDCD9LKTFp0mxI6813BS3EbeTzBMBzfzG5JYJY1qJLGzBEeWkR91WOOwed22H8wfW0A20KfevIq542OmqVVHh8Gg0kR3QJenQgtg5V6Jl7ReqsonZmRDw_P43VeHCLsZ5MemJdkH2FqyKi6j3tgPBquDDLNbO4yYMwD8lXFfe1NNLgwSd3RU694SNiZEQC7FUUSilQmRSWhKzKfJ-OWRhuYQefo0rlvbYbG9I5MAGOE5A-XLR2CW0xUK2q8J3-l22qk4qyUKSDMBPSLS0SsufFBsqt3cdHywIN10qvFLYEUCaivbVHF8AjyKqvxdM7dKpjA9z2aOHQ8tr4KoXAkgoEGP3NhM0WsnAK2W4vsmph7PZZnmjLPwdGbhHeqVvhU-K84U5S6l4XdWDj8VUdroXsgtWjmxlAU7EuHFkiu5ggTp06w4cpoFz9YiE3SOUjei1u9QFhwFB4Vjtu2XvIb_IRmWQ-Ym1B09VFewOUUdBWcBX8gR9Dj-6X1lsFYqUS7u5tbO7FiJw0cRKKVl7eZ_01wSf-YKLFA2SNgCTdypTIzw3R57VB-9ecaoxzUNw_FlP8dCtJHbkPzNx6-NR6KU321uEsEcAYvf-TlygACluKdxZCDzfzk1j21BIIUJ9LeMI9pdChDrt4Fq9UZ5xQRv6jBFEfwkJ'

# Kanallar və onların URL-ləri
CHANNELS = {
    'ERSTRM': 'https://www.nowtv.com.tr/canli-yayin',
    'DAISTRM': 'https://www.nowtv.com.tr/canli-dai'
}

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def fetch_tokened_link(url):
    try:
        resp = requests.get(url, verify=False)
        if resp.status_code == 200:
            match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Xəta: {e}")
    return None

def upload_to_dropbox(channel_name, link):
    filename = f'/NowTV/{channel_name}/{channel_name}.m3u8'
    try:
        dbx.files_upload(link.encode(), filename, mode=dropbox.files.WriteMode.overwrite)
        print(f'{channel_name} faylı Dropbox-a yazıldı: {filename}')
    except dropbox.exceptions.ApiError as e:
        print(f'Dropbox API xətası: {e}')

def main():
    for name, url in CHANNELS.items():
        link = fetch_tokened_link(url)
        if link:
            upload_to_dropbox(name, link)
        else:
            print(f'{name} üçün link tapılmadı!')

if __name__ == "__main__":
    main()
