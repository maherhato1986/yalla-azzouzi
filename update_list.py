import requests
import json
import re

# المصادر المحدثة بناءً على ملفاتك الجديدة في GitHub
SOURCES = [
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/mbc_osn.m3u8",
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/amazonprimesports.m3u8",
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8",
    "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/ARABIPTV.m3u"
]

def fetch_channels():
    channels_list = []
    seen_urls = set()
    # كلمات دلالية للقنوات التي نريد إظهارها
    keywords = ["BEIN", "SSC", "OSN", "MBC", "AMAZON", "PRIME", "AD SPORTS", "DUBAI"]

    for url in SOURCES:
        try:
            print(f"جاري جلب القنوات من: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        # استخراج اسم القناة
                        name_match = re.search(',(.+)$', line)
                        current = {"name": name_match.group(1).strip() if name_match else "قناة غير معروفة", "logo": "assets/img/default-logo.png"}
                    elif line.startswith("http") and current:
                        # فلترة ذكية
                        if any(k in current['name'].upper() for k in keywords):
                            if line not in seen_urls:
                                current["url"] = line
                                channels_list.append(current)
                                seen_urls.add(line)
                        current = {}
        except Exception as e:
            print(f"خطأ في المصدر {url}: {e}")

    # حفظ النتائج في الملف الذي يقرأ منه الموقع
    with open('channels.json', 'w', encoding='utf-8') as f:
        json.dump({"channels": channels_list}, f, ensure_ascii=False, indent=4)
    print(f"تم بنجاح! تم العثور على {len(channels_list)} قناة.")

if __name__ == "__main__":
    fetch_channels()
