import os
import json
import re
import requests

TARGET_KEYWORDS = ["beIN", "SSC", "KSA", "Alkass", "AD SPORT", "Sport", "Live", "Yalla", "Shoot"]
OUTPUT_FILE = "channels.json"

# إضافة Headers لإيهام السيرفر أننا متصفح حقيقي
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': 'https://www.yalashots.com/',
    'Origin': 'https://www.yalashots.com/'
}

def check_link(url):
    """فحص الرابط مع استخدام Headers المتصفح"""
    try:
        # نستخدم GET مع stream لضمان استجابة البث
        response = requests.get(url, timeout=5, headers=HEADERS, stream=True)
        # إذا كانت الحالة 200 أو 206 (بث جزئي) يعني الرابط يعمل
        return response.status_code in [200, 206]
    except:
        return False

def fetch_and_clean():
    all_raw_channels = []
    print("📡 جاري جمع الروابط وفحص الجودة...")

    # 1. روابط من ملفاتك (يلا شوت) مع تنظيف عميق
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".html", ".txt")):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # فك تشفير المائلات العكسية \/
                        links = re.findall(r'https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*', content)
                        for l in links:
                            clean_url = l.replace('\\/', '/').replace('\\', '')
                            all_raw_channels.append({"name": f"Live {file[:5]}", "url": clean_url})
                except: continue

    # 2. مصادر GitHub (الأكثر استقراراً)
    github_sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u",
        "https://raw.githubusercontent.com/Moebis-Iptv/M3U/main/Arabic.m3u"
    ]
    for src in github_sources:
        try:
            r = requests.get(src, timeout=5, headers=HEADERS)
            matches = re.findall(r'#EXTINF.*?,(.*?)\n(http.*)', r.text)
            for name, url in matches:
                all_raw_channels.append({"name": name.strip(), "url": url.strip()})
        except: pass

    # 3. الفحص والفلترة
    unique_links = {c['url']: c for c in all_raw_channels}.values()
    final_working_channels = []
    
    for chan in unique_links:
        name_upper = chan['name'].upper()
        if any(word.upper() in name_upper for word in TARGET_KEYWORDS) or "Live" in chan['name']:
            # إذا نجح الفحص نعتمدها
            if check_link(chan['url']):
                print(f"✅ شغالة ومضافة: {chan['name']}")
                final_working_channels.append({
                    "name": chan['name'],
                    "url": chan['url'],
                    "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                })
            else:
                print(f"❌ معطلة أو محجوبة: {chan['name']}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_working_channels, f, ensure_ascii=False, indent=4)
    print(f"✨ تم العثور على {len(final_working_channels)} قناة شغالة فعلياً.")

if __name__ == "__main__":
    fetch_and_clean()
