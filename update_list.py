import os
import json
import re
import requests

# كلمات مفتاحية واسعة لضمان جلب أكبر عدد من القنوات
TARGET_KEYWORDS = ["beIN", "SSC", "KSA", "Alkass", "AD SPORT", "Sport", "Live", "Yalla", "Shoot"]
OUTPUT_FILE = "channels.json"

def check_link(url):
    """تجربة الرابط إذا كان شغالاً أم لا"""
    try:
        # نرسل طلب فحص بمدة انتظار قصيرة (3 ثواني) لكي لا يتأخر السكريبت
        response = requests.get(url, timeout=3, stream=True)
        # إذا كان الكود يبدأ بـ 200 يعني الرابط شغال
        return response.status_code == 200
    except:
        return False

def fetch_and_clean():
    all_raw_channels = []
    print("📡 جاري جمع الروابط من الملفات المحلية والمصادر الخارجية...")

    # 1. فحص الملفات المسحوبة (يلا شوت)
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".html", ".txt")):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        links = re.findall(r'https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*', content)
                        for l in links:
                            clean_url = l.replace('\\/', '/').replace('\\', '')
                            all_raw_channels.append({"name": f"Live {file[:5]}", "url": clean_url})
                except: continue

    # 2. فحص مستودعات GitHub العالمية
    github_sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u",
        "https://raw.githubusercontent.com/Moebis-Iptv/M3U/main/Arabic.m3u"
    ]
    for src in github_sources:
        try:
            r = requests.get(src, timeout=5)
            matches = re.findall(r'#EXTINF.*?,(.*?)\n(http.*)', r.text)
            for name, url in matches:
                all_raw_channels.append({"name": name.strip(), "url": url.strip()})
        except: pass

    # 3. إزالة التكرار قبل الفحص لتوفير الوقت
    unique_links = {c['url']: c for c in all_raw_channels}.values()
    print(f"🔎 وجدنا {len(unique_links)} رابط فريد. جاري فحص الشغال منها الآن...")

    # 4. الفحص الحقيقي (الخطوة الأهم)
    final_working_channels = []
    for chan in unique_links:
        # إذا كانت القناة رياضية أو من ملفاتك، سنفحصها
        if any(word.upper() in chan['name'].upper() for word in TARGET_KEYWORDS) or "Live" in chan['name']:
            if check_link(chan['url']):
                print(f"✅ شغالة: {chan['name']}")
                final_working_channels.append({
                    "name": chan['name'],
                    "url": chan['url'],
                    "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                })
            else:
                print(f"❌ معطلة: {chan['name']}")

    # حفظ النتائج
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_working_channels, f, ensure_ascii=False, indent=4)
    
    print(f"✨ العملية تمت! تم العثور على {len(final_working_channels)} قناة شغالة.")

if __name__ == "__main__":
    fetch_and_clean()
