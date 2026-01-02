<?php
include 'db_config.php'; // الاتصال بقاعدة البيانات

$match_id = $_GET['id'];
// جلب رابط البث المشفر من القاعدة
$query = $db->prepare("SELECT stream_url FROM matches WHERE id = ?");
$query->execute([$match_id]);
$match = $query->fetch();

if ($match) {
    $stream_url = $match['stream_url'];
    // هنا نضع مشغل الفيديو (Video.js) ونمرر له الرابط
?>
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <video id="my-video" class="video-js" controls preload="auto" width="640" height="264">
        <source src="<?php echo $stream_url; ?>" type="application/x-mpegURL">
    </video>
    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
<?php
} else {
    echo "المباراة غير متوفرة حالياً.";
}
?>
