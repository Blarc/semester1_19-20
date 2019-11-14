<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Avtorizacija na podlagi polj certifikata X.509</title>
</head>
<body>
<?php
# Avtorizirani uporabniki (to navadno pride iz podatkovne baze)
$authorized_users = ["Ana"];

# preberemo odjemaÄev certifikat
$client_cert = filter_input(INPUT_SERVER, "SSL_CLIENT_CERT");

# in ga razÄlenemo
$cert_data = openssl_x509_parse($client_cert);

# preberemo ime uporabnika (polje "common name")
$commonname = $cert_data['subject']['CN'];

# Äe se ime nahaja na seznam avtoriziranih uporabnikov prikaĹžemo Äas.
if (in_array($commonname, $authorized_users)) {
    echo "$commonname je avtoriziran uporabnik, zato vidi trenutni Äas: " . date("H:i");
} else {
    # Sicer Äasa ne prikaĹžemo.
    echo "$commonname ni avtoriziran uporabnik in nima dostopa do ure";
}

# Celotna vsebina certifikata.
echo "<p>Vsebina certifikata: ";
var_dump($cert_data);
?>
</body>
</html>
