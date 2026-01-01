import requests
import json
import re

SOURCES = [
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/mbc_osn.m3u8",
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/amazonprimesports.m3u8", 
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/ARABIPTV.m3u", 
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8",
     "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist88.m3u8",
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/ARABIPTV.m3u"
]

def fetch_channels():
    channels_list = []
    seen_urls = set()
    keywords = ["BEIN", "SSC", "OSN", "MBC", "AMAZON", "PRIME", "SHAHID", "NETFLIX"]

    for url in SOURCES:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        name_match = re.search(',(.+)$', line)
                        current = {"name": name_match.group(1).strip() if name_match else "Unknown", "logo": ""}
                    elif line.startswith("http") and current:
                        if any(k in current['name'].upper() for k in keywords):
                            if line not in seen_urls:
                                current["url"] = line
                                channels_list.append(current)
                                seen_urls.add(line)
                        current = {}
        except: continue

    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": channels_list}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_channels()
