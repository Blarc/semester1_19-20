<!DOCTYPE html>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>V celoti dinamična spletna stran po metodi POST</title>

<?php
if (isset($_POST["ime_uporabnika"]) && isset($_POST["priimek_uporabnika"])) {
    $ime = $_POST["ime_uporabnika"];
    $priimek = $_POST["priimek_uporabnika"];

    echo "Pozdravljen $ime $priimek. Ura je " . date("H:i");
} else {
    ?>
    <form action="<?php echo $_SERVER["PHP_SELF"]; ?>" method="post">
        Ime <input type="text" name="ime_uporabnika"> 
        Priimek <input type="text" name="priimek_uporabnika" />
        <input type="submit" value="Pošlji podatke">
    </form><?php
}
