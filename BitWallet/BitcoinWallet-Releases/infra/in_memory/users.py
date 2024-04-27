from dataclasses import dataclass, field
from uuid import UUID

from BitcoinWallet.core.errors import DoesNotExistError, ExistsError
from BitcoinWallet.core.transactions import Transaction
from BitcoinWallet.core.users import User
from BitcoinWallet.core.wallets import Wallet


@dataclass
class UserInMemory:
    users: dict[UUID, User] = field(default_factory=dict)

    def create(self, user: User) -> User:
        for existing_user in self.users.values():
            if existing_user.username == user.username:
                raise ExistsError("User already exists.")

        self.users[user.API_key] = user
        return user

    def get(self, key: UUID) -> User:
        user = self.users.get(key)
        if user is None:
            raise DoesNotExistError(f"User with key {key} does not exist.")
        return user

    def get_wallet(self, key: UUID, address: UUID) -> Wallet:
        user = self.get(key)
        wallet = user.wallets.get(address)
        if wallet is None:
            raise DoesNotExistError("User does not have this wallet")
        return wallet

    def get_transactions(self, key: UUID) -> list[Transaction]:
        user = self.get(key)
        return user.transactions
