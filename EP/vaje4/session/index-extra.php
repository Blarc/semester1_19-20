<?php
session_start();

$url = filter_input(INPUT_SERVER, "PHP_SELF", FILTER_SANITIZE_SPECIAL_CHARS);
$action = filter_input(INPUT_POST, "do", FILTER_SANITIZE_SPECIAL_CHARS);

if ($action == "delete") {
    session_destroy();
    $message = "Seja koncana, Stevec pobrisan. <a href='$url'>Nadaljuj ...</a>";
} elseif (!isset($_SESSION["counter"])) {
    $_SESSION["counter"] = 1;
    $message = "To je tvoj prvi obisk te strani!";
} else {
    $_SESSION["counter"]++;
    $message = "To je ze tvoj $_SESSION[counter]. obisk.";
}
?>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Primer stevca obiskov z uporabo seje PHP</title>
</head>
<body>
<p><?= $message ?></p>

<form action="<?= $url ?>" method="POST">
    <input type="hidden" name ="do" value="delete" />
    <input type="submit" value="Ukini sejo" />
</form>
</body>
</html>