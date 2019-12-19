# Za delovanje preusmeritev na nivoju strežnika Apache moramo
# vklopiti modul rewrite. To naredimo z naslednjim ukazom

sudo a2enmod rewrite

# V datoteko /etc/apache2/sites-available/000-default.conf
# pod vrstico Alias /netbeans... dodamo spodnjo vsebino

Alias /netbeans/ "/home/ep/NetBeansProjects/"
<Directory /home/ep/NetBeansProjects/>
        Require all granted
        AllowOverride All
</Directory>

# Enako vsebino dodamo v konfiguracijo datoteko, ki v Apacheju določa strežbo 
# datoteko po protokolu SSL (default-ssl.conf)


# Uporaba odjemalca HTTPie

# Namestitev
sudo apt install httpie

# Preskus: poizvedba na storitev trola.si
# parameter --json nastavi polje v zaglavju accept: application/json
http --json GET "https://www.trola.si/živalski vrt/"

# Poizvedba po vseh knjigah
http http://localhost/netbeans/mvc-rest/api/books/

# Poizvedba po knjigi z izbrano številko ID
http http://localhost/netbeans/mvc-rest/api/books/1

# Dodajanje zapisa z metodo POST in pošiljanjem podatkov z obrazcem
# (znak \ pomeni skok v novo vrstico)
http --form POST http://localhost/netbeans/mvc-rest/api/books \
    title='Nova knjiga' \
    author='Nek avtor' \
    description='Nek opis' \
    price=500 \
    year=2018

# Poglejmo si nov zapis
http GET http://localhost/netbeans/mvc-rest/api/books/4

# Posodabljanje zapisa z metodo PUT
http --form PUT http://localhost/netbeans/mvc-rest/api/books/4 \
    title='Popravljen naslov knjige' \
    author='Nek avtor' \
    description='Posodobljen opis' \
    price=500 \
    year=2018

# Izbris z metodo DELETE
http DELETE http://localhost/netbeans/mvc-rest/api/books/4

# Dodatni primeri in dokumentacija
https://httpie.org/doc
