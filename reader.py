import subprocess
from sysdata import get_stream_url

def main():
    url = get_stream_url()
    if not url:
        print("URL tapılmadı.")
        return

    # DAI linki yaratmaq
    dai_url = url.replace("live-ad.ercdn.net/nowtv/playlist.m3u8", 
                          "daioncdn.net/nowtv/nowtv.m3u8")

    # M3U fayllarını yeniləmək
    files = ["core.m3u", "set1.m3u", "set2.m3u"]
    for f in files:
        try:
            # ERC linki dəyiş
            subprocess.run(f'sed -i "s|https://[^ \'""]*ercdn.net/nowtv[^ \'""]*|{url}|g" {f}', shell=True)
            # DAI linki dəyiş
            subprocess.run(f'sed -i "s|https://[^ \'""]*daioncdn.net/nowtv[^ \'""]*|{dai_url}|g" {f}', shell=True)
        except:
            pass

    print("M3U faylları yeniləndi.")


if __name__ == "__main__":
    main()
