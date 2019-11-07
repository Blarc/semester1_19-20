<?php

/**
 * Razred Knjiga
 */
class Knjiga {

    /**
     * Naslov knjige
     * @var type String
     */
    public $naslov = null;

    /**
     * Avtor knjige
     * @var type String
     */
    public $avtor = null;

    /**
     * Identifikator knjige
     * @var type int
     */
    public $id = 0;

    /**
     * Cena knjige
     * @var type Double
     */
    public $cena = 0;

    /**
     * Kreira novo instanco s podanim naslovom, avtorjem,
     * identifikatorjem in ceno.
     * @param type $naslov
     * @param type $avtor
     * @param type $id
     * @param type $cena
     */
    public function __construct($naslov, $avtor, $id, $cena) {
        $this->naslov = $naslov;
        $this->avtor = $avtor;
        $this->id = $id;
        $this->cena = $cena;
    }

    /**
     * Vrne predstavitev knige v nizu.
     * @return type String
     */
    public function __toString() {
        return $this->avtor . ': ' . $this->naslov . ' ('
            . number_format($this->cena, 2, ',', '.') . ' âŹ)';
    }

}
