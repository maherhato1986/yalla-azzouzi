import os
import json
import re
import requests

# الكلمات التي نبحث عنها
TARGETS = ["beIN", "SSC", "Alkass", "AD SPORT", "Yalla", "Shoot", "Sport", "Live"]
OUTPUT_FILE = "channels.json"

def clean_url(url):
    """تنظيف الرابط من أي تشفير JavaScript"""
    url = url.replace('\\/', '/').replace('\\', '')
    if url.startswith('//'):
        url = 'https:' + url
    return url

def scan_files():
    print("🕵️ جاري فحص الملفات المسحوبة وفك التشفير...")
    all_channels = []
    
    # 1. البحث في كل ملفات المشروع (JS, HTML, Text)
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js", ".html", ".txt", ".json", ".m3u8")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # ابحث عن أي رابط ينتهي بـ m3u8 أو يحتوي على كلمة live
                        # جلب الروابط حتى لو كانت داخل " " أو ' '
                        links = re.findall(r'["\'](https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*)["\']', content)
                        
                        # إضافة الروابط التي لا تنتهي بـ m3u8 ولكنها تبدو كروابط بث
                        stream_links = re.findall(r'["\'](https?[:\/\\]+[^\s"\']+/live/[^\s"\']*)["\']', content)
                        
                        for link in (links + stream_links):
                            cleaned = clean_url(link)
                            all_channels.append({
                                "name": f"قناة مستخرجة ({file[:10]}...)",
                                "url": cleaned,
                                "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                            })
                            print(f"🎯 وجدنا رابط في: {file}")
                except: continue

    # 2. إضافة مصادر عالمية كاحتياط (لضمان أن الموقع لن يكون فارغاً)
    backup_sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u",
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u"
    ]
    for src in backup_sources:
        try:
            r = requests.get(src, timeout=10)
            if r.status_code == 200:
                m3u_links = re.findall(r'#EXTINF.*?,(.*?)\n(http.*)', r.text)
                for name, url in m3u_links:
                    if any(t.lower() in name.lower() for t in TARGETS):
                        all_channels.append({"name": name.strip(), "url": url.strip(), "logo": ""})
        except: continue

    return all_channels

def save_and_verify(channels):
    # إزالة التكرار
    unique = {c['url']: c for c in channels}.values()
    
    # حفظ في الملف
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique), f, ensure_ascii=False, indent=4)
    print(f"✅ تم حفظ {len(unique)} قناة في channels.json")

if __name__ == "__main__":
    found = scan_files()
    save_and_verify(found)
