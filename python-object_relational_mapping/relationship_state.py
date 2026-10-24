#!/usr/bin/python3
"""Define the State model and its relationship with cities."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class State(Base):
    """Represent a state and its linked cities."""

    __tablename__ = "states"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City",
        backref="state",
        cascade="all, delete-orphan"
    )
