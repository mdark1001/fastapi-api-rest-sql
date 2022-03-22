"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 16/03/22
@name: schemas
"""
from typing import Optional

from pydantic import BaseModel, Field


class CalculatorConfigBase(BaseModel):
    """

    """
    amount_min: float = Field(...)
    amount_max: float = Field(...)
    amount_tax: float = Field(...)


class CalculatorConfigStore(CalculatorConfigBase):
    id: Optional[int] = Field(None)

