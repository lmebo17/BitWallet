import os
from typing import Any, Dict

from fastapi import FastAPI

from BitcoinWallet.infra.fast_api.statistics_api import statistic_api
from BitcoinWallet.infra.fast_api.transactions_api import transaction_api
from BitcoinWallet.infra.fast_api.users_api import user_api
from BitcoinWallet.infra.fast_api.wallets_api import wallet_api
from BitcoinWallet.infra.in_database.statistic_sqlite import StatisticInDatabase
from BitcoinWallet.infra.in_database.transaction_sqlite import TransactionInDatabase
from BitcoinWallet.infra.in_database.user_sqlite import UserInDatabase
from BitcoinWallet.infra.in_database.wallet_sqlite import WalletInDatabase
from BitcoinWallet.infra.in_memory.statistics import StatisticInMemory
from BitcoinWallet.infra.in_memory.transactions import TransactionInMemory
from BitcoinWallet.infra.in_memory.users import UserInMemory
from BitcoinWallet.infra.in_memory.wallets import WalletInMemory

REPOSITORY_MAPPING: Dict[str, Dict[str, Any]] = {
    "sqlite": {
        "wallets": WalletInDatabase,
        "users": UserInDatabase,
        "statistics": StatisticInDatabase,
        "transactions": TransactionInDatabase,
    },
    "memory": {
        "wallets": WalletInMemory,
        "users": UserInMemory,
        "statistics": StatisticInMemory,
        "transactions": TransactionInMemory,
    },
}


def configure_app(app: FastAPI) -> None:
    repository_kind = os.getenv("REPOSITORY_KIND", "memory")
    repositories = REPOSITORY_MAPPING.get(repository_kind, REPOSITORY_MAPPING["memory"])

    for name, repository_class in repositories.items():
        setattr(app.state, name, repository_class())


def init_app() -> FastAPI:
    app = FastAPI()

    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)
    app.include_router(statistic_api)

    os.environ["REPOSITORY_KIND"] = "sqlite"
    configure_app(app)

    return app
