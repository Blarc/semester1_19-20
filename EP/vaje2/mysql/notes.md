# MySQL

## Terminal

mysql -u root -p
geslo

show databases;

use mysql;

show tables;

describe user;

select * from user;
// grd izpis, ker je veliko podatkov

select Host, User, password_expired from user;
// izpiše tabelo

## MySQL Workbench

klikneš + pri models in izbereš?

poimenovanje baze: dvakrat kliknemo na mydb in spremenimo
spodej imamo default collation:
* collation - kaj se zgodi ko damo order by
* nastavimo UTF-8 CI
* ci - case insensitive

dvakrat kliknemo na "add diagram"
pokaže se canvas kamor lahko rišemo entitetne tipe oz. modele

* izberemo place a new table
* dvakrat kliknemo in jo preimenujemo
* colation default in engine InnoDB (že vnaprej, je ok)

* id - PK (primary key), NN (not null), AI (auto increment)
* ime - varchar(255), NN
* priimek - varchar(255), NN

zavihek database
* reverse engineer - poveži v DB v neko schemo, preglej katere tabele so, in not nariši
* forward engineer - namestit DB
* synchornise model - že imamo db hkrati pa modeliramo

izberemo formward
local instance
geslo: ep
naprej, naprej, naprej

preverimo v terminalu da se je res naredilo

## Terminal

show databases;
use vaja;
show tables;
describe oseba;

## SQL Workbench

dodamo ulica_stevilka varchar(255), NN

nova tabela (place a new table): posta
columns:
* id PK, AI, NN
* stevilka (int) NN, UQ
* kraj varchar(255), NN

dve vrsti povezav:
* identifying - oseba dobi nov atribut id posta, ampak postane del PK
* non-identifying - ena tabela dobi nov atribut id posta

1 proti N, non-identifying (med oseba in posta)

database -> synchornise model
naprej
naprej
se je povezal na DB
dalje
diff
next
execute

## Terminal

show tables;
describe oseba; (ulica, številka in pošta)
describe pošta;
insert into posta (stevilka, kraj) values (1000, 'Ljubljana');
select * from posta;

## SQL Workbench

home ikona
local instance 3306
povezava na DB
vaja -> tables -> posta -> desni klik -> select rows -> definirala poizvedba
-> vidimo zapise
dodaš Maribor in klikneš apply


NOW() - current date

## Kako se povezati na mySQL s PhP

* ne uporabljaj mysql_, manj varne, delajo samo s mySQL

### Library PDO
* PHP Data Objects
* podpira veliko sistemov
* med bazami lahko poljbno prehajamo
* omogoče objektno programiranje
* bolj varna

### Kako povezati na bazo?
* glej prosojnice - koda





