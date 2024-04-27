from dataclasses import dataclass

from BitcoinWallet.core.constants import COMMISSION
from BitcoinWallet.core.errors import BalanceError, DoesNotExistError, EqualityError
from BitcoinWallet.core.transactions import Transaction
from BitcoinWallet.core.users import User


@dataclass
class TransactionInMemory:
    @staticmethod
    def create(transaction: Transaction, user_from: User, user_to: User) -> int:
        wallet_from = user_from.wallets[transaction.wallet_from]
        wallet_to = user_to.wallets[transaction.wallet_to]

        if wallet_from is None or wallet_to is None:
            raise DoesNotExistError("wallet does not exists.")

        if transaction.wallet_from == transaction.wallet_to:
            raise EqualityError("Can not send money on the same wallet.")

        if wallet_from.balance < transaction.amount_in_satoshi:
            raise BalanceError("Not enough money.")

        wallet_from.balance -= transaction.amount_in_satoshi
        wallet_to.balance += transaction.amount_in_satoshi * (1 - COMMISSION)
        if transaction not in wallet_from.transactions:
            wallet_from.transactions.append(transaction)
        if transaction not in wallet_to.transactions:
            wallet_to.transactions.append(transaction)

        if transaction not in user_from.transactions:
            user_from.transactions.append(transaction)
        if transaction not in user_to.transactions:
            user_to.transactions.append(transaction)

        commission = (
            round(transaction.amount_in_satoshi * COMMISSION)
            if wallet_from.API_key != wallet_to.API_key
            else 0
        )
        return commission
