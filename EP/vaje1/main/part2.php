<?php

$a = 10;
$b = "20";
$c = $a + $b;

# konkatenacija je .
# plus je sestavanje

var_dump($c);

# echo($c . "\n");
echo "$a + $b = $c\n";
echo '$a + $b = $c\n'; #nizi ki se ne interpolirajo
# echo $a . " + " . $b . " = " . $c . "\n";
