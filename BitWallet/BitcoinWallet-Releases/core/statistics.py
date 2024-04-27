from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass
class Statistic:
    transaction_number: int = 0
    profit_in_satoshi: int = 0


class StatisticRepository(Protocol):
    def get(self, key: UUID) -> Statistic:
        pass

    def update(self, commission: float) -> None:
        pass


@dataclass
class StatisticsService:
    statistics: StatisticRepository
