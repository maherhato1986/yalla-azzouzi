import requests
import json
import re

# الكلمات المستهدفة - أضفت كلمات من "يلا شوت" لزيادة دقة البحث
TARGET_CHANNELS = ["beIN", "SSC", "Alkass", "AD SPORT", "KSA", "Yalla", "Shoot", "Sport", "Arryadia"]
OUTPUT_FILE = "channels.json"

def fetch_channels():
    print("🚀 جاري فحص مصادر يلا شوت ومستودعات GitHub...")
    all_channels = []
    
    # أضفت لك رابط ملفاتك في GitHub ليفحصها الروبوت بنفسه
    sources = [
        "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/external_source.m3u", # ملفك الخاص
        "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/playlist.m3u8",   # ملف آخر محتمل
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u",
        "https://raw.githubusercontent.com/ZonSlayer/m3u8/main/sports.m3u"
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for source in sources:
        try:
            print(f"📡 فحص المصدر: {source}")
            response = requests.get(source, timeout=15, headers=headers)
            if response.status_code == 200:
                lines = response.text.split('\n')
                name, logo = "", "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                
                for i, line in enumerate(lines):
                    if "#EXTINF" in line:
                        # استخراج الاسم واللوجو من السطر
                        name_match = re.search('tvg-name="(.*?)"', line) or re.search(',(.*?)$', line)
                        logo_match = re.search('tvg-logo="(.*?)"', line)
                        if name_match: name = name_match.group(1).strip()
                        if logo_match: logo = logo_match.group(1) or logo
                        
                        if i + 1 < len(lines):
                            url = lines[i+1].strip()
                            if url.startswith("http"):
                                # إذا وجدنا الكلمة المطلوبة سنعتبرها شغالة مبدئياً لملء الموقع
                                if any(t.lower() in name.lower() for t in TARGET_CHANNELS):
                                    all_channels.append({"name": name, "url": url, "logo": logo})
                                    print(f"✅ تم العثور على: {name}")
        except Exception as e:
            print(f"❌ تعذر جلب {source}")
            continue

    # حذف التكرار بناءً على الرابط لضمان عدم تكرار القناة
    unique_channels = {c['url']: c for c in all_channels}.values()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique_channels), f, ensure_ascii=False, indent=4)
    
    print(f"✨ اكتملت العملية! وجدنا {len(unique_channels)} قناة جاهزة للعرض.")

if __name__ == "__main__":
    fetch_channels()
