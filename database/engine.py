"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: engine
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
    "check_same_thread": False
})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AppModel = declarative_base()

