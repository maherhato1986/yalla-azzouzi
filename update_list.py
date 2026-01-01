import requests
import json
import re

# الكلمات التي سيبحث عنها الروبوت في كل GitHub والمصادر
TARGET_CHANNELS = ["beIN", "SSC", "Alkass", "AD SPORT", "KSA SPORT", "Oman Sport", "Dubai Sport", "Arryadia"]
OUTPUT_FILE = "channels.json"

def is_live(url):
    """فحص سريع جداً للرابط لضمان عدم تعليق السكريبت"""
    try:
        # نستخدم HEAD بدلاً من GET لسرعة الفحص
        r = requests.head(url, timeout=3)
        return r.status_code < 400
    except:
        return False

def fetch_channels():
    print("🚀 جاري البحث عن القنوات الرياضية في GitHub والمصادر العالمية...")
    all_channels = []
    
    # مصادر IPTV ضخمة ومحدثة باستمرار
    sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u",
        "https://raw.githubusercontent.com/byte-capsule/sk_iptv/main/sk_iptv.m3u",
        "https://raw.githubusercontent.com/Moebis-Iptv/M3U/main/Arabic.m3u",
        "https://raw.githubusercontent.com/Hasibul-Hasan-1/Hasibul-Hasan-1/main/Hasibul-Hasan-1.m3u"
    ]

    for source in sources:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('\n')
                name, logo = "", "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                
                for i, line in enumerate(lines):
                    if "#EXTINF" in line:
                        # استخراج الاسم واللوجو بدقة
                        name_match = re.search('tvg-name="(.*?)"', line) or re.search(',(.*?)$', line)
                        logo_match = re.search('tvg-logo="(.*?)"', line)
                        if name_match: name = name_match.group(1).strip()
                        if logo_match: logo = logo_match.group(1)
                        
                        if i + 1 < len(lines):
                            url = lines[i+1].strip()
                            if url.startswith("http"):
                                # فحص الاسم (تجاهل حالة الأحرف)
                                if any(t.lower() in name.lower() for t in TARGET_CHANNELS):
                                    # الفحص الحقيقي للرابط
                                    if is_live(url):
                                        print(f"✅ وجدنا قناة شغالة: {name}")
                                        all_channels.append({"name": name, "url": url, "logo": logo})
        except: continue

    # إزالة التكرار
    unique_channels = {c['url']: c for c in all_channels}.values()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique_channels), f, ensure_ascii=False, indent=4)
    
    print(f"✨ تم التحديث! إجمالي القنوات الشغالة المكتشفة: {len(unique_channels)}")

if __name__ == "__main__":
    fetch_channels()
