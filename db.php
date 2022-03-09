<!-- ESQUEMA DE CONECCION A LA BASE DE DATOS -->
<?php


session_start();


$conn = mysqli_connect(
    // AQUI SE PONEN TODOS LOS DATOS DE LA BASE DE DATOS
    'localhost',
    'root',
    '',
    'criptografia'
);
