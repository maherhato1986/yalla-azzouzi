<?php
// جلب البيانات من ملف JSON المرفق
$jsonFile = 'channels.json';
$allChannels = [];

if (file_exists($jsonFile)) {
    $jsonContent = file_get_contents($jsonFile);
    $data = json_decode($jsonContent, true);
    $allChannels = $data['channels'] ?? [];
}
?>

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yalla Azzouzi Live - البث المباشر الشامل</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <style>
        :root { --bg-dark: #090c10; --accent: #00d1ff; --card-bg: #161b22; }
        body { background-color: var(--bg-dark); color: #e6edf3; font-family: 'Segoe UI', sans-serif; overflow-x: hidden; }
        .player-wrapper { background: #000; border-radius: 12px; overflow: hidden; border: 1px solid #30363d; margin-bottom: 20px; position: relative; }
        .ratio-16x9 { position: relative; padding-bottom: 56.25%; height: 0; }
        .ratio-16x9 iframe, .ratio-16x9 video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
        .channel-card { background: var(--card-bg); border: 1px solid #30363d; border-radius: 12px; cursor: pointer; transition: 0.2s; height: 100%; min-height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .channel-card:hover { border-color: var(--accent); transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0, 209, 255, 0.2); }
        .channel-logo { width: 45px; height: 45px; object-fit: contain; margin-bottom: 8px; filter: drop-shadow(0 0 5px rgba(255,255,255,0.2)); }
        .search-box { background: #161b22; border: 1px solid #30363d; color: white; border-radius: 25px; padding: 10px 20px; }
        .search-box:focus { background: #1c2128; border-color: var(--accent); color: white; box-shadow: none; }
        .badge-live { position: absolute; top: 10px; right: 10px; font-size: 10px; background: red; padding: 2px 6px; border-radius: 4px; animation: blink 1.5s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        .warp-banner { background: linear-gradient(90deg, #00d1ff11, #0055ff11); border: 1px solid #30363d; border-radius: 15px; padding: 15px; margin-bottom: 30px; }
    </style>
</head>
<body>

<div class="container py-4 text-center">
    <h1 class="fw-bold mb-1" style="color: var(--accent);">YALLA AZZOUZI <span class="text-white">LIVE</span></h1>
    <p class="small text-secondary mb-4">بث مباشر لقنوات beIN, OSN, MBC وأكثر</p>

    <div class="warp-banner mx-auto col-lg-8">
        <div class="row align-items-center">
            <div class="col-md-9 text-md-start mb-2 mb-md-0">
                <h6 class="mb-1 text-info">💡 هل البث يقطع لديك؟</h6>
                <p class="small mb-0 text-secondary">استخدم <b>Cloudflare WARP (1.1.1.1)</b> لتجاوز حظر مزود الخدمة وتسريع البث.</p>
            </div>
            <div class="col-md-3">
                <a href="https://1.1.1.1/" target="_blank" class="btn btn-sm btn-outline-info w-100">تحميل WARP</a>
            </div>
        </div>
    </div>

    <div id="mainPlayer" class="d-none">
        <div class="player-wrapper shadow-lg mx-auto" style="max-width: 900px;">
            <div class="ratio ratio-16x9" id="videoBox"></div>
        </div>
        <h4 id="nowPlaying" class="mb-4 text-info"></h4>
    </div>

    <div class="row mb-4 justify-content-center">
        <div class="col-md-6">
            <input type="text" id="channelSearch" class="form-control search-box" placeholder="ابحث عن قناة (مثل: beIN, MBC, OSN)...">
        </div>
    </div>

    <div class="row g-3" id="channelsContainer">
        <?php foreach ($allChannels as $index => $ch): ?>
            <div class="col-6 col-md-3 col-lg-2 channel-item" data-name="<?php echo strtolower($ch['name']); ?>">
                <div class="channel-card p-2 position-relative" onclick='handlePlay(<?php echo json_encode($ch); ?>)'>
                    <span class="badge-live">LIVE</span>
                    <img src="<?php echo $ch['logo'] ?: 'https://via.placeholder.com/50/161b22/00d1ff?text=LIVE'; ?>" class="channel-logo" onerror="this.src='https://via.placeholder.com/50/161b22/00d1ff?text=TV'">
                    <div class="small fw-bold text-truncate w-100"><?php echo $ch['name']; ?></div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>

<script>
    const videoBox = document.getElementById('videoBox');
    const nowPlaying = document.getElementById('nowPlaying');
    const searchInput = document.getElementById('channelSearch');
    const channelItems = document.querySelectorAll('.channel-item');

    // وظيفة البحث
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        channelItems.forEach(item => {
            const name = item.getAttribute('data-name');
            item.style.display = name.includes(term) ? 'block' : 'none';
        });
    });

function setSource(url, type) {
    // هذه الخطوة هي التي تجعل الـ PHP يعمل فعلياً
    // نقوم بتمرير الرابط عبر ملف proxy.php لفك الحظر وتحويله لـ https
    const finalUrl = type === 'hls' ? 'proxy.php?link=' + btoa(url) : url;

    if (type === 'iframe') {
        videoBox.innerHTML = `<iframe src="${url}" allowfullscreen allow="autoplay; encrypted-media"></iframe>`;
    } else {
        videoBox.innerHTML = `<video id="video" controls autoplay class="w-100"></video>`;
        const video = document.getElementById('video');
        if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(finalUrl); // هنا نستخدم الرابط المحمي عبر البروكسي
            hls.attachMedia(video);
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = finalUrl;
        }
    }
}

    function handlePlay(ch) {
        document.getElementById('mainPlayer').classList.remove('d-none');
        nowPlaying.innerText = "أنت تشاهد الآن: " + ch.name;
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setSource(ch.url);
    }
</script>
</body>
</html>
