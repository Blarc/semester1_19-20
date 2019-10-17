<!DOCTYPE html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Procesiranje zahtevka POST</title>

<?php
$ime = $_POST["ime_uporabnika"];
$priimek = $_POST["priimek_uporabnika"];

echo "Pozdravljen $ime $priimek. Ura je " . date("H:i");
