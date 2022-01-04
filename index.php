<?php include('db.php') ?>
<?php include('include/heder.php') ?>


<div class="container p-4">
    <div class="row">
        <div class="col-md-4">
            <?php if (isset($_SESSION['message'])) { ?>
                <div class="alert alert-<?= $_SESSION['message_type'] ?> alert-dismissible fade show" role="alert">
                    <?= $_SESSION['message'] ?>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            <?php session_unset();
            } ?>


            <script>
                window.addEventListener("load", function() {

                    // icono para mostrar contraseña
                    showPassword = document.querySelector('.show-password');
                    showPassword.addEventListener('click', () => {

                        // elementos input de tipo clave
                        password1 = document.querySelector('.password1');

                        if (password1.type === "text") {
                            password1.type = "password"
                            showPassword.classList.remove('fa-eye-slash');
                        } else {
                            password1.type = "text"
                            showPassword.classList.toggle("fa-eye-slash");
                        }

                    })

                });
            </script>

            <div class="card card-body">
                <h5>Enter your account</h5>
                <h5></h5>
                <form action="save_account.php" class="input-wrapper" id="contact" method="POST">
                    <div class="form-group">
                        <input type="text" name="platform" class="form-control" placeholder="Enter platform" autofocus>
                    </div>
                    <div class="form-group">
                        <input type="text" name="username" class="form-control" placeholder="Enter username" autofocus>
                    </div>
                    <div class="form-group input-group-append ">
                        <input type="password" name="password" class="form-control password1" placeholder="Enter password" autofocus>
                        <span class="fa fa-fw fa-eye password-icon show-password btn btn-online-secondary"></span>
                    </div>
                    <input type="Submit" class="btn btn-success btn-block" name="save_account" value="Save Account">
                </form>
            </div>
            <br>
            <div class="card card-body">
                <h5>Enter your key</h5>
                <h5></h5>
                <form action="save_account.php" class="input-wrapper" id="contact" method="POST">
                    <div class="form-group">
                        <input type="text" name="key" class="form-control" placeholder="Enter key" autofocus>
                    </div>

                    <input type="Submit" class="btn btn-success btn-block" name="key" value="Validate key">
                </form>
            </div>

        </div>


        <div class="col-md-8">
            <h1>Accounts</h1>
            <table class="table table-hover table-bordered table-responsive">
                <thead class="thead-dark">
                    <tr>
                        <th>Platform</th>
                        <th>Username</th>
                        <th>Password</th>
                        <th>Created at</th>
                        <th>Actions</th>

                    </tr>
                </thead>
                <tbody>
                    <?php
                    $query = "SELECT * FROM tb_cuenta";
                    $result_tasks = mysqli_query($conn, $query);

                    while ($row = mysqli_fetch_array($result_tasks)) { ?>
                        <tr>
                            <td><?php echo $row['platform'] ?></td>
                            <td><?php echo $row['username'] ?></td>
                            <td><?php echo $row['password'] ?></td>
                            <td><?php echo $row['create_at'] ?></td>
                            <td>
                                <a href="edit.php?id=<?php echo $row['id'] ?>" class="btn btn-secondary btn-group">
                                    <i class="far fa-edit"></i>
                                    <a href="delete.php?id=<?php echo $row['id'] ?>" class="btn btn-danger btn-group">
                                        <i class="far fa-trash-alt"></i>
                                    </a>
                                </a>
                            </td>
                        </tr>
                    <?php } ?>

                </tbody>
            </table>
        </div>
    </div>

</div>


<?php include('include/footer.php') ?>