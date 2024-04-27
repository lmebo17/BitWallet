from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from BitcoinWallet.core.statistics import StatisticRepository
from BitcoinWallet.core.transactions import TransactionRepository
from BitcoinWallet.core.users import UserRepository
from BitcoinWallet.core.wallets import WalletRepository


def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.users  # type: ignore


UserRepositoryDependable = Annotated[UserRepository, Depends(get_user_repository)]


def get_wallet_repository(request: Request) -> WalletRepository:
    return request.app.state.wallets  # type: ignore


WalletRepositoryDependable = Annotated[WalletRepository, Depends(get_wallet_repository)]


def get_transaction_repository(request: Request) -> TransactionRepository:
    return request.app.state.transactions  # type: ignore


TransactionRepositoryDependable = Annotated[
    TransactionRepository, Depends(get_transaction_repository)
]


def get_statistic_repository(request: Request) -> StatisticRepository:
    return request.app.state.statistics  # type: ignore


StatisticRepositoryDependable = Annotated[
    StatisticRepository, Depends(get_statistic_repository)
]
