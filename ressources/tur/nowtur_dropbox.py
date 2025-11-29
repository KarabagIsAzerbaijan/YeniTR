import requests
import re
import dropbox

# Dropbox access token
DROPBOX_TOKEN = "sl.u.AGL5nJRI1Ff2rZ_3e5igLIb70rbKHTwmvVkF47zvT63y71IrPjsYsK0SemwUT4NhuSAZ_7EdgnNCq1eMCTn4hkjmNG2YzXF-k_g-4db-_Uy9H3DrwQ8nP-a7WFhZDq2jVzJtu7XL6C9qsCq4yq2lJ56tNN_L2mSl4wIVtjqzkNQXHxFl6WQBvyFbwAo-F7ZBC2_YKqV3ULuIeAQRXWnbHpH-brlz0iocMaHzV8i2K5_Q-VvkFzPjeaWs8hPzcf0LaHbWZQ5aK3uE4iIM5OzKKxpLDEFguNm1-gZODKMXCIav5JKG0Bzywi8QzTVw018Ru4Lzc4YB_LtPtPWDBjRopkD3FworUX0tPZue0K1Q3Kfqb_Rvol2ycyKIjn9D5Vk0DIaGK-a7V9tQ5LItUvdILQQZMlM6UmG47uGYWw9v-CYUa_Rm2gXNtomoW5g-qpS_DrX6QrKpzdyzyAROA5KBljbuzWboKJjJLb2RPVOo1-Np8iX1_pGbvGejCEGrvDqL2ftJZ-v2Zr-Aldh6_me3AKmBnz2MJtIIiJNo7Ex-i2nYfJT4YZEhRW9DUfnXyUsFYeSOFNntgTn18UeQ6c2fRldo2LiM_UPtve2WDAK12qG8B2Y5kyJSlYncgLqARELXLtqWHEThLQV-osaGI1i7MpmEU7LK8VFlV7-Bmh-t3HDNf1OOFp_Wm5OncpbQ19F4d3t3vMyBLRZMAFhIn0USwM4yZYHw20DQxjHbFXj3CeaZr4PRm4VwaC3YootQI7ZObP0B6SnvrM3zzCEQJyESjE5Zjfjg6lm0Y8gyPADfZcsYx2e76ZwGGDWKpJaWRAydcx6xg_-suSAhCGtI-cHTz6eBkknqtxuuAHlEXXJWslrHwU3EbBsHixr266PtcAQH8fvjIpjstwfZA3Pb8r0YqEPmuIj3c0gsOufYzdWu-ek8tErLmwGPnz4CZM_NOPtxUV8PshLQswiZXF7cQE5DnjK7fpWsb-XMZ7pbXIeKtI00BMJHzStFVih4B0-ebHzTS3aIhXF6bXVeM0CWgNzNA_5HL6Wa6P1H0e24-2z4C2s-XcXtDRSBnW5uwE9VsHLhRtvRrHTFJwmPwZI9zdQ_8Nfi-oaDTX7AdCSfO5xHpNSHwf_wNSl4MAl2Ka7n0Z5h2lQQXN36WPues1evFXcgsboOMv2Pbn5BnamCWEcbn_5c-9_D9l96Ut4Ab1la5YKXnUofbirAnHqWHMdXiAj9ee4cUxZRGUGLL5ED4iBDHwXH6vhtjPQ5VLDKVBUTdBs0ID5jSrfP2h1WXZ4w5ysm_FhL"
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
#EXT-X-VERSION:3
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
