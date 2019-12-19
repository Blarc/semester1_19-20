<!DOCTYPE html>

<link rel="stylesheet" type="text/css" href="<?= CSS_URL . "style.css" ?>">
<meta charset="UTF-8" />
<title>Book detail</title>

<h1>Details of: <?= $title ?></h1>

<p>[
    <a href="<?= BASE_URL . "books" ?>">All books</a> |
    <a href="<?= BASE_URL . "books/add" ?>">Add new</a>
    ]</p>

<ul>
    <li>Author: <b><?= $author ?></b></li>
    <li>Title: <b><?= $title ?></b></li>
    <li>Price: <b><?= $price ?> EUR</b></li>
    <li>Year: <b><?= $year ?></b></li>
    <li>Description: <i><?= $description ?></i></li>
</ul>

<p>[ <a href="<?= BASE_URL . "books/edit/" . $id ?>">Edit</a> |
    <a href="<?= BASE_URL . "books" ?>">Book index</a> ]</p>
