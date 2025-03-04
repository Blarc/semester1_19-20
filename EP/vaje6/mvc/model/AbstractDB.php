<?php

require_once 'model/DB.php';

abstract class AbstractDB {

    /**
     * Instanca razreda PDO
     * @var type PDO
     */
    protected static $dbh = null;

    /**
     * Vrne referenco na instanco  razreda PDO za dostop do baze. Privzeto se
     * instanca pridobi z metodo DB::getInstance(), lahko pa jo tudi nastavimo
     * sami z metodo self::setConnection($dbh).
     *
     * @return type PDO
     */
    public static function getConnection() {
        if (is_null(self::$dbh)) {
            self::$dbh = DBInit::getInstance();
        }

        return self::$dbh;
    }

    /**
     * Metoda nastavi instanco razreda PDO na v parametru podano vrednost.
     * @param type $dbh
     */
    public static function setConnection($dbh) {
        self::$dbh = $dbh;
    }

    /**
     * IzvrĹĄi poizvedbo za spremembo podatkov s podanimi parametri ter
     * vrne TRUE v primeru uspeha, sicer FALSE.
     *
     * Äe poizvedba ne vsebuje parametrov, drugi argument ni potreben. Primer:
     * modify("TRUNCATE tabela");
     *
     * Äe je poizvedba parametrizirana, je potrebno uporabiti imenske parametre
     * (angl. named parameters), tj. take, ki jih oznaÄimo z dvopiÄjem pred
     * imenom; denimo ':parameter'. Poizvedba ne sme vsebovati pozicijskih
     * parametrov (takih z uporabo vpraĹĄajev ('?')).
     *
     * Parametri se podajo kot asociativno polje, pri katerem je kljuÄ ime
     * parametra, vrednost pa njegova vsebina.
     *
     * Primer veljavnega klica:
     * modify("DELETE FROM tabela WHERE atribut = :parameter", array("parameter" => 1));
     *
     * Metoda sproĹži izjemo, Äe se podani parametri ne ujemajo s parametri
     * v poizvedbi.
     *
     * @param type $sql Poizvedba SQL
     * @param array $params Parametri poizvedbe
     * @return type Boolean
     */
    protected static function modify($sql, array $params = array()) {
        $stmt = self::getConnection()->prepare($sql);
        $params_filtered = self::filterParams($sql, $params);
        $stmt->execute($params_filtered);

        return self::getConnection()->lastInsertId();
    }

    /**
     * IzvrĹĄi poizvedbo s podanimi parametri ter vrne rezultat kot
     * numeriÄno indeksirano polje.
     *
     * Äe poizvedba ne vsebuje parametrov, drugi argument ni potreben. Primer:
     * query("SELECT * FROM tabela");
     *
     * Äe je poizvedba parametrizirana, je potrebno uporabiti imenske parametre
     * (angl. named parameters), tj. take ki jih oznaÄimo z dvopiÄjem pred
     * imenom -- npr. ':parameter'. Poizvedba ne sme vsebovati pozicijskih
     * parametrov, tj. takih z uporabo vpraĹĄajev ('?').
     *
     * Parametri se podajo kot asociativno polje, pri katerem je kljuÄ ime
     * parametra, vrednost pa njegova vsebina.
     *
     * Primer veljavnega klica:
     * query("SELECT * FROM tabela WHERE atribut = :parameter", array("parameter" => 1));
     *
     * Metoda sproĹži Exception, Äe se podani parametri ne ujemajo s parametri
     * v poizvedbi.
     *
     * @param type $sql Poizvedba SQL
     * @param array $params Parametri poizvedbe
     * @return type array Rezulat poizvedbe
     */
    protected static function query($sql, array $params = array()) {
        $stmt = self::getConnection()->prepare($sql);
        $params_filtered = self::filterParams($sql, $params);
        $stmt->execute($params_filtered);

        return $stmt->fetchAll();
    }

    /**
     * Metoda preveri ustreznost podanih parametrov za podano poizvedbo. Kot
     * rezultat vrne asociativno polje parametrov, ki vsebuje le tiste zapise,
     * ki sovpadajo s parametri podane poizvedbe.
     *
     * Äe je podanih veÄ parametrov, kot jih je navedenih v poizvedbi,
     * se odveÄni parametri ignorirajo.
     *
     * V primeru, da poizvedba vsebuje parametre, ki jih v podanem polju
     * parametrov ni, se sproĹži izjema.
     *
     * @param type $sql Poizvedba SQL
     * @param array $params Polje parametrov
     * @return array type Parametri
     */
    protected static function filterParams($sql, array $params) {
        $params_altered = self::alterKeys($params);
        $sql_split = preg_split("/[\(\) ,]/", $sql);
        $sql_params = array_values(preg_grep('/^:/', $sql_split));

        $result = array();

        foreach ($sql_params as $key => $value) {
            if (isset($params_altered[$value])) {
                $result[$value] = $params_altered[$value];
            }
        }

        if (count($sql_params) != count($result)) {
            $message = "Podani in zahtevani parametri se ne ujemajo: "
                . "zahtevani: (" . implode(", ", $sql_params) . "), "
                . "podani: (" . implode(", ", array_keys($params)) . ")";

            throw new Exception($message);
        }

        return $result;
    }

    /**
     * PomoĹžna metoda, ki spremeni kljuÄe podanemu asociativnemu polju. Metoda
     * doda dvopiÄje (':') na zaÄetek imena kljuÄev.
     *
     * Primer:
     * array("kljuc" => "vrednost") postane array(":kljuc" => "vrednost")
     *
     * @param type $params
     * @return type
     */
    protected static function alterKeys(array $params) {
        $result = array();

        foreach ($params as $key => $value) {
            $result[':' . $key] = $value;
        }

        return $result;
    }

    public static abstract function get(array $id);

    public static abstract function getAll();

    public static abstract function insert(array $params);

    public static abstract function update(array $params);

    public static abstract function delete(array $id);
}
