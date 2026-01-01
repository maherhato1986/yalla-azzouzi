import requests
import json
import re

# مصادر عالمية متخصصة في روابط beIN والرياضة (Raw Links)
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/qa.m3u", # قنوات قطر الأساسية
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u", # روابط عربية مباشرة
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8", # ملفك الحالي
    "https://raw.githubusercontent.com/Guu-M/IPTV/main/Bein.m3u" # مصدر خارجي متخصص لـ beIN
]

def fetch_channels():
    channels_list = []
    seen_urls = set()

    for url in SOURCES:
        try:
            print(f"Searching in: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current_channel = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        # استخراج اسم القناة واللوجو بدقة
                        name_match = re.search('tvg-name="([^"]+)"', line)
                        logo_match = re.search('tvg-logo="([^"]+)"', line)
                        title = name_match.group(1) if name_match else line.split(',')[-1]
                        
                        current_channel = {
                            "name": title,
                            "logo": logo_match.group(1) if logo_match else "assets/img/default-logo.png"
                        }
                    
                    elif line.startswith("http") and current_channel:
                        # فلترة مركزة على beIN Sports
                        target_keys = ["beIN", "Sports", "SSC", "Alkass", "AD Sports"]
                        if any(key.lower() in current_channel['name'].lower() for key in target_keywords):
                            if line not in seen_urls:
                                current_channel["url"] = line
                                channels_list.append(current_channel)
                                seen_urls.add(line)
                        current_channel = {}
        except Exception as e:
            print(f"Error skipping {url}: {e}")

    # حفظ النتائج في channels.json ليعرضها الموقع
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": channels_list}, f, ensure_ascii=False, indent=4)
    
    print(f"Done! Found {len(channels_list)} sports channels.")

if __name__ == "__main__":
    fetch_channels()
