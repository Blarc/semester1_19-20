<?php
require_once 'database_jokes.php';
?>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Primer z bazo in knjiznico PDO</title>
</head>
<body>
<?php
if (isset($_GET["do"]) && $_GET["do"] == "add"): // VNOS -- ZASLONSKA MASKA
    ?>
    <h1>Dodajanje</h1>
    <form action="<?= $_SERVER["PHP_SELF"] ?>" method="post">
        <input type="hidden" name="do" value="add" />
        Datum: <input type="text" name="joke_date" value="<?= date("Y-m-d") ?>" /><br />
        <textarea rows="8" cols="60" name="joke_text"></textarea><br />
        <input type="submit" value="Shrani" />
    </form>
<?php
elseif (isset($_POST["do"]) && $_POST["do"] == "add"):
    try
    {
        DBJokes::insert($_POST["joke_date"], $_POST["joke_text"]);
    }
    catch(Exception $exc)
    {
        var_dump($exc);
        exit();
    }
    echo "Sala uspesno dodana!";
elseif (isset($_GET["do"]) && $_GET["do"] == "edit"): // UREJANJE -- ZASLONSKA MASKA
    ?>
    <h1>Urejanje</h1>
    <?php
    /* TODO: Nalozite podatke iz baze
     * Namigi:
     * - ID preberite iz globalne spremenljivke $_GET
     * - in ga uporabite, da iz PB naloĹžite vsebino ĹĄale
     */
    // var_dump($_GET);
    $id = $_GET["id"];
    $sala = DBJokes::get($id);
    // var_dump($sala);
    $date = $sala["joke_date"];
    $text = $sala["joke_text"];
    ?>
    <h2>Urejanje zapisa id = <?= $id ?></h2>
    <form action="<?= $_SERVER["PHP_SELF"] ?>" method="post">
        <input type="hidden" name="id" value="<?= $id ?>" />
        <input type="hidden" name="do" value="edit" />
        Datum: <input type="text" name="joke_date" value="<?= $date ?>" /><br />
        <textarea rows="8" cols="60" name="joke_text"><?= $text ?></textarea><br />
        <input type="submit" value="Shrani" />
    </form>

    <h2>Izbris zapisa</h2>
    <form action="<?= $_SERVER["PHP_SELF"] ?>" method="post">
        <input type="hidden" name="id" value="<?= $id ?>" />
        <input type="hidden" name="do" value="delete" />
        <input type="submit" value="Brisi" />
    </form>
<?php
elseif (isset($_POST["do"]) && $_POST["do"] == "delete"): // BRISANJE -- SQL
    ?>
    <h1>Brisanje zapisa</h1>
    <?php
    try {
        DBJokes::delete($_POST["id"]);
        echo "Sala uspesno odstranjena. <a href='$_SERVER[PHP_SELF]'>Na prvo stran.</a></p>";
    } catch (Exception $e) {
        echo "<p>Napaka pri brisanju: {$e->getMessage()}.</p>";
    }
// PRIKAZ VSEH ZAPISOV
else:
    ?>
    <h1>Vse sale</h1>
    <h2><a href="<?= $_SERVER["PHP_SELF"] . "?do=add" ?>">Dodajanje sal</a></h2>
    <?php
    try {
        $allJokes = DBJokes::getAll();
    } catch (Exception $e) {
        echo "Prislo je do napake: {$e->getMessage()}";
    }

    foreach ($allJokes as $key => $row) {
        $url = $_SERVER["PHP_SELF"] . "?do=edit&id=" . $row["id"];
        $date = $row["joke_date"];
        $text = $row["joke_text"];

        echo "<p><b>$date</b>. $text [<a href='$url'>Uredi</a>]";
    }
endif;
?>
</body>
</html>
