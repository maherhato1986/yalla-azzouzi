<?php
// جلب البيانات من ملف JSON الصغير
$jsonFile = 'channels.json';
$externalChannels = [];

if (file_exists($jsonFile)) {
    $jsonContent = file_get_contents($jsonFile);
    $data = json_decode($jsonContent, true);
    $externalChannels = $data['channels'] ?? [];
}

// قنوات beIN و SSC الثابتة (يمكنك تعديل الروابط من هنا مباشرة)
$premiumChannels = [
    [
        "name" => "beIN Sports 1",
        "logo" => "https://upload.wikimedia.org/wikipedia/commons/b/bc/BeIN_Sports_logo.svg",
        "servers" => [
            ["name" => "سيرفر 1", "url" => "https://vdo.m7sy.com/e/be1", "type" => "iframe"],
            ["name" => "سيرفر 2", "url" => "https://fcdn.fustv.pro/v/bein1.html", "type" => "iframe"]
        ]
    ],
    [
        "name" => "beIN Sports 2",
        "logo" => "https://upload.wikimedia.org/wikipedia/commons/b/bc/BeIN_Sports_logo.svg",
        "servers" => [
            ["name" => "سيرفر 1", "url" => "https://vdo.m7sy.com/e/be2", "type" => "iframe"],
            ["name" => "سيرفر 2", "url" => "https://fcdn.fustv.pro/v/bein2.html", "type" => "iframe"]
        ]
    ],
    [
        "name" => "SSC Sports 1 HD",
        "logo" => "https://upload.wikimedia.org/wikipedia/commons/5/5e/SSC_Logo.svg",
        "servers" => [
            ["name" => "سيرفر 1", "url" => "https://vdo.m7sy.com/e/ssc1", "type" => "iframe"],
            ["name" => "سيرفر 2", "url" => "https://fcdn.fustv.pro/v/ssc1.html", "type" => "iframe"]
        ]
    ]
];

// دمج القنوات الثابتة مع القنوات القادمة من JSON
$allChannels = array_merge($premiumChannels, $externalChannels);
?>

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yalla Azzouzi Live - البث المباشر</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <style>
        :root { --bg-dark: #090c10; --accent: #00d1ff; --card-bg: #161b22; }
        body { background-color: var(--bg-dark); color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
        .player-wrapper { background: #000; border-radius: 12px; overflow: hidden; border: 1px solid #30363d; margin-bottom: 20px; position: relative; }
        .ratio-16x9 { position: relative; padding-bottom: 56.25%; height: 0; }
        .ratio-16x9 iframe, .ratio-16x9 video { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
        .server-btn { margin: 5px; border-radius: 20px; font-size: 13px; font-weight: bold; }
        .channel-card { background: var(--card-bg); border: 1px solid #30363d; border-radius: 12px; cursor: pointer; transition: 0.2s; height: 100%; }
        .channel-card:hover { border-color: var(--accent); transform: translateY(-3px); }
        .channel-logo { width: 50px; height: 50px; object-fit: contain; margin-bottom: 10px; }
        .warp-notice { background: rgba(0, 209, 255, 0.1); border: 1px dashed var(--accent); padding: 10px; border-radius: 10px; font-size: 12px; margin-bottom: 15px; }
    </style>
</head>
<body>

<div class="container py-4 text-center">
    <h1 class="fw-bold mb-2" style="color: var(--accent);">YALLA AZZOUZI <span class="text-white">LIVE</span></h1>
    
    <div class="warp-notice mx-auto" style="max-width: 600px;">
        💡 تواجه تقطيع؟ جرب تفعيل <b>Cloudflare WARP</b> لتجاوز حظر الشبكة وتسريع البث.
    </div>

    <div id="mainPlayer" class="d-none">
        <div class="player-wrapper shadow-lg">
            <div class="ratio ratio-16x9" id="videoBox"></div>
        </div>
        <div id="serverSwitch" class="mb-4"></div>
    </div>

    <div class="row g-3" id="channelsContainer">
        <?php foreach ($allChannels as $index => $ch): ?>
            <div class="col-6 col-md-3 col-lg-2">
                <div class="channel-card p-3" onclick='handlePlay(<?php echo json_encode($ch); ?>)'>
                    <img src="<?php echo $ch['logo'] ?: 'https://via.placeholder.com/50'; ?>" class="channel-logo">
                    <div class="small fw-bold text-truncate"><?php echo $ch['name']; ?></div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>

<script>
    const videoBox = document.getElementById('videoBox');
    const serverSwitch = document.getElementById('serverSwitch');

    function setSource(url, type) {
        if (type === 'iframe') {
            videoBox.innerHTML = `<iframe src="${url}" allowfullscreen allow="autoplay; encrypted-media"></iframe>`;
        } else {
            videoBox.innerHTML = `<video id="video" controls autoplay class="w-100"></video>`;
            const video = document.getElementById('video');
            if (Hls.isSupported()) {
                const hls = new Hls();
                hls.loadSource(url);
                hls.attachMedia(video);
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = url;
            }
        }
    }

    function handlePlay(ch) {
        document.getElementById('mainPlayer').classList.remove('d-none');
        serverSwitch.innerHTML = '';
        window.scrollTo({ top: 0, behavior: 'smooth' });

        if (ch.servers && ch.servers.length > 0) {
            ch.servers.forEach((s, idx) => {
                const btn = document.createElement('button');
                btn.className = 'btn btn-outline-info server-btn';
                btn.innerText = s.name;
                btn.onclick = () => setSource(s.url, s.type);
                serverSwitch.appendChild(btn);
                if(idx === 0) setSource(s.url, s.type);
            });
        } else if (ch.url) {
            setSource(ch.url, 'hls');
        }
    }
</script>
</body>
</html>
