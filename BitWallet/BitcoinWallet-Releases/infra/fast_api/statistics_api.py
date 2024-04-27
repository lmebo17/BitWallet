from typing import Any
from uuid import UUID

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from BitcoinWallet.core.errors import AccessError
from BitcoinWallet.infra.fast_api.dependables import StatisticRepositoryDependable

statistic_api = APIRouter(tags=["Statistics"])


class StatisticItem(BaseModel):
    transaction_number: int
    profit_in_satoshi: int


class StatisticItemEnvelope(BaseModel):
    statistics: StatisticItem


@statistic_api.get(
    "/statistics",
    status_code=200,
    response_model=StatisticItemEnvelope,
)
def show_statistic(
    statistics: StatisticRepositoryDependable, API_key: UUID = Header(alias="API_key")
) -> dict[str, Any] | JSONResponse:
    try:
        statistic = statistics.get(API_key)
        return {"statistics": statistic}
    except AccessError:
        return JSONResponse(
            status_code=403,
            content={"message": "User does not have access to statistics."},
        )
