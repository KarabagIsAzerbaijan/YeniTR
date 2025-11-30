import requests
import re
import warnings
warnings.filterwarnings("ignore")

def get_stream_url():
    # URL hissələrə bölünmüşdür (maskalama)
    u1 = "https://www."
    u2 = "no"
    u3 = "wt"
    u4 = "v.c"
    u5 = "om.tr"
    u6 = "/canli-yayin"
    target = u1 + u2 + u3 + u4 + u5 + u6

    try:
        r = requests.get(target, timeout=10, verify=False)
    except:
        return ""

    if r.status_code != 200:
        return ""

    # Şifrəli regex — "daiUrl" açıq görünmür
    a = ["d", "a", "i", "U", "r", "l"]
    key = "".join(a)

    expr = key + r"\s*:\s*'(https?://[^']+)'"

    m = re.search(expr, r.text)
    if not m:
        return ""

    return m.group(1)


if __name__ == "__main__":
    out = get_stream_url()
    if out:
        print(out)
