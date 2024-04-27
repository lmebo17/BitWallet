from dataclasses import dataclass, field
from uuid import UUID

from BitcoinWallet.core.constants import ADMIN_API_KEY
from BitcoinWallet.core.errors import AccessError
from BitcoinWallet.core.statistics import Statistic


@dataclass
class StatisticInMemory:
    statistic: Statistic = field(default_factory=Statistic)

    def get(self, key: UUID) -> Statistic:
        if key == UUID(ADMIN_API_KEY):
            return self.statistic
        raise AccessError("User does not have access to statistics.")

    def update(self, commission: int) -> None:
        self.statistic.transaction_number += 1
        self.statistic.profit_in_satoshi += commission
