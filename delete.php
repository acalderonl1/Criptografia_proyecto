<?php 
    include('db.php');

    if (isset($_GET['id'])) {
      $id = $_GET['id'];
      $query = "DELETE FROM tb_cuenta WHERE id = $id";
      $result = mysqli_query($conn, $query);
      if (!$result){
          die("Query Failed!");
      }

      $_SESSION['message'] = 'Account Removed Successfully';
      $_SESSION['message_type'] = 'danger';
      header("Location: index.php");
    }
?>