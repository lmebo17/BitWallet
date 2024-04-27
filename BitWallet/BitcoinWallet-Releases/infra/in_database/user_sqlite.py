import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import List
from uuid import UUID

from BitcoinWallet.core.errors import DoesNotExistError, ExistsError
from BitcoinWallet.core.transactions import Transaction
from BitcoinWallet.core.users import User
from BitcoinWallet.core.wallets import Wallet


@dataclass
class UserInDatabase:
    db_path: str = "./database.db"

    def __init__(self, db_path: str = "./database.db") -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                API_key TEXT NOT NULL,
                wallets_number INTEGER NOT NULL
            );
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()

    def clear_tables(self) -> None:
        truncate_units_query = """
            DELETE FROM users;
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(truncate_units_query)
            connection.commit()

    def create(self, user: User) -> User:
        self.create_table()

        create_user_query = """
            INSERT INTO users (API_KEY, username, password, wallets_number)
            VALUES (?, ?, ?, ?)
        """

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
            existing_user = cursor.fetchone()
            if existing_user:
                raise ExistsError("User already exists.")

            cursor.execute(
                create_user_query,
                (str(user.API_key), user.username, user.password, user.wallets_number),
            )
            connection.commit()

        return user

    def get(self, key: UUID) -> User:
        get_user_query = """
            SELECT * FROM users WHERE API_key = ?
        """

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(get_user_query, (str(key),))
            user_data = cursor.fetchone()

            if user_data:
                return User(
                    username=user_data[0],
                    password=user_data[1],
                    API_key=UUID(user_data[2]),
                    wallets_number=user_data[3],
                )
            else:
                raise DoesNotExistError(f"User with key {key} does not exist.")

    def increment_wallets_number(self, key: UUID) -> int:
        increment_query = """
            UPDATE users
            SET wallets_number = wallets_number + 1
            WHERE API_key = ?
        """

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(increment_query, (str(key),))
            connection.commit()

            cursor.execute(
                "SELECT wallets_number FROM users WHERE API_key = ?", (str(key),)
            )
            updated_wallets_number = cursor.fetchone()

            if updated_wallets_number:
                return int(updated_wallets_number[0])
            else:
                raise DoesNotExistError(f"User with key {key} does not exist.")

    def get_wallet(self, key: UUID, address: UUID) -> Wallet:
        user_query = """
            SELECT * FROM users WHERE API_key = ?
        """

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(user_query, (str(key),))
            user_data = cursor.fetchone()

            if user_data:
                wallet_query = """
                    SELECT * FROM wallets WHERE API_key = ? AND address = ?
                """
                cursor.execute(wallet_query, (str(key), str(address)))
                wallet_data = cursor.fetchone()
                if wallet_data:
                    return Wallet(
                        address=UUID(wallet_data[2]),
                        balance=wallet_data[1],
                        API_key=key,
                        transactions=self.get_wallet_transactions(UUID(wallet_data[2])),
                    )
                else:
                    raise DoesNotExistError("User does not have this wallet")
            else:
                raise DoesNotExistError(f"User with key {key} does not exist.")

    def get_transactions(self, key: UUID) -> List[Transaction]:
        self.get(key)

        wallets = self.get_user_wallets(key)
        addresses = [str(wallet.address) for wallet in wallets]

        user_query = """
                SELECT *
                FROM wallet_transactions
                WHERE
                    wallet_from IN ({})
                    OR wallet_to IN ({})
            """.format(
            ",".join(["?"] * len(addresses)), ",".join(["?"] * len(addresses))
        )

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(user_query, addresses + addresses)
            data = cursor.fetchall()

            transactions_dict = defaultdict(list)
            for result in data:
                transaction = Transaction(
                    transaction_id=result[0],
                    wallet_from=result[1],
                    wallet_to=result[2],
                    amount_in_satoshi=result[3],
                )
                transactions_dict[
                    (transaction.wallet_from, transaction.wallet_to)
                ].append(transaction)

            unique_transactions = []
            for transaction_list in transactions_dict.values():
                unique_transactions.append(transaction_list[0])

            return unique_transactions

    def get_user_wallets(self, API_key: UUID) -> list[Wallet]:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT API_key, balance, address
                FROM wallets
                WHERE API_key = ?
                """,
                (str(API_key),),
            )
            results = cursor.fetchall()

        wallets = []
        for result in results:
            wallet = Wallet(
                API_key=result[0],
                balance=result[1],
                address=result[2],
                transactions=self.get_wallet_transactions(UUID(result[2])),
            )
            wallets.append(wallet)

        return wallets

    def get_wallet_transactions(self, address: UUID) -> list[Transaction]:
        transactions = []

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT *
                FROM wallet_transactions
                WHERE wallet_from = ? or wallet_to = ?
                """,
                (
                    str(address),
                    str(address),
                ),
            )

            results = cursor.fetchall()
            for result in results:
                transaction = Transaction(
                    transaction_id=result[0],
                    wallet_from=result[1],
                    wallet_to=result[2],
                    amount_in_satoshi=result[3],
                )
                transactions.append(transaction)
        return transactions
