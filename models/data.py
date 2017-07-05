from app import db
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    Boolean,
    event,
)


class Temperature(db.Model):
    """
    A test streaming storage
    """
    __tablename__ = 'temperatures'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<temp {}>'.format(self.id)


class Rain(db.Model):
    """
    A test streaming storage
    """
    __tablename__ = 'rains'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<rain {}>'.format(self.id)


class Gas(db.Model):
    """
    A test streaming storage
    """
    __tablename__ = 'gases'

    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<gas {}>'.format(self.id)
