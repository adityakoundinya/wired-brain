CREATE DATABASE IF NOT EXISTS products;

USE products;

CREATE TABLE IF NOT EXISTS products (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR (128) NOT NULL
) ENGINE=INNODB
