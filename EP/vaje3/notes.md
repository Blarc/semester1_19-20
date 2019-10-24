### Notes
* htmlspecialchars(string)
* spremenljivka $_SERVER["PHP_SELF"]/poljubna/vsebina -> XSS
    * skopira se v telo dokumenta
    * rešitev -> htmlspecialchars
    * ali namesto nje basename(__FILE__)
    * $_SERVER["SCRIPT_FILENAME"]
    * lahko kar #
* filter_input() -> preverjanje.php
* filter_input_array() -> preverjanje.php
* SQL injection
   * konkatencija spremenljivk neposredeno v pozvedbi NO GO
   * resitev -> bind value
   * obramba -> vse vnose precistit, ampak res VSE
   * pdo, prepared statemente
   * mysql_real_escape_string() - don't use, ancient
   
* regularni izrazi (extra)