<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Primer strani za prijavo</title>
</head>
<body>
<?php
if (isset($_POST["uname"]) && isset($_POST["password"])):
    try {
        $dbh = new PDO("mysql:host=localhost;dbname=injection", "root", "ep");
        $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $dbh->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        // konkatencija spremenljivk neposredeno v pozvedbi NO GO
        // reistev -> bind value
        $query = "SELECT * FROM users WHERE uname = '$_POST[uname]' "
            . "AND password = '$_POST[password]'";
        $stmt = $dbh->prepare($query);
        $stmt->execute();
        $user = $stmt->fetch();

        if ($user) {
            echo "DobrodoĹĄli na skrivni strani!";
            var_dump($user);
        } else {
            echo "Prijava neuspeĹĄna.";
        }
    } catch (Exception $e) {
        die($e->getMessage());
    }
else:
    ?>
    <form action="<?= $_SERVER["PHP_SELF"] ?>" method="post">
        Username <input type="text" name="uname" />
        Password <input type="password"	name="password" />
        <input type="submit" value="PoĹĄlji podatke">
    </form>
<?php
endif;
?>
</body>
</html>
