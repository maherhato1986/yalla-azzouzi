import requests
import json
import re

# قائمة بمصادر الروابط المفتوحة (M3U Playlists)
SOURCES = [
    "https://iptv-org.github.io/iptv/countries/qa.m3u", # قنوات قطر ومنها beIN
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8" # ملفك الحالي
]

def fetch_channels():
    found_channels = []
    
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                # تقسيم الملف بناءً على وسوم M3U
                lines = content.split('\n')
                current_name = ""
                
                for line in lines:
                    if "#EXTINF" in line:
                        # استخراج اسم القناة باستخدام Regex
                        name_match = re.search('tvg-name="([^"]+)"', line)
                        if not name_match:
                            name_match = re.search(',(.+)$', line)
                        
                        if name_match:
                            current_name = name_match.group(1).strip()
                    
                    elif line.startswith("http"):
                        # فلترة القنوات لتشمل beIN Sports فقط أو القنوات الرياضية
                        if "beIN" in current_name or "Sports" in current_name:
                            found_channels.append({
                                "name": current_name,
                                "url": line.strip(),
                                "category": "Sports"
                            })
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    # حفظ النتائج في ملف channels.json
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": found_channels}, f, ensure_ascii=False, indent=4)
    
    print(f"تم تحديث القائمة بنجاح! تم العثور على {len(found_channels)} قناة.")

if __name__ == "__main__":
    fetch_channels()
