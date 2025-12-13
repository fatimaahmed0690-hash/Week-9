mysql -u root -p 

DROP DATABASE IF EXISTS week9_cyber_db;

CREATE DATABASE week9_cyber_db;

DROP USER IF EXISTS 'week9user'@'localhost';

CREATE USER 'week9user'@'localhost'
IDENTIFIED VIA mysql_native_password
USING PASSWORD('MyPassword123');

GRANT ALL PRIVILEGES ON week9_cyber_db.* TO 'week9user'@'localhost';

FLUSH PRIVILEGES;

USE week9_cyber_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);
EXIT;
mysql -u week9user -p
MyPassword123
