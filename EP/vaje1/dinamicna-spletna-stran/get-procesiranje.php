<!DOCTYPE html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Procesiranje zahtevka GET</title>

<?php
$ime = $_GET["ime_uporabnika"];
$priimek = $_GET["priimek_uporabnika"];

echo "Pozdravljen $ime $priimek. Ura je " . date("H:i");
