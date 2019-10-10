<?php

$a = 10;
$b = "20";
$c = $a + $b;

# konkatenacija je .
# plus je sestavanje

var_dump($c);

# echo($c . "\n");
echo "$a + $b = $c\n";
# echo '$a + $b = $c\n'; #nizi ki se ne interpolirajo
# echo $a . " + " . $b . " = " . $c . "\n";

# $a = array();
# $a = [0, 10, 20];
$a = [
    0 => 0,
    # 1 => 10,
    "dvajset" => 20
];
# v php-ju lahko indexe izpustimo, oz. index je
# lahko poljuben objekt ki je 
var_dump($a);