import os
import json
import re
import requests

# تم إلغاء حصر الكلمات في الرياضة فقط لجلب كل القنوات
OUTPUT_FILE = "channels.json"

# إعدادات الفحص
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

def check_link(url):
    """فحص الرابط إذا كان يعمل فعلياً"""
    try:
        # فحص سريع للرأس (Head) للتأكد من استجابة السيرفر
        response = requests.get(url, timeout=4, headers=HEADERS, stream=True)
        return response.status_code in [200, 206]
    except:
        return False

def fetch_all_channels():
    all_raw_channels = []
    print("🌍 جاري البحث عن جميع القنوات المتاحة (رياضة، أفلام، أخبار، أطفال)...")

    # 1. البحث في ملفاتك المسحوبة (Yalla Shoot وغيرها)
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".html", ".txt", ".json")):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # استخراج أي رابط m3u8
                        links = re.findall(r'https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*', content)
                        for l in links:
                            clean_url = l.replace('\\/', '/').replace('\\', '')
                            all_raw_channels.append({"name": f"قناة من ملف ({file[:8]})", "url": clean_url})
                except: continue

    # 2. مصادر IPTV عالمية ضخمة (تشمل آلاف القنوات العربية والأجنبية)
    sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u", # القنوات العربية
        "https://raw.githubusercontent.com/Moebis-Iptv/M3U/main/Arabic.m3u", # منوعات عربية
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u", # قنوات منوعة
        "https://iptv-org.github.io/iptv/categories/movies.m3u", # أفلام
        "https://iptv-org.github.io/iptv/categories/kids.m3u", # أطفال
        "https://iptv-org.github.io/iptv/categories/news.m3u"  # أخبار
    ]

    for src in sources:
        try:
            print(f"📡 جلب من المصدر: {src}")
            r = requests.get(src, timeout=10, headers=HEADERS)
            # استخراج اسم القناة والرابط من ملفات m3u
            matches = re.findall(r'#EXTINF.*?,(.*?)\n(http.*)', r.text)
            for name, url in matches:
                all_raw_channels.append({"name": name.strip(), "url": url.strip()})
        except: pass

    # 3. تصفية التكرار وفحص الجودة
    unique_links = {c['url']: c for c in all_raw_channels}.values()
    print(f"🔎 وجدنا إجمالي {len(unique_links)} رابط. جاري تصفية الشغال منها...")

    final_channels = []
    for chan in unique_links:
        # هنا نفحص الرابط، إذا كان شغالاً نضيفه فوراً بغض النظر عن نوع القناة
        if check_link(chan['url']):
            print(f"✅ إضافة: {chan['name']}")
            final_channels.append({
                "name": chan['name'],
                "url": chan['url'],
                "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png" # لوجو افتراضي
            })
            # سنكتفي بـ 200 قناة كحد أقصى لضمان سرعة الموقع
            if len(final_channels) >= 200: 
                break

    # حفظ النتائج
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_channels, f, ensure_ascii=False, indent=4)
    print(f"✨ اكتمل التحديث! تم العثور على {len(final_channels)} قناة شغالة من جميع الأنواع.")

if __name__ == "__main__":
    fetch_all_channels()
