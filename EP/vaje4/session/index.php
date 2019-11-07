<?php
session_start();

if (!isset($_SESSION["counter"])) {
    $_SESSION["counter"] = 1;
    $message = "To je tvoj prvi obisk te strani!";
} else {
    $_SESSION["counter"] = $_SESSION["counter"] + 1;
    $message = "To je ze tvoj $_SESSION[counter]. obisk te strani!";
}
?>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Primer stevca obiskov z uporabo seje PHP</title>
</head>
<body>
<p><?= $message ?></p>
</body>
</html>
