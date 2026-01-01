import os
import json
import re
import requests

OUTPUT_FILE = "channels.json"

def fetch_all():
    all_channels = []
    print("🚀 جاري البدء في عملية استخراج الروابط العميقة...")

    # 1. روابط احتياطية لضمان عمل الموقع فوراً
    all_channels.append({
        "name": "beIN SPORTS NEWS", 
        "url": "https://beinsports.ercdn.net/beinsports/test.m3u8", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/bc/BeIN_Sports_logo.svg"
    })

    # 2. فحص جميع الملفات التي سحبتها (نبحث عن أنماط m3u8 المخفية)
    for root, dirs, files in os.walk("."):
        for file in files:
            # نتجاهل ملفات النظام ونركز على ملفات الكود
            if file.endswith((".js", ".html", ".txt", ".json")):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # استخراج روابط m3u8 حتى لو كانت مشفرة بـ \/
                        # هذا النمط يبحث عن أي شيء يبدأ بـ http وينتهي بـ m3u8
                        links = re.findall(r'https?[:\/\\]+[^\s"\']+\.m3u8[^\s"\']*', content)
                        
                        for l in links:
                            # تنظيف الرابط من التشفير (إزالة المائلات العكسية)
                            clean_url = l.replace('\\/', '/').replace('\\', '')
                            all_channels.append({
                                "name": f"قناة من يلا شوت ({file[:8]})", 
                                "url": clean_url, 
                                "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                            })
                            print(f"🎯 تم استخراج رابط من: {file}")
                except: continue

    # 3. جلب روابط من GitHub (لضمان الامتلاء)
    try:
        r = requests.get("https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u", timeout=10)
        matches = re.findall(r'#EXTINF.*?,(.*?)\n(http.*)', r.text)
        for name, url in matches:
            if any(x in name.upper() for x in ["BEIN", "SSC", "KSA", "ALKASS", "SPORT"]):
                all_channels.append({"name": name.strip(), "url": url.strip(), "logo": ""})
    except: pass

    # إزالة التكرار وحفظ الملف
    unique = {c['url']: c for c in all_channels}.values()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique), f, ensure_ascii=False, indent=4)
    print(f"✅ تم الانتهاء! وجدنا {len(unique)} قناة.")

if __name__ == "__main__":
    fetch_all()
