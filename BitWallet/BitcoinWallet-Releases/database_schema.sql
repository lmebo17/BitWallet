DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users
(
    username       TEXT    NOT NULL,
    password       TEXT    NOT NULL,
    API_key        TEXT    NOT NULL,
    wallets_number INTEGER NOT NULL
);

DROP TABLE IF EXISTS wallets;
CREATE TABLE IF NOT EXISTS wallets
(
    API_key        TEXT    NOT NULL,
    balance        float   NOT NULL,
    address        TEXT    NOT NULL
);

DROP TABLE IF EXISTS wallet_transactions;
CREATE TABLE IF NOT EXISTS wallet_transactions
(
    transaction_id          TEXT    NOT NULL,
    wallet_from               TEXT    NOT NULL,
    wallet_to                 float   NOT NULL,
    amount_in_satoshi        int    NOT NULL
);


DROP TABLE IF EXISTS statistics;
CREATE TABLE IF NOT EXISTS statistics
(

    transaction_number        int    NOT NULL,
    profit_in_satoshi        int    NOT NULL
);