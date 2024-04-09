CREATE DATABASE IF NOT EXISTS kubernetes_eval;
USE kubernetes_eval;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    admin BOOLEAN DEFAULT FALSE,
    UNIQUE(username)
);

INSERT INTO users (username, password, admin) 
VALUES ('administrator', 'securepassword', TRUE);