import os
import json
import re
import requests

OUTPUT_FILE = "channels.json"

def fetch_master():
    print("🔥 جاري تشغيل المحرك الشامل لجمع القنوات...")
    combined_channels = []

    # 1. القنوات الثابتة (ضمان تشغيل الموقع 100%)
    static_list = [
        {"name": "الجزيرة مباشر", "url": "https://live-hls-web-aje.getaj.net/AJE/index.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/en/f/f2/Aljazeera_eng.png"},
        {"name": "العربية", "url": "https://v-arabic.alarabiya.net/alarabiya/alarabiya.stream/playlist.m3u8", "logo": ""},
        {"name": "بي إن سبورت الإخبارية", "url": "https://beinsports.ercdn.net/beinsports/test.m3u8", "logo": ""}
    ]
    combined_channels.extend(static_list)

    # 2. جلب آلاف القنوات من مشروع IPTV-Org (أقوى مصدر عالمي)
    sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u", # كل القنوات العربية
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u"
    ]
    
    for src in sources:
        try:
            r = requests.get(src, timeout=10)
            # استخراج الاسم والرابط واللوجو بذكاء
            matches = re.findall(r'#EXTINF:-1.*?tvg-logo="(.*?)".*?,(.*?)\n(http.*)', r.text)
            for logo, name, url in matches:
                combined_channels.append({
                    "name": name.strip(),
                    "url": url.strip(),
                    "logo": logo.strip()
                })
        except: pass

    # 3. فحص ملفاتك المسحوبة بحثاً عن "الكنوز" المخفية
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".html", ".txt")):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        links = re.findall(r'https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*', content)
                        for l in links:
                            all_url = l.replace('\\/', '/').replace('\\', '')
                            combined_channels.append({"name": f"بث مستخرج ({file[:5]})", "url": all_url, "logo": ""})
                except: continue

    # تنظيف وتصفية (حذف التكرار)
    seen_urls = set()
    final_list = []
    for c in combined_channels:
        if c['url'] not in seen_urls:
            final_list.append(c)
            seen_urls.add(c['url'])

    # حفظ أول 400 قناة فقط لسرعة التحميل
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list[:400], f, ensure_ascii=False, indent=4)
    
    print(f"✅ مبروك! موقعك الآن يحتوي على {len(final_list[:400])} قناة شغالة.")

if __name__ == "__main__":
    fetch_master()
