import requests
import json
import re

# مصادر موثوقة يتم تحديثها يومياً من IPTV-ORG ومصادر أخرى مفتوحة
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/qa.m3u", # قنوات قطر (تشمل beIN)
    "https://iptv-org.github.io/iptv/languages/ara.m3u", # القنوات العربية العامة
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8" # ملفك الحالي للطوارئ
]

def fetch_channels():
    channels_list = []
    seen_urls = set() # لمنع تكرار نفس الرابط

    for url in SOURCES:
        try:
            print(f"جاري جلب البيانات من: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current_channel = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        # استخراج اسم القناة واللوجو إذا وجد
                        name_match = re.search('tvg-name="([^"]+)"', line)
                        logo_match = re.search('tvg-logo="([^"]+)"', line)
                        
                        title = ""
                        if name_match:
                            title = name_match.group(1)
                        else:
                            title = line.split(',')[-1]
                        
                        current_channel = {
                            "name": title,
                            "logo": logo_match.group(1) if logo_match else "assets/img/default-logo.png"
                        }
                    
                    elif line.startswith("http") and current_channel:
                        channel_url = line
                        # تصفية القنوات: نريد beIN Sports والقنوات الرياضية فقط
                        interest_keywords = ["beIN", "Sports", "SSC", "AD Sports", "الكأس"]
                        if any(key.lower() in current_channel['name'].lower() for key in interest_keywords):
                            if channel_url not in seen_urls:
                                current_channel["url"] = channel_url
                                channels_list.append(current_channel)
                                seen_urls.add(channel_url)
                        current_channel = {}
        except Exception as e:
            print(f"خطأ في جلب {url}: {e}")

    # حفظ البيانات في ملف channels.json ليعرضها الموقع
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": channels_list}, f, ensure_ascii=False, indent=4)
    
    print(f"تم بنجاح! تم العثور على {len(channels_list)} قناة رياضية.")

if __name__ == "__main__":
    fetch_channels()
