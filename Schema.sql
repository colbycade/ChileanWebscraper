DROP DATABASE ScrapeChile;
CREATE DATABASE ScrapeChile;
USE ScrapeChile;

-- Entries Table
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    entry_id INT PRIMARY KEY AUTO_INCREMENT,
    entry_name VARCHAR(255) NOT NULL UNIQUE
);

-- Users Table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE
);

-- Definitions Table
DROP TABLE IF EXISTS definitions;
CREATE TABLE definitions (
    definition_id INT PRIMARY KEY AUTO_INCREMENT,
    definition_text TEXT NOT NULL,
    example_text TEXT,
    synonyms TEXT,
    display_time VARCHAR(50),
    time_in_days INT,
    votes INT,
    entry_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES entries(entry_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);