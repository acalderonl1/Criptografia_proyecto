<?php

include("db.php");
// metodo de ingreso a la base de datos
if (isset($_POST['save_account'])){
    $platform = $_POST['platform'];
    $username = $_POST['username'];
    $password = $_POST['password'];
    // query para ingresar a la base directamente
    $query = "INSERT INTO tb_cuenta(platform ,username, password) VALUES ('$platform', '$username', '$password')";
    $result = mysqli_query($conn, $query);
    if (!$result){
        die("Query Fail!");
    }
    // manejo de sesiones y mensajes
    $_SESSION['message'] = 'Account Saved successfully';
    $_SESSION['message_type'] = 'success';


    header("Location: index.php");
}
