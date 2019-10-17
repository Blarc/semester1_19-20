<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Spletne šale: seznam vseh</title>
    </head>
    <body>
        <h1>Vnos šale</h1>
        <p><a href="index.php">Seznam vseh</a></p>
        <form action="vnos-procesiranje.php" method="???">
            <label>Datum: <input required type="date" name="joke_date" 
                                 value="<?= date("Y-m-d") ?>" /></label><br />
            <textarea required rows="8" cols="60" name="joke_text"></textarea><br />
            <button>Shrani</button>
        </form>
    </body>
</html>
