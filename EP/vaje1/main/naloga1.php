<?php

function isPrime($n) {
    for ($i = 2; $i <= sqrt($n); $i++) {
        if ($n % $i == 0) {
            return false;
        }
    }
    return true;
}

for ($i = 0; $i < 30; $i++) {
    if (isPrime($i)) {
        echo "$i\n";
    }
}

