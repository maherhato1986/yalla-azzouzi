import requests

# أقوى مستودعات GitHub المحدثة حالياً لقنوات beIN و SSC والعرب
sources = [
    "https://raw.githubusercontent.com/arab-iptv/arab-iptv/master/arab-iptv.m3u",
    "https://raw.githubusercontent.com/MoamenHany/IPTV/master/Arab.m3u",
    "https://raw.githubusercontent.com/S-K-S-K/IPTV/main/Arab.m3u",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
    "https://raw.githubusercontent.com/mahmoud-m-ismail/IPTV/main/M3U/BeIN_Sports.m3u"
]

def update_m3u():
    combined_content = "#EXTM3U\n"
    # لضمان عدم تكرار القنوات
    unique_urls = set()
    
    for url in sources:
        try:
            print(f"جاري السحب من: {url}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                lines = r.text.split('\n')
                for i in range(len(lines)):
                    if lines[i].startswith('#EXTINF'):
                        # استخراج رابط القناة (السطر التالي)
                        stream_url = lines[i+1].strip() if (i+1) < len(lines) else ""
                        
                        # فلتر رياضي: جلب قنوات BEIN, SSC, الرياضية فقط لضمان الجودة
                        info = lines[i].upper()
                        keywords = ["BEIN", "SSC", "KSA SPORT", "AD SPORT", "ALKASS", "SPORT", "بطولة"]
                        
                        if any(key in info for key in keywords) or "ARA.M3U" in url.lower():
                            if stream_url.startswith('http') and stream_url not in unique_urls:
                                combined_content += lines[i] + "\n" + stream_url + "\n"
                                unique_urls.add(stream_url)
        except:
            continue

    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(combined_content)
    print(f"تم! وجدت {len(unique_urls)} قناة رياضية وعربية.")

if __name__ == "__main__":
    update_m3u()
