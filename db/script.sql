create table tb_cuenta (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	platform varchar(50),
	username varchar(25),
	password varchar(50),
	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
