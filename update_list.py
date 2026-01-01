import os
import json
import re
import requests

OUTPUT_FILE = "channels.json"

def fetch_all():
    all_channels = []
    print("🧹 تنظيف البيانات والبدء بجلب شامل لجميع القنوات...")

    # قنوات "ضمان عمل الموقع" (أخبار ومنوعات عالمية) تعمل 24 ساعة
    all_channels.append({"name": "Al Jazeera (Live)", "url": "https://live-hls-web-aje.getaj.net/AJE/index.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/en/f/f2/Aljazeera_eng.png"})
    all_channels.append({"name": "BBC Arabic", "url": "https://vs-hls-push-ww-live.akamaized.net/x=4/i=static/bbc_arabic_tv/main.m3u8", "logo": ""})
    all_channels.append({"name": "TRT Arabic", "url": "https://tv-trtarabic.medyahizmetleri.com/live/hls/trt_arabic.m3u8", "logo": ""})

    # 1. فحص ملفاتك المسحوبة
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".html", ".txt", ".json")):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # فك تشفير المائلات العكسية التي تستخدمها Cloudflare
                        links = re.findall(r'https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*', content)
                        for l in links:
                            clean_url = l.replace('\\/', '/').replace('\\', '')
                            all_channels.append({"name": f"قناة مستخرجة ({file[:5]})", "url": clean_url, "logo": ""})
                except: continue

    # 2. جلب مئات القنوات العربية من مصادر GitHub العامة
    sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/Moebis-Iptv/M3U/main/Arabic.m3u"
    ]
    for src in sources:
        try:
            r = requests.get(src, timeout=10)
            matches = re.findall(r'#EXTINF.*?,(.*?)\n(http.*)', r.text)
            for name, url in matches:
                all_channels.append({"name": name.strip(), "url": url.strip(), "logo": ""})
        except: pass

    # حذف التكرار وحفظ أول 500 قناة فقط
    unique = {c['url']: c for c in all_channels}.values()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique)[:500], f, ensure_ascii=False, indent=4)
    
    print(f"✅ تم حفظ {len(list(unique)[:500])} قناة في الملف.")

if __name__ == "__main__":
    fetch_all()
