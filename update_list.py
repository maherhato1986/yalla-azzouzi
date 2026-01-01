import requests
import re

# قائمة بمصادر ضخمة ومحدثة باستمرار (مصادر عالمية وعربية)
sources = [
    "https://iptv-org.github.io/iptv/languages/ara.m3u", # قنوات عربية عامة
    "https://iptv-org.github.io/iptv/categories/sports.m3u", # قنوات رياضية عالمية
    "https://raw.githubusercontent.com/skylive-iptv/skylive/main/SkyLive.m3u", # مصدر بديل قوي
    "https://raw.githubusercontent.com/M3U-Arabic/M3U-Arabic/main/Arabic.m3u" # مصدر قنوات عربية
]

def update_m3u():
    combined_content = "#EXTM3U\n"
    found_channels = []

    for url in sources:
        try:
            print(f"جاري فحص المصدر: {url}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                lines = r.text.split('\n')
                for i in range(len(lines)):
                    # فلتر البحث عن قنوات beIN أو الرياضية العربية
                    if lines[i].startsWith('#EXTINF'):
                        line_content = lines[i].upper()
                        # الكلمات المفتاحية التي نبحث عنها
                        keywords = ["BEIN", "SSC", "KSA SPORT", "AD SPORT", "AL KASS", "RMC SPORT"]
                        
                        if any(key in line_content for key in keywords):
                            stream_url = lines[i+1].strip() if (i+1) < len(lines) else ""
                            if stream_url.startswith('http') and stream_url not in found_channels:
                                combined_content += lines[i] + "\n" + stream_url + "\n"
                                found_channels.append(stream_url)
                
                # إضافة القنوات العربية العامة أيضاً لضمان التنوع
                if "ara.m3u" in url:
                    combined_content += "\n".join(lines[1:200]) # جلب أول 200 قناة عربية
                    
        except Exception as e:
            print(f"خطأ في جلب {url}: {e}")

    # حفظ الملف النهائي
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(combined_content)
    print(f"تم تحديث القائمة بنجاح! إجمالي الروابط الفريدة: {len(found_channels)}")

if __name__ == "__main__":
    update_m3u()
