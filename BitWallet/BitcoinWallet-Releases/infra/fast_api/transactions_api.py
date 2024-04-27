from typing import Any
from uuid import UUID

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from BitcoinWallet.core.errors import BalanceError, DoesNotExistError, EqualityError
from BitcoinWallet.core.transactions import Transaction
from BitcoinWallet.infra.fast_api.dependables import (
    StatisticRepositoryDependable,
    TransactionRepositoryDependable,
    UserRepositoryDependable,
    WalletRepositoryDependable,
)

transaction_api = APIRouter(tags=["Transactions"])


def extract_transaction_fields(transaction: Transaction) -> dict[str, Any]:
    return {
        "wallet_from": transaction.wallet_from,
        "wallet_to": transaction.wallet_to,
        "amount_in_satoshi": transaction.amount_in_satoshi,
    }


class CreateTransactionRequest(BaseModel):
    API_key: UUID
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshi: int


class EmptyItem(BaseModel):
    pass


class DoesNotExistsError:
    pass


class TransactionItem(BaseModel):
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshi: int


class TransactionItemEnvelope(BaseModel):
    transaction: TransactionItem


class TransactionListEnvelope(BaseModel):
    transactions: list[TransactionItem]


@transaction_api.post(
    "/transactions",
    status_code=201,
    response_model=EmptyItem,
)
def create_transaction(
    request: CreateTransactionRequest,
    transactions: TransactionRepositoryDependable,
    wallets: WalletRepositoryDependable,
    users: UserRepositoryDependable,
    statistics: StatisticRepositoryDependable,
) -> dict[str, Any] | JSONResponse:
    try:
        transaction = Transaction(
            wallet_from=request.wallet_from,
            wallet_to=request.wallet_to,
            amount_in_satoshi=request.amount_in_satoshi,
        )
        user_from = users.get(request.API_key)
        user_to = users.get(wallets.get(request.wallet_to).API_key)
        commission = transactions.create(transaction, user_from, user_to)
        statistics.update(commission)
        return {}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"message": "Wallet does not exist."},
        )
    except EqualityError:
        return JSONResponse(
            status_code=400,
            content={"message": "Transaction within the same wallet is not allowed."},
        )

    except BalanceError:
        return JSONResponse(
            status_code=400,
            content={"message": "Not enough balance to complete the transaction."},
        )


@transaction_api.get(
    "/transactions",
    status_code=200,
    response_model=TransactionListEnvelope,
)
def show_transaction(
    users: UserRepositoryDependable, API_key: UUID = Header(alias="API_key")
) -> dict[str, list[Any]] | JSONResponse:
    try:
        transactions = users.get_transactions(API_key)
        modified_transactions = [
            extract_transaction_fields(item) for item in transactions
        ]
        return {"transactions": modified_transactions}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"message": "User does not exist."},
        )
