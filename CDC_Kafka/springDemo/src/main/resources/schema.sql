DROP TABLE account IF EXISTS;

CREATE TABLE account (
    account_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_number VARCHAR(50) NOT NULL UNIQUE,
    account_holder_first_name VARCHAR(100) NOT NULL,
    account_holder_last_name VARCHAR(100) NOT NULL,
    balance DECIMAL(18, 2) NOT NULL
);