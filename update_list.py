import requests
import base64
import time

# البحث في GitHub عن أحدث ملفات m3u8 عربية رياضية
GITHUB_SEARCH_API = "https://api.github.com/search/code?q=extension:m3u8+arab+sport+in:path&sort=indexed&order=desc"

def is_live(url):
    """فحص فوري للرابط قبل إضافته للقائمة"""
    try:
        # نستخدم Headers تحاكي متصفح حقيقي لتجنب المنع أثناء الفحص
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=3, stream=True)
        return response.status_code == 200
    except:
        return False

def fetch_github_m3u():
    combined_content = "#EXTM3U\n"
    seen_urls = set()
    count = 0
    
    try:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(GITHUB_SEARCH_API, headers=headers, timeout=20)
        
        if response.status_code == 200:
            items = response.json().get('items', [])
            print(f"جاري فحص {len(items)} ملف من GitHub...")
            
            for item in items[:15]: # فحص أفضل 15 نتيجة حديثة
                file_res = requests.get(item['url'], headers=headers).json()
                try:
                    content = base64.b64decode(file_res['content']).decode('utf-8')
                    lines = content.split('\n')
                    for i in range(len(lines)):
                        if lines[i].startswith('#EXTINF'):
                            stream_url = lines[i+1].strip() if (i+1) < len(lines) else ""
                            if stream_url.startswith('http') and stream_url not in seen_urls:
                                name = lines[i].upper()
                                # فلترة القنوات الرياضية والعربية المطلوبة
                                if any(k in name for k in ["BEIN", "SSC", "SPORT", "ARA", "KSA", "MBC", "OSN", "AD"]):
                                    if is_live(stream_url): # الفحص الحقيقي
                                        combined_content += lines[i] + "\n" + stream_url + "\n"
                                        seen_urls.add(stream_url)
                                        count += 1
                                        print(f"✅ تم تأكيد القناة: {name.split(',')[-1]}")
                except: continue
        
        with open("playlist.m3u8", "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"🚀 تم تجهيز قائمة بـ {count} قناة شغالة 100%")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_github_m3u()
