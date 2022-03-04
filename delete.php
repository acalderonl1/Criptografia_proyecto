<?php
    // INCLUIMOS EL ARCHIVO DEL ESQUEMA DE LA CONECCION
    include('db.php');

    if (isset($_GET['id'])) {
      $id = $_GET['id'];
      // DETALLAMOS CON SENTENCIA SQL EL SCRIPT PARA PODER ELIMONAR DE LA BASE DE DATOS
      $query = "DELETE FROM tb_cuenta WHERE id = $id";
      $result = mysqli_query($conn, $query);
      if (!$result){
          die("Query Failed!");
      }
      
      $_SESSION['message'] = 'Account Removed Successfully';
      $_SESSION['message_type'] = 'danger';
      // REDIRECCIONAMOS AL ARCHIVO INDEX
      header("Location: index.php");
    }
