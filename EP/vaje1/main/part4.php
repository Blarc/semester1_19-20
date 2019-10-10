<?php

# $a = array();
# $a = [0, 10, 20];
$a = [
    0 => 0,
    1 => 10,
    2 => 20
];
# v php-ju lahko indexe izpustimo, oz. index je
# lahko poljuben objekt ki je 

for ($i = 0; $i < count($a); $i++) {
    echo "$i: $a[$i]\n";
}

$f = [
    0 => 0,
    1 => 10,
    "dvajset" => 20
];

foreach($f as $key => $value) {
    echo "$key: $value\n";
}


var_dump(isset($f["dvajset"]));
unset($f["dvajset"]);
var_dump(isset($f["dvajset"]));