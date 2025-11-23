import requests
import re
import json
import dropbox

# Dropbox access token
DROPBOX_TOKEN = "sl.u.AGJiccuo2DBfCn45A2GHUq4u-b6VZVW96jQtvedXeVyrIxTOC7FLzDU5Q-BzdOWZlR2YcFugA5ejOKfvVZuGUmnCKsQk5vlQje4z5BSTICv6izXjnoVuF9gt9bycLYZgoF9xEKqYRnmxrH0_FlZUQ1tEkS3wW0uvZU4sQaXPw_FdM3lxMB8eDG1-c5Jv7ax3_8dVYHyYG0u3pmyuBjxim60838VnYu1Msl8X5N61XHWbGgVyfqrjdP-HgUGNViukFcAKeUdZcT5fYw1vvuIsb8KVHufwqdRdOLRz_-duhHikjVt6UNTuS8Hpjh-tJqcu5HJghalfLEJP3Hap8irX1Dd3Ij7sHBTpIBpF9aI7ctCtIsB9XI00mpbXzyy70Adu4ja6A6g1FF-fq065L5hSMYu5kaH9acClnoWR1qk7_wok4Blj4ig-dIoZWLOcU7foVuDld2aNxMAATpuw7VLlwnWoRywHJb34BeJfxaB9wLT71457tMxscQpJl5ndU90mgAOkbZTpq9_M8sqoV1vcXrjnFYgenLWeJQel0YZA2_9SNZ96ozcFltFY_eTCpKUpRO_VYjLWkzqjWy_sofjq5Q3p7DhFjdMvG4APEy50uNJ8dWaa6CmsuI0H4s9J5ORXPHR10nykPiUhg0avxZPh0IYlmOD1CxC9ECBsqHIc1RQ3UjPI7wlstqpNlJjfzN01qt_B3kbFmO3Wwvcf9pASPTzW4UBFScma4V_NRfzngVoXDzTv7SqrG5RI-na2fMpN41kOraZ2iYzdjLHd5Enl9DxQRu7AaU3rll5RFv9yyBuaFa3OnwHTZ2VOxaDQauDYc-G3dKiq9v92-5NlBFcuJkjPuj-q7fWcmkHd-exs_qd6fCHZN1Dqb2N2HWLn-UKK2KXKviS1bd_0RqXix4snYzR3xgv5m9Mpw0IiSHT9-S5nLbIc6ua1ENzkvRUoX9Hyc485PtDbnu3XWljwV1I7R0kVW8qf6XPqc0wDfGOr1LeIRtHbtFTJyvqjYRxg7EVj8kq7NHt7Zg-mS5CaqoEQw24bMAibQNpqpCkbeOHA7hXT84ba91oeil8De7RdduP6OfjBjOkZbaSgI3a8EnjAErgHu4O799gYVsKAgetxJKP_bch0QZmy0u9tIVSKZYJK_3Wsn1cJ77JPxKsZNcylIzYhW3eemnJfS6UksT3JT0c0D5RRlYlhgK_es_mGCnBM5UqsB4gy3PkAs57iIzR6vyiNUEHICs53wHcwOQtTsRZepzUSXrg6xH3L58EjRfnFzdFs9QcM3MQV0IiqXAIqZ6Ds"

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
