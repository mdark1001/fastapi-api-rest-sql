"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 17/03/22
@name: user_credit_schema
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from credits.schemas.config_schema import CalculatorConfigStore


class CreditRequest(BaseModel):
    credit_config_id: int = Field(
        ...,
        description="Calculator config",
    )
    amount_credit: float = Field(
        ...,
        description="User's credit request"
    )


class CreditUser(CreditRequest):
    id: int
    credit_config_id: CalculatorConfigStore
    amount_credit_tax: float
    state: int
    credit_state: int
    comments: Optional[str]
    date_judgmented: Optional[date]
