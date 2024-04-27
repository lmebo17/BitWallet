from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid4

from BitcoinWallet.core.constants import BTC_TO_SATOSHI
from BitcoinWallet.core.transactions import Transaction


@dataclass
class Wallet:
    API_key: UUID

    balance: float = 1 * BTC_TO_SATOSHI
    transactions: list[Transaction] = field(default_factory=list)
    address: UUID = field(default_factory=uuid4)

    def balance_in_btc(self) -> float:
        return self.balance / BTC_TO_SATOSHI


class WalletRepository(Protocol):
    def create(self, wallet: Wallet, user: Any) -> Wallet:
        pass

    def get(self, key: UUID) -> Wallet:
        pass


@dataclass
class WalletService:
    wallets: WalletRepository
