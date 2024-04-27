import os
from dataclasses import dataclass, field
from typing import Any

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from BitcoinWallet.core.constants import MAXIMUM_NUMBER_OF_WALLETS
from BitcoinWallet.infra.in_database.statistic_sqlite import StatisticInDatabase
from BitcoinWallet.infra.in_database.transaction_sqlite import TransactionInDatabase
from BitcoinWallet.infra.in_database.user_sqlite import UserInDatabase
from BitcoinWallet.infra.in_database.wallet_sqlite import WalletInDatabase
from BitcoinWallet.runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def user(self) -> dict[str, Any]:
        return {"username": self.faker.word(), "password": self.faker.word()}

    def unknown_id(self) -> str:
        return str(self.faker.uuid4())


def clear_tables() -> None:
    if os.getenv("REPOSITORY_KIND", "memory") == "sqlite":
        UserInDatabase().clear_tables()
        StatisticInDatabase().clear_tables()
        TransactionInDatabase().clear_tables()
        WalletInDatabase().clear_tables()


def test_should_create(client: TestClient) -> None:
    clear_tables()
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]

    response = client.post("/wallets", json={"API_key": API_key})
    assert response.status_code == 201
    assert response.json()["wallet"]["balance_in_BTC"] == 1


def test_should_not_create(client: TestClient) -> None:
    clear_tables()
    API_key = Fake().unknown_id()

    response = client.post("/wallets", json={"API_key": API_key})
    assert response.status_code == 404
    assert response.json() == {"message": "User does not exists."}


def test_should_not_4_wallet(client: TestClient) -> None:
    clear_tables()
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]
    for i in range(MAXIMUM_NUMBER_OF_WALLETS + 1):
        response = client.post("/wallets", json={"API_key": API_key})
    assert response.status_code == 403
    assert response.json() == {
        "message": "User has reached the maximum capacity of wallets."
    }


def test_should_not_read_without_user(client: TestClient) -> None:
    clear_tables()
    API_key = Fake().unknown_id()
    address = Fake().unknown_id()
    response = client.get(f"/wallets/{address}", headers={"API_key": API_key})

    assert response.status_code == 404
    assert response.json() == {"message": "Wallet does not exist."}


def test_should_not_read_without_address(client: TestClient) -> None:
    clear_tables()
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]
    address = Fake().unknown_id()
    response = client.get(f"/wallets/{address}", headers={"API_key": API_key})

    assert response.status_code == 404
    assert response.json() == {"message": "Wallet does not exist."}


def test_should_persist(client: TestClient) -> None:
    clear_tables()
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]

    response = client.post("/wallets", json={"API_key": API_key})
    address = response.json()["wallet"]["address"]

    response = client.get(f"/wallets/{address}", headers={"API_key": API_key})

    assert response.status_code == 200
    assert response.json()["wallet"]["balance_in_BTC"] == 1
