<?php
// منع الوصول المباشر للملف بدون رابط
if (!isset($_GET['link'])) {
    die("No link provided.");
}

// فك تشفير الرابط
$url = base64_decode($_GET['link']);

// إعدادات الطلب لإيهام السيرفر الأصلي أن الطلب شرعي
$options = [
    "http" => [
        "header" => "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\r\n" .
                    "Accept: */*\r\n" .
                    "Connection: close\r\n"
    ]
];

$context = stream_context_create($options);

// جلب المحتوى وتمريره للمتصفح
$content = @file_get_contents($url, false, $context);

if ($content === FALSE) {
    header("HTTP/1.1 404 Not Found");
    die("Stream not reachable.");
}

// إرسال الـ Headers الصحيحة للمشغل
header("Content-Type: application/vnd.apple.mpegurl");
header("Access-Control-Allow-Origin: *"); // للسماح بالتشغيل من أي دومين
echo $content;
?>
