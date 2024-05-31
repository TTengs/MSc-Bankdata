-- Create a table
CREATE TABLE account (
    account_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_number VARCHAR(50) NOT NULL UNIQUE,
    account_holder_first_name VARCHAR(100) NOT NULL,
    account_holder_last_name VARCHAR(100) NOT NULL,
    balance DECIMAL(18, 2) NOT NULL
);

CREATE TABLE account_loan_type (
    loan_type_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id BIGINT NOT NULL,
    loan_type VARCHAR(10) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);
