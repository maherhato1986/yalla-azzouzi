import requests
import base64
import time

# البحث عن ملفات m3u8 تحتوي على قنوات عربية ورياضية ومحدثة مؤخراً
GITHUB_SEARCH_API = "https://api.github.com/search/code?q=extension:m3u8+arab+sport+in:path&sort=indexed&order=desc"

def fetch_github_m3u():
    combined_content = "#EXTM3U\n"
    seen_urls = set()
    
    try:
        # طلب البحث من GitHub API
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(GITHUB_SEARCH_API, headers=headers, timeout=30)
        
        if response.status_code == 200:
            items = response.json().get('items', [])
            print(f"تم العثور على {len(items)} مستودع محتمل...")
            
            for item in items[:15]:  # فحص أفضل 15 نتيجة حديثة جداً
                file_raw_url = item['url']
                file_data = requests.get(file_raw_url, headers=headers).json()
                
                # فك تشفير المحتوى
                try:
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    lines = content.split('\n')
                    
                    for i in range(len(lines)):
                        if lines[i].startswith('#EXTINF'):
                            stream_url = lines[i+1].strip() if (i+1) < len(lines) else ""
                            
                            # التأكد أن الرابط يبدأ بـ http ولم يسبق جلبة
                            if stream_url.startswith('http') and stream_url not in seen_urls:
                                # تصفية ذكية للقنوات المهمة فقط (beIN, SSC, MBC, إلخ)
                                name = lines[i].upper()
                                if any(k in name for k in ["BEIN", "SSC", "SPORT", "ARA", "KSA", "MBC", "OSN"]):
                                    combined_content += lines[i] + "\n" + stream_url + "\n"
                                    seen_urls.add(stream_url)
                except: continue
                time.sleep(1) # لتجنب حظر GitHub API
        
        # حفظ كل ما تم صيده في ملف واحد للموقع
        with open("playlist.m3u8", "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"تم بنجاح استخراج {len(seen_urls)} قناة شغالة!")

    except Exception as e:
        print(f"حدث خطأ أثناء الصيد: {e}")

if __name__ == "__main__":
    fetch_github_m3u()
