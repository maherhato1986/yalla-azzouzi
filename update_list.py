import requests
import json
import re

# مصادر مجمعة (Aggregators) ومستودعات GitHub نشطة جداً
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/qa.m3u", # beIN الأساسية
    "https://iptv-org.github.io/iptv/countries/sa.m3u", # SSC وقنوات السعودية
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/Guu-M/IPTV/main/Bein.m3u", # مستودع خارجي متخصص
    "https://raw.githubusercontent.com/Moebis/tv/master/playlist.m3u", # قنوات متنوعة
    "https://raw.githubusercontent.com/Yousof-A-A/Arabic_IPTV/main/Arabic_IPTV.m3u" # قنوات عربية مشفرة
]

def fetch_channels():
    channels_list = []
    seen_urls = set()
    
    # كلمات دلالية للبحث عن القنوات الرياضية والمشفرة
    target_keywords = ["beIN", "SSC", "Alkass", "AD Sports", "Osn", "Shahid", "Starz", "Netflix"]

    for url in SOURCES:
        try:
            print(f"جاري الفحص في: {url}")
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                content = response.text
                lines = content.split('\n')
                current_item = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        # استخراج الاسم واللوجو
                        name_match = re.search('tvg-name="([^"]+)"', line) or re.search(',(.+)$', line)
                        logo_match = re.search('tvg-logo="([^"]+)"', line)
                        
                        name = name_match.group(1).strip() if name_match else "Unknown Channel"
                        current_item = {
                            "name": name,
                            "logo": logo_match.group(1) if logo_match else "assets/img/default-logo.png"
                        }
                    
                    elif line.startswith("http") and current_item:
                        # فلترة ذكية: إذا كان الاسم يحتوي على أحد الكلمات المستهدفة
                        if any(key.lower() in current_item["name"].lower() for key in target_keywords):
                            if line not in seen_urls:
                                current_item["url"] = line
                                channels_list.append(current_item)
                                seen_urls.add(line)
                        current_item = {}
                        
        except Exception as e:
            print(f"تخطى المصدر بسبب خطأ: {e}")

    # حفظ في channels.json ليعرضه الموقع مباشرة
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": channels_list}, f, ensure_ascii=False, indent=4)
    
    print(f"تم بنجاح! تم العثور على {len(channels_list)} قناة مشفرة/رياضية.")

if __name__ == "__main__":
    fetch_channels()
