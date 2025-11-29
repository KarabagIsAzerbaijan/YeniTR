import requests
import re
import dropbox

DROPBOX_TOKEN = "sl.u.AGJewAJYjnJTXi2g0z7OWdzCsKJrF86v9RvZeBKYzeGWEORjnOyjxhJQTqS5LHcZ0xuCIbzla4t1ScBoStuh2UwCNgerKDDjJnDjV5wdaIwsFkxplmpEo1YNGh9GUwQ-Ru1WUWiPZ49hPnBzp1e1JGjPi2pxB1lvrbmAACblyUFN5K5IDQn6QhP-uuAqUgvtkgp1MigZbhXcOYzAG5HNOFLMrHzk8hET4APwfvlelTXJSY8NDk4f-cMc7kyQueKMrhSIwrpcBwExb5ytmBVgZbXJ22-DM9qk-oWONydXB_k6Dm8eOE0DqNjp4PjUxz-dwE6hCpcPgz8H9CIyq43Cml0mfjTmCAvIETOc0L3v-VuvdfPz1tJtg6dn7H7Qf8hIKC4poesCnM0e7mD1Oy631XAX8xs3h0hxLCtuq_e66IfTDyo0205TEV0nbORxrGak1whEfGCaKyTilcNv08IE5TU8vIvhaHliMTaJzmWoThDMOEPp9unFmgL6tKZLxA4PbLiUdTn3zmzcqMumUb6Ja8ynavauIOTec0FNKC64j6TeBZrqG6khiEtC0o3LGEf_Q2XdOkK7DT4SRlGza_Ay3KZsgqnq7coo0DQo1zqg40KF2Vz2sQ9kdllu313h06MhoG12AoaqxFGSf9zvRDy52IepFcOpZ1NeDgSj1qcqJV7NjDhwQhV2Ar5B0ldGJotk_yD3d8NCG_7RrJmdTDl1niPkveAv7yJxpH6SNQAzDHh6I2K0WUTxmJmGh6krgaRVWgGXniv4WfP6LXqhByNwkPGKHWx94Lerhma1q5diqPMB8Ags56PUcpHwI_-zFeEiU1Mg0pHK0H1GZEPKIXvNjjUOiWRJKxt6W38qpWR70jAMdx2c_Q_gy0Vqd2dU3XR28zmiDExoWDKdpUblPGiNvorVwwHRUVgU7dZfugV8uqUJ_IeiQlRxHkHlcXcdGxEkQIrW-AAe8nfrVPxx4bzdWra_jD48eJJFfoog9OwSZtc3WiOjbcqwiSf8GvXyngULd4__0P2RqASvFEzElenZZPrBZQkzXjExia5NYT7uLHSHlLAX6rdC0VGUyB9GByUgsw7xZ0YZObVVlgimGXxvCrtatPoEGF1e5VpHHIbm3-jUPCm_I-z7qqoBWVymKL3aGJkYV5vBJmIVZjH2Tsge6Axf30A31cmr6YHYRY9Ug97TaYcOGQTgv4woSDgYb5XgN-6bQIl6DF9IW04yO3LiZ8Y_Bo-iWU3FibuTTMZWbS2qCilrpDo5W8PGBBbMAS1XdIRCOyAL90vwY3I04RUX31OO"
DROPBOX_PATH_ERC = "/ercdn.m3u8"
DROPBOX_PATH_DAI = "/dai.m3u8"

URL = "https://www.nowtv.com.tr/canli-yayin"

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def extract_links(html):
    # daioncdn linki
    dai = re.search(
        r"daiUrl\s*[:=]\s*['\"](https?://[^\"]+)['\"]",
        html
    )

    # ercdn linki
    er = re.search(
        r"erUrl\s*[:=]\s*['\"](https?://[^\"]+)['\"]",
        html
    )

    dai_link = dai.group(1) if dai else None
    er_link = er.group(1) if er else None

    return er_link, dai_link

def make_m3u8(url):
    return f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=2500000
{url}
"""

def upload(path, content):
    dbx.files_upload(
        content.encode(),
        path,
        mode=dropbox.files.WriteMode.overwrite
    )

def main():
    print("HTML yüklənir...")

    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
    resp.raise_for_status()

    er_link, dai_link = extract_links(resp.text)

    if not er_link or not dai_link:
        print("Tokenlər tapılmadı!")
        print("Tapılan ERC  :", er_link)
        print("Tapılan DAI :", dai_link)
        raise SystemExit(1)

    print("Tokenlər tapıldı!")
    print("ERC  =", er_link)
    print("DAI  =", dai_link)

    upload(DROPBOX_PATH_ERC, make_m3u8(er_link))
    upload(DROPBOX_PATH_DAI, make_m3u8(dai_link))

    print("Dropbox-a uğurla yazıldı!")

if __name__ == "__main__":
    main()
