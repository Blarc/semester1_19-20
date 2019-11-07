<?php
$cookieCounter = filter_input(INPUT_COOKIE, "counter", FILTER_VALIDATE_INT);
$url = filter_input(INPUT_SERVER, "PHP_SELF", FILTER_SANITIZE_SPECIAL_CHARS);
$action = filter_input(INPUT_POST, "do", FILTER_SANITIZE_SPECIAL_CHARS);

if ($cookieCounter === NULL) {
    setcookie('counter', 1, time() + 3600);
    $message = "To je tvoj prvi obisk.";
} else if ($cookieCounter === FALSE) {
    $message = "Piskotek ima neveljaven format.";
} else {
    $counter = $cookieCounter + 1;
    $message = "To je ze tvoj $counter. obisk.";
    setcookie('counter', $counter, time() + 3600);
}

if ($action == "delete") {
    setcookie('counter', NULL, -1);
    $message = "Piskotek je bil izbrisan. <a href='$url'>Nadaljuj ...</a>";
}
?><!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Stevec obiskov posameznega uporabnika</title>
</head>
<body>
<p><?= $message ?></p>

<form action="<?= $url ?>" method="POST">
    <input type="hidden" name="do" value="delete" />
    <input type="submit" value="IzbriĹĄi piĹĄkotek!" />
</form>
</body>
</html>
