create table tb_cuenta (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	usuario varchar(25),
	contrasena varchar(50),
	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
