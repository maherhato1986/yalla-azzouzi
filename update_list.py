import requests
import json
import re
import os

# المصادر العالمية + روابط ملفاتك الجديدة في المستودع
SOURCES = [
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/mbc%26osn.m3u8", # ملفك الجديد لـ OSN
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/amazon%20prime%20sports.m3u8", # ملفك الجديد لـ Amazon
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8",
    "https://raw.githubusercontent.com/Guu-M/IPTV/main/Bein.m3u", # مصدر beIN العالمي
    "https://iptv-org.github.io/iptv/countries/qa.m3u"
]

def fetch_channels():
    channels_list = []
    seen_urls = set()
    # الكلمات التي نبحث عنها لضمان ظهور القنوات المشفرة
    target_keys = ["BEIN", "SSC", "OSN", "MBC", "AMAZON", "PRIME", "SHAHID", "NETFLIX"]

    for url in SOURCES:
        try:
            print(f"Scanning source: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        name_match = re.search(',(.+)$', line)
                        logo_match = re.search('tvg-logo="([^"]+)"', line)
                        current = {
                            "name": name_match.group(1).strip() if name_match else "Channel",
                            "logo": logo_match.group(1) if logo_match else "assets/img/default-logo.png"
                        }
                    elif line.startswith("http") and current:
                        if any(k in current['name'].upper() for k in target_keys):
                            if line not in seen_urls:
                                current["url"] = line
                                channels_list.append(current)
                                seen_urls.add(line)
                        current = {}
        except: continue

    # حفظ النتائج ليقرأها الموقع من channels.json
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": channels_list}, f, ensure_ascii=False, indent=4)
    print(f"Success! Found {len(channels_list)} encrypted channels.")

if __name__ == "__main__":
    fetch_channels()
