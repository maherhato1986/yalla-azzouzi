import requests
import json
import re

# إعدادات البحث والقنوات المستهدفة
TARGET_CHANNELS = ["beIN SPORTS", "SSC", "AD SPORTS", "Alkass"]
OUTPUT_FILE = "channels.json"

def is_live(url):
    """فحص الرابط للتأكد من أنه يعمل (Status 200)"""
    try:
        r = requests.get(url, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

def fetch_channels():
    print("جاري البحث عن روابط قنوات جديدة...")
    all_channels = []
    
    # مصادر جلب القنوات (تعديل المصادر التي كانت في صورتك لزيادة الجودة)
    sources = [
        "https://iptv-org.github.io/iptv/countries/ar.m3u", # القنوات العربية
        "https://raw.githubusercontent.com/maherhato1986/yalla-azzouzi/main/external_source.m3u" # مصدر خارجي خاص بك
    ]

    for source in sources:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('\n')
                current_name = ""
                current_logo = "https://via.placeholder.com/150?text=TV"
                
                for line in lines:
                    if "#EXTINF" in line:
                        # استخراج اسم القناة واللوجو
                        name_match = re.search('tvg-name="(.*?)"', line) or re.search(',(.*?)$', line)
                        logo_match = re.search('tvg-logo="(.*?)"', line)
                        
                        if name_match: current_name = name_match.group(1).strip()
                        if logo_match: current_logo = logo_match.group(1)
                    
                    elif "http" in line and current_name:
                        url = line.strip()
                        # فلترة القنوات الرياضية فقط لضمان جودة المحتوى
                        if any(target.lower() in current_name.lower() for target in TARGET_CHANNELS):
                            print(f"تم العثور على: {current_name}")
                            # فحص الرابط قبل إضافته
                            if is_live(url):
                                all_channels.append({
                                    "name": current_name,
                                    "url": url,
                                    "logo": current_logo
                                })
                        current_name = "" # إعادة التعيين للقناة التالية
        except Exception as e:
            print(f"خطأ في جلب المصدر {source}: {e}")

    # حفظ القنوات في ملف JSON الذي يقرأ منه موقعك
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_channels, f, ensure_ascii=False, indent=4)
    print(f"تم تحديث القائمة بنجاح! إجمالي القنوات الشغالة: {len(all_channels)}")

if __name__ == "__main__":
    fetch_channels()
