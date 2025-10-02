<?php
$mysql = file_get_contents("http://crud-mysql:8000/pessoas");
$pg = file_get_contents("http://crud-postgres:8000/pessoas");

echo "<h1>Gestão de Pessoas</h1>";
echo "<h2>MySQL</h2><pre>$mysql</pre>";
echo "<h2>Postgres</h2><pre>$pg</pre>";
?>
