<?php

// enables sessions for the entire app
session_start();

require_once("controller/BooksController.php");
require_once("controller/BooksRESTController.php");

define("BASE_URL", rtrim($_SERVER["SCRIPT_NAME"], "index.php"));
define("IMAGES_URL", rtrim($_SERVER["SCRIPT_NAME"], "index.php") . "static/images/");
define("CSS_URL", rtrim($_SERVER["SCRIPT_NAME"], "index.php") . "static/css/");

$path = isset($_SERVER["PATH_INFO"]) ? trim($_SERVER["PATH_INFO"], "/") : "";

$urls = [
    "/^books$/" => function ($method) {
        BooksController::index();
    },
    "/^books\/(\d+)$/" => function ($method, $id) {
        BooksController::get($id);
    },
    "/^books\/add$/" => function ($method) {
        if ($method == "POST") {
            BooksController::add();
        } else {
            BooksController::addForm();
        }
    },
    "/^books\/edit\/(\d+)$/" => function ($method, $id) {
        if ($method == "POST") {
            BooksController::edit($id);
        } else {
            BooksController::editForm($id);
        }
    },
    "/^books\/delete\/(\d+)$/" => function ($method, $id) {
        if ($method == "POST") {
            BooksController::delete($id);
        }
    },
    "/^books\/(\d+)\/(foo|bar|baz)\/(\d+)$/" => function ($method, $id, $val, $num) {
        // primer kako definirati funkcijo, ki vzame dodatne parametre
        // http://localhost/netbeans/mvc-rest/books/1/foo/10
        echo "$id, $val, $num";
    },
    "/^$/" => function () {
        ViewHelper::redirect(BASE_URL . "books");
    },
    # REST API
    "/^api\/books\/(\d+)$/" => function ($method, $id) {
        // TODO: izbris knjige z uporabo HTTP metode DELETE
        switch ($method) {
            case "PUT":
                BooksRESTController::edit($id);
                break;
            default: # GET
                BooksRESTController::get($id);
                break;
        }
    },
    "/^api\/books$/" => function ($method) {
        switch ($method) {
            case "POST":
                BooksRESTController::add();
                break;
            default: # GET
                BooksRESTController::index();
                break;
        }
    },
];

foreach ($urls as $pattern => $controller) {
    if (preg_match($pattern, $path, $params)) {
        try {
            $params[0] = $_SERVER["REQUEST_METHOD"];
            $controller(...$params);
        } catch (InvalidArgumentException $e) {
            ViewHelper::error404();
        } catch (Exception $e) {
            ViewHelper::displayError($e, true);
        }

        exit();
    }
}

ViewHelper::displayError(new InvalidArgumentException("No controller matched."), true);
