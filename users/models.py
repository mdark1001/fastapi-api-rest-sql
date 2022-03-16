"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: models
"""

from sqlalchemy import String, Column, Integer, Boolean

from database.engine import AppModel


class User(AppModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
