"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 16/03/22
@name: models
"""
from sqlalchemy import Column, Integer, Float

from database.depends import CRUD
from database.engine import AppModel


class CalculatorConfig(AppModel, CRUD):
    """
        Calculator config
    """
    __tablename__ = 'calculator_config'

    id = Column(Integer, primary_key=True)
    amount_min = Column(Float, default=0, )
    amount_max = Column(Float, default=1, )
    amount_tax = Column(Float, default=16, )
