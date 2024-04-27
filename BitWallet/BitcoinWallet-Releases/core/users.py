from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from BitcoinWallet.core.transactions import Transaction
from BitcoinWallet.core.wallets import Wallet


@dataclass
class User:
    username: str
    password: str

    API_key: UUID = field(default_factory=uuid4)
    wallets: dict[UUID, Wallet] = field(default_factory=dict)
    wallets_number: int = 0
    transactions: list[Transaction] = field(default_factory=list)


class UserRepository(Protocol):
    def create(self, user: User) -> User:
        pass

    def get(self, key: UUID) -> User:
        pass

    def get_wallet(self, key: UUID, address: UUID) -> Wallet:
        pass

    def get_transactions(self, key: UUID) -> list[Transaction]:
        pass


@dataclass
class UserService:
    users: UserRepository
