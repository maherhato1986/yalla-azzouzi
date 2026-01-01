import requests

# مصادر روابط متجددة يومياً (IPTV-Org)
sources = [
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

def update_m3u():
    combined_content = "#EXTM3U\n"
    for url in sources:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                # نأخذ القنوات فقط بدون الترويسة المتكررة
                lines = r.text.split('\n')[1:]
                combined_content += "\n".join(lines) + "\n"
        except:
            print(f"Failed to fetch {url}")

    # حفظ النتيجة في ملفك الأساسي
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(combined_content)

if __name__ == "__main__":
    update_m3u()
