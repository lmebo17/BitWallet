from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid4


@dataclass
class Transaction:
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshi: float
    transaction_id: UUID = field(default_factory=uuid4)

    def __eq__(self, other: Any) -> bool:
        return bool(self.transaction_id == other.transaction_id)


@dataclass
class TransactionRepository(Protocol):
    def create(self, transaction: Transaction, user_from: Any, user_to: Any) -> int:
        pass


@dataclass
class TransactionService:
    transactions: TransactionRepository
