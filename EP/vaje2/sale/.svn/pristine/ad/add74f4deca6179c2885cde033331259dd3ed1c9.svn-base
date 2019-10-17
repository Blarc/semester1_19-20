<?php
try {
    $options = array(
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_PERSISTENT => true,
        PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8'
    );

    $db = new PDO("mysql:host=localhost;dbname=jokes", "root", "ep", $options);

    # preberemo id iz zahtevka GET
    $id = null;

    # pripravimo poizvedbo
    $statement = $db->prepare("");
    
    # Spremenljivke dodamo z imenskimi parametri
    # $statement->bindParam(...);
    
    $statement->execute();

    $joke = $statement->fetch();

    // zapišemo podatke v spremenljivke
    $date = $joke["joke_date"];
    $text = $joke["joke_text"];
} catch (PDOException $e) {
    echo "Napaka pri poizvedbi: " . $e->getMessage();
    exit();
}
?><!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Spletne šale: urejanje</title>
    </head>
    <body>
        <h1>Urejanje šal</h1>
        <p><a href="index.php">Seznam vseh</a></p>
        <h2>Urejanje (id=<?= $id ?>)</h2>
        <!-- spremenljivke uporabimo, da nastavimo privzete vrednosti obrazca -->
        <form action="urejanje-procesiranje.php" method="????">
            <input type="hidden" name="id" value="<?= $id ?>" />
            <label>Datum: <input type="date" name="joke_date" value="<?= $date ?>" /></label><br />
            <textarea required rows="8" cols="60" name="joke_text"><?= $text ?></textarea><br />
            <button>Shrani</button>
        </form>

        <h2>Izbris</h2>
        <form action="izbris-procesiranje.php" method="????">
            <input type="hidden" name="id" value="<?= $id ?>" />
            <button>Briši</button>
        </form>
    </body>
</html>
