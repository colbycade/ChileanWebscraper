DROP DATABASE SCRAPECHILE;
CREATE DATABASE ScrapeChile;
USE ScrapeChile;

-- Entries Table
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    ENTRY_ID   INT PRIMARY KEY AUTO_INCREMENT,
    ENTRY_NAME VARCHAR(255) NOT NULL UNIQUE
);

-- Users Table
DROP TABLE IF EXISTS USERS;
CREATE TABLE USERS (
    USER_ID  INT PRIMARY KEY AUTO_INCREMENT,
    USERNAME VARCHAR(255) NOT NULL UNIQUE
);

-- Note the use of auto-incrementing ids as primary keys.
-- This doesn't violate 3NF because entry_name and username are candidate keys.
-- Numerical primary keys may speed up insertions and joins, however, they really aren't necessary here.
-- I just wanted to experiment with the auto-incrementer and thought ids looked more "traditional".
-- In the Oracle implementation I remove these ids to simplify batch inserts.

-- Definitions Table
DROP TABLE IF EXISTS DEFINITIONS;
CREATE TABLE DEFINITIONS (
    DEFINITION_ID     CHAR(64) PRIMARY KEY, -- hash column as primary key insures no duplicate definitions (at least not by the same user)
    DEFINITION_TEXT   TEXT NOT NULL,
    EXAMPLE_TEXT      TEXT,
    SYNONYMS          TEXT,
    TIME_SINCE_UPLOAD VARCHAR(50),
    TIME_IN_DAYS      FLOAT,
    VOTES             INT,
    ENTRY_ID          INT NOT NULL,
    USER_ID           INT NOT NULL,
    FOREIGN KEY ( ENTRY_ID )
        REFERENCES ENTRIES ( ENTRY_ID ),
    FOREIGN KEY ( USER_ID )
        REFERENCES USERS ( USER_ID )
);