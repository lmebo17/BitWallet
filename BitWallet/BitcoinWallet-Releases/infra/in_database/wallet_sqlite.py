import sqlite3
from dataclasses import dataclass
from uuid import UUID

from BitcoinWallet.core.constants import MAXIMUM_NUMBER_OF_WALLETS
from BitcoinWallet.core.errors import CapacityError, DoesNotExistError
from BitcoinWallet.core.users import User
from BitcoinWallet.core.wallets import Wallet
from BitcoinWallet.infra.in_database.user_sqlite import UserInDatabase


@dataclass
class WalletInDatabase:
    def __init__(self, db_path: str = "./database.db") -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS wallets (
                API_key TEXT,
                balance INT,
                address TEXT
            );
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()

    def clear_tables(self) -> None:
        truncate_units_query = """
            DELETE FROM wallets;
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(truncate_units_query)
            connection.commit()

    def create(self, wallet: Wallet, user: User) -> Wallet:
        if user.wallets_number == MAXIMUM_NUMBER_OF_WALLETS:
            raise CapacityError

        self.create_table()

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO wallets (API_key, balance, address)
                VALUES (?, ?, ?)
                """,
                (str(wallet.API_key), wallet.balance, str(wallet.address)),
            )
            connection.commit()
        UserInDatabase().increment_wallets_number(user.API_key)
        return wallet

    def get(self, key: UUID) -> Wallet:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT API_key, balance, address
                FROM wallets
                WHERE address = ?
                """,
                (str(key),),
            )
            result = cursor.fetchone()

        if result is None:
            raise DoesNotExistError(f"Wallet with key {key} does not exist.")

        wallet = Wallet(
            API_key=result[0],
            balance=result[1],
            address=result[2],
        )

        return wallet

    def change_balance(self, address: UUID, new_balance: int) -> None:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE wallets
                SET balance = ?
                WHERE address = ?;
                """,
                (new_balance, str(address)),
            )
            connection.commit()
