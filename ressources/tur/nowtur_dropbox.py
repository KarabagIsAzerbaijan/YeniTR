import requests
import re
import dropbox

# Dropbox tokenini buraya əlavə et
DROPBOX_TOKEN = 'sl.u.AGIc4Hk24vj_2UDLOYZ0Eg8a1hruLwhB_tTItnhexnioPUumBuUasstq_pigWVaJZ-_o-YSaB9LcPuXhtrrzQaVHrBpn3MpBfNXeVraqfJU375YqrWq-xlNwKj8GDA7-t4hA4KyPtqOu2juJhax4NqI4Jbor0X84ISzOobiRveNItxZ5aO2fZNVgIR6OxGQJ3zKpUzXa1P9tYzGMBr1j-ddNsgcJ1-TE0IcHTTj2tcCGt5xPeOp1D5cNWuLvtb6cdsEmm8Tq3HtD3WvOoiw2xkOa09zRN9mOw_98zUjGzDUNP6MF434iBXhP2yT5w1vFgeCLE5COKHRbak1SEbzVP3UyfwmmZt3ajQVXJlhoiBBRnUsTzdREgfBJa8kE5t1WgsI-Iv7neYrzOtm0KACZp0Bbtvdutvq_Mi0_p2SH8cOHITQU6uOoMhEUKdpjj-gwBXhgAgU4rIycTEbA1lOWs1wgbM-rRmwt3O-D_XQ2af61YmATaf8tG48dcIYJHzmjyeV5eSI6G_1PgyyDHYJcFrxZhGdySiH8af7N_37BDnL0lK7kghvhNkijCaSsJ_djwExhhkL5n43qCQVgZAj-n0LsEYaWihu3nRvqb9w0mrwD9FiCY7tVY6AzSIHH9LTteIOik3gTdL3498Iyj3rGlNOMMH73DAhi4tPUNXR9WfPsbwAoUiZ3O1dPM0uPYrjPw2ry-FSSoXd7DYT2Dl4eR3xJZLUNdC8uNeh94zFX9LWy4Rr7PTLSDofR6qA2QUd41gAruSbfvMwo9YfXn5UekFf3fCVbdDXXaON3WIJdyNZ-w0KkPzW7HJgxXJIkfocLwxyDXJwRtr2HqjzUyY4tXYqQe1lK3FnHfEC9_w86Ma5NDuqqC_jcRfz_HUhM0nmatlaLbTSKwocEkVANiSZAN-zBiMurBryDvyBIvJQQhQEkC6rVsKRCLviYuf3zpkLBh2Moko6gdSfgwfZi6i2WP9M31dBEZzyvdaU_4mr6wKVBHSRHomOzpHGgFLSK2UpUsMVzhWvNDjbex7cjKNoNbVoxwxT7M_eJTi5zxwSbxW89xopK8fh6pgu6RE-hUth6TRbq4tCZ2ewVNztNqYAY0hu6AlXB2sJQAKIG3ejLm0V1BrBPX8f264B8woc18bdDlKtSK9Q_4YlnWYc9YQaqp2J-524gPQyRHC2rY1OuPiXaYSzDBe4CSWxjcIEs18eX9ZiZEW3bmx4gzDpA9QGK-mYLNFQ4DxxjAQTh1iY3rjFO8wmCqPR2Hbeb8QABYRAGmD4S-gCTWjisiPaBqAW2yfNX'

# Kanallar və onların URL-ləri
CHANNELS = {
    'ERSTRM': 'https://www.nowtv.com.tr/canli-yayin',
    'DAISTRM': 'https://www.nowtv.com.tr/canli-dai'
}

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def fetch_tokened_link(url):
    try:
        resp = requests.get(url, verify=False)
        if resp.status_code == 200:
            match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", resp.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Xəta: {e}")
    return None

def upload_to_dropbox(channel_name, link):
    filename = f'/NowTV/{channel_name}/{channel_name}.m3u8'
    try:
        dbx.files_upload(link.encode(), filename, mode=dropbox.files.WriteMode.overwrite)
        print(f'{channel_name} faylı Dropbox-a yazıldı: {filename}')
    except dropbox.exceptions.ApiError as e:
        print(f'Dropbox API xətası: {e}')

def main():
    for name, url in CHANNELS.items():
        link = fetch_tokened_link(url)
        if link:
            upload_to_dropbox(name, link)
        else:
            print(f'{name} üçün link tapılmadı!')

if __name__ == "__main__":
    main()
