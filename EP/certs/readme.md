# Navodila 

Ta mapa vsebuje nekaj primerov digitalnih potrdil. Nekatere se namestijo
v brskalnik, druge v spletni streĹžnik.

* Datoteke s koncnico `.p12` vsebujejo osebne certifikate. Uvozite jih v
  brskalnik. Geslo za uvoz je `ep`.

* Datoteki `localhost-cert.pem` ter `localhost-key.pem` predstavljata streĹžnikov
  certifikat oz. zasebni kljuÄ. Namestite ju v ustrezno mapo (denimo
  `/etc/apache2/ssl`), nato pa v konfiguracijsko datoteko streĹžnika Apache2
  (`/etc/apache2/sites-available/default-ssl.conf`) dodajte direktivi
  `SSLCertificateFile` oz. `SSLCertificateKeyFile`, ki kaĹžeta na omenjeni
  datoteki.

* Datoteka `epca-cacert.pem` predstavlja certifikat certifikatne agencije EPCA,
  ki je podpisala vse certifikate. Njeno lokacijo najavite streĹžniku Apache2 v
  konfiguracijski datoteki z ukazom `SSLCACertificateFile /pot/do/epca-cacert.pem`.

  Pravtako morate ta certifikat uvoziti v brskalnik kot zaupanja vredno
  avtoriteto za identifikacijo spletnih strani.

* Datoteka `epca-crl.pem` predstavlja seznam preklicanih digitalnih potrdil.
  Njeno lokacijo prijavite v konfiguracijsko datoteko streĹžnika Apache2 z
  ukazom `SSLCARevocationFile /pot/do/epca-crl.pem`.

* Za pravilno delovanje datotek `.htaccess` mora biti vklopljen modul `rewrite`.
  Slednje storite z ukazom `sudo a2enmod rewrite`.

  Nato pa v datoteki `/etc/apache2/sites-available/{000-default,default-ssl}.conf`
  pod vrstico `Alias /netbeans ...` dodamo spodnjo vsebino

  ```
  Alias /netbeans/ "/home/ep/NetBeansProjects/"
  <Directory /home/ep/NetBeansProjects/>
        Require all granted
        AllowOverride All
  </Directory>
  ```
