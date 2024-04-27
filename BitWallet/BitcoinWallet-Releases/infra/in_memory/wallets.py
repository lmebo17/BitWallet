from dataclasses import dataclass, field
from uuid import UUID

from BitcoinWallet.core.constants import MAXIMUM_NUMBER_OF_WALLETS
from BitcoinWallet.core.errors import CapacityError, DoesNotExistError
from BitcoinWallet.core.users import User
from BitcoinWallet.core.wallets import Wallet


@dataclass
class WalletInMemory:
    wallets: dict[UUID, Wallet] = field(default_factory=dict)

    def create(self, wallet: Wallet, user: User) -> Wallet:
        if user.wallets_number == MAXIMUM_NUMBER_OF_WALLETS:
            raise CapacityError
        self.wallets[wallet.address] = wallet
        user.wallets[wallet.address] = wallet
        user.wallets_number += 1
        return wallet

    def get(self, key: UUID) -> Wallet:
        wallet = self.wallets.get(key)
        if wallet is None:
            raise DoesNotExistError(f"User with key {key} does not exist.")
        return wallet
