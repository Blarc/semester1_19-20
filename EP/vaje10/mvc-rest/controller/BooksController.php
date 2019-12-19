<?php

require_once("model/BookDB.php");
require_once("ViewHelper.php");

class BooksController {

    public static function get($id) {
        echo ViewHelper::render("view/book-detail.php", BookDB::get(["id" => $id]));
    }

    public static function index() {
        echo ViewHelper::render("view/book-list.php", [
            "books" => BookDB::getAll()
        ]);
    }

    public static function addForm($values = [
        "author" => "",
        "title" => "",
        "price" => "",
        "year" => "",
        "description" => ""
    ]) {
        echo ViewHelper::render("view/book-add.php", $values);
    }

    public static function add() {
        $data = filter_input_array(INPUT_POST, self::getRules());

        if (self::checkValues($data)) {
            $id = BookDB::insert($data);
            echo ViewHelper::redirect(BASE_URL . "books/" . $id);
        } else {
            self::addForm($data);
        }
    }

    public static function editForm($params) {
        if (is_array($params)) {
            $values = $params;
        } else if (is_numeric($params)) {
            $values = BookDB::get(["id" => $params]);
        } else {
            throw new InvalidArgumentException("Cannot show form.");
        }

        echo ViewHelper::render("view/book-edit.php", $values);
    }

    public static function edit($id) {
        $data = filter_input_array(INPUT_POST, self::getRules());

        if (self::checkValues($data)) {
            $data["id"] = $id;
            BookDB::update($data);
            ViewHelper::redirect(BASE_URL . "books/" . $data["id"]);
        } else {
            self::editForm($data);
        }
    }

    public static function delete($id) {
        $data = filter_input_array(INPUT_POST, [
            'delete_confirmation' => FILTER_REQUIRE_SCALAR
        ]);

        if (self::checkValues($data)) {
            BookDB::delete(["id" => $id]);
            $url = BASE_URL . "books";
        } else {
            $url = BASE_URL . "books/edit/" . $id;
        }

        ViewHelper::redirect($url);
    }

    /**
     * Returns TRUE if given $input array contains no FALSE values
     * @param type $input
     * @return type
     */
    public static function checkValues($input) {
        if (empty($input)) {
            return FALSE;
        }

        $result = TRUE;
        foreach ($input as $value) {
            $result = $result && $value != false;
        }

        return $result;
    }

    /**
     * Returns an array of filtering rules for manipulation books
     * @return type
     */
    public static function getRules() {
        return [
            'title' => FILTER_SANITIZE_SPECIAL_CHARS,
            'author' => FILTER_SANITIZE_SPECIAL_CHARS,
            'description' => FILTER_SANITIZE_SPECIAL_CHARS,
            'price' => FILTER_VALIDATE_FLOAT,
            'year' => [
                'filter' => FILTER_VALIDATE_INT,
                'options' => [
                    'min_range' => 1800,
                    'max_range' => date("Y")
                ]
            ]
        ];
    }

}
