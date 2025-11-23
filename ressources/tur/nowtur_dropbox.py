import requests
import dropbox
import time

# ==============================
# CONFIG
# ==============================
DROPBOX_TOKEN = "sl.u.AGIJRqaC4BbSSTPoQZzJr-EipI2yxxeP1Z9rG504GCO5NXPceYy-Do3u-M2Xb3DwD5e8zeDTLzgiQ4aNOQ5P6jsrH5W91htq1CcJmQNI-lOZL_GlR_W2Rur04DWoEor3WGcFaki-cECLvASKfZseZlJkWt0hOeK_V3shaOdAOGrCiidJW8YTjxxnYVrEVwvkGc_3trbUa_Vz5VwnESg7Q0xpZkfRqReknPmo9ejRhJMH6hnJmi28NAg9lN9Rqv7qcG4oB8ki09SKmGvP23EOowVjB1j0LQN6qPtPk_lB0rwqvYleXfUhDQrkaI5keEy-OqTp_UfZH_s3MtGdwlGqRmCk-20HgNKmDEcB2wM-9Y3jr-6bi0dIMeyl0WheqPjtHWhMY13jjz4UT5NjhCWe66SjOKq0n68mHJ6JOClMfblRwWfOZWlS-fxZwmzWBoiXKcpXPglBj4nIFLEuROgGtC1L9J3xTVSQ18BjAnlciWxwK5pS72-lPs99LGXX4YfrZYYoF-i5hVhbJ_459zA4SxXrm1f342sj000_yPJgBlOIq35VIKl13l-BBR45Yg5rhIHW-29PEYxVT-QX_2ERVzkpphp4wk2cDUUsSg6cLtY-wuYTSyhP0dxYPI1SdlMNRuYE3slhTzHy79hqWq4S3T-dEgcpUvN_9plaJhW6Q1zxxLRWUDcPDgQYGC9TQeoRi6yoaSbiaCof2fa_Pzk0xZy5ccbRXTKVW8sij9dtcGDsax6BH75hczBz6F_nfWNE-QCeHQmlduKgAKBSeZtImMbtoBy2mShDOPIJxTqDQ0oQfbVshzl3JY6hwUya3GdP3y7wWbJQmyEPFBstMo6S6y2OWVZ6tPXt-tPterxLJeh7Xj6joRx8AkAEAsmClS6a3wV2j813EHCVe4wBHZZT0ZZuMuAC71Lx7xGIcWrH-Xr9N2NGJKr5Kn_HwWjQESJz0yX9z1KGMCHsgAWDbBfY6jFIQIP4VAZ_AQhntxnhxUnsMttdR2c7kQlBjZJ2HqfgDrM2XBfrmYxH5cVU2_8OQT3erxQ8zPdPvFdy-lPFisDVpVvvXxVUARj3_aV7Zrg3waybJBwrD_CtUd2Vq5AD8MJJeiAL0l6S89ZOLf7EQdhXWx0Co3Ko5eHHS1Vy5_82k6qZJZBs3QsdgPde4LZuqpXkXRBP20JvLY-VF59ngRGhm17iO4M4WU_9fgE_WZQwzp0B9XAn_iC2bMMtUJln74TIww72x_4s5aHwggWO7X9MStZBVTDHC3XMjpeex4fjzE6hRI6NoER-Wd0O0GI1vcSu"  # buraya Dropbox tokenini yaz
DROPBOX_ERCDN_PATH = "/nowtur/ercdn.m3u8"
DROPBOX_DAI_PATH = "/nowtur/dai.m3u8"

ERCDN_URL = "https://www.nowtv.com.tr/ercdn_endpoint"  # buraya ERCDN master link
DAI_URL = "https://www.nowtv.com.tr/dai_endpoint"      # buraya DAI master link

# ==============================
# FUNCTIONS
# ==============================
def get_tokened_link(url):
    """
    URL-dən tokenli linki çəkir
    """
    resp = requests.get(url, verify=False)
    resp.raise_for_status()
    # tokeni çıxarmaq üçün regexp və ya manual parse
    # burada sadə nümunə, öz ehtiyacına görə dəyişdir
    start = resp.text.find("https://")
    end = resp.text.find(".m3u8", start)
    if start != -1 and end != -1:
        return resp.text[start:end+5]  # .m3u8 ilə bitir
    return None

def upload_to_dropbox(name, link, dropbox_path):
    """
    Tokenli linki Dropbox-a yazır (.m3u8)
    """
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    
    content = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:BANDWIDTH=230000,CODECS=\"avc1.4d001e,avc1.42000d,avc1.64000c,avc1.64001e,avc1.64001f,mp4a.40.2,mp4a.40.5\"\n"
    content += link + "\n"

    dbx.files_upload(content.encode(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    print(f"{name} uploaded to Dropbox at {dropbox_path}")

# ==============================
# MAIN
# ==============================
def main():
    try:
        ercdn_link = get_tokened_link(ERCDN_URL)
        dai_link = get_tokened_link(DAI_URL)

        if ercdn_link:
            upload_to_dropbox("ERCDN", ercdn_link, DROPBOX_ERCDN_PATH)
        else:
            print("ERCDN link not found.")

        if dai_link:
            upload_to_dropbox("DAI", dai_link, DROPBOX_DAI_PATH)
        else:
            print("DAI link not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
