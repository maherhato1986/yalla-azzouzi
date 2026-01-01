import requests
import base64
import time

# إعدادات البحث
GITHUB_SEARCH_API = "https://api.github.com/search/code?q=extension:m3u8+arab+sport+in:path&sort=indexed&order=desc"

def is_live(url):
    """وظيفة لفحص إذا كان الرابط يعمل فعلياً أم لا"""
    try:
        # نرسل طلباً قصيراً جداً (Head) للتأكد من استجابة السيرفر في أقل من 3 ثواني
        response = requests.head(url, timeout=3, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def fetch_github_m3u():
    combined_content = "#EXTM3U\n"
    seen_urls = set()
    found_count = 0
    
    try:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(GITHUB_SEARCH_API, headers=headers, timeout=30)
        
        if response.status_code == 200:
            items = response.json().get('items', [])
            
            for item in items[:10]: # فحص أهم 10 ملفات حديثة
                file_data = requests.get(item['url'], headers=headers).json()
                try:
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    lines = content.split('\n')
                    
                    for i in range(len(lines)):
                        if lines[i].startswith('#EXTINF'):
                            stream_url = lines[i+1].strip() if (i+1) < len(lines) else ""
                            
                            if stream_url.startswith('http') and stream_url not in seen_urls:
                                name = lines[i].upper()
                                # فلترة القنوات المهمة
                                if any(k in name for k in ["BEIN", "SSC", "SPORT", "ARA", "MBC"]):
                                    # الفحص الحقيقي: هل الرابط شغال الآن؟
                                    if is_live(stream_url):
                                        combined_content += lines[i] + "\n" + stream_url + "\n"
                                        seen_urls.add(stream_url)
                                        found_count += 1
                                        print(f"✅ شغال: {name[:30]}")
                except: continue
        
        with open("playlist.m3u8", "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"🚀 تم تجهيز {found_count} قناة تم التحقق من جودتها!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_github_m3u()
