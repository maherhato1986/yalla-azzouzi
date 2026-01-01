import os
import json
import re
import requests
import base64

# الكلمات المستهدفة للبحث
TARGET_CHANNELS = ["beIN", "SSC", "Alkass", "AD SPORT", "ON TIME", "Sport", "Yalla"]
OUTPUT_FILE = "channels.json"

def deobfuscate_logic(text):
    """محاولة فك تشفير النصوص المخفية (Base64 أو الروابط المقطعة)"""
    found = []
    # 1. البحث عن روابط Base64 (شائع في ملفات JS المشفرة)
    b64_matches = re.findall(r'["\']([A-Za-z0-9+/]{20,}=*)["\']', text)
    for b in b64_matches:
        try:
            decoded = base64.b64decode(b).decode('utf-8')
            if "http" in decoded:
                found.append(decoded)
        except: continue
    return found

def extract_from_files():
    print("🕵️ جاري فحص وفك تشفير جميع الملفات المسحوبة...")
    all_found = []
    
    # يمر على كل ملفات المجلد
    for root, dirs, files in os.walk("."):
        for file in files:
            # نفحص ملفات JS, HTML, CSS وحتى الـ TXT
            if file.endswith((".js", ".html", ".txt", ".json")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 1. البحث المباشر عن روابط m3u8
                        direct_links = re.findall(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', content)
                        
                        # 2. البحث عن روابط مخفية (بدون امتداد واضح)
                        proxy_links = re.findall(r'(https?://[^\s"\']+/live/[^\s"\']*)', content)
                        
                        # 3. محاولة فك التشفير المنطقي (Base64)
                        hidden_links = deobfuscate_logic(content)
                        
                        total_links = direct_links + proxy_links + hidden_links
                        
                        for link in total_links:
                            # فلترة الروابط الرياضية فقط
                            # بما أننا نسحب من يلا شوت، سنعتبر أي رابط m3u8 هو قناة رياضية محتملة
                            all_found.append({
                                "name": f"قناة مستخرجة ({file})",
                                "url": link.replace("\\/", "/"), # تنظيف الرابط من علامات الهروب
                                "logo": "https://cdn-icons-png.flaticon.com/512/716/716429.png"
                            })
                            print(f"🎯 تم العثور على رابط في: {file}")
                except: continue
    return all_found

def fetch_channels():
    # جلب القنوات من الملفات المحلية
    channels = extract_from_files()
    
    # إضافة مصادر الإنترنت الاحتياطية لضمان عدم فراغ الموقع
    sources = [
        "https://raw.githubusercontent.com/skid9000/All-In-One-IPTV/main/All-In-One-IPTV.m3u",
        "https://iptv-org.github.io/iptv/countries/ar.m3u"
    ]
    
    for src in sources:
        try:
            r = requests.get(src, timeout=10)
            # (كود الاستخراج من m3u المعتاد...)
        except: continue

    # توحيد القائمة وحذف التكرار
    unique = {c['url']: c for c in channels}.values()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(unique), f, ensure_ascii=False, indent=4)
    print(f"✅ انتهى البحث. وجدنا {len(unique)} قناة.")

if __name__ == "__main__":
    fetch_channels()
