import requests
import dropbox

# Dropbox token və yollar
DROPBOX_TOKEN = "sənin_dropbox_token"
DROPBOX_ERSTRM_PATH = "/nowtur1/ERSTRM/ERSTRM.m3u8"
DROPBOX_DASTRM_PATH = "/nowtur1/DASTRM/DASTRM.m3u8"

# Tokenləri çək
def get_tokened_link(url):
    resp = requests.get(url, verify=False)
    # regex ilə tokenli linki tap
    return tokened_link

# Faylı Dropbox-a yaz
def upload_to_dropbox(dbx, path, content):
    dbx.files_upload(content.encode(), path, mode=dropbox.files.WriteMode.overwrite)

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

erstrm_link = get_tokened_link("https://www.nowtv.com.tr/canli-yayin")
dastrm_link = get_tokened_link("...")

# Faylları Dropbox-a yaz
upload_to_dropbox(dbx, DROPBOX_ERSTRM_PATH, erstrm_link)
upload_to_dropbox(dbx, DROPBOX_DASTRM_PATH, dastrm_link)
