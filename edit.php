<?php
include("db.php");
$platform = '';
$username = '';
$password = '';

if (isset($_GET['id'])) {
  $id = $_GET['id'];
  $query = "SELECT * FROM tb_cuenta WHERE id=$id";
  $result = mysqli_query($conn, $query);
  if (mysqli_num_rows($result) == 1) {
    $row = mysqli_fetch_array($result);
    $platform = $row['platform'];
    $username = $row['username'];
    $password = $row['password'];
  }
}

if (isset($_POST['update'])) {
  $id = $_GET['id'];

  $platform = $_POST['platform'];
  $username = $_POST['username'];
  $password = $_POST['password'];

  $query = "UPDATE tb_cuenta set platform = '$platform', username = '$username', password = '$password' WHERE id=$id";
  mysqli_query($conn, $query);
  $_SESSION['message'] = 'Account Updated Successfully';
  $_SESSION['message_type'] = 'warning';
  header('Location: index.php');
}

if(isset($_POST['back'])){
  $_SESSION['message'] = 'Account Not Updated';
  $_SESSION['message_type'] = 'danger';
  header("Location: index.php");
}

?>
<?php include('include/heder.php'); ?>
<div class="container p-4">
  <div class="row">
    <div class="col-md-4 mx-auto">
      <div class="card card-body">
        <form action="edit.php?id=<?php echo $_GET['id']; ?>" method="POST">
          <div class="form-group">
            <input name="platform" type="text" class="form-control" value="<?php echo $platform; ?>" placeholder="Update usermane">
          </div>
          <div class="form-group">
            <input name="username" type="text" class="form-control" value="<?php echo $username; ?>" placeholder="Update usermane">
          </div>
          <div class="form-group">
            <input name="password" type="text" class="form-control" value="<?php echo $password; ?>" placeholder="Update password">
          </div>
          <button class="btn btn-success" name="update">
            Update
          </button>
          <button class="btn btn-danger" name="back">
            Back
          </button>
        </form>
      </div>
    </div>
  </div>
</div>
<?php include('include/footer.php'); ?>