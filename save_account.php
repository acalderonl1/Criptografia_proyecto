<?php

include("db.php");

if (isset($_POST['save_account'])){
    $username = $_POST['username'];
    $password = $_POST['password'];

    $query = "INSERT INTO tb_cuenta(username, password) VALUES ('$username', '$password')";
    $result = mysqli_query($conn, $query);
    if (!$result){
        die("Query Fail!");
    }

    $_SESSION['message'] = 'Account Saved successfully';
    $_SESSION['message_type'] = 'success';


    header("Location: index.php");
}

?>