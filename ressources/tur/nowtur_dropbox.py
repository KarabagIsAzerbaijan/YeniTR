import requests
import re
import dropbox

DROPBOX_TOKEN = "sl.u.AGIi9JLTFPiWGc_hSXBZiKP861aK2kogszNJm1m-PPFkGs_pYeH8qMs_Zm5_2oW33enIXfF3cTo6Xvf1ndYjSjtrygdEUJlz78Fg_Fm9vaQztyKOxSclJxl8u3G5Ko7OA3BkHf0jS67eN6spM4dunXzbNBm3FXjolQKXAZJ0bVwIaHkbfYId5WIOg4BbqKEepFrvBRD8FmElLRE35euJLXf4MsJw5OA_CeYYy502DTGHoaWFV9acOz2tTBlzdGByy_TvNQX_G2eb2Y5YIXjv897mGD3IQzW6BmhK1UJCHZy_DPWtaRFlVqBiEEIgI6M73WIzeeeag6rgocnLCbrqHFmO_d0Es1SmyC2G4rQWLla-Is_r3xWSgVtCOawpb5TAf_Q6q65sDI6IkeMA4MlPIVdr2-mSx8gmg-e8JWN_HWOtopxZontthG89EhsewgRfRb6CpQKxCkgsh76bBPgLG-cE-f8hlcXy247tW0oKyJjzKcENRfAeJdZlAkO86NvSJVpuJyTUecP_O9DrEDjJNEnY3JBLOUIKYYpH47JeMuT4WQsXF5ZFcMll3B9lOVnvWrHs2S3AY2KKXSxfKPOmwPOVSXx6ezjLgWdQ0sGyrVp8yZZJbpa4oidmZ8ol3x7UPwCmN-W-UkpaPxzE0RQA6gsV5qzrUyJ4WTrRFRm5JsASG47bpFUytQdx6PEoe2aLqFEugDcqNRoGgOO2ELjMgogzTu30EVyVyLv1kOsW1OWqF6rS2ngl2XoSrCE7gGumLiND1waMBmHqpiM84CTXrOOM5v8YWLopkn92WzkOFU7Qo8VBDUaAkw_2kek0HWIUzq9ZCSmDfI9kMcr_3PsrOYC6eHfEa4L5vfa1Aqxw49PTEufZVRL9q1fCRLsCXCGAPZeMwPJxbU6JcK0MtSpy1m9jwV5JdegcKxo0WN0tPPaXRPPVy7iXwb-12ZYWw5QdLk_7cOSP8PeFIodkcyjGdXzeRRe9oqeUEgUiWx1eTMjSQCObTvEbkdXqXsZUY6lxLAeKAr2O5UJ5Lgv2vFiqsQqL-7maMryh2ygskKY12sSVcBxSdoakIrj9DFfEP6FArXdIZQ1S4k2A5EmBe4AeTYQdpaHBYA1LXVIKhj0VxDZo8Sc92BN29kRPkm_NKx1Hh-ewb7szEO3zVN8nLUHONeeq7mL6DXcvYevv_Qfecl3d5MR3iq_VwdrjJRXLHft6IOBahvjGZhLwkH6MXV2eAOh3KnJEZJ0yP9BbkvJrB63omW1KeQi2TmncMWuNGsDiD_sqEbAMNlV-VY7D4379JE8y"
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
