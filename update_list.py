import requests
import json
import re

# أهداف بحث أوسع لضمان إيجاد القنوات
TARGET_CHANNELS = ["beIN", "SSC", "KSA", "Alkass", "AD SPORT", "Oman Sport", "Dubai Sport", "Arryadia"]
OUTPUT_FILE = "channels.json"

def is_live(url):
    """فحص سريع للرابط"""
    try:
        r = requests.head(url, timeout=3)
        return r.status_code < 400
    except:
        return False

def fetch_channels():
    print("جاري البحث عن روابط...")
    all_channels = []
    
    # مصادر متنوعة وقوية
    sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u",
        "https://raw.githubusercontent.com/Free-IPTV/Countries/master/Arab_World.m3u"
    ]

    for source in sources:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('\n')
                name = ""
                logo = "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                
                for i, line in enumerate(lines):
                    if "#EXTINF" in line:
                        # استخراج الاسم واللوجو بشكل أذكى
                        name_match = re.search('tvg-name="(.*?)"', line) or re.search(',(.*?)$', line)
                        logo_match = re.search('tvg-logo="(.*?)"', line)
                        if name_match: name = name_match.group(1).strip()
                        if logo_match: logo = logo_match.group(1)
                        
                        # الحصول على الرابط من السطر التالي
                        if i + 1 < len(lines):
                            url = lines[i+1].strip()
                            if url.startswith("http"):
                                # فحص الكلمات المفتاحية (تجاهل حالة الأحرف)
                                if any(t.lower() in name.lower() for t in TARGET_CHANNELS):
                                    all_channels.append({"name": name, "url": url, "logo": logo})
        except: continue

    # إزالة التكرار وحفظ الملف
    unique_channels = {c['url']: c for c in all_channels}.values()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique_channels), f, ensure_ascii=False, indent=4)
    print(f"تم! وجدنا {len(unique_channels)} قناة.")

if __name__ == "__main__":
    fetch_channels()
