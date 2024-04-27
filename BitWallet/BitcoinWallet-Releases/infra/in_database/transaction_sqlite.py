import sqlite3
from dataclasses import dataclass

from BitcoinWallet.core.constants import COMMISSION
from BitcoinWallet.core.errors import BalanceError, DoesNotExistError, EqualityError
from BitcoinWallet.core.transactions import Transaction
from BitcoinWallet.core.users import User
from BitcoinWallet.infra.in_database.wallet_sqlite import WalletInDatabase


@dataclass
class TransactionInDatabase:
    def __init__(self, db_path: str = "./database.db") -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS wallet_transactions (
                transaction_id TEXT NOT NULL,
                wallet_from TEXT NOT NULL,
                wallet_to TEXT NOT NULL,
                amount_in_satoshi INT NOT NULL
            );
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()

    def clear_tables(self) -> None:
        delete_table_query = """
              DELETE FROM wallet_transactions;
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(delete_table_query)

    def create(self, transaction: Transaction, user_from: User, _: User) -> int:
        wallet_from = WalletInDatabase().get(transaction.wallet_from)
        wallet_to = WalletInDatabase().get(transaction.wallet_to)

        if str(wallet_from.API_key) != str(user_from.API_key):
            raise DoesNotExistError("wallet does not exists.")

        if wallet_from is None or wallet_to is None:
            raise DoesNotExistError("wallet does not exists.")

        if transaction.wallet_from == transaction.wallet_to:
            raise EqualityError("Can not send money on the same wallet.")

        if wallet_from.balance < transaction.amount_in_satoshi:
            raise BalanceError("Not enough money.")

        WalletInDatabase().change_balance(
            transaction.wallet_from,
            round(wallet_from.balance - transaction.amount_in_satoshi),
        )
        new_balance = wallet_to.balance + transaction.amount_in_satoshi * (
            1 - COMMISSION
        )

        WalletInDatabase().change_balance(transaction.wallet_to, round(new_balance))

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO wallet_transactions
                    (transaction_id, wallet_from, wallet_to, amount_in_satoshi)
                VALUES
                    (?, ?, ?, ?);
                """,
                (
                    str(transaction.transaction_id),
                    str(transaction.wallet_from),
                    str(transaction.wallet_to),
                    transaction.amount_in_satoshi,
                ),
            )
            connection.commit()

        commission = (
            round(transaction.amount_in_satoshi * COMMISSION)
            if wallet_from.API_key != wallet_to.API_key
            else 0
        )
        return commission
