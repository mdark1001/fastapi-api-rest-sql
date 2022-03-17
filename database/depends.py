"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: depends
"""
import sqlalchemy

from database.engine import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class CRUD:
    @staticmethod
    def objects():
        return next(get_db())

    def create(self):
        db = self.objects()
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    @classmethod
    def read(cls, id: int):
        return cls.objects().query(cls).filter(cls.id == id).first()

    @classmethod
    def unlink(cls, id: int):
        if cls.read(id):
            db = cls.objects()
            db.query(cls).filter(cls.id == id).delete()
            db.commit()
        raise Exception("Resource with id %s not found" % id)

    @classmethod
    def get_first(cls):
        return cls.objects().query(cls).first()

    @classmethod
    def get_last(cls):
        return cls.objects().query(cls).order_by(sqlalchemy.desc(cls.id)).first()
