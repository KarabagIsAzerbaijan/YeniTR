import requests
import dropbox
import time

# ====== CONFIG ======
DROPBOX_TOKEN = 'sl.u.AGI7QOF-nGw-SqxF0l-cqJKGQZuYlzyMNFLPxRsBYQOkaT1ghRGIjhFqcdqKogSgnz6wjG3Tp6YH0r9lO8k2eAtyTngt4ouPk4C1HYJrDwq_k7nbZfosEJqs-VAC3ybFGuafr4RdvvjXCvblH2Em7kiasZtrDBcRWQtr8LJt_arJIf_CEIeSyfPHRYBSEfGAWLV1vFnSZupDMSnHOXonxnzBWChc3cmHqBD_6mUdwag7HDCFwR3vruZOtJQ8IH3eOtemjYUij0IX-m2XBdSjaQOO7K_uQ13xNmp0VpJJe8O44cbSvSAcEsKp1NCgajGhoqjyfR0hr8u_IvBTjKDG1igRgJbxhxQX2UKBKE1e0Nuvk6XP-zLWTQojJsJNg3K_Iz6H-jQxao39lYYCcAaz0PIQWAJ-9u8jXayZQuMv5WGloefD9pl6c8jc4NoFJlHWm7k0aECSIiKIkmnkpjHIp0PbiSYWS4oh1sMF6DDYtXpW1fqJWOkySgSMkdIbR3X8N9nFSEKVCMmmwizhqZoH_RE5OT7FMEOQmRxLKZv9jYllgKuVMRzjRrlWinZLgc8tXWTnUHMsZK5D6Wb3PjfpuPguqIs-Voe8jO0sot79KCrfN38pB6zTZHDSKcllMRCfly5ru9mV5hMRMhFvYVFiZn2LyL_5dJR7QUQEjAACpVmswjtUsZ-k_tjqRN5N3xOnI_b6EBO3_hJGXBRIwQ_z99htKJciwejM2UM_K3zrXtGZIUZPMLNhPfhDuLl9VeeWi-0fvgRl0B8JpZNvHkrse6vc5-0lwZVPR299AaSnnao1h9sIhlIfOFav5wqYqQLS4Ho1vU3MjchgfMD1Bzb19lgp5v537Jb_ruHMeWDe6q-Xaswy63HmdC5MRXG6rLkwzA356m-RSLITcbJT_b8OfXuVq0rPNyuUb9xokahplvE4MKcLtjdV215eblaheCj94-zFMY_BbMd-87w-2sx1sCnbzOx1D_w9Uj3V01G33mOaIDcxnVJBiivJmFkdkm5J0ieHYxDzjVYP4jPbTp3re5ILwt7etx4APriJdvzUdvNAKmt88HneRjiO63avaLfseNnnSL-7sRj3dbjSti2iVS0MbWXX1EiEBPmssywGEudFFhl0QgZOvvENgIaVVB3sXnSXzOeNEiwHDdaGAa_twMKbbFHf-p8oreo_Hhv2M54heej7LIvCjrd5K6fZj8529As9u3SRUMDKI5sGk6qqNoabUNa_uyTkWWkTfoa0QHr66TVjXLLdsz3TvJOq4fJ4H1X5n2EorHyhzAgMf8m_wL4T'
DROPBOX_ERSTRM_PATH = '/ercdn.txt'   # Dropbox-da yazılacaq sabit fayl
DROPBOX_DAI_PATH = '/dai.txt'        # Dropbox-da yazılacaq sabit fayl

# Tokenli linkləri götürəcək saytlar
ERSTRM_URL = 'https://www.nowtv.com.tr/canli-yayin'  # ersite tokenli link
DAI_URL = 'https://www.nowtv.com.tr/canli-dai'       # dai tokenli link

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_tokened_link(url):
    print(f"Fetching link from: {url}")
    resp = requests.get(url, verify=False)
    if resp.status_code == 200:
        # Sadə nümunə regex; lazım olsa dəyişmək olar
        import re
        match = re.search(r"(https?://[^\s'\"<>]+\.m3u8[^\s'\"<>]*)", resp.text)
        if match:
            tokened_link = match.group(1)
            print(f"Tokened link found: {tokened_link}")
            return tokened_link
        else:
            print("No tokened link found in content.")
            return None
    else:
        print(f"Failed to fetch page. Status: {resp.status_code}")
        return None

def upload_to_dropbox(name, link, path):
    if not link:
        print(f"No link for {name}, skipping upload.")
        return
    try:
        print(f"Uploading {name} to Dropbox: {path}")
        dbx.files_upload(link.encode(), path, mode=dropbox.files.WriteMode.overwrite)
        print(f"{name} uploaded successfully.")
    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API Error for {name}: {e}")

def main():
    erstrm_link = get_tokened_link(ERSTRM_URL)
    dai_link = get_tokened_link(DAI_URL)

    upload_to_dropbox('ERSTRM', erstrm_link, DROPBOX_ERSTRM_PATH)
    upload_to_dropbox('DAI', dai_link, DROPBOX_DAI_PATH)

if __name__ == "__main__":
    main()
