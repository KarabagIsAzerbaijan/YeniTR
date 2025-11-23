import os
import requests
import re

# Secrets-dən alınan URL-ləri istifadə edirik
erstrm_url = os.environ.get("ERSTRM_URL")
dastrm_url = os.environ.get("DASTRM_URL")

if not erstrm_url or not dastrm_url:
    raise ValueError("ERSTRM_URL və ya DASTRM_URL environment dəyişəni təyin olunmayıb.")

# Hər iki URL-i fayla yazmaq üçün dictionary
streams = {
    "erstrm": erstrm_url,
    "dastrm": dastrm_url
}

output_dir = "outputs/nowtur1"
os.makedirs(output_dir, exist_ok=True)

for name, url in streams.items():
    filepath = os.path.join(output_dir, f"{name}.m3u8")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=1280x720,CODECS=\"avc1.4d401f,mp4a.40.2\"\n")
        f.write(url + "\n")

print("M3U8 faylları yaradıldı:", ", ".join(streams.keys()))
