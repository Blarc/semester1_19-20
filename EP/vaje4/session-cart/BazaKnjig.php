<?php

require_once 'Knjiga.php';

/**
 * BazaKnjig je razred, ki imitira podatkovno bazo. SluĹži kot pripomoÄek,
 * ki hrani seznam knjig, ki jih uporablja spletna prodajalna. Funkcije
 * tega razreda bi tipiÄno bile realizirane z uporabo podatkovne baze.
 */
class BazaKnjig {

    /**
     * Vrne seznam vseh knjig, ki se nahajajo v spletni knjigarni.
     *
     * @return Seznam vseh knjig.
     */
    public static function seznamVsehKnjig() {
        $knjige = array();
        $knjige[] = new Knjiga("Prolog Programming for Artificial Intelligence", "Ivan Bratko", 1, 134);
        $knjige[] = new Knjiga("Arhitektura racunalniskih sistemov", "Dusan Kodek", 2, 70.2);
        $knjige[] = new Knjiga("Managing Information Systems Security and Privacy", "Denis Trcek", 3, 120.6);
        $knjige[] = new Knjiga("Studijski koledar", "FRI", 4, 19.99);

        return $knjige;
    }

    /**
     * Vrne knjigo za podano vrednost $id. Äe zapis ne obstaja se sproĹži izjema.
     * @param type $id
     * @return type Knjiga
     */
    public static function vrniKnjigo($id) {
        foreach (self::seznamVsehKnjig() as $knjiga) {
            if ($id == $knjiga->id) {
                return $knjiga;
            }
        }

        throw new InvalidArgumentException("Knjiga z id = $id ne obstaja.");
    }

}
