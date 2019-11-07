<?php
session_start();

require_once 'Knjiga.php';
require_once 'BazaKnjig.php';

$url = filter_input(INPUT_SERVER, "PHP_SELF", FILTER_SANITIZE_SPECIAL_CHARS);
$validationRules = [
    'do' =>
        [
        'filter' => FILTER_VALIDATE_REGEXP,
        'options' =>
            [
                "regexp" => "/^(add_into_cart|update_cart|purge_cart)$/"
            ]
        ],
    'id' =>
        [
        'filter' => FILTER_VALIDATE_INT,
        'options' => ['min_range' => 0]
        ],
    'kolicina' =>
        [
        'filter' => FILTER_VALIDATE_INT,
        'options' => ['min_range' => 0]
        ]
];
$data = filter_input_array(INPUT_POST, $validationRules);

if ($data['do'] == "add_into_cart") {
    try {
        $knjiga = BazaKnjig::vrniKnjigo($data["id"]);

        // $knjiga_counter = $_SESSION["cart"][$knjiga -> id];
        if (isset($_SESSION["cart"][$knjiga -> id])) {
            $_SESSION["cart"][$knjiga -> id] += 1;
        }
        else {
            $_SESSION["cart"][$knjiga -> id] = 1;
        }
    }
    catch (Exception $exc) {
        die($exc -> getMessage());
    }
}

?><!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <meta charset="UTF-8" />
    <title>Knjigarna</title>
</head>
<body>
<h1>Knjigarna</h1>

<div id="main">
    <?php foreach (BazaKnjig::seznamVsehKnjig() as $knjiga): ?>
        <div class="book">
            <form action="<?= $url ?>" method="post">
                <input type="hidden" name="do" value="add_into_cart" />
                <input type="hidden" name="id" value="<?= $knjiga->id ?>" />
                <p><?= $knjiga->avtor ?>: <?= $knjiga->naslov ?></p>
                <p><?= number_format($knjiga->cena, 2) ?> EUR<br/>
                    <button type="submit">V kosarico</button>
            </form>
        </div>
    <?php endforeach; ?>
</div>

<div class="cart">
    <h3>Kosarica</h3>
    <?php
    $kosara = isset($_SESSION["cart"]) ? $_SESSION["cart"] : [];

    // var_dump($kosara);
    if ($kosara) {
        foreach ($kosara as $id => $kolicina) {
            $knjiga = BazaKnjig::vrniKnjigo($id);
            var_dump($knjiga, $kolicina);
        }
    }

    ?>
</div>
</body>
</html>
