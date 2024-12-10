/* SQL DB in PostgreSQL to store user login data */

CREATE TABLE users (
    username VARCHAR(80) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);
