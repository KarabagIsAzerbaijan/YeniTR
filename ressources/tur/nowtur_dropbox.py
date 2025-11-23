import requests
import dropbox

# Dropbox token
DROPBOX_TOKEN = "sl.u.AGLTF72w-iQWxN1Xf0ZM0KGT_v8ZcfvUi472uwnh_b0tr4lRD-5c4H0vRrTVGZYe2C3XkEQv3IV7nK4R1TsPedhDBv_O8_HOrgk95_HbVZy1VaS8PpNrpczTtxOxGiDacbQAbwpLH8N8RoI1JzmZ1IzUXeAn1GzixB-JNvAK-GwspP8kbvJ34R9vCx1YWSl1DWcLDKsAe_Y3cbilZW1V_Ho0do1IvwAtgOFyOC8GxxOQ43aZKnPY7QTLD9Nu7_boBhvogAe6QkBaxVFHRlr5H8kea7E_IaD6zSVrE2CxPlcdOtAtzMRwNXFFtHEFIxYffR3tazLDMDSA4euEzniJzyLNIVOyD-buTFyH20Yq2UC9x-4rBLlnyhSqGfY9zBISyUvwk0bwnqFOjnjZsH7WXR5i8OmwX250Vy3oOKRQQ3XWoqsXVSpmHIS8yRG8G-QdaOxiBfb_Jv9xL7CjENKiMzHyiTt4frtgq8tkNayB0fxa2qCfLihVazMYR0rwv05illzZYwIGdak3noqFrCQwzOLERz3slzFx3L6eHyeX5Gx6bwh9axIg8ck5Sx8r6P03fekxi2XgLUkA-suOuXt8rCpSUX3zevRVADSlPWTwM76njvxvAHdDDse_7j8AHab3bCFQac-yIzzPz7JSJ7C6m2T8wlxMHC69LKjC2LRiTxyiV8hUGEZqtllcBZ4hbiBguTYFmxZcvA2BA76lZTlM7K6xkxZKgxl9RovOfrLmC4GP75lp-LuhEKbBZesl0B8nt_lVvTi20K-4JaiVhqQKqlrByCAefkMguaITlHbpZU9OfTHnAsd6E0xy6fp1U3JM6mAbufSk5jmNsR5tnRObONe4i53oilAdwON9WGkFTyOFPU-Hxjoly5EISSAQZz86cKOBrZgDs8wmVw-SXz0nP77DHmQ61l-m9bub-ivtTozVrY2znkQ7bt5QmygcB0oW5hSRM3_AIMtBElW7oKU_Q3Fm7f_1q9I8SqHBVb5blBEuA_dA0AOYK0gxHzTtzp35qAmkZPgziYYZLwPKj2sIfiInEbWUJbCw9S3iw61lROX9ZR3UOL2N2JgGo7xITBcdYtP99mGOuzco5XSwLsJueqGmaqO8X3qvus59nQzbNoEsYy97C2rC1JZ3PcFzwQM3iH0oVe2saIGDsbwi28tjsrzgNvo59ErudFvs-ukcw3yw23OXlAN5xMl9kCt1SXcjr5XLIByCF-u2GP52u86mMlryr0IB7WKT3i2nsG2IGsPGkQTPcHQOei_HV6DI42MGjI9P3fsPe14NZmIi7g0sBYzB"

# Fayl adları
DROPBOX_ERCDN_PATH = "/ercdn.m3u8"
DROPBOX_DAI_PATH = "/dai.m3u8"

# Kanal linkləri
ERCDN_URL = "https://www.nowtv.com.tr/canli-yayin"  # ERCDN linkini burada əldə et
DAI_URL = "https://www.nowtv.com.tr/canli-yayin"    # DAI linkini burada əldə et

def get_tokened_link(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        # regex ilə tokenli linki çıxart
        import re
        match = re.search(r"(https?://[^\']+)", response.text)
        if match:
            return match.group(1)
    return None

def upload_to_dropbox(name, link, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    # Faylın məzmunu: .m3u8 formatı
    content = f"#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS=\"avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5\"\n{link}"
    dbx.files_upload(content.encode(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    print(f"{name} faylı Dropbox-a yazıldı: {dropbox_path}")

def main():
    ercdn_link = get_tokened_link(ERCDN_URL)
    if ercdn_link:
        upload_to_dropbox("ERCDN", ercdn_link, DROPBOX_ERCDN_PATH)
    dai_link = get_tokened_link(DAI_URL)
    if dai_link:
        upload_to_dropbox("DAI", dai_link, DROPBOX_DAI_PATH)

if __name__ == "__main__":
    main()
