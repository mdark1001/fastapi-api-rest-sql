"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 17/03/22
@name: user_credit
"""
import enum
from sqlalchemy import Float, DateTime, func, ForeignKey, Enum, Date, Text, Integer, Column
from sqlalchemy.ext.hybrid import hybrid_property

from credits.models.config import CalculatorConfig
from database.depends import CRUD
from database.engine import AppModel
from users.models import User


class CreditRequestState(enum.Enum):
    sent = 1
    accepted = 2
    reject = 3


class CreditState(enum.Enum):
    paying = 1
    paid = 2
    cancelled = 3
    dont_apply = 4


class UserCredits(AppModel, CRUD):
    """
     User request creds, history about user and their credits accepted or rejected
    """
    __tablename__ = 'credits_user_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    credit_config_id = Column(Integer, ForeignKey(CalculatorConfig.id))
    amount_credit = Column(Float, default=0)
    amount_credit_tax = Column(Float, default=0)
    state = Column(Enum(CreditRequestState), default=CreditRequestState.sent)  # state of user  request
    credit_state = Column(Enum(CreditState), default=CreditState.dont_apply)  # current state of credit
    comments = Column(Text, nullable=True)
    date_judgmented = Column(Date, nullable=True)  # date accepted or rejected credit request
    created_at = Column(DateTime, server_default=func.now())  # date requested

    @hybrid_property
    def amount_total(self):
        return self.amount_credit + (self.amount_credit * self.amount_credit_tax)
