<?php
// ugotovi ali smo dobili zahtevek POST
    // nismo podali pravil
$prikazPodatkov = filter_input(INPUT_SERVER, 'REQUEST_METHOD') == 'POST';
# enakovredno: $prikazPodatkov = $_SERVER["REQUEST_METHOD"] == 'POST';
// ugotovi in pocisti url te skripte
    // zapelji cez filter, tle smo na boljsem
$url = filter_input(INPUT_SERVER, 'PHP_SELF', FILTER_SANITIZE_SPECIAL_CHARS);
# enakovredno: $url = htmlspecialchars($_SERVER["PHP_SELF"])
// Ce je zahtevek post, preberemo podatke iz zahtevka
if ($prikazPodatkov) {
    $pravila = [
        'ime' => FILTER_SANITIZE_SPECIAL_CHARS,
        'starost' => [
            'filter' => FILTER_VALIDATE_INT,
            'options' => [
                'min_range' => 1,
                'max_range' => 110
            ]
        ],
        'spol' => [
            'filter' => FILTER_VALIDATE_REGEXP,
            'options' => [
                "regexp" => "/^[mMzZ]{1}$/"
            ]
        ],
        'tekst' => FILTER_SANITIZE_SPECIAL_CHARS
    ];

    // vse kar je v postu sfiltriraj
    $podatki = filter_input_array(INPUT_POST, $pravila);
}
?><!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Preverjanje poslanih podatkov s funkcijo filter_input()</title>
</head>
<body>
<?php
if ($prikazPodatkov):
    // prikaz oÄiĹĄÄenih podatkov
    var_dump($podatki);
else:
    ?>
<form action="<?= $url ?>" method="post" >
        <label>Ime: <input type="text" name="ime" /></label>
        <label>Spol (m/Ĺž): <input type="text" name="spol" /></label>
        <label>Starost (1-110): <input type="text" name="starost" /></label><br/>
        <textarea cols="30" rows="10" name="tekst"></textarea><br/>
        <input type="submit" name="PoĹĄlji" />
    </form><?php
endif;
?>
</body>
</html>
