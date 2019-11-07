<?php
session_start();

require_once 'Knjiga.php';
require_once 'BazaKnjig.php';

$url = filter_input(INPUT_SERVER, "PHP_SELF", FILTER_SANITIZE_SPECIAL_CHARS);
$validationRules = ['do' => [
    'filter' => FILTER_VALIDATE_REGEXP,
    'options' => [
        "regexp" => "/^(add_into_cart|update_cart|purge_cart)$/"
    ]
],
    'id' => [
        'filter' => FILTER_VALIDATE_INT,
        'options' => ['min_range' => 0]
    ],
    'kolicina' => [
        'filter' => FILTER_VALIDATE_INT,
        'options' => ['min_range' => 0]
    ]
];
$data = filter_input_array(INPUT_POST, $validationRules);

switch ($data["do"]) {
    case "add_into_cart":
        try {
            $knjiga = BazaKnjig::vrniKnjigo($data["id"]);

            if (isset($_SESSION["cart"][$knjiga->id])) {
                $_SESSION["cart"][$knjiga->id] ++;
            } else {
                $_SESSION["cart"][$knjiga->id] = 1;
            }
        } catch (Exception $exc) {
            die($exc->getMessage());
        }
        break;
    case "update_cart":
        if (isset($_SESSION["cart"][$data["id"]])) {
            if ($data["kolicina"] > 0) {
                $_SESSION["cart"][$data["id"]] = $data["kolicina"];
            } else {
                unset($_SESSION["cart"][$data["id"]]);
            }
        }
        break;
    case "purge_cart":
        unset($_SESSION["cart"]);
        break;
    default:
        break;
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
                    <button type="submit">V koĹĄarico</button>
            </form>
        </div>
    <?php endforeach; ?>
</div>

<div class="cart">
    <h3>Kosarica</h3>

    <?php
    $kosara = isset($_SESSION["cart"]) ? $_SESSION["cart"] : [];

    if ($kosara):
        $znesek = 0;

        foreach ($kosara as $id => $kolicina):
            $knjiga = BazaKnjig::vrniKnjigo($id);
            $znesek += $knjiga->cena * $kolicina;
            ?>
            <form action="<?= $url ?>" method="post">
                <input type="hidden" name="do" value="update_cart" />
                <input type="hidden" name="id" value="<?= $knjiga->id ?>" />
                <input type="number" name="kolicina" value="<?= $kolicina ?>"
                       class="short_input" />
                &times; <?=
                (strlen($knjiga->naslov) < 30) ?
                    $knjiga->naslov :
                    substr($knjiga->naslov, 0, 26) . " ..."
                ?>
                <button type="submit">Posodobi</button>
            </form>
        <?php endforeach; ?>

        <p>Total: <b><?= number_format($znesek, 2) ?> EUR</b></p>

        <form action="<?= $url ?>" method="POST">
            <input type="hidden" name="do" value="purge_cart" />
            <input type="submit" value="Izprazni koĹĄarico" />
        </form>
    <?php else: ?>
        Kosara je prazna.
    <?php endif; ?>
</div>
</body>
</html>
