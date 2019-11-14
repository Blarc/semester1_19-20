<?php
if (!isset($_SERVER["HTTPS"])) {
    $url = "https://" . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"];
    header("Location: " . $url);
}
?>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Sistemski Äas in datum</title>
</head>
<body>
<?= "Sistemski cas in datum: " . date("d. m. Y, H:i") ?>.
</body>
</html>
