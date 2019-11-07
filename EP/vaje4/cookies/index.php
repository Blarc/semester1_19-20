<?php
$cookieCounter = filter_input(INPUT_COOKIE, "counter", FILTER_VALIDATE_INT);
$url = filter_input(INPUT_SERVER, "PHP_SELF", FILTER_SANITIZE_SPECIAL_CHARS);

if ($cookieCounter === NULL) {
    # Trojni enacaj preverja tudi tip; Ce piskotek ni nastavljen bo spremenljivka nastavljena na null
    # http://php.net/manual/en/language.operators.comparison.php
    setcookie('counter', 1, time() + 5);
    $message = "To je tvoj prvi obisk.";
} else if ($cookieCounter === FALSE) {
    $message = "Piskotek ima neveljaven format.";
} else {
    $counter = $cookieCounter + 1;
    $message = "To je ze tvoj $counter. obisk.";
    setcookie('counter', $counter, time() + 5);
}
?><!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Stevec obiskov posameznega uporabnika</title>
</head>
<body>
<p><?= $message ?></p>
</body>
</html>
