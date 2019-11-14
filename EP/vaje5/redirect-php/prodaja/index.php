<?php
if (!isset($_SERVER["HTTPS"])) {
    $url = "https://" . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"];
    header("Location: " . $url);
}
?>
<html>
<head>
    <title>Preusmerjanje HTTP/HTTPS</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
Spremenljivke globalnega polja <b>$_SERVER</b>:<br>
<?= var_dump($_SERVER) ?>
</body>
</html>