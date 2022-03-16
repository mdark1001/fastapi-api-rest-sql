"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: depends
"""
from database.engine import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



